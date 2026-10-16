#!/usr/bin/env python3
"""Validate curriculum and execute Python/C++ reference solutions. No third-party Python packages."""
from pathlib import Path
import json,sys,tempfile,subprocess,copy,signal
root=Path(__file__).resolve().parents[1]
files=[Path(x).resolve() for x in sys.argv[1:]] or [root/'dsa.json']
problems=[p for f in files for p in json.loads(f.read_text())]
assert len({p['id'] for p in problems})==len(problems),'Duplicate problem IDs'
assert len({p['title'].casefold() for p in problems})==len(problems),'Duplicate titles'
failures=[]; count=0
for p in problems:
    for field in ['id','title','topic','difficulty','statement','inputFormat','outputFormat','constraints','exampleExplanation','approaches','solutions','starters','tests']:
        assert p.get(field),f'{p["id"]}: missing {field}'
    assert p['difficulty'] in ['Easy','Medium','Hard']
    assert isinstance(p['constraints'],list)
    env={};exec(p['solutions']['python'],env)
    for test in p['tests']:
        try:
            actual=env['solve'](copy.deepcopy(test['input']))
            if actual!=test['expected']: failures.append((p['id'],'python',actual,test['expected']))
        except Exception as e: failures.append((p['id'],'python',str(e)))
        count+=1
print(f'Python: {count} tests, {len(failures)} failures',flush=True)
if failures: print(failures);sys.exit(1)
with tempfile.TemporaryDirectory(prefix='switch-check-') as td:
    td=Path(td)
    for offset in range(0,len(problems),40):
        batch=problems[offset:offset+40]
        parts=['#include "switch_runtime.hpp"']
        for i,p in enumerate(batch): parts.append(f'namespace p{i} {{\n'+p['solutions']['cpp']+'\n}')
        parts.append('int main(){json cases;cin>>cases; int failed=0; for(const auto& c:cases){try{json actual;int id=c["id"];switch(id){')
        for i in range(len(batch)):parts.append(f'case {i}: actual=p{i}::solve(c["input"]);break;')
        parts.append('}if(actual!=c["expected"]){cerr<<c["name"]<<": "<<actual<<" expected "<<c["expected"]<<endl;failed++;}}catch(const exception& e){cerr<<c["name"]<<": "<<e.what()<<endl;failed++;}}return failed?1:0;}')
        src=td/'batch.cpp';binary=td/'batch';src.write_text('\n'.join(parts))
        result=subprocess.run(['clang++','-std=c++17','-O0','-I',str(root/'native/include'),str(src),'-o',str(binary)],capture_output=True,text=True,timeout=180)
        if result.returncode: print(result.stderr);sys.exit(1)
        cases=[dict(id=i,name=p['id'],**test) for i,p in enumerate(batch) for test in p['tests']]
        result=subprocess.run([str(binary)],input=json.dumps(cases),capture_output=True,text=True,timeout=30)
        if result.returncode: print(result.stderr);sys.exit(1)
        print(f'C++: problems {offset+1}–{offset+len(batch)} passed',flush=True)
print(f'All {len(problems)} problems and {count} tests passed in Python and C++.')
