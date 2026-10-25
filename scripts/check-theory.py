#!/usr/bin/env python3
"""Check worked lesson code and expected output using isolated temporary files."""
from pathlib import Path
import json, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
examples=json.loads((root/'theory-examples.json').read_text())
lessons=json.loads((root/'lessons.json').read_text())+json.loads((root/'design-lessons.json').read_text())
ids={lesson['id'] for lesson in lessons}
with tempfile.TemporaryDirectory(prefix='switch-theory-') as folder:
    td=Path(folder)
    for index, example in enumerate(examples):
        assert example['lessonId'] in ids, example['lessonId']
        for key in ('title','concept','walkthrough','code','expectedOutput','tradeoffs','exercise','solution','diagram'):
            assert example.get(key), (example['lessonId'],key)
        if example['language']=='C++17':
            source=td/'example.cpp'; source.write_text(example['code'])
            result=subprocess.run(['clang++','-std=c++17',str(source),'-o',str(td/'example')],capture_output=True,text=True,timeout=60)
            assert result.returncode==0,result.stderr
            command=[str(td/'example')]
        else:
            assert example['language']=='Python 3'
            source=td/'example.py';source.write_text(example['code']);command=[sys.executable,'-I',str(source)]
        result=subprocess.run(command,cwd=td,capture_output=True,text=True,timeout=10)
        if result.returncode or result.stdout.strip()!=example['expectedOutput'].strip():
            print(example['lessonId'],example['title'],'\nACTUAL:',repr(result.stdout),'\nEXPECTED:',repr(example['expectedOutput']),result.stderr)
            sys.exit(1)
print(f'{len(examples)} worked theory examples compile/run and match expected output.')
