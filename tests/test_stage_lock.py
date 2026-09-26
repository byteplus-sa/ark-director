import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / '.agents/skills/showcase-html/scripts'
sys.path.insert(0, str(SCRIPTS))
import stage_lock

HAS_FFMPEG = shutil.which('ffmpeg') is not None and shutil.which('ffprobe') is not None


@unittest.skipUnless(HAS_FFMPEG, 'ffmpeg is required for media inspection')
class StageLockTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / 'demo'
        self.root.mkdir()
        (self.root / 'project.md').write_text('---\ntitle: Demo\napproval_mode: approve_for_me\n---\n\nBrief.\n')
        subprocess.run([sys.executable, str(SCRIPTS / 'generate_showcase.py'), str(self.root), '--init'], check=True, capture_output=True)
        data = json.loads((self.root / 'showcase.json').read_text())
        for stage in data['canvas']['stages']:
            if stage['id'] == 'assembly-review':
                stage['status'] = 'active'
                break
            stage['status'] = 'skipped' if stage['id'] == 'audio-preparation' else 'complete'
            stage['sources'] = [{'path': 'project.md', 'kind': 'brief'}]
        data['canvas']['currentStage'] = 'assembly-review'
        (self.root / 'showcase.json').write_text(json.dumps(data, indent=2))
        subprocess.run([
            'ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc=size=72x128:rate=24:duration=1',
            '-f', 'lavfi', '-i', 'sine=duration=1', '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-shortest', str(self.root / 'master.mp4'),
        ], check=True)

    def run_cli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = stage_lock.main([*argv])
        return code, json.loads(out.getvalue() or err.getvalue())

    def canvas(self):
        return json.loads((self.root / 'showcase.json').read_text())['canvas']

    def review(self, out='qa/review_master.json', method='temporal playback review'):
        return self.run_cli(
            'review', str(self.root), '--artifact', 'master.mp4', '--out', out, '--method', method,
            '--coverage', 'whole master', '--check', 'technical=pass: decodes', '--observation', 'clean',
            '--recommendation', 'lock')

    def lock(self, kind='picture', decision_id=None, *extra):
        args = ['lock', str(self.root), '--kind', kind, '--artifact', 'master.mp4',
                '--review', 'qa/review_master.json', '--reason', 'passes review']
        if decision_id:
            args += ['--decision-id', decision_id]
        return self.run_cli(*args, *extra)

    def test_review_rejects_video_without_playback_evidence(self):
        code, result = self.review(method='contact sheet of frames')
        self.assertEqual(code, 1)
        self.assertIn('temporal or playback', result['error'])
        self.assertFalse((self.root / 'qa/review_master.json').exists())

    def test_review_with_failing_check_is_written_as_fail(self):
        code, result = self.run_cli(
            'review', str(self.root), '--artifact', 'master.mp4', '--out', 'qa/r.json',
            '--method', 'temporal playback', '--coverage', 'all', '--check', 'dialogue=fail: wrong word',
            '--observation', 'wrong word', '--recommendation', 'retake')
        self.assertEqual(code, 1)
        self.assertEqual(result['status'], 'fail')

    def test_review_refuses_to_overwrite_without_replace(self):
        self.assertEqual(self.review()[0], 0)
        code, result = self.review()
        self.assertEqual(code, 1)
        self.assertIn('--replace', result['error'])

    def test_advance_requires_lock_then_moves_to_next_stage(self):
        code, result = self.run_cli('advance', str(self.root), '--stage', 'assembly-review')
        self.assertEqual(code, 1)
        self.assertIn('picture lock is required', result['error'])
        self.review()
        code, result = self.lock()
        self.assertEqual(code, 0, result)
        code, result = self.run_cli('advance', str(self.root), '--stage', 'assembly-review')
        self.assertEqual(code, 1)
        self.assertIn('--source', result['error'])
        code, result = self.run_cli('advance', str(self.root), '--stage', 'assembly-review', '--source', 'master.mp4:media')
        self.assertEqual(code, 0, result)
        canvas = self.canvas()
        self.assertEqual(canvas['currentStage'], 'delivery')
        statuses = {stage['id']: stage['status'] for stage in canvas['stages']}
        self.assertEqual(statuses['assembly-review'], 'complete')
        self.assertEqual(statuses['delivery'], 'active')
        decision = json.loads((self.root / 'decisions/lock_picture_master.json').read_text())
        self.assertEqual(decision['stage_id'], 'assembly-review')
        self.assertIn('decided_at', decision)

    def test_advance_rejects_wrong_asserted_stage(self):
        code, result = self.run_cli('advance', str(self.root), '--stage', 'delivery')
        self.assertEqual(code, 1)
        self.assertIn('current stage is assembly-review', result['error'])

    def test_lock_for_user_requires_authorization(self):
        self.review()
        code, result = self.lock('picture', None, '--actor', 'user')
        self.assertEqual(code, 1)
        self.assertIn('--authorization', result['error'])

    def test_reopen_supersedes_locks_and_resets_later_stages(self):
        self.review()
        self.lock()
        self.assertEqual(self.run_cli('advance', str(self.root), '--source', 'master.mp4:media')[0], 0)
        code, result = self.run_cli('reopen', str(self.root), '--stage', 'assembly-review', '--reason', 'user asked for a recut')
        self.assertEqual(code, 0, result)
        canvas = self.canvas()
        stages = {stage['id']: stage for stage in canvas['stages']}
        self.assertEqual(canvas['currentStage'], 'assembly-review')
        self.assertEqual(stages['assembly-review']['status'], 'active')
        self.assertEqual(stages['delivery']['status'], 'pending')
        self.assertNotIn('locks', stages['assembly-review'])
        history = stages['assembly-review']['supersededLocks'][0]
        self.assertEqual(history['reason'], 'user asked for a recut')
        self.assertIn('picture', history['locks'])
        event = json.loads((self.root / 'selection.log').read_text().splitlines()[-1])
        self.assertEqual(event['event'], 'reopen_stage')
        check = subprocess.run([sys.executable, str(SCRIPTS / 'generate_showcase.py'), str(self.root), '--check', '--stage', 'assembly-review'], capture_output=True, text=True, check=False)
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_reopen_rejects_future_stage(self):
        code, result = self.run_cli('reopen', str(self.root), '--stage', 'delivery', '--reason', 'skip ahead')
        self.assertEqual(code, 1)
        self.assertIn('use advance', result['error'])


if __name__ == '__main__':
    unittest.main()
