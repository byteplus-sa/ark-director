import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests/fixtures'


def outside_fences(text):
    output = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            character = marker.group(1)[0]
            if fence is None:
                fence = character
            elif fence == character:
                fence = None
        elif fence is None:
            output.append(line)
    if fence is not None:
        raise ValueError('Unclosed Markdown code fence')
    return '\n'.join(output)


class PromptContractResourceTests(unittest.TestCase):
    def setUp(self):
        self.inventory = json.loads((FIXTURES / 'prompt_disclosure_inventory.json').read_text())

    def test_each_split_skill_has_a_small_entrypoint_and_focused_local_references(self):
        for skill in self.inventory['skills']:
            entry = ROOT / '.agents/skills' / skill['skill'] / 'SKILL.md'
            with self.subTest(skill=skill['skill']):
                self.assertLess(len(entry.read_text().splitlines()), 500)
                self.assertGreater(len(skill['references']), 1)
                for reference in skill['references']:
                    path = ROOT / reference
                    self.assertTrue(path.is_file(), reference)
                    self.assertLess(len(path.read_text().splitlines()), 350, reference)
                    self.assertEqual(path.parents[1], entry.parent)

    def test_mode_reference_links_resolve_without_loading_a_sibling_skill(self):
        for skill in self.inventory['skills']:
            entry = ROOT / '.agents/skills' / skill['skill'] / 'SKILL.md'
            for path in [entry, *(ROOT / item for item in skill['references'])]:
                with self.subTest(path=path):
                    prose = outside_fences(path.read_text())
                    for target in re.findall(r'\]\(([^\s)]+)\)', prose):
                        if re.match(r'^[a-z]+:|#', target):
                            continue
                        destination = (path.parent / target.split('#')[0]).resolve()
                        self.assertTrue(destination.is_file(), f'{path}: {target}')
                        if destination.name == 'SKILL.md':
                            self.assertEqual(destination, entry)

    def test_markdown_fence_reader_accepts_literal_headings_and_rejects_unclosed_blocks(self):
        self.assertEqual(outside_fences('## Real\n```text\n## Example\n```\n'), '## Real')
        with self.assertRaises(ValueError):
            outside_fences('```text\nunfinished')

    def test_review_provenance_resolves_owned_catalog_and_stable_rule_ids(self):
        path = ROOT / '.agents/skills/prompt-review/references/rule-provenance.json'
        provenance = json.loads(path.read_text())
        catalog = json.loads((path.parent / provenance['rule_catalog']).read_text())
        self.assertEqual(catalog['schema_version'], provenance['rule_catalog_schema_version'])
        self.assertTrue((path.parent / provenance['policy_owner']).is_file())
        known_rules = {rule['id'] for rule in catalog['rules']}
        self.assertTrue(set(provenance['rule_ids']).issubset(known_rules))

    def test_behavior_scenarios_are_unique_and_contain_decisions_not_prose_matchers(self):
        fixtures = json.loads((FIXTURES / 'prompt_reliability_cases.json').read_text())
        cases = fixtures['cases']
        self.assertEqual(fixtures['generation_policy'], 'mocked_only')
        self.assertEqual(len(cases), len({case['id'] for case in cases}))
        for case in cases:
            with self.subTest(case=case['id']):
                self.assertTrue((ROOT / '.agents/skills' / case['skill'] / 'SKILL.md').is_file())
                self.assertTrue(case['prompt'])
                self.assertTrue(case['expected_decisions'])
                self.assertNotIn('contains_text', case['expected_decisions'])
                self.assertNotIn('observed_decisions', case)

    def test_production_guidance_has_no_financial_prerequisite(self):
        paths = [
            ROOT / 'AGENTS.md',
            ROOT / '.agents/contracts/production-policy.md',
            ROOT / '.agents/contracts/performance-direction.md',
        ]
        for name in ('film-production', 'micro-drama', 'byteplus-katana',
                     'seedance-vfx-pipeline', 'seedance-vfx-prompt',
                     'seedance-effects-studio', 'scene-board-sheet',
                     'seedream-storyboard', 'brief-intake',
                     'seed-audio-commercial', 'seed-audio-prompt',
                     'seedance-ai-avatar', 'template-factory',
                     'prompt-review', 'ark-mcp', 'seedance-prompt-25'):
            paths.extend((ROOT / '.agents/skills' / name).rglob('*.md'))
            paths.extend((ROOT / '.agents/skills' / name).rglob('evals.json'))
        financial_gate = re.compile(
            r'\brun budget\b|\bdeclared budget\b|\bbudget cap\b|\bcredit cap\b'
            r'|\bcredit budget\b|\bspend authority\b|\bstop at.*\bcap\b'
            r'|\bcost preview is confirmed\b|\b90 s at final resolution\b'
            r'|\bbudget posture\b|\bcapability and cost are resolved\b'
            r'|\bestimate exceeds the cap\b'
            r'|\bprivacy and cost checks\b|\bbudget spare\b'
            r'|\bresolve current token cost\b'
            r'|\bSet `DAILY_BUDGET_USD`'
            r'|\bright[s]?(?: and|,) budget\b|\brevision within budget\b'
            r'|\boutput and budget\b',
            re.IGNORECASE,
        )
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                text = ' '.join(path.read_text().split())
                self.assertIsNone(financial_gate.search(text))


if __name__ == '__main__':
    unittest.main()
