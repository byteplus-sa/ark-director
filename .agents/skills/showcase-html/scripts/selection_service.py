import contextlib
import datetime
import fcntl
import hashlib
import io
import json
import os
import re
import subprocess
import tempfile
import uuid
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError


class SelectionError(ValueError):
    pass


class SelectionConflict(SelectionError):
    pass


SCHEMA_ROOT = Path(__file__).resolve().parents[3] / 'contracts' / 'schemas'
APPROVAL_MODES = {'approve_for_me', 'ask_for_approval'}
STAGE_LOCKS = {
    'picture': 'assembly-review',
    'audio': 'assembly-review',
    'final_master': 'delivery',
}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.mkv', '.webm'}
AUDIO_EXTENSIONS = {'.wav', '.mp3', '.m4a', '.aac', '.flac'}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_schema(value, schema_name):
    schema = json.loads((SCHEMA_ROOT / schema_name).read_text())
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value))
    if errors:
        raise SelectionError(f'{schema_name}: {errors[0].message}')


def contained_path(root, relative, must_exist=True):
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise SelectionError('Expected a nonempty project-relative path')
    value = Path(relative)
    if value.is_absolute() or '..' in value.parts:
        raise SelectionError(f'Path must remain inside the project: {relative}')
    path = root / value
    if not path.resolve().is_relative_to(root.resolve()):
        raise SelectionError(f'Symlink escapes the project: {relative}')
    if must_exist and not path.is_file():
        raise SelectionError(f'Missing file: {relative}')
    return path


def parse_frontmatter(text):
    match = re.match(r'\A---(\r?\n)(.*?)(\r?\n)---(?=\r?\n|$)(.*)\Z', text, re.DOTALL)
    if not match:
        raise SelectionError('Expected YAML frontmatter enclosed by --- lines')
    yaml = YAML(typ='rt')
    yaml.preserve_quotes = True
    yaml.width = 4096
    try:
        document = yaml.load((match[2] + match[3]).replace('\r\n', '\n'))
    except YAMLError as error:
        raise SelectionError(f'Unsupported or invalid YAML: {error}') from error
    if not isinstance(document, Mapping):
        raise SelectionError('Frontmatter must be a mapping')
    if re.search(r'(^|\s)[&*][\w-]+', match[2]):
        raise SelectionError('Selection editing does not support YAML anchors or aliases; expand them explicitly first')
    return yaml, document, match


def read_project_mode(root):
    root = Path(root).resolve()
    project = root / 'project.md'
    if not project.exists():
        return {'mode': 'approve_for_me', 'source': 'legacy_default', 'project_sha256': None}
    content = contained_path(root, 'project.md').read_bytes()
    metadata = {}
    if content.startswith(b'---'):
        _, metadata, _ = parse_frontmatter(content.decode('utf-8'))
    mode = metadata.get('approval_mode', 'approve_for_me')
    if mode not in APPROVAL_MODES:
        raise SelectionError('Invalid project approval_mode')
    return {
        'mode': mode,
        'source': 'explicit' if 'approval_mode' in metadata else 'legacy_default',
        'project_sha256': hashlib.sha256(content).hexdigest(),
    }


def edited_manifest(text, meta, filename, evidence=None):
    yaml, document, match = parse_frontmatter(text)
    field = meta.get('field', 'selected_variant')
    if field == 'selected_variants':
        key = meta.get('key')
        if not isinstance(key, str) or not key.strip():
            raise SelectionError('selected_variants requires a nonempty key')
        if field not in document:
            document[field] = {}
        if not isinstance(document[field], Mapping):
            raise SelectionError('selected_variants must be a mapping')
        document[field][key] = filename
        if evidence is not None:
            if 'selection_evidence' not in document:
                document['selection_evidence'] = {}
            if not isinstance(document['selection_evidence'], Mapping):
                raise SelectionError('selection_evidence must be a mapping')
            document['selection_evidence'][key] = evidence
    elif field == 'selected_variant':
        if isinstance(document.get(field), (Mapping, list)):
            raise SelectionError('selected_variant must be a scalar')
        document[field] = filename
        if evidence is not None:
            document['selection_evidence'] = evidence
            document['status'] = 'approved'
    else:
        raise SelectionError(f'Unsupported selection field: {field}')
    output = io.StringIO()
    yaml.dump(document, output)
    newline = match[1]
    frontmatter = output.getvalue().rstrip('\n').replace('\n', newline)
    return '---' + newline + frontmatter + newline + '---' + match[4]


