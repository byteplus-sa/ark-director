import datetime
import hashlib
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import test_showcase_selection as fixtures

showcase = fixtures.showcase


class ShowcaseCanvasModeTests(unittest.TestCase):
    setUp = fixtures.ShowcaseRegressionTests.setUp
    lifecycle_canvas = fixtures.ShowcaseRegressionTests.lifecycle_canvas

    def test_default_mode_and_project_edit_refresh_canvas_snapshot(self):
        data = self.lifecycle_canvas()
        data['canvas']['approvalContractVersion'] = 1
        (self.root / 'showcase.json').write_text(json.dumps(data))
        showcase.generate(self.root, data, 'index.html', expected_stage='brief-development')
        embedded = showcase.embedded_showcase_data(self.root / 'index.html')
        self.assertEqual(embedded['approvalMode']['mode'], 'approve_for_me')
        self.assertEqual(embedded['approvalMode']['source'], 'legacy_default')
        self.assertEqual(showcase.canvas_sync_errors(data, self.root, self.root / 'index.html', 'brief-development'), [])

        (self.root / 'project.md').write_text('---\napproval_mode: ask_for_approval\n---\n# Project brief\n')
        self.assertIn('stale', ' '.join(showcase.canvas_sync_errors(data, self.root, self.root / 'index.html', 'brief-development')))
        showcase.generate(self.root, data, 'index.html', expected_stage='brief-development')
        embedded = showcase.embedded_showcase_data(self.root / 'index.html')
        self.assertEqual(embedded['approvalMode']['mode'], 'ask_for_approval')
        self.assertEqual(embedded['approvalMode']['source'], 'explicit')
        self.assertEqual(showcase.canvas_sync_errors(data, self.root, self.root / 'index.html', 'brief-development'), [])

    @patch.object(showcase, 'validate_stage_media')
    def test_versioned_stage_lock_requires_sources_and_current_hashes(self, media_check):
        data = self.lifecycle_canvas()
        canvas = data['canvas']
        canvas['approvalContractVersion'] = 1
        canvas['currentStage'] = 'assembly-review'
        for stage in canvas['stages']:
            if stage['id'] == 'assembly-review':
                stage['status'] = 'complete'
                stage['sources'] = [{'path': 'project.md', 'kind': 'brief'}]
            elif stage['id'] == 'audio-preparation':
                stage['status'] = 'skipped'
            elif stage['id'] != 'delivery':
                stage['status'] = 'complete'
                stage['sources'] = [{'path': 'project.md', 'kind': 'brief'}]
        stage = canvas['stages'][-2]
        self.assertIn('picture lock is required', ' '.join(showcase.canvas_validation_errors(data, self.root, 'assembly-review')))

        picture = b'picture bytes'
        review = {
            'schema_version': 1,
            'artifact_path': 'picture.mp4',
            'artifact_sha256': hashlib.sha256(picture).hexdigest(),
            'status': 'pass',
            'inspection_method': 'direct_video_playback',
            'coverage': 'Complete synthetic video reviewed.',
            'checks': [{'criterion': 'Continuity', 'status': 'pass', 'evidence': 'Synthetic fixture'}],
            'observations': ['The picture meets the test brief.'],
            'limitations': [],
            'recommendation': 'Approve the picture.',
        }
        paths = {'picture.mp4': picture, 'picture-review.json': json.dumps(review).encode()}
        (self.root / 'decisions').mkdir()
        for name, content in paths.items():
            (self.root / name).write_bytes(content)
            stage['sources'].append({'path': name})
        stage['locks'] = {'picture': {
            'decision_id': 'picture-1',
            'result': 'approved',
            'artifact_path': 'picture.mp4',
            'artifact_sha256': hashlib.sha256(paths['picture.mp4']).hexdigest(),
            'review_path': 'picture-review.json',
            'review_sha256': hashlib.sha256(paths['picture-review.json']).hexdigest(),
            'actor': 'agent',
            'reason': 'Passing continuity review',
        }}
        lock = stage['locks']['picture']
        decision = {
            'schema_version': 1,
            'decision_id': lock['decision_id'],
            'decision_type': 'stage_lock',
            'stage_id': 'assembly-review',
            'lock_kind': 'picture',
            'result': lock['result'],
            'actor': lock['actor'],
            'approval_mode': 'approve_for_me',
            'project_sha256': hashlib.sha256((self.root / 'project.md').read_bytes()).hexdigest(),
            'subject_path': lock['artifact_path'],
            'subject_sha256': lock['artifact_sha256'],
            'review_path': lock['review_path'],
            'review_sha256': lock['review_sha256'],
            'reason': lock['reason'],
            'upstream_sha256': {'prompt_hero.md': hashlib.sha256((self.root / 'prompt_hero.md').read_bytes()).hexdigest()},
            'decided_at': datetime.datetime.now(datetime.UTC).isoformat(),
        }
        decision_content = json.dumps(decision)
        (self.root / 'decisions/picture-1.json').write_text(decision_content)
        lock['decision_sha256'] = hashlib.sha256(decision_content.encode()).hexdigest()
        stage['sources'].append({'path': 'decisions/picture-1.json'})
        (self.root / 'showcase.json').write_text(json.dumps(data))
        self.assertEqual(showcase.canvas_validation_errors(data, self.root, 'assembly-review'), [])
        showcase.generate(self.root, data, 'index.html', expected_stage='assembly-review')
        self.assertEqual(showcase.canvas_sync_errors(data, self.root, self.root / 'index.html', 'assembly-review'), [])
        media_check.assert_called()
        (self.root / 'project.md').write_text('---\napproval_mode: ask_for_approval\n---\n# Project brief\n')
        self.assertEqual(showcase.canvas_validation_errors(data, self.root, 'assembly-review'), [])
        decision['approval_mode'] = 'ask_for_approval'
        decision_content = json.dumps(decision)
        (self.root / 'decisions/picture-1.json').write_text(decision_content)
        lock['decision_sha256'] = hashlib.sha256(decision_content.encode()).hexdigest()
        self.assertIn('production-decision.schema.json', ' '.join(showcase.canvas_validation_errors(data, self.root, 'assembly-review')))
        decision['actor'] = 'user'
        decision['authorization'] = {'source': 'chat', 'evidence': 'untrusted statement'}
        lock['actor'] = 'user'
        decision_content = json.dumps(decision)
        (self.root / 'decisions/picture-1.json').write_text(decision_content)
        lock['decision_sha256'] = hashlib.sha256(decision_content.encode()).hexdigest()
        self.assertIn('production-decision.schema.json', ' '.join(showcase.canvas_validation_errors(data, self.root, 'assembly-review')))
        decision['actor'] = 'agent'
        decision['approval_mode'] = 'approve_for_me'
        decision.pop('authorization')
        lock['actor'] = 'agent'
        decision_content = json.dumps(decision)
        (self.root / 'decisions/picture-1.json').write_text(decision_content)
        lock['decision_sha256'] = hashlib.sha256(decision_content.encode()).hexdigest()
        (self.root / 'picture.mp4').write_bytes(b'changed picture')
        self.assertIn('hash is stale', ' '.join(showcase.canvas_sync_errors(data, self.root, self.root / 'index.html', 'assembly-review')))
        (self.root / 'picture.mp4').write_bytes(picture)
        (self.root / 'prompt_hero.md').write_text('Changed upstream prompt.\n')
        self.assertIn('upstream source hash is stale', ' '.join(showcase.canvas_validation_errors(data, self.root, 'assembly-review')))

    def test_new_delivery_requires_final_master_lock(self):
        data = self.lifecycle_canvas()
        canvas = data['canvas']
        canvas['approvalContractVersion'] = 1
        canvas['currentStage'] = 'delivery'
        for stage in canvas['stages']:
            stage['status'] = 'complete'
            stage['sources'] = [{'path': 'project.md', 'kind': 'brief'}]
        errors = showcase.canvas_validation_errors(data, self.root, 'delivery')
        self.assertTrue(any('final_master lock is required' in error for error in errors))

    def test_malformed_lock_candidates_return_validation_findings(self):
        data = self.lifecycle_canvas()
        data['canvas']['approvalContractVersion'] = 1
        stage = data['canvas']['stages'][0]
        for candidate in (
            {'lock_kind': [], 'artifact_path': [], 'review_path': {}, 'reason': 7, 'upstream_sha256': []},
            {'lock_kind': 'picture', 'artifact_path': 'new.png', 'review_path': 'new.png', 'reason': 'Review', 'upstream_sha256': {'new.png': 'bad'}},
        ):
            stage['lockCandidates'] = [candidate]
            errors = showcase.canvas_validation_errors(data, self.root, 'brief-development')
            self.assertTrue(any('lock candidate' in error for error in errors))

    def test_selection_evidence_map_is_embedded_for_multi_asset_manifest(self):
        self.manifest.write_text('---\nselected_variants:\n  hero: new.png\nselection_evidence:\n  hero:\n    decision_id: choice-1\n    decision_path: decisions/choice-1.json\n    actor: agent\n    result: approved\n---\n')
        showcase.generate(self.root, self.data, 'index.html')
        embedded = showcase.embedded_showcase_data(self.root / 'index.html')
        self.assertEqual(embedded['selectionEvidence']['hero']['decision_id'], 'choice-1')
        self.assertEqual(embedded['selectionEvidence']['hero']['actor'], 'agent')

    def test_mode_cli_regenerates_canvas_and_check_passes(self):
        data = self.lifecycle_canvas()
        data['canvas']['approvalContractVersion'] = 1
        (self.root / 'showcase.json').write_text(json.dumps(data))
        command = [sys.executable, str(Path(showcase.__file__)), str(self.root), '--stage', 'brief-development']
        changed = subprocess.run(command + ['--set-approval-mode', 'ask_for_approval'], capture_output=True, text=True, check=False)
        self.assertEqual(changed.returncode, 0, changed.stdout + changed.stderr)
        self.assertEqual(showcase.embedded_showcase_data(self.root / 'index.html')['approvalMode']['mode'], 'ask_for_approval')
        checked = subprocess.run(command + ['--check'], capture_output=True, text=True, check=False)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_stage_decision_cli_writes_lock_and_refreshes_canvas(self):
        if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
            self.skipTest('ffmpeg and ffprobe required for synthetic stage media')
        data = self.lifecycle_canvas()
        canvas = data['canvas']
        canvas['approvalContractVersion'] = 1
        canvas['currentStage'] = 'assembly-review'
        for stage in canvas['stages']:
            if stage['id'] == 'assembly-review':
                stage['status'] = 'active'
                stage['sources'] = [{'path': 'project.md', 'kind': 'brief'}]
            elif stage['id'] == 'audio-preparation':
                stage['status'] = 'skipped'
            elif stage['id'] != 'delivery':
                stage['status'] = 'complete'
                stage['sources'] = [{'path': 'project.md', 'kind': 'brief'}]
        (self.root / 'showcase.json').write_text(json.dumps(data))
        subprocess.run([
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-f', 'lavfi',
            '-i', 'color=c=blue:s=160x90:r=24:d=1', '-an', '-c:v',
            'libx264', '-pix_fmt', 'yuv420p', str(self.root / 'picture.mp4'),
        ], check=True, capture_output=True)
        artifact_hash = hashlib.sha256((self.root / 'picture.mp4').read_bytes()).hexdigest()
        review = {
            'schema_version': 1,
            'artifact_path': 'picture.mp4',
            'artifact_sha256': artifact_hash,
            'status': 'pass',
            'inspection_method': 'direct_video_playback',
            'coverage': 'Complete synthetic artifact reviewed.',
            'checks': [{'criterion': 'Continuity', 'status': 'pass', 'evidence': 'Synthetic fixture'}],
            'observations': ['The picture meets the test brief.'],
            'limitations': [],
            'recommendation': 'Approve the picture.',
        }
        (self.root / 'picture-review.json').write_text(json.dumps(review))
        decision = {
            'schema_version': 1,
            'decision_id': 'picture-cli',
            'decision_type': 'stage_lock',
            'stage_id': 'assembly-review',
            'lock_kind': 'picture',
            'subject_path': 'picture.mp4',
            'subject_sha256': artifact_hash,
            'actor': 'agent',
            'approval_mode': 'approve_for_me',
            'project_sha256': hashlib.sha256((self.root / 'project.md').read_bytes()).hexdigest(),
            'result': 'approved',
            'review_path': 'picture-review.json',
            'review_sha256': hashlib.sha256((self.root / 'picture-review.json').read_bytes()).hexdigest(),
            'upstream_sha256': {},
            'reason': 'Passing continuity review',
            'decided_at': datetime.datetime.now(datetime.UTC).isoformat(),
        }
        command = [sys.executable, str(Path(showcase.__file__)), str(self.root), '--stage', 'assembly-review']
        locked = subprocess.run(command + ['--stage-decision', json.dumps(decision)], capture_output=True, text=True, check=False)
        self.assertEqual(locked.returncode, 0, locked.stdout + locked.stderr)
        saved = json.loads((self.root / 'showcase.json').read_text())
        self.assertEqual(saved['canvas']['stages'][-2]['locks']['picture']['decision_id'], 'picture-cli')
        self.assertEqual(showcase.canvas_sync_errors(saved, self.root, self.root / 'index.html', 'assembly-review'), [])

    def test_completed_selection_stage_rejects_changed_media_and_review(self):
        data = self.lifecycle_canvas()
        canvas = data['canvas']
        canvas['approvalContractVersion'] = 1
        canvas['currentStage'] = 'canon-elements'
        for stage in canvas['stages'][:2]:
            stage['status'] = 'complete'
            stage['sources'] = [{'path': 'project.md', 'kind': 'brief'}]
        canvas['stages'][2]['status'] = 'active'
        data['sections'].append({
            'id': 'hero-options',
            'title': 'Hero options',
            'stage': 'canon-elements',
            'kind': 'grid',
            'cards': [{
                'id': 'hero',
                'manifest': 'shot.md',
                'field': 'selected_variants',
                'key': 'hero',
                'media': {'type': 'image', 'src': 'new.png'},
                'reviewPath': 'hero-review.json',
            }],
        })
        self.manifest.write_text('---\nselected_variants: {}\n---\n')
        (self.root / 'showcase.json').write_text(json.dumps(data))
        media_hash = hashlib.sha256((self.root / 'new.png').read_bytes()).hexdigest()
        review = {
            'schema_version': 1,
            'artifact_path': 'new.png',
            'artifact_sha256': media_hash,
            'status': 'pass',
            'inspection_method': 'direct_image_inspection',
            'coverage': 'Complete synthetic image reviewed.',
            'checks': [{'criterion': 'Identity', 'status': 'pass', 'evidence': 'Synthetic fixture'}],
            'observations': ['The image meets the test brief.'],
            'limitations': [],
            'recommendation': 'Approve this image.',
        }
        (self.root / 'hero-review.json').write_text(json.dumps(review))
        self.assertEqual(showcase.canvas_validation_errors(data, self.root, 'canon-elements'), [])
        canvas['stages'][2]['status'] = 'complete'
        canvas['stages'][3]['status'] = 'active'
        canvas['stages'][3]['sources'] = [{'path': 'project.md', 'kind': 'brief'}]
        canvas['currentStage'] = 'storyboard-visual-plan'
        self.assertIn('requires a registered selected variant', ' '.join(showcase.canvas_validation_errors(data, self.root, 'storyboard-visual-plan')))
        canvas['stages'][2]['status'] = 'active'
        canvas['stages'][3]['status'] = 'pending'
        canvas['stages'][3]['sources'] = []
        canvas['currentStage'] = 'canon-elements'
        decision = {
            'schema_version': 1,
            'decision_id': 'hero-choice',
            'decision_type': 'variant_selection',
            'asset_id': 'hero',
            'subject_path': 'new.png',
            'selected_variant': 'new.png',
            'selected_sha256': media_hash,
            'actor': 'agent',
            'approval_mode': 'approve_for_me',
            'project_sha256': hashlib.sha256((self.root / 'project.md').read_bytes()).hexdigest(),
            'result': 'approved',
            'review_path': 'hero-review.json',
            'review_sha256': hashlib.sha256((self.root / 'hero-review.json').read_bytes()).hexdigest(),
            'upstream_sha256': {},
            'reason': 'Passing identity review',
            'decided_at': datetime.datetime.now(datetime.UTC).isoformat(),
        }
        envelope = {'selections': {'hero': 'new.png'}, 'decisions': {'hero': decision}}
        command = [sys.executable, str(Path(showcase.__file__)), str(self.root), '--stage', 'canon-elements']
        applied = subprocess.run(command + ['--apply', json.dumps(envelope)], capture_output=True, text=True, check=False)
        self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
        self.assertTrue(json.loads(applied.stdout)['canvasSynced'])
        saved = json.loads((self.root / 'showcase.json').read_text())
        saved['canvas']['stages'][2]['status'] = 'complete'
        saved['canvas']['stages'][3]['status'] = 'active'
        saved['canvas']['stages'][3]['sources'] = [{'path': 'project.md', 'kind': 'brief'}]
        saved['canvas']['currentStage'] = 'storyboard-visual-plan'
        (self.root / 'showcase.json').write_text(json.dumps(saved))
        self.assertEqual(showcase.canvas_validation_errors(saved, self.root, 'storyboard-visual-plan'), [])
        decision_path = self.root / 'decisions/hero-choice.json'
        original_decision = decision_path.read_text()
        original_manifest = self.manifest.read_text()
        forged = json.loads(original_decision)
        forged['approval_mode'] = 'ask_for_approval'
        decision_path.write_text(json.dumps(forged))
        _, metadata, _ = fixtures.selection.parse_frontmatter(original_manifest)
        original_hash = metadata['selection_evidence']['hero']['decision_sha256']
        forged_hash = hashlib.sha256(decision_path.read_bytes()).hexdigest()
        self.manifest.write_text(original_manifest.replace(original_hash, forged_hash))
        self.assertIn('production-decision.schema.json', ' '.join(showcase.canvas_validation_errors(saved, self.root, 'storyboard-visual-plan')))
        decision_path.write_text(original_decision)
        self.manifest.write_text(original_manifest)
        showcase.generate(self.root, saved, 'index.html', expected_stage='storyboard-visual-plan')
        self.assertEqual(showcase.canvas_sync_errors(saved, self.root, self.root / 'index.html', 'storyboard-visual-plan'), [])
        (self.root / 'new.png').write_bytes(b'changed image')
        self.assertIn('selected media hash is stale', ' '.join(showcase.canvas_validation_errors(saved, self.root, 'storyboard-visual-plan')))
        (self.root / 'new.png').write_bytes(b'fixture')
        (self.root / 'hero-review.json').write_text('{}')
        self.assertIn('approval evidence is unavailable', ' '.join(showcase.canvas_validation_errors(saved, self.root, 'storyboard-visual-plan')))


if __name__ == '__main__':
    unittest.main()
