import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / '.agents/skills/showcase-html/scripts'
sys.path.insert(0, str(SCRIPTS))
import portfolio

HAS_FFMPEG = shutil.which('ffmpeg') is not None and shutil.which('ffprobe') is not None


def make_clip(path, frequency, volume):
    subprocess.run([
        'ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc=size=72x128:rate=24:duration=1',
        '-f', 'lavfi', '-i', f'sine=frequency={frequency}:duration=1', '-af', f'volume={volume}',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', str(path),
    ], check=True)


@unittest.skipUnless(HAS_FFMPEG, 'ffmpeg is required')
class PortfolioTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)

    def project(self, slug, locked=True, volume=1.0):
        root = self.base / slug
        (root / 'assembly').mkdir(parents=True)
        (root / 'project.md').write_text(f'---\ntitle: {slug.title()}\nlogline: A {slug} story.\n---\n')
        delivery = {'id': 'delivery', 'status': 'active', 'sources': []}
        if locked:
            master = root / 'assembly' / f'{slug}_master_v01.mp4'
            make_clip(master, 440, volume)
            (root / 'assembly' / f'{slug}_master_v01.en.srt').write_text('1\n00:00:00,000 --> 00:00:00,900\nHello.\n')
            delivery['sources'] = [{'path': f'assembly/{slug}_master_v01.en.srt', 'kind': 'data'}]
            delivery['locks'] = {'final_master': {
                'result': 'approved', 'artifact_path': f'assembly/{slug}_master_v01.mp4',
                'artifact_sha256': hashlib.sha256(master.read_bytes()).hexdigest()}}
        (root / 'showcase.json').write_text(json.dumps({'canvas': {'stages': [delivery]}}))
        return root

    def test_page_uses_locked_masters_and_marks_unlocked_projects(self):
        projects = [self.project('alpha'), self.project('beta', locked=False)]
        out = self.base / 'hub'
        manifest = portfolio.build(out, projects, 'Hub', 'Two stories', False, -16.0, 0.79)
        page = (out / 'index.html').read_text()
        self.assertIn('../alpha/assembly/alpha_master_v01.mp4', page)
        self.assertIn('In production', page)
        self.assertIn('A alpha story.', page)
        self.assertTrue((out / 'alpha.en.vtt').read_text().startswith('WEBVTT'))
        self.assertIn('00:00:00.900', (out / 'alpha.en.vtt').read_text())
        self.assertIsNone(manifest['projects'][1]['master'])

    def test_showreel_requires_every_final_lock(self):
        projects = [self.project('alpha'), self.project('beta', locked=False)]
        with self.assertRaisesRegex(ValueError, 'missing: beta'):
            portfolio.build(self.base / 'hub', projects, 'Hub', '', True, -16.0, 0.79)

    def test_showreel_matches_loudness_and_records_inputs(self):
        projects = [self.project('alpha', volume=0.05), self.project('beta', volume=0.5)]
        manifest = portfolio.build(self.base / 'hub', projects, 'Hub', '', True, -20.0, 0.79)
        record = manifest['showreel']
        self.assertAlmostEqual(record['duration_s'], 2.0, delta=0.2)
        gains = [item['gain_db'] for item in record['inputs']]
        self.assertGreater(gains[0], gains[1])
        self.assertEqual(record['inputs'][0]['start_s'], 0.0)
        self.assertTrue((self.base / 'hub/showreel.json').exists())
        self.assertIn('showreel.mp4', (self.base / 'hub/index.html').read_text())

    def test_changed_master_after_lock_is_rejected(self):
        root = self.project('alpha')
        (root / 'assembly/alpha_master_v01.mp4').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'changed after its lock'):
            portfolio.build(self.base / 'hub', [root], 'Hub', '', False, -16.0, 0.79)


if __name__ == '__main__':
    unittest.main()