def collect_selectable(data):
    registry: dict[str, dict[str, Any]] = {}
    if not isinstance(data, dict) or not isinstance(data.get('sections'), list):
        raise SelectionError('showcase.json requires a sections array')
    targets: dict[tuple[str, str, str | None], str] = {}
    for section in data['sections']:
        cards = section.get('cards', [])
        if section.get('kind') == 'takes':
            cards = [take for group in section.get('groups', []) for take in group.get('takes', [])]
        for card in cards:
            if not card.get('id') and not card.get('manifest'):
                continue
            asset_id = card.get('id')
            if not isinstance(asset_id, str) or not asset_id or not card.get('manifest'):
                raise SelectionError('Selectable cards require a string id and manifest')
            source = card.get('media', {}).get('src')
            if not isinstance(source, str) or not source:
                raise SelectionError(f'{asset_id}: selectable cards require media.src')
            filename = card.get('filename', Path(source).name)
            if filename != Path(source).name or not isinstance(filename, str):
                raise SelectionError(f'{asset_id}: filename must match media basename')
            meta = {'manifest': card['manifest'], 'field': card.get('field', 'selected_variant'), 'key': card.get('key'), 'stage': section.get('stage')}
            if meta['field'] not in ('selected_variant', 'selected_variants'):
                raise SelectionError(f'{asset_id}: unsupported selection field')
            if meta['field'] == 'selected_variants' and (not isinstance(meta['key'], str) or not meta['key']):
                raise SelectionError(f'{asset_id}: selected_variants requires key')
            target = (meta['manifest'], meta['field'], meta['key'])
            if target in targets and targets[target] != asset_id:
                raise SelectionError(f'{asset_id}: manifest selection target belongs to another id')
            targets[target] = asset_id
            if asset_id in registry:
                if any(registry[asset_id][key] != value for key, value in meta.items()):
                    raise SelectionError(f'{asset_id}: inconsistent variant metadata')
            else:
                registry[asset_id] = {**meta, 'variants': {}, 'reviews': {}}
            existing = registry[asset_id]['variants'].get(filename)
            if existing and existing != source:
                raise SelectionError(f'{asset_id}: duplicate filename maps to different media')
            registry[asset_id]['variants'][filename] = source
            review_path = card.get('reviewPath')
            if review_path is not None:
                if not isinstance(review_path, str) or not review_path:
                    raise SelectionError(f'{asset_id}: reviewPath must be a nonempty string')
                existing_review = registry[asset_id]['reviews'].get(filename)
                if existing_review and existing_review != review_path:
                    raise SelectionError(f'{asset_id}: inconsistent reviewPath')
                registry[asset_id]['reviews'][filename] = review_path
    return registry


def read_selection(registry, root):
    selections = {}
    for asset_id, meta in registry.items():
        path = contained_path(root, meta['manifest'])
        _, document, _ = parse_frontmatter(path.read_bytes().decode('utf-8'))
        value = document.get(meta['field'])
        if meta['field'] == 'selected_variants':
            if value is not None and not isinstance(value, Mapping):
                raise SelectionError(f'{asset_id}: selected_variants must be a mapping')
            value = value.get(meta['key']) if value else None
        if value is not None:
            if not isinstance(value, str):
                raise SelectionError(f'{asset_id}: selected value must be a string')
            selections[asset_id] = value
    return selections


def revision(root, registry):
    root = Path(root).resolve()
    hashes = {}
    for meta in registry.values():
        path = contained_path(root, meta['manifest'])
        hashes[meta['manifest']] = hashlib.sha256(path.read_bytes()).hexdigest()
    hashes['registry'] = hashlib.sha256(json.dumps(registry, sort_keys=True).encode()).hexdigest()
    showcase = root / 'showcase.json'
    if showcase.exists():
        hashes['showcase.json'] = hashlib.sha256(contained_path(root, 'showcase.json').read_bytes()).hexdigest()
    project = root / 'project.md'
    if project.exists():
        hashes['project.md'] = sha256(contained_path(root, 'project.md'))
    return hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()


