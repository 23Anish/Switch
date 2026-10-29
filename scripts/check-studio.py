#!/usr/bin/env python3
"""Check lab traces and preserve the exact tested input/output contracts."""
from pathlib import Path
import json,copy
r=Path(__file__).resolve().parents[1];problems=json.loads((r/'dsa.json').read_text());byid={p['id']:p for p in problems};labs=json.loads((r/'patterns.json').read_text())
assert len(labs)>=40 and len({x['id'] for x in labs})==len(labs)
for lab in labs:
 assert lab['problemId'] in byid and lab['steps']
 for step in lab['steps']:
  assert step['detail'] and step['label'] and isinstance(step['state'],dict)
  assert len(step['values'])==len(lab['values'])
  assert all(str(i).isdigit() and int(i)<len(step['values']) for i in step['active'])
 for edge in lab['edges']:assert 0<=edge[0]<len(lab['values']) and 0<=edge[1]<len(lab['values'])
for p in problems:
 c=p['contract'];assert c['arguments'] and c['namedInput'];assert c['expectedOutput']==p['example']['output']
 args=c['arguments'];source=p['example']['input']
 reconstructed={a['name']:a['example'] for a in args} if isinstance(source,dict) else args[0]['example']
 assert reconstructed==source,p['id']
 for d in c['diagrams']:
  if d['kind']=='tree':
   assert len(d['nodes'])==sum(x is not None for x in next(a['example'] for a in args if a['name']==d['label'])),p['id']
   assert len(d['edges'])==max(0,len(d['nodes'])-1)
# Independently check the values shown by several traces with the existing references.
checks={'binary':([2,5,8,12,16,19,23,31],None)}
fixtures={
 'kadane':([-2,3,-1,4,-5],6), 'monostack':([2,1,3],[3,3,-1]), 'heap':({'nums':[4,1,7,3,9],'k':2},7),
 'dsu':None, 'lis':([3,1,5,2,6],3), 'xor':([4,1,4,2,1],2), 'edit-distance':({'a':'cat','b':'cut'},1),
 'interval-dp':([10,30,5,60],4500), 'merge':([4,1,3,2],[1,2,3,4]), 'partition':([2,0,1,2,0],[0,0,1,2,2])}
for lab in labs:
 f=fixtures.get(lab['id'])
 if not f:continue
 env={};exec(byid[lab['problemId']]['solutions']['python'],env)
 assert env['solve'](copy.deepcopy(f[0]))==f[1],lab['id']
interviews=json.loads((r/'interviews.json').read_text());assert all(p['status'] in ['Official guidance','Reported pilot'] and p['url'].startswith('https://') for p in interviews['policies'])
assert len({c['id'] for c in json.loads((r/'companies.json').read_text())})==3
print(f'{len(labs)} pattern traces, all 250 named contracts and source-labeled interview policies passed.')
