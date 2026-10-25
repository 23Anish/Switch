from pathlib import Path
import copy
import json
import re

root = Path(__file__).resolve().parents[1]
dsa = json.loads((root / 'dsa.json').read_text())
lessons = json.loads((root / 'lessons.json').read_text())
if (root / 'design-lessons.json').exists():
    lessons += json.loads((root / 'design-lessons.json').read_text())
companies = json.loads((root / 'companies.json').read_text()) if (root / 'companies.json').exists() else []
assert len({p['id'] for p in dsa}) == len(dsa)
assert len({p['id'] for p in lessons}) == len(lessons)
for p in dsa:
    assert p['cpp']['version'] == 2 and p['cpp']['signature'] and p['cpp']['adapter'], p['id']
    for field in ('starters', 'solutions'):
        assert not re.search(r'\b(?:json|nlohmann)\b', p[field]['cpp']), f"{p['id']}: exposed runner in {field}"
web_dsa = copy.deepcopy(dsa)
for p in web_dsa:
    del p['cpp']['adapter']
(root / 'web/data.js').write_text('window.DSA = ' + json.dumps(web_dsa, ensure_ascii=False) + ';\nwindow.LESSONS = ' + json.dumps(lessons, ensure_ascii=False) + ';\nwindow.COMPANIES = ' + json.dumps(companies, ensure_ascii=False) + ';\n')
include = root / 'native/include'
(include / 'cpp-adapters.json').write_text(json.dumps({p['id']: p['cpp']['adapter'] for p in dsa}, ensure_ascii=False))
# Exercise nullable values, strings, lists, trees, graphs, and dynamic programming
# through the same bundled adapter lookup used by the app's UI.
smoke_ids = {'dsa-002', 'dsa-031', 'dsa-051', 'dsa-081', 'dsa-101', 'dsa-121', 'dsa-171', 'dsa-225'}
(include / 'cpp-smoke.json').write_text(json.dumps([{'id': p['id'], 'code': p['solutions']['cpp'], 'tests': p['tests']} for p in dsa if p['id'] in smoke_ids]))
print(f'Bundled {len(dsa)} problems, {len(lessons)} lessons, {len(companies)} company tracks; C++ API v2')

examples=json.loads((root / 'theory-examples.json').read_text())
with (root / 'web/data.js').open('a') as bundle:
    bundle.write('window.THEORY_EXAMPLES = ' + json.dumps(examples, ensure_ascii=False) + ';\n')
print(f'Bundled {len(examples)} worked theory examples')