def stage_revision(root):
    return revision(Path(root).resolve(), {})


def validate_selections(root, registry, selections):
    if not isinstance(selections, dict) or not selections:
        raise SelectionError('selections must be a nonempty mapping of asset ids to filenames')
    prepared: dict[str, str] = {}
    for asset_id, filename in selections.items():
        if asset_id not in registry:
            raise SelectionError(f'{asset_id}: not a selectable asset')
        if not isinstance(filename, str) or not filename.strip() or re.search(r'[\\/\r\n]', filename):
            raise SelectionError(f'{asset_id}: invalid filename')
        meta = registry[asset_id]
        if filename not in meta['variants']:
            raise SelectionError(f'{asset_id}: variant is not registered: {filename}')
        contained_path(root, meta['variants'][filename])
        path = contained_path(root, meta['manifest'])
        current = prepared.get(meta['manifest'], path.read_bytes().decode('utf-8'))
        prepared[meta['manifest']] = edited_manifest(current, meta, filename)
    for name in ('selection.json', 'selection.log', '.selection-journal.json', '.selection.lock'):
        contained_path(root, name, must_exist=False)
    return {'registry': registry, 'selections': dict(selections), 'prepared': prepared, 'revision': revision(root, registry)}


def validated_review(root, review_path, review_sha256, subject_path, subject_sha256):
    path = contained_path(root, review_path)
    if sha256(path) != review_sha256:
        raise SelectionError('Candidate review hash changed')
    try:
        review = json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise SelectionError('Candidate review is unreadable') from error
    validate_schema(review, 'candidate-review.schema.json')
    if review['status'] != 'pass' or not any(check['status'] == 'pass' for check in review['checks']) or any(check['status'] not in {'pass', 'not_applicable'} for check in review['checks']):
        raise SelectionError('Candidate review does not pass')
    if review['artifact_path'] != subject_path:
        raise SelectionError('Candidate review references another artifact')
    if review['artifact_sha256'] != subject_sha256:
        raise SelectionError('Candidate review artifact hash changed')
    suffix = Path(subject_path).suffix.lower()
    method = review['inspection_method'].lower()
    if suffix in {'.mp4', '.mov', '.mkv', '.webm'} and not any(word in method for word in ('playback', 'temporal')):
        raise SelectionError('Video review requires temporal or playback evidence')
    if suffix in {'.wav', '.mp3', '.m4a', '.aac', '.flac'} and 'listen' not in method:
        raise SelectionError('Audio review requires listening evidence')
    return review


def probe_media_streams(path):
    try:
        completed = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type', '-of', 'json', str(path)],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise SelectionError('Media stream inspection is unavailable') from error
    if completed.returncode != 0:
        raise SelectionError(f'Media stream inspection failed: {path.name}')
    try:
        streams = json.loads(completed.stdout)['streams']
    except (ValueError, KeyError, TypeError) as error:
        raise SelectionError(f'Media stream inspection returned invalid data: {path.name}') from error
    if not isinstance(streams, list):
        raise SelectionError(f'Media stream inspection returned invalid data: {path.name}')
    return {stream.get('codec_type') for stream in streams if isinstance(stream, dict)}


def validate_stage_media(root, lock_kind, subject_path, review, audio_required=False):
    suffix = Path(subject_path).suffix.lower()
    if lock_kind in {'picture', 'final_master'}:
        if suffix not in VIDEO_EXTENSIONS:
            raise SelectionError(f'{lock_kind} lock requires a video artifact')
        required_streams = {'video'}
    elif lock_kind == 'audio':
        if suffix not in AUDIO_EXTENSIONS:
            raise SelectionError('Audio lock requires an audio artifact')
        required_streams = {'audio'}
    else:
        raise SelectionError('Unknown stage lock kind')
    if lock_kind == 'final_master' and audio_required:
        required_streams.add('audio')
        if 'listen' not in review['inspection_method'].lower():
            raise SelectionError('Audiovisual final master requires listening evidence')
    streams = probe_media_streams(contained_path(Path(root).resolve(), subject_path))
    if not required_streams.issubset(streams):
        missing = ', '.join(sorted(required_streams - streams))
        raise SelectionError(f'{lock_kind} lock requires a {missing} stream')


