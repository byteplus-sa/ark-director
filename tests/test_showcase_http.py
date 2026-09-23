import hashlib
import http.client
import json
import secrets
import shutil
import subprocess
import threading
import unittest
from http.server import HTTPServer

import test_showcase_selection as fixtures

showcase = fixtures.showcase


class ShowcaseHTTPTests(unittest.TestCase):
    files = fixtures.ShowcaseRegressionTests.files
    lifecycle_canvas = fixtures.ShowcaseRegressionTests.lifecycle_canvas
    def setUp(self):
        fixtures.ShowcaseRegressionTests.setUp(self)
        handler = type('TestHandler', (showcase.ShowcaseHandler,), {
            'proj': self.root,
            'service': self.service,
            'session_token': secrets.token_urlsafe(32),
        })
        self.server = HTTPServer(('127.0.0.1', 0), handler)
        self.worker = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.worker.start()
        self.addCleanup(self.close_server)
        self.token = handler.session_token
        self.origin = f'http://127.0.0.1:{self.server.server_port}'

    def close_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.worker.join(2)

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=3)
        self.addCleanup(connection.close)
        connection.request(method, path, body, headers or {})
        response = connection.getresponse()
        return response.status, dict(response.headers), response.read()

    def configure_stage_lock_project(self):
        if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
            self.skipTest('ffmpeg and ffprobe required for stage lock media')
        data = self.lifecycle_canvas()
        data['canvas']['approvalContractVersion'] = 1
        data['canvas']['currentStage'] = 'assembly-review'
        for stage in data['canvas']['stages']:
            if stage['id'] == 'assembly-review':
                stage['status'] = 'review'
                stage['sources'] = [{'path': 'project.md', 'kind': 'brief'}]
                stage['lockCandidates'] = [{
                    'lock_kind': 'picture',
                    'artifact_path': 'picture.mp4',
                    'review_path': 'picture-review.json',
                    'reason': 'Passing picture review',
                    'upstream_sha256': {},
                }]
            elif stage['id'] == 'audio-preparation':
                stage['status'] = 'skipped'
            elif stage['id'] != 'delivery':
                stage['status'] = 'complete'
                stage['sources'] = [{'path': 'project.md', 'kind': 'brief'}]
        (self.root / 'project.md').write_text('---\napproval_mode: ask_for_approval\n---\n# Project brief\n')
        subprocess.run([
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-f', 'lavfi',
            '-i', 'color=c=blue:s=160x90:r=24:d=1', '-an', '-c:v',
            'libx264', '-pix_fmt', 'yuv420p', str(self.root / 'picture.mp4'),
        ], check=True, capture_output=True)
        review = {
            'schema_version': 1,
            'artifact_path': 'picture.mp4',
            'artifact_sha256': hashlib.sha256((self.root / 'picture.mp4').read_bytes()).hexdigest(),
            'status': 'pass',
            'inspection_method': 'direct_video_playback',
            'coverage': 'Complete synthetic picture reviewed.',
            'checks': [{'criterion': 'Picture continuity', 'status': 'pass', 'evidence': 'Synthetic fixture'}],
            'observations': ['The picture meets the test brief.'],
            'limitations': [],
            'recommendation': 'Approve the picture.',
        }
        (self.root / 'picture-review.json').write_text(json.dumps(review))
        (self.root / 'showcase.json').write_text(json.dumps(data))
        handler = self.server.RequestHandlerClass
        handler.service = fixtures.selection.SelectionService(self.root, data)
        handler.data = data
        handler.expected_stage = 'assembly-review'
        showcase.generate(self.root, data, 'index.html', expected_stage='assembly-review')
        return data

    def test_save_requires_origin_and_session_then_reloads(self):
        _, _, body = self.request('GET', '/api/session')
        snapshot = json.loads(body)
        payload = json.dumps({'selections': {'hero': 'new.png'}, 'expected_revision': snapshot['revision']})
        headers = {'Content-Type': 'application/json', 'Origin': self.origin, 'X-Showcase-Token': self.token}
        before = self.files()
        for overrides in ({'Origin': 'https://example.com'}, {'X-Showcase-Token': 'wrong'}):
            status, _, _ = self.request('POST', '/api/select', payload, {**headers, **overrides})
            self.assertEqual(status, 403)
            self.assertEqual(before, self.files())
        status, _, body = self.request('POST', '/api/select', payload, headers)
        self.assertEqual(status, 200, body)
        _, _, body = self.request('GET', '/api/selection')
        self.assertEqual(json.loads(body)['selections'], {'hero': 'new.png'})
        status, _, _ = self.request('POST', '/api/select', payload, headers)
        self.assertEqual(status, 409)

    def test_oversized_request_and_wrong_host_rejected(self):
        headers = {'Content-Type': 'application/json', 'Origin': self.origin, 'X-Showcase-Token': self.token}
        status, _, _ = self.request('POST', '/api/select', 'x' * 65537, headers)
        self.assertEqual(status, 413)
        status, _, _ = self.request('GET', '/api/session', headers={'Host': 'untrusted.test'})
        self.assertEqual(status, 403)

    def test_streamed_byte_ranges_and_path_containment(self):
        media = bytes(range(256)) * 1024
        (self.root / 'video.mp4').write_bytes(media)
        status, headers, body = self.request('GET', '/video.mp4', headers={'Range': 'bytes=100-199'})
        self.assertEqual(status, 206)
        self.assertEqual(body, media[100:200])
        self.assertEqual(headers['Content-Range'], f'bytes 100-199/{len(media)}')
        status, _, body = self.request('GET', '/video.mp4', headers={'Range': 'bytes=-17'})
        self.assertEqual(status, 206)
        self.assertEqual(body, media[-17:])
        status, _, _ = self.request('GET', '/video.mp4', headers={'Range': 'bytes=999999-'})
        self.assertEqual(status, 416)
        for path in ('/../outside.md', '/%2e%2e/outside.md', '/.selection.lock'):
            status, _, _ = self.request('GET', path)
            self.assertEqual(status, 404)

    def test_selection_save_refreshes_production_canvas(self):
        data = self.lifecycle_canvas()
        card = data['sections'][0]['cards'][0]
        card.update({'id': 'hero', 'manifest': 'shot.md'})
        (self.root / 'showcase.json').write_text(json.dumps(data))
        handler = self.server.RequestHandlerClass
        handler.service = fixtures.selection.SelectionService(self.root, data)
        handler.data = data
        handler.expected_stage = 'brief-development'
        showcase.generate(self.root, data, 'index.html', expected_stage='brief-development')
        _, _, body = self.request('GET', '/api/session')
        snapshot = json.loads(body)
        payload = json.dumps({'selections': {'hero': 'new.png'}, 'expected_revision': snapshot['revision']})
        headers = {'Content-Type': 'application/json', 'Origin': self.origin, 'X-Showcase-Token': self.token}
        status, _, body = self.request('POST', '/api/select', payload, headers)
        self.assertEqual(status, 200, body)
        self.assertTrue(json.loads(body)['canvasSynced'])
        self.assertEqual(showcase.canvas_sync_errors(data, self.root, self.root / 'index.html', 'brief-development'), [])

    def test_versioned_browser_save_records_user_actor_and_refreshes_canvas(self):
        data = self.lifecycle_canvas()
        data['canvas']['approvalContractVersion'] = 1
        card = data['sections'][0]['cards'][0]
        card.update({'id': 'hero', 'manifest': 'shot.md', 'field': 'selected_variants', 'key': 'hero', 'reviewPath': 'hero-review.json'})
        review = {
            'schema_version': 1,
            'artifact_path': 'new.png',
            'artifact_sha256': hashlib.sha256((self.root / 'new.png').read_bytes()).hexdigest(),
            'status': 'pass',
            'inspection_method': 'direct_image_inspection',
            'coverage': 'The complete synthetic image was inspected.',
            'checks': [{'criterion': 'Identity', 'status': 'pass', 'evidence': 'Synthetic fixture'}],
            'observations': ['Image matches the test brief.'],
            'limitations': [],
            'recommendation': 'Approve.',
        }
        (self.root / 'hero-review.json').write_text(json.dumps(review))
        (self.root / 'showcase.json').write_text(json.dumps(data))
        handler = self.server.RequestHandlerClass
        handler.service = fixtures.selection.SelectionService(self.root, data)
        handler.data = data
        handler.expected_stage = 'brief-development'
        showcase.generate(self.root, data, 'index.html', expected_stage='brief-development')
        _, _, body = self.request('GET', '/api/session')
        revision = json.loads(body)['revision']
        payload = json.dumps({'selections': {'hero': 'new.png'}, 'expected_revision': revision, 'actor': 'agent'})
        headers = {'Content-Type': 'application/json', 'Origin': self.origin, 'X-Showcase-Token': self.token}
        status, _, body = self.request('POST', '/api/select', payload, headers)
        self.assertEqual(status, 200, body)
        result = json.loads(body)
        self.assertTrue(result['canvasSynced'])
        decision = json.loads((self.root / f"decisions/{result['decisions']['hero']}.json").read_text())
        self.assertEqual(decision['actor'], 'user')
        self.assertEqual(decision['authorization']['source'], 'local_ui')
        self.assertGreaterEqual(len(decision['authorization']['evidence']), 24)
        self.assertEqual(showcase.canvas_sync_errors(json.loads((self.root / 'showcase.json').read_text()), self.root, self.root / 'index.html', 'brief-development'), [])

    def test_ask_mode_stage_lock_requires_registered_candidate_and_refreshes_canvas(self):
        self.configure_stage_lock_project()
        _, _, body = self.request('GET', '/api/session')
        session = json.loads(body)
        payload = {
            'candidate': {'lock_kind': 'picture', 'artifact_path': 'picture.mp4'},
            'canvas_manifest_sha256': hashlib.sha256((self.root / 'showcase.json').read_bytes()).hexdigest(),
            'expected_revision': session['stageRevision'],
        }
        headers = {'Content-Type': 'application/json', 'Origin': self.origin, 'X-Showcase-Token': self.token}
        before = self.files()
        invalid = {**payload, 'candidate': {'lock_kind': 'picture', 'artifact_path': 'unlisted.mp4'}}
        status, _, _ = self.request('POST', '/api/stage-lock', json.dumps(invalid), headers)
        self.assertEqual(status, 400)
        self.assertEqual(self.files(), before)
        status, _, _ = self.request('POST', '/api/stage-lock', json.dumps(payload), {**headers, 'X-Showcase-Token': 'wrong'})
        self.assertEqual(status, 403)
        self.assertEqual(self.files(), before)
        status, _, body = self.request('POST', '/api/stage-lock', json.dumps(payload), headers)
        self.assertEqual(status, 200, body)
        result = json.loads(body)
        self.assertTrue(result['canvasSynced'])
        saved = json.loads((self.root / 'showcase.json').read_text())
        lock = saved['canvas']['stages'][-2]['locks']['picture']
        self.assertEqual(lock['actor'], 'user')
        decision = json.loads((self.root / f"decisions/{lock['decision_id']}.json").read_text())
        self.assertEqual(decision['authorization']['source'], 'local_ui')
        self.assertGreaterEqual(len(decision['authorization']['evidence']), 24)
        self.assertEqual(showcase.canvas_sync_errors(saved, self.root, self.root / 'index.html', 'assembly-review'), [])
        status, _, _ = self.request('POST', '/api/stage-lock', json.dumps(payload), headers)
        self.assertEqual(status, 409)


if __name__ == '__main__':
    unittest.main()
