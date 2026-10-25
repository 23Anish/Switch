#!/usr/bin/env python3
"""Validate curriculum, typed starters, and Python/C++ reference solutions."""
from pathlib import Path
import copy
import json
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

root = Path(__file__).resolve().parents[1]
files = [Path(x).resolve() for x in sys.argv[1:]] or [root / 'dsa.json']
problems = [p for f in files for p in json.loads(f.read_text())]
assert len({p['id'] for p in problems}) == len(problems), 'Duplicate problem IDs'
assert len({p['title'].casefold() for p in problems}) == len(problems), 'Duplicate titles'
failures = []
count = 0
for p in problems:
    for field in ['id', 'title', 'topic', 'difficulty', 'statement', 'inputFormat', 'outputFormat', 'constraints', 'exampleExplanation', 'approaches', 'solutions', 'starters', 'tests', 'cpp']:
        assert p.get(field), f'{p["id"]}: missing {field}'
    assert p['difficulty'] in ['Easy', 'Medium', 'Hard']
    assert isinstance(p['constraints'], list)
    assert p['cpp']['version'] == 2 and p['cpp']['signature'] and p['cpp']['adapter']
    for field in ('solutions', 'starters'):
        assert not re.search(r'\b(?:json|nlohmann)\b', p[field]['cpp']), f'{p["id"]}: runner exposed in {field}'
    env = {}
    exec(p['solutions']['python'], env)
    for test in p['tests']:
        try:
            actual = env['solve'](copy.deepcopy(test['input']))
            if actual != test['expected']:
                failures.append((p['id'], 'python', actual, test['expected']))
        except Exception as e:
            failures.append((p['id'], 'python', str(e)))
        count += 1
print(f'Python: {count} tests, {len(failures)} failures', flush=True)
if failures:
    print(failures)
    sys.exit(1)

with tempfile.TemporaryDirectory(prefix='switch-check-') as folder:
    td = Path(folder)
    # Compile each visible snippet using only its own standard-library includes.
    # Runtime headers must not hide missing includes or nonstandard C++ dependencies.
    jobs = [(p, field) for p in problems for field in ('solutions', 'starters')]
    def standalone(job):
        p, field = job
        source = td / f'{p["id"]}-{field}.cpp'
        source.write_text(p[field]['cpp'])
        result = subprocess.run(['clang++', '-std=c++17', '-fsyntax-only', str(source)], capture_output=True, text=True, timeout=60)
        return None if result.returncode == 0 else f'{p["id"]} {field}:\n{result.stderr}'
    with ThreadPoolExecutor(max_workers=4) as pool:
        for error in pool.map(standalone, jobs):
            if error:
                print(error)
                sys.exit(1)
    print(f'C++: all {len(jobs)} standalone starter/solution snippets compile', flush=True)
    for offset in range(0, len(problems), 40):
        batch = problems[offset:offset + 40]
        # Include all standard headers outside namespaces, then place algorithms
        # in separate namespaces so unrelated solutions can reuse helper names.
        headers = sorted({line for p in batch for field in ('solutions', 'starters') for line in p[field]['cpp'].splitlines() if line.startswith('#include')})
        parts = ['#include "switch_runtime.hpp"', *headers]
        starters = parts.copy()
        for i, p in enumerate(batch):
            parts.append(f'namespace p{i} {{\n' + p['solutions']['cpp'] + '\n' + p['cpp']['adapter'] + '\n}')
            starters.append(f'namespace p{i} {{\n' + p['starters']['cpp'] + '\n' + p['cpp']['adapter'] + '\n}')
        starter_source = td / 'starters.cpp'
        starter_source.write_text('\n'.join(starters))
        checked = subprocess.run(['clang++', '-std=c++17', '-fsyntax-only', '-I', str(root / 'native/include'), str(starter_source)], capture_output=True, text=True, timeout=180)
        if checked.returncode:
            print(checked.stderr)
            sys.exit(1)
        parts.append('int main(){json cases;cin>>cases; int failed=0; for(const auto& c:cases){try{json actual;int id=c["id"];switch(id){')
        for i in range(len(batch)):
            parts.append(f'case {i}: actual=p{i}::switchSolve(c["input"]);break;')
        parts.append('}if(actual!=c["expected"]){cerr<<c["name"]<<": "<<actual<<" expected "<<c["expected"]<<endl;failed++;}}catch(const exception& e){cerr<<c["name"]<<": "<<e.what()<<endl;failed++;}}return failed?1:0;}')
        source = td / 'batch.cpp'
        binary = td / 'batch'
        source.write_text('\n'.join(parts))
        result = subprocess.run(['clang++', '-std=c++17', '-O0', '-I', str(root / 'native/include'), str(source), '-o', str(binary)], capture_output=True, text=True, timeout=180)
        if result.returncode:
            print(result.stderr)
            sys.exit(1)
        cases = [dict(id=i, name=p['id'], **test) for i, p in enumerate(batch) for test in p['tests']]
        result = subprocess.run([str(binary)], input=json.dumps(cases), capture_output=True, text=True, timeout=30)
        if result.returncode:
            print(result.stderr)
            sys.exit(1)
        print(f'C++: problems {offset + 1}–{offset + len(batch)} and their starter adapters passed', flush=True)
print(f'All {len(problems)} problems and {count} tests passed in Python and C++.')
