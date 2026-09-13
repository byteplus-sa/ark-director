import json
import os
import shutil
import subprocess
import unittest

import test_showcase_http as http_fixtures
import test_showcase_selection as fixtures


@unittest.skipUnless(os.environ.get('SHOWCASE_BROWSER_SMOKE') == '1', 'Set SHOWCASE_BROWSER_SMOKE=1 with Node playwright and ffmpeg available')
class ShowcaseBrowserSmoke(unittest.TestCase):
    request = http_fixtures.ShowcaseHTTPTests.request
    close_server = http_fixtures.ShowcaseHTTPTests.close_server
    files = fixtures.ShowcaseRegressionTests.files
    setUp = http_fixtures.ShowcaseHTTPTests.setUp

    def write_video(self, filename, color):
        subprocess.run([
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-f', 'lavfi',
            '-i', f'color=c={color}:s=160x90:r=24:d=1', '-an', '-c:v',
            'libx264', '-pix_fmt', 'yuv420p', str(self.root / filename),
        ], check=True, capture_output=True)

    def test_takes_only_save_reload_playback_and_file_read_only(self):
        if not shutil.which('ffmpeg'):
            self.skipTest('ffmpeg required for synthetic media')
        self.manifest.write_text('---\nselected_variant: first.mp4\n---\nSynthetic shot\n')
        for name, color in (('first.mp4', 'blue'), ('second.mp4', 'red')):
            self.write_video(name, color)
        data = {'title': 'Takes-only browser smoke', 'sections': [{'kind': 'takes', 'id': 'takes', 'title': 'Takes', 'groups': [{'title': 'Synthetic scene', 'takes': [{'id': 'shot', 'manifest': 'shot.md', 'filename': name, 'media': {'type': 'video', 'src': name}} for name in ('first.mp4', 'second.mp4')]}]}]}
        (self.root / 'showcase.json').write_text(json.dumps(data))
        self.server.RequestHandlerClass.service = fixtures.selection.SelectionService(self.root, data)
        fixtures.showcase.generate(self.root, data, 'index.html')
        script = r'''
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({headless: true, channel: process.env.SHOWCASE_BROWSER_CHANNEL || 'chrome'});
  try {
    const page = await browser.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(process.env.SHOWCASE_SMOKE_URL);
    await page.locator('[data-filename="first.mp4"].selected').waitFor();
    await page.locator('.sel-save').waitFor();
    await page.waitForFunction(() => [...document.querySelectorAll('video')].every(video => video.readyState >= 1));
    await page.locator('[data-filename="second.mp4"]').click();
    await page.locator('.sel-save').click();
    await page.waitForFunction(() => document.querySelector('.sel-status').textContent.startsWith('Saved 1'));
    await page.reload();
    await page.locator('[data-filename="second.mp4"].selected').waitFor();
    await page.goto(process.env.SHOWCASE_SMOKE_FILE);
    if (await page.locator('.sel-save, .select-toggle').count()) throw new Error('file review exposed writes');
    if (errors.length) throw new Error(errors.join('\n'));
    process.stdout.write('Takes-only selection saved, reloaded, media metadata loaded; file preview read-only.\n');
  } finally {
    await browser.close();
  }
})().catch(error => { process.stderr.write(error.stack + '\n'); process.exit(1); });
'''
        environment = {**os.environ, 'SHOWCASE_SMOKE_URL': self.origin + '/index.html', 'SHOWCASE_SMOKE_FILE': (self.root / 'index.html').as_uri()}
        result = subprocess.run(['node', '-e', script], env=environment, capture_output=True, text=True, timeout=90, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.server.RequestHandlerClass.service.snapshot()['selections'], {'shot': 'second.mp4'})

    def test_video_cards_lazy_load_and_play_in_both_review_modes(self):
        if not shutil.which('ffmpeg'):
            self.skipTest('ffmpeg required for synthetic media')
        self.write_video('video.mp4', 'green')
        data = {'title': 'Video card browser smoke', 'sections': [{'kind': 'grid', 'id': 'videos', 'title': 'Videos', 'cards': [{'type': 'video', 'media': {'type': 'video', 'src': 'video.mp4'}}]}]}
        (self.root / 'showcase.json').write_text(json.dumps(data))
        self.server.RequestHandlerClass.service = fixtures.selection.SelectionService(self.root, data)
        fixtures.showcase.generate(self.root, data, 'index.html')
        script = r'''
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({headless: true, channel: process.env.SHOWCASE_BROWSER_CHANNEL || 'chrome'});
  try {
    const page = await browser.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    for (const url of [process.env.SHOWCASE_SMOKE_URL, process.env.SHOWCASE_SMOKE_FILE]) {
      await page.goto(url);
      if (await page.locator('video').count()) throw new Error('video initialized before activation');
      await page.getByRole('button', {name: 'Play video', exact: true}).click();
      await page.locator('video').waitFor();
      await page.waitForFunction(() => {
        const video = document.querySelector('video');
        return video && video.readyState >= 2 && video.currentTime > 0 && !video.paused;
      });
    }
    if (errors.length) throw new Error(errors.join('\n'));
    process.stdout.write('Video card lazy playback works in served and file review modes.\n');
  } finally {
    await browser.close();
  }
})().catch(error => { process.stderr.write(error.stack + '\n'); process.exit(1); });
'''
        environment = {**os.environ, 'SHOWCASE_SMOKE_URL': self.origin + '/index.html', 'SHOWCASE_SMOKE_FILE': (self.root / 'index.html').as_uri()}
        result = subprocess.run(['node', '-e', script], env=environment, capture_output=True, text=True, timeout=90, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