def validated_decision(root, decision, subject_path, subject_sha256, mode, user_event=None):
    if not isinstance(decision, dict):
        raise SelectionError('Expected a structured production decision')
    validate_schema(decision, 'production-decision.schema.json')
    project_mode = read_project_mode(root)
    if project_mode['project_sha256'] is None:
        raise SelectionError('A project.md file is required for production decisions')
    if decision['project_sha256'] != project_mode['project_sha256'] or decision['approval_mode'] != mode:
        raise SelectionConflict('Project mode or project.md changed before decision')
    if decision['actor'] == 'agent' and mode != 'approve_for_me':
        raise SelectionError('Agent cannot approve in ask_for_approval mode')
    if decision['actor'] == 'user' and (decision['authorization']['source'] != 'local_ui' or user_event != decision['authorization']['evidence']):
        raise SelectionError('User authorization must come from the local review server')
    if decision['result'] != 'approved':
        raise SelectionError('Only approved decisions can promote an artifact')
    if decision['subject_path'] != subject_path:
        raise SelectionError('Decision subject is not the selected artifact')
    if sha256(contained_path(root, subject_path)) != subject_sha256:
        raise SelectionError('Selected artifact hash changed')
    validated_review(root, decision['review_path'], decision['review_sha256'], subject_path, subject_sha256)
    for relative, expected_hash in decision['upstream_sha256'].items():
        if sha256(contained_path(root, relative)) != expected_hash:
            raise SelectionError(f'Upstream artifact changed: {relative}')
    decision_path = f"decisions/{decision['decision_id']}.json"
    if contained_path(root, decision_path, must_exist=False).exists():
        raise SelectionConflict('Decision ID already exists')
    content = json.dumps(decision, indent=2, ensure_ascii=False, allow_nan=False) + '\n'
    return decision_path, content, hashlib.sha256(content.encode('utf-8')).hexdigest()


def decision_evidence(decision, decision_path, decision_sha256, subject_sha256):
    return {
        'decision_id': decision['decision_id'],
        'decision_path': decision_path,
        'decision_sha256': decision_sha256,
        'review_path': decision['review_path'],
        'review_sha256': decision['review_sha256'],
        'selected_sha256': subject_sha256,
        'actor': decision['actor'],
        'approval_mode': decision['approval_mode'],
        'result': decision['result'],
        'reason': decision['reason'],
    }


def add_stage_sources(showcase, stage_id, paths):
    if not stage_id or not isinstance(showcase.get('canvas'), dict):
        return False
    stage = next((item for item in showcase['canvas'].get('stages', []) if item.get('id') == stage_id), None)
    if stage is None:
        raise SelectionError(f'Missing canvas stage: {stage_id}')
    sources = stage.setdefault('sources', [])
    existing = {source.get('path') for source in sources if isinstance(source, dict)}
    changed = False
    for relative, kind in paths:
        if relative not in existing:
            sources.append({'path': relative, 'kind': kind})
            existing.add(relative)
            changed = True
    return changed


