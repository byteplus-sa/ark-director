import datetime
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / '.agents/skills/showcase-html/scripts'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS.parents[2] / 'scripts'))
import generate_showcase as showcase
import selection_service as selection
import validate_request as request_validation


class ApprovalModeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / 'project.md').write_text('---\ntitle: Example\n---\n\nKeep this brief.\n')
        (self.root / 'element.md').write_text('---\nselected_variant: null\nstatus: review\n---\nElement body.\n')
        (self.root / 'old.png').write_bytes(b'old image')
        (self.root / 'new.png').write_bytes(b'new image')
        self.review('new.png', 'image_review.json', 'direct_image_inspection')
        self.data = {
            'title': 'Fixture',
            'canvas': {
                'approvalContractVersion': 1,
                'currentStage': 'canon-elements',
                'stages': [{'id': 'canon-elements', 'status': 'active', 'sources': []}, {'id': 'assembly-review', 'status': 'pending', 'sources': []}, {'id': 'delivery', 'status': 'pending', 'sources': []}],
            },
            'sections': [{
                'stage': 'canon-elements',
                'kind': 'grid',
                'cards': [{
                    'id': 'hero',
                    'manifest': 'element.md',
                    'media': {'src': 'new.png', 'type': 'image'},
                    'reviewPath': 'image_review.json',
                }],
            }],
        }
        (self.root / 'showcase.json').write_text(json.dumps(self.data))

    def hash(self, relative):
        return hashlib.sha256((self.root / relative).read_bytes()).hexdigest()

    def review(self, artifact, name, method, status='pass'):
        content = {
            'schema_version': 1,
            'artifact_path': artifact,
            'artifact_sha256': self.hash(artifact),
            'status': status,
            'inspection_method': method,
            'coverage': 'The complete synthetic artifact was reviewed.',
            'checks': [{'criterion': 'Matches the brief', 'status': status, 'evidence': 'Fixture evidence'}],
            'observations': ['The requested content is visible.'],
            'limitations': [],
            'recommendation': 'Approve the passing candidate.',
        }
        (self.root / name).write_text(json.dumps(content))

    def decision(self, artifact='new.png', review='image_review.json', actor='agent', decision_type='variant_selection'):
        content = {
            'schema_version': 1,
            'decision_id': 'fixture-decision-' + artifact.replace('.', '-'),
            'decision_type': decision_type,
            'subject_path': artifact,
            'actor': actor,
            'approval_mode': selection.read_project_mode(self.root)['mode'],
            'project_sha256': self.hash('project.md'),
            'result': 'approved',
            'review_path': review,
            'review_sha256': self.hash(review),
            'upstream_sha256': {},
            'reason': 'The candidate passes the recorded checks.',
            'decided_at': datetime.datetime.now(datetime.UTC).isoformat(),
        }
        if decision_type == 'variant_selection':
            content.update({'asset_id': 'hero', 'selected_variant': artifact, 'selected_sha256': self.hash(artifact)})
        else:
            content.update({'stage_id': 'assembly-review', 'lock_kind': 'picture', 'subject_sha256': self.hash(artifact)})
        return content

    def service(self):
        return selection.SelectionService(self.root, self.data)

    def test_default_agent_selection_records_hash_bound_decision_and_canvas_sources(self):
        service = self.service()
        result = service.apply({'hero': 'new.png'}, decisions={'hero': self.decision()})
        self.assertEqual(result['decisions']['hero'], 'fixture-decision-new-png')
        self.assertEqual(service.snapshot()['selections'], {'hero': 'new.png'})
        manifest = (self.root / 'element.md').read_text()
        self.assertIn('selected_variant: new.png', manifest)
        self.assertIn('status: approved', manifest)
        self.assertIn('actor: agent', manifest)
        self.assertTrue((self.root / 'decisions/fixture-decision-new-png.json').is_file())
        stage = json.loads((self.root / 'showcase.json').read_text())['canvas']['stages'][0]
        self.assertEqual({source['path'] for source in stage['sources']}, {'new.png', 'image_review.json', 'decisions/fixture-decision-new-png.json'})

    def test_ask_mode_rejects_agent_and_accepts_local_user_choice(self):
        selection.set_project_mode(self.root, 'ask_for_approval')
        service = self.service()
        with self.assertRaises(selection.SelectionError):
            service.apply({'hero': 'new.png'}, decisions={'hero': self.decision()})
        self.assertNotIn('selected_variant: new.png', (self.root / 'element.md').read_text())
        result = service.apply({'hero': 'new.png'}, user_event='local_review_ui')
        self.assertEqual(len(result['decisions']), 1)
        saved = json.loads(next((self.root / 'decisions').glob('*.json')).read_text())
        self.assertEqual(saved['actor'], 'user')
        self.assertEqual(saved['authorization'], {'source': 'local_ui', 'evidence': 'local_review_ui'})

    def test_mode_change_rejects_stale_selection_revision(self):
        service = self.service()
        revision = service.snapshot()['revision']
        selection.set_project_mode(self.root, 'ask_for_approval')
        with self.assertRaises(selection.SelectionConflict):
            service.apply({'hero': 'new.png'}, revision, decisions={'hero': self.decision()})

    def test_agent_cannot_adopt_existing_user_selection(self):
        (self.root / 'element.md').write_text('---\nselected_variant: old.png\nstatus: approved\n---\nElement body.\n')
        with self.assertRaises(selection.SelectionError):
            self.service().apply({'hero': 'new.png'}, decisions={'hero': self.decision()})
        self.assertIn('selected_variant: old.png', (self.root / 'element.md').read_text())

    def test_keyed_selection_records_approval_without_approving_entire_bundle(self):
        (self.root / 'element.md').write_text('---\nselected_variants:\n  hero: null\nstatus: review\n---\nElement body.\n')
        card = self.data['sections'][0]['cards'][0]
        card['field'] = 'selected_variants'
        card['key'] = 'hero'
        (self.root / 'showcase.json').write_text(json.dumps(self.data))
        self.service().apply({'hero': 'new.png'}, decisions={'hero': self.decision()})
        manifest = (self.root / 'element.md').read_text()
        self.assertIn('hero: new.png', manifest)
        self.assertIn('status: review', manifest)
        self.assertIn('selection_evidence:', manifest)
        self.assertIn('actor: agent', manifest)

    def test_failed_review_cannot_approve(self):
        self.review('new.png', 'image_review.json', 'direct_image_inspection', status='fail')
        with self.assertRaises(selection.SelectionError):
            self.service().apply({'hero': 'new.png'}, decisions={'hero': self.decision()})
        self.assertFalse((self.root / 'decisions').exists())

    def test_generation_preflight_rejects_non_temporal_video_and_unheard_audio(self):
        for artifact, method in (('take.mp4', 'contact_sheet'), ('mix.wav', 'waveform')):
            (self.root / artifact).write_bytes(b'synthetic media')
            review_path = f'{artifact}.json'
            self.review(artifact, review_path, method)
            review = json.loads((self.root / review_path).read_text())
            findings = request_validation.candidate_review_findings(self.root, review, artifact, self.hash(artifact))
            self.assertTrue(any(finding.rule_id == 'approval.inspection_method' for finding in findings))

    def test_interrupted_decision_write_recovers_canvas_and_audit_once(self):
        service = self.service()
        original = selection.atomic_write

        def fail_on_selection_index(path, content):
            if path.name == 'selection.json':
                raise OSError('simulated write failure')
            original(path, content)

        with patch.object(selection, 'atomic_write', side_effect=fail_on_selection_index), self.assertRaises(selection.SelectionConflict):
            service.apply({'hero': 'new.png'}, decisions={'hero': self.decision()})
        self.assertTrue((self.root / '.selection-journal.json').exists())
        self.assertEqual(service.snapshot()['selections'], {'hero': 'new.png'})
        self.assertFalse((self.root / '.selection-journal.json').exists())
        self.assertEqual(len((self.root / 'selection.log').read_text().splitlines()), 1)

    def test_stage_lock_records_picture_decision_without_variant_selection(self):
        (self.root / 'picture.mp4').write_bytes(b'picture')
        self.review('picture.mp4', 'picture_review.json', 'direct_video_playback')
        showcase = json.loads((self.root / 'showcase.json').read_text())
        showcase['canvas']['currentStage'] = 'assembly-review'
        showcase['canvas']['stages'][0]['status'] = 'complete'
        showcase['canvas']['stages'][1]['status'] = 'active'
        (self.root / 'showcase.json').write_text(json.dumps(showcase))
        decision = self.decision('picture.mp4', 'picture_review.json', decision_type='stage_lock')
        result = selection.record_stage_decision(self.root, decision)
        self.assertEqual(result['decision_id'], decision['decision_id'])
        stage = json.loads((self.root / 'showcase.json').read_text())['canvas']['stages'][1]
        self.assertEqual(stage['locks']['picture']['artifact_sha256'], self.hash('picture.mp4'))
        self.assertEqual({source['path'] for source in stage['sources']}, {'picture.mp4', 'picture_review.json', 'decisions/fixture-decision-picture-mp4.json'})
        self.assertIn('selected_variant: null', (self.root / 'element.md').read_text())

    def test_ask_mode_stage_lock_requires_user_decision(self):
        selection.set_project_mode(self.root, 'ask_for_approval')
        (self.root / 'picture.mp4').write_bytes(b'picture')
        self.review('picture.mp4', 'picture_review.json', 'direct_video_playback')
        data = json.loads((self.root / 'showcase.json').read_text())
        data['canvas']['currentStage'] = 'assembly-review'
        data['canvas']['stages'][0]['status'] = 'complete'
        data['canvas']['stages'][1]['status'] = 'active'
        (self.root / 'showcase.json').write_text(json.dumps(data))
        agent_decision = self.decision('picture.mp4', 'picture_review.json', decision_type='stage_lock')
        with self.assertRaises(selection.SelectionError):
            selection.record_stage_decision(self.root, agent_decision)
        self.assertFalse((self.root / 'decisions').exists())
        user_decision = self.decision('picture.mp4', 'picture_review.json', actor='user', decision_type='stage_lock')
        user_decision['authorization'] = {'source': 'chat', 'evidence': 'User selected the inspected picture cut.'}
        selection.record_stage_decision(self.root, user_decision)
        saved = json.loads((self.root / 'showcase.json').read_text())
        self.assertEqual(saved['canvas']['stages'][1]['locks']['picture']['actor'], 'user')

    def test_selected_element_passes_version_two_generation_preflight(self):
        self.service().apply({'hero': 'new.png'}, decisions={'hero': self.decision()})
        (self.root / 'prompt.md').write_text('Use the selected character from @Image 1.\n')
        _, manifest, _ = selection.parse_frontmatter((self.root / 'element.md').read_text())
        evidence = dict(manifest['selection_evidence'])
        approval_fields = ('decision_id', 'decision_path', 'decision_sha256', 'review_path', 'review_sha256', 'selected_sha256')
        reference = {
            'path': 'new.png',
            'sha256': self.hash('new.png'),
            'role': 'reference_image',
            'binding': '@Image 1',
            'approval_evidence': {'manifest': 'element.md', 'field': 'selected_variant', **{key: evidence[key] for key in approval_fields}},
        }
        params = {'duration': 5, 'resolution': '720p'}
        request = {
            'schema_version': 2,
            'operation_id': 'new-shot',
            'asset_id': 'new-shot',
            'transport': 'ark-mcp',
            'model': 'fixture-model',
            'operation': 'generate',
            'prompt_file': 'prompt.md',
            'prompt_sha256': self.hash('prompt.md'),
            'request_sha256': request_validation.compute_request_hash(
                (self.root / 'prompt.md').read_bytes(), [reference], 'fixture-model', 'generate', params,
                approval_mode='approve_for_me', project_sha256=self.hash('project.md'),
            ),
            'references': [reference],
            'params': params,
            'submission_status': 'prepared',
            'provider_task_id': None,
            'provider_status': None,
            'review_status': 'not_started',
            'cost': {'estimated': None, 'confirmed': None, 'currency': 'USD'},
            'approval_mode': 'approve_for_me',
            'project_sha256': self.hash('project.md'),
        }
        capabilities = {
            'model': 'fixture-model',
            'source': 'fixture tool schema',
            'verified_at': '2026-09-23T00:00:00Z',
            'operations': ['generate'],
            'parameters': {'duration': {'minimum': 4, 'maximum': 15}, 'resolution': {'enum': ['720p']}},
            'reference_roles': ['reference_image'],
            'max_references': 3,
            'supports_first_frame_with_reference_images': False,
        }
        self.assertEqual(request_validation.validate_request(self.root, request, capabilities), [])
        (self.root / 'new.png').write_bytes(b'changed image')
        self.assertTrue(request_validation.validate_request(self.root, request, capabilities))

    def test_agent_mode_completes_synthetic_pipeline_with_fresh_canvas(self):
        stages = [{'id': stage_id, 'status': 'pending', 'sources': []} for stage_id in showcase.CANVAS_STAGE_IDS]
        for stage in stages:
            stage['sources'] = [{'path': 'project.md', 'kind': 'brief'}]
        stages[0]['status'] = stages[1]['status'] = 'complete'
        stages[2]['status'] = 'active'
        self.data['canvas']['stages'] = stages
        self.data['sections'][0]['id'] = 'hero-options'
        (self.root / 'showcase.json').write_text(json.dumps(self.data))

        self.service().apply({'hero': 'new.png'}, decisions={'hero': self.decision()})
        data = json.loads((self.root / 'showcase.json').read_text())
        showcase.generate(self.root, data, 'index.html', expected_stage='canon-elements')
        self.assertEqual(showcase.canvas_sync_errors(data, self.root, self.root / 'index.html', 'canon-elements'), [])

        (self.root / 'shot.md').write_text('---\nselected_variant: null\nstatus: review\n---\nShot body.\n')
        (self.root / 'take.mp4').write_bytes(b'synthetic video')
        self.review('take.mp4', 'take_review.json', 'direct_video_playback')
        data['sections'].append({
            'id': 'shot-options', 'stage': 'shot-generation', 'kind': 'takes',
            'groups': [{'takes': [{'id': 'shot', 'manifest': 'shot.md',
                                   'media': {'src': 'take.mp4', 'type': 'video'},
                                   'reviewPath': 'take_review.json'}]}],
        })
        for stage in data['canvas']['stages'][:6]:
            stage['status'] = 'complete'
        data['canvas']['stages'][5]['status'] = 'active'
        data['canvas']['currentStage'] = 'shot-generation'
        (self.root / 'showcase.json').write_text(json.dumps(data))
        take_decision = self.decision('take.mp4', 'take_review.json')
        take_decision['asset_id'] = 'shot'
        selection.SelectionService(self.root, data).apply({'shot': 'take.mp4'}, decisions={'shot': take_decision})
        data = json.loads((self.root / 'showcase.json').read_text())
        showcase.generate(self.root, data, 'index.html', expected_stage='shot-generation')
        self.assertEqual(showcase.canvas_sync_errors(data, self.root, self.root / 'index.html', 'shot-generation'), [])

        data['canvas']['stages'][5]['status'] = 'complete'
        data['canvas']['stages'][6]['status'] = 'active'
        data['canvas']['currentStage'] = 'assembly-review'
        (self.root / 'showcase.json').write_text(json.dumps(data))
        for kind, artifact, method in (
            ('picture', 'picture.mp4', 'direct_video_playback'),
            ('audio', 'mix.wav', 'direct_audio_listening'),
        ):
            (self.root / artifact).write_bytes(kind.encode())
            review_path = f'{kind}_review.json'
            self.review(artifact, review_path, method)
            decision = self.decision(artifact, review_path, decision_type='stage_lock')
            decision['lock_kind'] = kind
            selection.record_stage_decision(self.root, decision)
        data = json.loads((self.root / 'showcase.json').read_text())
        data['canvas']['stages'][6]['status'] = 'complete'
        data['canvas']['stages'][7]['status'] = 'active'
        data['canvas']['currentStage'] = 'delivery'
        (self.root / 'showcase.json').write_text(json.dumps(data))
        showcase.generate(self.root, data, 'index.html', expected_stage='delivery')
        self.assertEqual(showcase.canvas_sync_errors(data, self.root, self.root / 'index.html', 'delivery'), [])

        (self.root / 'master.mp4').write_bytes(b'synthetic master')
        self.review('master.mp4', 'master_review.json', 'direct_video_playback_and_listening')
        decision = self.decision('master.mp4', 'master_review.json', decision_type='stage_lock')
        decision['stage_id'] = 'delivery'
        decision['lock_kind'] = 'final_master'
        selection.record_stage_decision(self.root, decision)
        data = json.loads((self.root / 'showcase.json').read_text())
        data['canvas']['stages'][7]['status'] = 'complete'
        (self.root / 'showcase.json').write_text(json.dumps(data))
        showcase.generate(self.root, data, 'index.html', expected_stage='delivery')
        self.assertEqual(showcase.canvas_sync_errors(data, self.root, self.root / 'index.html', 'delivery'), [])
        self.assertEqual(len(list((self.root / 'decisions').glob('*.json'))), 5)


if __name__ == '__main__':
    unittest.main()
