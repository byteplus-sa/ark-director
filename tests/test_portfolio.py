import hashlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

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


class SubtitleContractTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / 'sample'
        self.root.mkdir()
        master = self.root / 'master.mp4'
        master.write_bytes(b'synthetic master')
        self.source = {'path': 'master.srt', 'kind': 'data'}
        (self.root / 'master.srt').write_text('1\n00:00:00,000 --> 00:00:00,900\nCaption.\n')
        self.delivery = {'id': 'delivery', 'sources': [self.source], 'locks': {'final_master': {
            'result': 'approved', 'artifact_path': 'master.mp4',
            'artifact_sha256': hashlib.sha256(master.read_bytes()).hexdigest()}}}
        self.out = self.base / 'hub'

    def write_manifest(self):
        (self.root / 'showcase.json').write_text(json.dumps({'canvas': {'stages': [self.delivery]}}))

    def render(self):
        self.write_manifest()
        with patch.object(portfolio, 'duration', return_value=1.0), patch.object(portfolio.subprocess, 'run'):
            portfolio.build(self.out, [self.root], 'Hub', '', False, -16.0, 0.79)
        return (self.out / 'index.html').read_text()

    def test_explicit_language_and_label_control_track_and_vtt(self):
        for language, label in [('en', 'English'), ('es', 'Spanish'), ('zh-Hant-TW', 'Traditional Chinese')]:
            with self.subTest(language=language):
                self.source.update(language=language, label=label)
                page = self.render()
                self.assertIn(f'srclang="{language}" label="{label}" src="sample.{language}.vtt"', page)
                self.assertIn('00:00:00.900', (self.out / f'sample.{language}.vtt').read_text())

    def test_explicit_metadata_overrides_filename_and_escapes_label(self):
        (self.root / 'master.srt').rename(self.root / 'master.en.srt')
        self.source.update(path='master.en.srt', language='fr', label='French "CC" & <notes>')
        page = self.render()
        self.assertIn('srclang="fr" label="French &quot;CC&quot; &amp; &lt;notes&gt;"', page)
        self.assertNotIn('srclang="en"', page)

    def test_legacy_language_suffix_remains_supported(self):
        for language in ['en', 'sw', 'pt-BR']:
            with self.subTest(language=language):
                path = self.root / f'master.{language}.srt'
                path.write_text('1\n00:00:00,000 --> 00:00:00,900\nCaption.\n')
                self.source['path'] = path.name
                self.assertIn(f'srclang="{language}"', self.render())

    def test_unknown_language_is_actionable_cli_error_without_rendering(self):
        self.write_manifest()
        errors = io.StringIO()
        with redirect_stderr(errors), patch.object(portfolio.subprocess, 'run') as run:
            result = portfolio.main([str(self.out), str(self.root)])
        self.assertEqual(result, 1)
        self.assertIn('language', json.loads(errors.getvalue())['error'])
        self.assertIn('master.srt', json.loads(errors.getvalue())['error'])
        run.assert_not_called()
        self.assertFalse((self.out / 'index.html').exists())

    def test_invalid_language_and_label_are_rejected_before_rendering(self):
        for language in ['', None, 123, [], 'und', 'en_US', '../en', 'en/../../escape', 'en" onload="x', 'e', 'en--US']:
            with self.subTest(language=language):
                self.source['language'] = language
                with self.assertRaisesRegex(ValueError, 'language'):
                    self.render()
        self.source['language'] = 'es'
        for label in ['', '   ', None, 123, []]:
            with self.subTest(label=label):
                self.source['label'] = label
                with self.assertRaisesRegex(ValueError, 'label'):
                    self.render()

    def test_subtitle_missing_traversal_and_symlink_escape_are_rejected(self):
        outside = self.base / 'master.es.srt'
        outside.write_text('Private fixture')
        (self.root / 'master.link.srt').symlink_to(outside)
        self.source['language'] = 'es'
        for path in ['master.missing.srt', '../master.es.srt', 'master.link.srt']:
            with self.subTest(path=path):
                self.source['path'] = path
                with self.assertRaisesRegex(ValueError, 'missing or escaping'):
                    self.render()

    def test_no_subtitles_requires_no_language(self):
        self.delivery['sources'] = []
        self.assertNotIn('<track', self.render())


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

    def test_cli_renders_explicit_non_english_subtitles(self):
        root = self.project('sample')
        showcase = json.loads((root / 'showcase.json').read_text())
        source = showcase['canvas']['stages'][0]['sources'][0]
        source.update(language='es', label='Spanish')
        (root / source['path']).write_text('1\n00:00:00,000 --> 00:00:00,900\nHola.\n')
        (root / 'showcase.json').write_text(json.dumps(showcase))
        out = self.base / 'cli-hub'
        result = subprocess.run(
            [sys.executable, '-B', str(SCRIPTS / 'portfolio.py'), str(out), str(root)],
            capture_output=True, text=True, check=True,
        )
        self.assertTrue(json.loads(result.stdout)['ok'])
        self.assertIn('srclang="es" label="Spanish"', (out / 'index.html').read_text())
        self.assertIn('Hola.', (out / 'sample.es.vtt').read_text())
        self.assertFalse((out / 'sample.en.vtt').exists())
        self.assertGreater((out / 'poster_sample.jpg').stat().st_size, 0)

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