def atomic_write(path, content):
    descriptor, temporary = tempfile.mkstemp(prefix='.selection-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if path.exists():
            os.chmod(temporary, path.stat().st_mode & 0o777)
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextlib.contextmanager
def writer_lock(root):
    path = contained_path(root, '.selection.lock', must_exist=False)
    with path.open('a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def recover_selection(root):
    journal_path = contained_path(root, '.selection-journal.json', must_exist=False)
    if not journal_path.exists():
        return False
    try:
        journal = json.loads(journal_path.read_text())
    except (json.JSONDecodeError, UnicodeError) as error:
        raise SelectionConflict('Unreadable selection recovery journal; inspect it before saving') from error
    if not isinstance(journal, dict):
        raise SelectionConflict('Invalid selection recovery journal; inspect it before saving')
    if journal.get('version') != 1 or not isinstance(journal.get('files'), dict):
        raise SelectionConflict('Invalid selection recovery journal; inspect it before saving')
    for relative, entry in journal['files'].items():
        if not isinstance(entry, dict) or not isinstance(entry.get('after'), str) or not (entry.get('before') is None or isinstance(entry['before'], str)):
            raise SelectionConflict('Invalid recovery entry; journal retained for inspection')
        path = contained_path(root, relative, must_exist=False)
        current = path.read_bytes().decode('utf-8') if path.exists() else None
        if current not in (entry['before'], entry['after']):
            raise SelectionConflict(f'Recovery conflicts with a later edit: {relative}; journal retained')
    for relative, entry in journal['files'].items():
        path = contained_path(root, relative, must_exist=False)
        if path.exists() and path.read_bytes().decode('utf-8') == entry['after']:
            continue
        atomic_write(path, entry['after'].encode('utf-8'))
    journal_path.unlink()
    return True


def commit_targets(root, targets):
    journal: dict[str, Any] = {'version': 1, 'files': {}}
    for relative, after in targets.items():
        path = contained_path(root, relative, must_exist=False)
        if relative.startswith('decisions/'):
            path.parent.mkdir(exist_ok=True)
        journal['files'][relative] = {'before': path.read_bytes().decode('utf-8') if path.exists() else None, 'after': after}
    journal_path = root / '.selection-journal.json'
    atomic_write(journal_path, json.dumps(journal, ensure_ascii=False).encode('utf-8'))
    try:
        recover_selection(root)
    except OSError as error:
        raise SelectionConflict('Selection commit interrupted; recovery journal retained. Retry recovery before further edits') from error


def local_ui_decision(root, registry, asset_id, filename, mode, user_event):
    meta = registry[asset_id]
    review_path = meta['reviews'].get(filename)
    if not review_path:
        raise SelectionError(f'{asset_id}: reviewPath is required for approval')
    source = meta['variants'][filename]
    return {
        'schema_version': 1,
        'decision_id': uuid.uuid4().hex,
        'decision_type': 'variant_selection',
        'asset_id': asset_id,
        'subject_path': source,
        'selected_variant': filename,
        'selected_sha256': sha256(contained_path(root, source)),
        'actor': 'user',
        'approval_mode': mode['mode'],
        'project_sha256': mode['project_sha256'],
        'result': 'approved',
        'review_path': review_path,
        'review_sha256': sha256(contained_path(root, review_path)),
        'upstream_sha256': {},
        'reason': 'Selected in the local production canvas',
        'decided_at': datetime.datetime.now(datetime.UTC).isoformat(),
        'authorization': {'source': 'local_ui', 'evidence': user_event},
    }


def current_selection(metadata, meta):
    selected = metadata.get(meta['field'])
    if meta['field'] == 'selected_variants':
        selected = selected.get(meta['key']) if isinstance(selected, Mapping) else None
    evidence = metadata.get('selection_evidence')
    if meta['field'] == 'selected_variants':
        evidence = evidence.get(meta['key']) if isinstance(evidence, Mapping) else None
    return selected, evidence


def apply_selection_batch(root, batch, expected_revision, decisions=None, user_event=None):
    registry = batch['registry']
    if expected_revision != revision(root, registry):
        raise SelectionConflict('Stale selection revision; reload the page or preview current manifests')
    with writer_lock(root):
        recover_selection(root)
        if expected_revision != revision(root, registry):
            raise SelectionConflict('Stale selection revision; reload before saving')
        batch = validate_selections(root, registry, batch['selections'])
        mode = read_project_mode(root)
        showcase_path = root / 'showcase.json'
        showcase = json.loads(contained_path(root, 'showcase.json').read_text()) if showcase_path.exists() else None
        canvas = showcase.get('canvas') if isinstance(showcase, dict) else None
        production = mode['project_sha256'] is not None and isinstance(canvas, dict) and canvas.get('approvalContractVersion') == 1
        if production and decisions is None and user_event is None:
            raise SelectionError('Production selections require decision evidence or a local UI event')
        if decisions is not None and (not isinstance(decisions, dict) or set(decisions) != set(batch['selections'])):
            raise SelectionError('Provide one decision for every selected asset')
        selected = read_selection(registry, root)
        selected.update(batch['selections'])
        targets = dict(batch['prepared'])
        decision_ids = {}
        for asset_id, filename in batch['selections'].items():
            if decisions is None and user_event is None:
                continue
            meta = registry[asset_id]
            source = meta['variants'][filename]
            subject_sha256 = sha256(contained_path(root, source))
            decision = decisions[asset_id] if decisions is not None else local_ui_decision(root, registry, asset_id, filename, mode, user_event)
            if not isinstance(decision, dict) or decision.get('decision_type') != 'variant_selection' or decision.get('asset_id') != asset_id or decision.get('selected_variant') != filename or decision.get('selected_sha256') != subject_sha256:
                raise SelectionError(f'{asset_id}: decision does not match selected variant')
            manifest = contained_path(root, meta['manifest'])
            _, metadata, _ = parse_frontmatter(manifest.read_text())
            previous, previous_evidence = current_selection(metadata, meta)
            if decision.get('actor') == 'agent' and previous is not None and (not isinstance(previous_evidence, Mapping) or previous_evidence.get('actor') != 'agent'):
                raise SelectionError(f'{asset_id}: an agent cannot replace or adopt an existing user selection')
            decision_path, decision_content, decision_sha256 = validated_decision(root, decision, source, subject_sha256, mode['mode'], user_event)
            if decision_path in targets:
                raise SelectionError('Duplicate decision ID in selection batch')
            targets[decision_path] = decision_content
            evidence = decision_evidence(decision, decision_path, decision_sha256, subject_sha256)
            targets[meta['manifest']] = edited_manifest(targets[meta['manifest']], meta, filename, evidence)
            decision_ids[asset_id] = decision['decision_id']
            if showcase is not None:
                if production and not meta['stage']:
                    raise SelectionError(f'{asset_id}: production selection requires a canvas stage')
                add_stage_sources(showcase, meta['stage'], [(source, 'media'), (decision_path, 'data'), (decision['review_path'], 'review')])
        if decision_ids and showcase is not None:
            targets['showcase.json'] = json.dumps(showcase, indent=2, ensure_ascii=False, allow_nan=False) + '\n'
        targets['selection.json'] = json.dumps({'project': root.name, 'selections': selected}, indent=2, ensure_ascii=False) + '\n'
        audit_path = contained_path(root, 'selection.log', must_exist=False)
        audit = audit_path.read_text() if audit_path.exists() else ''
        record = {'ts': datetime.datetime.now(datetime.UTC).isoformat(), 'event': 'save', 'applied': list(batch['selections']), 'selections': batch['selections'], 'decisions': decision_ids, 'total': len(batch['selections']), 'errors': []}
        targets['selection.log'] = audit + json.dumps(record, ensure_ascii=False) + '\n'
        commit_targets(root, targets)
        return {'ok': True, 'applied': list(batch['selections']), 'decisions': decision_ids, 'errors': [], 'revision': revision(root, registry), 'selections': read_selection(registry, root)}


def record_stage_decision(root, decision, expected_revision=None, user_event=None):
    root = Path(root).resolve()
    expected = expected_revision or stage_revision(root)
    if expected != stage_revision(root):
        raise SelectionConflict('Stale project revision before stage decision')
    with writer_lock(root):
        recover_selection(root)
        if expected != stage_revision(root):
            raise SelectionConflict('Stale project revision before stage decision')
        if not isinstance(decision, dict) or decision.get('decision_type') != 'stage_lock':
            raise SelectionError('Expected a stage lock decision')
        stage_id = decision.get('stage_id')
        lock_kind = decision.get('lock_kind')
        if STAGE_LOCKS.get(lock_kind) != stage_id:
            raise SelectionError('Stage lock kind does not match stage')
        showcase_path = contained_path(root, 'showcase.json')
        showcase = json.loads(showcase_path.read_text())
        stage = next((item for item in showcase.get('canvas', {}).get('stages', []) if item.get('id') == stage_id), None)
        if stage is None:
            raise SelectionError(f'Missing canvas stage: {stage_id}')
        if showcase['canvas'].get('currentStage') != stage_id:
            raise SelectionError('Stage lock requires the matching current canvas stage')
        mode = read_project_mode(root)
        subject = decision.get('subject_path')
        if not isinstance(subject, str):
            raise SelectionError('Stage decision requires subject_path')
        subject_sha256 = sha256(contained_path(root, subject))
        if decision.get('subject_sha256') != subject_sha256:
            raise SelectionError('Stage decision artifact hash changed')
        existing = stage.get('locks', {}).get(lock_kind)
        if decision.get('actor') == 'agent' and existing and existing.get('actor') != 'agent':
            raise SelectionError('An agent cannot replace a user stage lock')
        decision_path, decision_content, decision_sha256 = validated_decision(root, decision, subject, subject_sha256, mode['mode'], user_event)
        review = validated_review(root, decision['review_path'], decision['review_sha256'], subject, subject_sha256)
        audio_stage = next((item for item in showcase['canvas'].get('stages', []) if item.get('id') == 'audio-preparation'), None)
        audio_required = audio_stage is None or audio_stage.get('status') != 'skipped'
        validate_stage_media(root, lock_kind, subject, review, audio_required=audio_required)
        stage.setdefault('locks', {})[lock_kind] = {
            'decision_id': decision['decision_id'],
            'decision_sha256': decision_sha256,
            'result': decision['result'],
            'artifact_path': subject,
            'artifact_sha256': subject_sha256,
            'review_path': decision['review_path'],
            'review_sha256': decision['review_sha256'],
            'actor': decision['actor'],
            'reason': decision['reason'],
        }
        add_stage_sources(showcase, stage_id, [(subject, 'media'), (decision['review_path'], 'review'), (decision_path, 'data')])
        targets = {
            decision_path: decision_content,
            'showcase.json': json.dumps(showcase, indent=2, ensure_ascii=False, allow_nan=False) + '\n',
        }
        commit_targets(root, targets)
        return {'ok': True, 'decision_id': decision['decision_id'], 'decision_path': decision_path, 'revision': stage_revision(root)}


def set_project_mode(root, mode, expected_revision=None):
    root = Path(root).resolve()
    if mode not in APPROVAL_MODES:
        raise SelectionError('Invalid project approval_mode')
    expected = expected_revision or stage_revision(root)
    if expected != stage_revision(root):
        raise SelectionConflict('Stale project revision before approval mode change')
    with writer_lock(root):
        recover_selection(root)
        if expected != stage_revision(root):
            raise SelectionConflict('Stale project revision before approval mode change')
        project = contained_path(root, 'project.md')
        current = project.read_text()
        if current.startswith('---'):
            yaml, metadata, match = parse_frontmatter(current)
            metadata['approval_mode'] = mode
            output = io.StringIO()
            yaml.dump(metadata, output)
            newline = match[1]
            updated = '---' + newline + output.getvalue().rstrip('\n').replace('\n', newline) + newline + '---' + match[4]
        else:
            updated = f'---\napproval_mode: {mode}\n---\n' + current
        if updated != current:
            commit_targets(root, {'project.md': updated})
        return {'mode': mode, 'revision': stage_revision(root)}


class SelectionService:
    def __init__(self, root, data):
        self.root = Path(root).resolve()
        self.registry = collect_selectable(data)
        self.showcase_hash = self._showcase_hash()

    def _showcase_hash(self):
        path = self.root / 'showcase.json'
        return hashlib.sha256(contained_path(self.root, 'showcase.json').read_bytes()).hexdigest() if path.exists() else None

    def _check_showcase(self):
        if self._showcase_hash() != self.showcase_hash:
            raise SelectionConflict('showcase.json changed; restart the review server before saving')

    def _recover_and_check_showcase(self):
        if not (self.root / '.selection-journal.json').exists():
            self._check_showcase()
            return
        with writer_lock(self.root):
            recovered = recover_selection(self.root)
            if recovered:
                self.showcase_hash = self._showcase_hash()
            else:
                self._check_showcase()

    def snapshot(self):
        if not (self.root / '.selection-journal.json').exists():
            self._check_showcase()
        with writer_lock(self.root):
            recovered = recover_selection(self.root)
            if recovered:
                self.showcase_hash = self._showcase_hash()
            else:
                self._check_showcase()
            return {'selections': read_selection(self.registry, self.root), 'revision': revision(self.root, self.registry)}

    def apply(self, selections, expected_revision=None, decisions=None, user_event=None):
        self._recover_and_check_showcase()
        batch = validate_selections(self.root, self.registry, selections)
        result = apply_selection_batch(self.root, batch, expected_revision or batch['revision'], decisions, user_event)
        self.showcase_hash = self._showcase_hash()
        return result
