from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
dsa=json.loads((root/'dsa.json').read_text())
lessons=json.loads((root/'lessons.json').read_text())
if (root/'design-lessons.json').exists(): lessons+=json.loads((root/'design-lessons.json').read_text())
companies=json.loads((root/'companies.json').read_text()) if (root/'companies.json').exists() else []
assert len({p['id'] for p in dsa})==len(dsa)
assert len({p['id'] for p in lessons})==len(lessons)
(root/'web/data.js').write_text('window.DSA = '+json.dumps(dsa,ensure_ascii=False)+';\nwindow.LESSONS = '+json.dumps(lessons,ensure_ascii=False)+';\nwindow.COMPANIES = '+json.dumps(companies,ensure_ascii=False)+';\n')
print(f'Bundled {len(dsa)} problems, {len(lessons)} lessons, {len(companies)} company tracks')
