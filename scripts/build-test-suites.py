#!/usr/bin/env python3
"""Build small deterministic regression suites using brute-force oracles and known-shape fixtures.
No reference solution is imported by this generator. Existing sample cases remain intact.
"""
from pathlib import Path
import itertools as it, math, json, collections, functools, copy
ROOT=Path(__file__).resolve().parents[1]
CASES={}
def put(ids,inputs,oracle):
 for id in ([ids] if isinstance(ids,int) else ids):
  CASES[id]=(inputs,oracle)
def fixed(id,pairs):CASES[id]=[{'input':x,'expected':v,'name':f'Boundary {i+1}'} for i,(x,v) in enumerate(pairs)]
A=[[0],[7],[-7],[2,2],[3,1],[0,0,0],[-4,-1,-8],[1,2,3,4],[4,3,2,1],[0,-1,0,2,-3],[5]*7,[-2,3,-1,4,-5]]
POS=[[1],[9],[1,1],[1,2],[2,1],[1,1,1],[3,2,4,1],[2,5,1,3,4],[5,4,3,2,1],[1,3,2,4,2,5]]
BITS=[[0],[1],[0,0],[1,1],[0,1],[1,0],[1,0,1],[0,0,1,1,1],[1,1,0,1,1],[0]*7,[1]*8]
def ranges(a):return [a[i:j] for i in range(len(a)) for j in range(i+1,len(a)+1)]
def subsets(a):return [list(c) for k in range(len(a)+1) for c in it.combinations(a,k)]
put(1,A,max)
put(2,A,lambda a:sorted(set(a))[-2] if len(set(a))>1 else None)
put(3,A,lambda a:all(a[i]<=a[i+1] for i in range(len(a)-1)))
put(4,[sorted(a) for a in A],lambda a:sorted(set(a)))
put(5,[{'nums':a,'k':k} for a in A for k in [0,1,len(a),len(a)+2]],lambda d:d['nums'][-(d['k']%len(d['nums'])):]+d['nums'][:-(d['k']%len(d['nums']))] if d['k']%len(d['nums']) else d['nums'])
put(6,A,lambda a:[x for x in a if x]+[0]*a.count(0))
put(7,[list(reversed([i for i in range(n+1) if i!=m])) for n in range(1,6) for m in [0,n]],lambda a:sum(range(len(a)+1))-sum(a))
put(8,BITS,lambda a:max([len(s) for s in ranges(a) if all(s)]+[0]))
put(9,A,lambda a:max(map(sum,ranges(a))))
put(10,POS,lambda a:max([a[j]-a[i] for i in range(len(a)) for j in range(i+1,len(a))]+[0]))
def nextperm(a):
 p=sorted(set(it.permutations(a)));q=tuple(a);return list(p[(p.index(q)+1)%len(p)])
put(11,[a for a in A if len(a)<=5],nextperm)
put(12,A,lambda a:[math.prod(a[:i]+a[i+1:]) for i in range(len(a))])
put([181,182,183,60],A,sorted)
put(184,A,lambda a:sum(a[i]>a[j] for i in range(len(a)) for j in range(i+1,len(a))))
put(185,[[i%3 for i in range(n,-1,-1)] for n in range(1,12)],sorted)
put(186,A,lambda a:sum(a[i]>2*a[j] for i in range(len(a)) for j in range(i+1,len(a))))
put(188,A,lambda a:[x for i,x in enumerate(a) if all(x>y for y in a[i+1:])])
put(13,[{'nums':[i,2*i,4*i,8*i],'target':3*i} for i in range(-6,7) if i],lambda d:[0,1])
put(14,A,lambda a:len(a)!=len(set(a)))
WORDS=['','a','aa','ab','abc','aabb','abcabc','abbac','ABC','abababa']
put(15,[{'a':a,'b':b} for a,b in [('', ''),('a','b'),('ab','ba'),('aab','aba'),('aab','abb'),('Ab','ab'),('zzz','zzz'),('abcd','dcba'),('a','aa'),('abc','abb')]],lambda d:collections.Counter(d['a'])==collections.Counter(d['b']))
put(20,[[i,i,i,i+1,i+2] for i in range(-5,7)],lambda a:collections.Counter(a).most_common(1)[0][0])
def iso(d):
 a,b=d['a'],d['b'];return len(a)==len(b) and len(set(zip(a,b)))==len(set(a))==len(set(b))
put(22,[{'a':a,'b':b} for a,b in [('',''),('a','z'),('ab','aa'),('aa','ab'),('foo','app'),('paper','title'),('aba','baa'),('abc','def'),('abca','zbcz'),('aabb','ccdd')]],iso)
put(24,[{'nums':a,'queries':[[0,len(a)-1],[0,0],[len(a)-1,len(a)-1]]} for a in A]+[{'nums':[2147483647,2147483647],'queries':[[0,1]]}],lambda d:[sum(d['nums'][l:r+1]) for l,r in d['queries']])
def groups(a):
 g={}
 for s in a:g.setdefault(''.join(sorted(s)),[]).append(s)
 return list(g.values())
put(16,[['a'*i,'b','a'*i,'ab','ba',''] for i in range(1,11)],groups)
put(17,A,lambda a:max([next((k for k in range(1,len(a)+2) if x+k not in set(a)),1) for x in set(a)]+[0]))
put(18,[{'nums':a,'k':k} for a in A for k in [0,2,-1]],lambda d:sum(sum(s)==d['k'] for s in ranges(d['nums'])))
put(19,A,lambda a:max([len(s) for s in ranges(a) if sum(s)==0]+[0]))
put(21,[{'nums':[i]*4+[i+1]*3+[i+2]*2+[i+3],'k':k} for i in range(-3,5) for k in [1,2,3]],lambda d:sorted(collections.Counter(d['nums']),key=lambda x:(-d['nums'].count(x),x))[:d['k']])
put(23,[{'nums':a,'k':k} for a in A for k in [2,3,5]],lambda d:sum(sum(s)%d['k']==0 for s in ranges(d['nums'])))
put(193,[{'nums':a,'goal':k} for a in BITS for k in [0,1,2]],lambda d:sum(sum(s)==d['goal'] for s in ranges(d['nums'])))
put(214,[{'nums':[abs(x) for x in a],'k':k} for a in A for k in [0,1,2]],lambda d:sum(functools.reduce(int.__xor__,s,0)==d['k'] for s in ranges(d['nums'])))
put(25,[{'nums':[i,2*i,4*i,8*i],'target':3*i} for i in range(1,13)],lambda d:[0,1])
put(29,['','a','A!a','.,','0P','racecar','ab','abBA','No lemon, no melon','12,21','a b c'],lambda s:(lambda a:a==a[::-1])(''.join(x.lower() for x in s if x.isalnum())))
put(190,[{'nums':a,'k':k} for a in A for k in range(1,len(a)+1)],lambda d:max(sum(d['nums'][i:i+d['k']]) for i in range(len(d['nums'])-d['k']+1)))
put(26,A,lambda a:sorted(map(list,{tuple(sorted(c)) for c in it.combinations(a,3) if sum(c)==0})))
put(187,[{'nums':a,'target':k} for a in A for k in [0,4]],lambda d:sorted(map(list,{tuple(sorted(c)) for c in it.combinations(d['nums'],4) if sum(c)==d['target']})))
put(27,POS,lambda a:max([(j-i)*min(a[i],a[j]) for i in range(len(a)) for j in range(i+1,len(a))]+[0]))
put(28,POS,lambda a:sum(max(0,min(max(a[:i+1]),max(a[i:]))-x) for i,x in enumerate(a)))
put(30,WORDS,lambda a:max([len(s) for s in ranges(a) if len(set(s))==len(s)]+[0]))
put(31,[{'nums':a,'k':k} for a in BITS for k in [0,1,2]],lambda d:max([len(s) for s in ranges(d['nums']) if s.count(0)<=d['k']]+[0]))
put(32,[{'nums':a,'target':k} for a in POS for k in [1,4,20]],lambda d:min([len(s) for s in ranges(d['nums']) if sum(s)>=d['target']]+[10**9]) if any(sum(s)>=d['target'] for s in ranges(d['nums'])) else 0)
put(33,[{'s':s.upper(),'k':k} for s in WORDS for k in [0,1,2]],lambda d:max([len(s) for s in ranges(d['s']) if len(s)-max(collections.Counter(s).values())<=d['k']]+[0]))
put(34,[{'s':s,'p':p} for s in WORDS for p in ['a','ab','aa']],lambda d:[i for i in range(len(d['s'])-len(d['p'])+1) if sorted(d['s'][i:i+len(d['p'])])==sorted(d['p'])])
put(189,[{'nums':a,'k':k} for a in POS for k in [1,4,15]],lambda d:max([len(s) for s in ranges(d['nums']) if sum(s)==d['k']]+[0]))
put(191,[{'nums':a,'k':k} for a in POS for k in [1,2,10]],lambda d:sum(math.prod(s)<d['k'] for s in ranges(d['nums'])))
put(192,[[abs(x)%3 for x in a] for a in A],lambda a:max([len(s) for s in ranges(a) if len(set(s))<=2]+[0]))
put(194,[{'text':s,'pattern':p} for s in WORDS for p in ['a','ab','aa']],lambda d:any(sorted(d['text'][i:i+len(d['pattern'])])==sorted(d['pattern']) for i in range(len(d['text'])-len(d['pattern'])+1)))
def minwindow(d):
 need=collections.Counter(d['t']);found=[(j-i,i,d['s'][i:j]) for i in range(len(d['s'])+1) for j in range(i+1,len(d['s'])+1) if not need-collections.Counter(d['s'][i:j])];return min(found)[2] if found else ''
put(35,[{'s':s,'t':t} for s in WORDS[1:] for t in ['a','ab','aa']],minwindow)
put(36,[{'nums':a,'k':k} for a in POS for k in [1,2,3]],lambda d:sum(len(set(s))==d['k'] for s in ranges(d['nums'])))
put(37,[{'nums':sorted(set(a)),'target':t} for a in A for t in [-10,0,2,10]],lambda d:d['nums'].index(d['target']) if d['target'] in d['nums'] else -1)
put(38,[{'nums':sorted(a),'target':t} for a in A for t in [-10,0,2,10]],lambda d:sum(x<d['target'] for x in d['nums']))
put(42,[0,1,2,3,4,15,16,17,999,10000,2147395600,2147483647],math.isqrt)
put(47,[{'nums':a,'k':k} for a in [[1],[2],[1,2,3],[2,4,6],[5,6,10]] for k in [1,2,5]],lambda d:[i for i in range(1,max(d['nums'])+d['k']+2) if i not in d['nums']][d['k']-1])
put(39,[{'nums':sorted(a),'target':t} for a in A for t in [-1,0,2,7]],lambda d:[d['nums'].index(d['target']),len(d['nums'])-1-d['nums'][::-1].index(d['target'])] if d['target'] in d['nums'] else [-1,-1])
ROT=[list(range(n))[r:]+list(range(n))[:r] for n in range(1,7) for r in range(n)]
put(40,[{'nums':a,'target':t} for a in ROT for t in [0,3,8]],lambda d:d['nums'].index(d['target']) if d['target'] in d['nums'] else -1)
put(41,ROT,min)
put(43,[[i for i in range(1,n+1)] for n in range(1,13)],lambda a:len(a)-1)
put(44,[{'matrix':[[i*2+j*2*n for i in range(n)] for j in range(2)],'target':t} for n in range(1,7) for t in [0,3,8]],lambda d:any(d['target'] in row for row in d['matrix']))
put(45,[{'piles':a,'h':len(a)+k} for a in POS for k in [0,1,5]],lambda d:next(speed for speed in range(1,max(d['piles'])+1) if sum(math.ceil(x/speed) for x in d['piles'])<=d['h']))
def ship(d):
 def days(cap):
  used=1;current=0
  for w in d['weights']:
   if current+w>cap:used+=1;current=0
   current+=w
  return used
 return next(c for c in range(max(d['weights']),sum(d['weights'])+1) if days(c)<=d['days'])
put(46,[{'weights':a,'days':k} for a in POS for k in [1,len(a)]],ship)
put(195,[{'nums':a+[a[-1]],'target':t} for a in ROT for t in [0,3,8]],lambda d:d['target'] in d['nums'])
put(196,[sorted([v for i in range(n) for v in ([i] if i==n//2 else [i,i])]) for n in range(1,12)],lambda a:next(x for x in a if a.count(x)==1))
put(198,[{'stalls':list(range(0,n*3,3)),'cows':c} for n in range(2,8) for c in [2,n]],lambda d:max(min(b-a for a,b in zip(c,c[1:])) for c in it.combinations(sorted(d['stalls']),d['cows'])))
def books(d):
 a=d['pages'];m=d['students']
 if m>len(a):return -1
 return min(max(sum(a[l:r]) for l,r in zip((0,)+cuts,cuts+(len(a),))) for cuts in it.combinations(range(1,len(a)),m-1))
put(199,[{'pages':a,'students':m} for a in POS for m in [1,len(a),len(a)+1]],books)
put(48,[{'a':sorted(a),'b':sorted(b)} for a,b in zip(A,POS)],lambda d:(lambda a:(a[(len(a)-1)//2]+a[len(a)//2])/2)(sorted(d['a']+d['b'])))
put(197,[{'a':sorted(a),'b':sorted(b),'k':k} for a,b in zip(A,POS) for k in [1,len(a)+len(b)]],lambda d:sorted(d['a']+d['b'])[d['k']-1])
put(200,[[sorted([i,i+2,i+5]),sorted([i-2,i+1,i+4]),sorted([i,i+3,i+7])] for i in range(-5,7)],lambda a:sorted(sum(a,[]))[len(sum(a,[]))//2])
# Lists use direct sequence identities; node construction is separately checked by the runner.
put(49,A,lambda a:a[::-1]);put(50,A,lambda a:a[len(a)//2])
put(51,[{'a':sorted(a),'b':sorted(b)} for a,b in zip(A,POS)],lambda d:sorted(d['a']+d['b']))
put(53,[{'values':a,'pos':pos} for a in A for pos in [-1,0,len(a)-1]],lambda d:d['pos']>=0)
put(54,[{'values':a,'pos':pos} for a in A for pos in [-1,0,len(a)-1]],lambda d:d['pos'])
put(55,A,lambda a:a==a[::-1])
put(52,[{'values':a,'n':n} for a in A for n in [1,len(a)]],lambda d:d['values'][:len(d['values'])-d['n']]+d['values'][len(d['values'])-d['n']+1:])
def digitsum(d):
 n=sum(x*10**i for i,x in enumerate(d['a']))+sum(x*10**i for i,x in enumerate(d['b']));return list(map(int,str(n)[::-1]))
put(56,[{'a':[9]*n,'b':[1]} for n in range(1,10)]+[{'a':[0],'b':[0]}],digitsum)
put(57,A,lambda a:a[::2]+a[1::2]);put(58,A,lambda a:sum([a[i:i+2][::-1] for i in range(0,len(a),2)],[]))
put(201,[{'values':a,'k':k} for a in A for k in [0,1,len(a)+2]],lambda d:d['values'][-(d['k']%len(d['values'])):]+d['values'][:-(d['k']%len(d['values']))] if d['k']%len(d['values']) else d['values'])
put(202,[sorted(a) for a in A],lambda a:[x for x in a if a.count(x)==1])
put(203,[{'values':a,'x':x} for a in A for x in [0,2,9]],lambda d:[x for x in d['values'] if x<d['x']]+[x for x in d['values'] if x>=d['x']])
put(204,[{'values':a,'left':1,'right':len(a)} for a in A]+[{'values':a,'left':len(a),'right':len(a)} for a in A],lambda d:d['values'][:d['left']-1]+d['values'][d['left']-1:d['right']][::-1]+d['values'][d['right']:])
put(205,[{'prefixA':[i],'prefixB':[i+1,i+2],'shared':[i+3,i+4]} for i in range(-4,5)]+[{'prefixA':[i],'prefixB':[i],'shared':[]} for i in range(4)],lambda d:d['shared'][0] if d['shared'] else None)
put(59,[{'values':a,'k':k} for a in A for k in [1,2,3]],lambda d:sum([d['values'][i:i+d['k']][::-1] if i+d['k']<=len(d['values']) else d['values'][i:] for i in range(0,len(d['values']),d['k'])],[]))
def reduce_brackets(s):
 while any(x in s for x in ['()','[]','{}']):s=s.replace('()','').replace('[]','').replace('{}','')
 return s==''

put(61,['','()','[]','{}','([{}])','([)]','(','())','((()))','{}[]()','}{'],reduce_brackets)
def operation_oracle(ops,queue=False):
 a=[];out=[]
 for op in ops:
  if op[0]=='push':a.append(op[1]);out.append(None)
  elif op[0]=='pop':out.append(a.pop(0 if queue else -1))
  elif op[0]=='peek':out.append(a[0] if a else None)
  elif op[0]=='top':out.append(a[-1] if a else None)
  elif op[0]=='min':out.append(min(a) if a else None)
 return out
put(63,[[['push',i],['push',-i],['peek'],['pop'],['peek'],['pop']] for i in range(-5,7)],lambda o:operation_oracle(o,True))
put(62,[[['push',i],['push',i-1],['min'],['top'],['pop'],['min']] for i in range(-5,7)],operation_oracle)
put(64,A,lambda a:[next((y for y in a[i+1:] if y>x),-1) for i,x in enumerate(a)])
put(65,[[abs(x)+50 for x in a] for a in A],lambda a:[next((j-i for j in range(i+1,len(a)) if a[j]>x),0) for i,x in enumerate(a)])
put(68,[[str(i),'2','/'] for i in range(-10,11)]+[['2','3','+','4','*']],lambda a:math.trunc(int(a[0])/2) if len(a)==3 else 20)
put(69,['/','/a','/a/','/a//b','/../','/a/../b','/a/./b/..','/a/.../b','//a///b/','/a/b/../../..'],lambda p:'/'+('/'.join(normalpath(p))))
def normalpath(p):
 a=[]
 for s in p.split('/'):
  if s=='..':
   if a:a.pop()
  elif s and s!='.':a.append(s)
 return a
put(70,[str(i)+'[ab]' for i in range(1,11)]+['2[a3[b]]','abc','2[xy]z'],lambda s:('ab'*int(s.split('[')[0])) if s.endswith('[ab]') else {'2[a3[b]]':'abbbabbb','abc':'abc','2[xy]z':'xyxyz'}[s])
def collide(a):
 while True:
  index=next((i for i in range(len(a)-1) if a[i]>0>a[i+1]),None)
  if index is None:return a
  x,y=a[index:index+2];a[index:index+2]=[x] if x>-y else [y] if x<-y else []
put(71,[[i,-i] for i in range(1,7)]+[[-2,-1,1,2],[8,2,-5],[-5,3,-2],[1,-2,-3,4]],collide)
put(72,POS,lambda a:[next((i-j for j in range(i-1,-1,-1) if a[j]>a[i]),i+1) for i in range(len(a))])
put(66,POS+[[0],[0,0],[2,0,2]],lambda a:max([min(a[i:j])*(j-i) for i in range(len(a)) for j in range(i+1,len(a)+1)]+[0]))
put(67,[{'nums':a,'k':k} for a in A for k in [1,len(a)]],lambda d:[max(d['nums'][i:i+d['k']]) for i in range(len(d['nums'])-d['k']+1)])
# Small exhaustive enumerations, preserving the documented output ordering.
put(145,[list(range(n)) for n in range(0,8)],lambda a:[[a[i] for i,b in enumerate(bits) if b] for bits in it.product([0,1],repeat=len(a))])
put(146,[[0]*n+[1] for n in range(0,8)],lambda a:sorted({tuple(s) for s in subsets(a)}))
# JSON serializes tuple rows as arrays.
put(147,[list(range(n)) for n in range(0,7)],lambda a:list(map(list,it.permutations(a))))
put(148,[[0]*n+[1] for n in range(0,7)],lambda a:list(map(list,sorted(set(it.permutations(a))))))
def combos(d,reuse):
 c=sorted(set(d['candidates'])) if reuse else sorted(d['candidates']);target=d['target'];out=set()
 for n in range(target//min(c)+1 if reuse and c else len(c)+1):
  for a in (it.combinations_with_replacement(c,n) if reuse else it.combinations(c,n)):
   if sum(a)==target:out.add(a)
 return list(map(list,sorted(out)))
put(149,[{'candidates':[2,3,5],'target':n} for n in range(0,12)],lambda d:combos(d,True))
put(150,[{'candidates':[1,1,2,3,5],'target':n} for n in range(0,12)],lambda d:combos(d,False))
def parentheses(n):
 out=[]
 for t in it.product('()',repeat=n*2):
  s=''.join(t);balance=0;ok=True
  for c in s:
   balance+=1 if c=='(' else -1
   if balance<0:ok=False;break
  if ok and balance==0:out.append(s)
 return out
put(151,list(range(0,8)),parentheses)
KEYS={'2':'abc','3':'def','4':'ghi','5':'jkl','6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}
put(152,['','2','3','4','5','6','7','8','9','22','79'],lambda s:[''.join(c) for c in it.product(*(KEYS[x] for x in s))] if s else [])
def palparts(s):
 if not s:return [[]]
 out=[]
 for cuts in it.product([False,True],repeat=len(s)-1):
  parts=[];last=0
  for i,c in enumerate(cuts):
   if c:parts.append(s[last:i+1]);last=i+1
  parts.append(s[last:])
  if all(p==p[::-1] for p in parts):out.append(parts)
 return sorted(out)
put(153,['a','aa','ab','aba','abb','abc','abba','aaaa','aaba','abca'],palparts)
put(155,[{'board':[['A','B'],['C','D']],'word':w} for w in ['A','B','AB','AC','ABD','ACD','ABDC','ABCA','AD','AAAA','DCBA']],lambda d:d['word'] in ['A','B','AB','AC','ABD','ACD','ABDC'])
put(242,[{'n':n,'k':k} for n in range(1,7) for k in [0,1,n]],lambda d:list(map(list,it.combinations(range(1,d['n']+1),d['k']))))
put(243,[{'k':k,'target':n} for k in [1,2,3] for n in [1,3,6,10,20]],lambda d:[list(c) for c in it.combinations(range(1,10),d['k']) if sum(c)==d['target']])
def ipv4(s):
 out=[]
 for a,b,c in it.combinations(range(1,len(s)),3):
  parts=[s[:a],s[a:b],s[b:c],s[c:]]
  if all(1<=len(p)<=3 and int(p)<=255 and (len(p)==1 or p[0]!='0') for p in parts):out.append('.'.join(parts))
 return out
put(244,['0000','1111','101023','010010','111111','123123','99999999','255255255255','1234','00000'],ipv4)
def josephus(d):
 a=list(range(d['n']));i=0
 while len(a)>1:i=(i+d['k']-1)%len(a);a.pop(i)
 return a[0]
put(246,[{'n':n,'k':k} for n in range(1,8) for k in [1,2,4]],josephus)
put(154,list(range(1,9)),lambda n:sum(len({i+p[i] for i in range(n)})==n and len({i-p[i] for i in range(n)})==n for p in it.permutations(range(n))))
put(156,[{'n':n,'k':k} for n in range(1,6) for k in [1,math.factorial(n)]],lambda d:''.join(map(str,list(it.permutations(range(1,d['n']+1)))[d['k']-1])))
# Complete small trees have independently known position/level identities.
TREES=[list(range(1,n+1)) for n in range(1,11)]
def tree_nodes(a):
 if not a:return None
 root={'v':a[0],'l':None,'r':None};q=[root];k=1
 for node in q:
  for side in ['l','r']:
   if k<len(a) and a[k] is not None:node[side]={'v':a[k],'l':None,'r':None};q.append(node[side])
   k+=1
 return root
# Oracles enumerate root-to-node coordinates instead of using solution adapters.
def tree_records(a):
 root=tree_nodes(a);out=[]
 def visit(n,path):
  if n is None:return
  out.append((path,n['v']));visit(n['l'],path+'0');visit(n['r'],path+'1')
 visit(root,'');return out
put(73,TREES,lambda a:[v for p,v in sorted(tree_records(a),key=lambda item:item[0]+'1')])
put(74,TREES,lambda a:[v for p,v in sorted(tree_records(a))])
put(75,TREES,lambda a:[v for p,v in sorted(tree_records(a),key=lambda item:item[0]+'2')])
put([76,206],TREES,lambda a:[[v for p,v in sorted(tree_records(a)) if len(p)==d] for d in range(len(a).bit_length())])
# Zigzag reverses alternate breadth levels.
put(206,TREES,lambda a:[row[::-1] if d%2 else row for d,row in enumerate([[v for p,v in sorted(tree_records(a)) if len(p)==depth] for depth in range(len(a).bit_length())])])
put(77,TREES,lambda a:len(a).bit_length())
put(78,TREES,lambda a:True)
put(79,TREES,lambda a:max([len(p)+len(q)-2*len(next((p[:i] for i in range(min(len(p),len(q)),-1,-1) if p[:i]==q[:i]),'')) for p,_ in tree_records(a) for q,_ in tree_records(a)]+[0]))
put(80,[[i,i+1,i+1] for i in range(1,9)]+[[1,2,3],[1,2,None]],lambda a:len(a)==3 and a[1]==a[2])
put(82,[{'tree':[1,2,3],'target':n} for n in range(0,12)],lambda d:d['target'] in [3,4])
put(81,TREES,lambda a:[max(v for p,v in tree_records(a) if len(p)==d) for d in range(len(a).bit_length())])
put(83,[{'tree':a,'p':a[-1],'q':1} for a in TREES],lambda d:1)
def boundary(a):
 records=dict(tree_records(a));left=[];right=[];p=''
 while p in records:
  if p:left.append(p)
  p+= '0' if p+'0' in records else '1'
 p=''
 while p in records:
  if p:right.append(p)
  p+='1' if p+'1' in records else '0'
 leaves=[p for p in sorted(records) if p+'0' not in records and p+'1' not in records]
 paths=['']+[p for p in left if p not in leaves]+leaves+[p for p in right[::-1] if p not in leaves]
 return [records[p] for i,p in enumerate(paths) if p not in paths[:i]]
put(207,TREES,boundary)
put(209,[{'preorder':list(range(1,n+1)),'inorder':list(range(1,n+1))} for n in range(1,10)],lambda d:sum([[x,None] for x in d['preorder'][:-1]],[])+d['preorder'][-1:])
put(210,TREES,lambda a:max([max([int('1'+p,2) for p,_ in tree_records(a) if len(p)==d])-min([int('1'+p,2) for p,_ in tree_records(a) if len(p)==d])+1 for d in range(len(a).bit_length())]))
put(211,TREES,len)
def serialize(a):
 r=tree_records(a);m=dict(r)
 def walk(p):return '#' if p not in m else str(m[p])+','+walk(p+'0')+','+walk(p+'1')
 return walk('')
put(212,TREES,serialize)
put(213,[{'tree':a,'target':1,'k':k} for a in TREES for k in [0,1,2]],lambda d:sorted(v for p,v in tree_records(d['tree']) if len(p)==d['k']))
def maxpath(a):
 records=tree_records(a);m=dict(records);best=-10**9
 for p,v in records:
  for q,w in records:
   common=next(p[:i] for i in range(min(len(p),len(q)),-1,-1) if p[:i]==q[:i]);paths={p[:i] for i in range(len(common),len(p)+1)}|{q[:i] for i in range(len(common),len(q)+1)};best=max(best,sum(m[z] for z in paths))
 return best
put(84,TREES+[[-1],[-2,-3,-4]],maxpath)
put(208,TREES,lambda a:[[v for p,v in sorted(tree_records(a),key=lambda z:(len(z[0]),z[1])) if p.count('1')-p.count('0')==x] for x in sorted({p.count('1')-p.count('0') for p,v in tree_records(a)})])
BSTS=[[i,i-1,i+1] for i in range(-4,8)]
put(87,[{'tree':a,'target':t} for a in BSTS for t in [a[0],a[0]+2]],lambda d:d['target'] in d['tree'])
put(85,BSTS+[[2,3,1],[2,2,3]],lambda a:a[1]<a[0]<a[2])
put(86,[{'tree':a,'k':k} for a in BSTS for k in [1,2,3]],lambda d:sorted(d['tree'])[d['k']-1])
put(88,[{'tree':a,'target':t} for a in BSTS for t in [a[0],a[0]-2,a[0]+2]],lambda d:[max([x for x in d['tree'] if x<=d['target']],default=None),min([x for x in d['tree'] if x>=d['target']],default=None)])
put(89,[{'tree':a,'p':a[1],'q':a[2]} for a in BSTS],lambda d:d['tree'][0])
put(90,[{'nums':a,'k':k} for a in A for k in [1,len(a)]],lambda d:sorted(d['nums'],reverse=True)[d['k']-1])
put(91,[[sorted(a),[],sorted(b)] for a,b in zip(A,POS)],lambda a:sorted(sum(a,[])))
put(92,A,lambda a:[(lambda s:(s[(len(s)-1)//2]+s[len(s)//2])/2)(sorted(a[:i])) for i in range(1,len(a)+1)])
def stones(a):
 while len(a)>1:
  a.sort();y=a.pop();x=a.pop()
  if y!=x:a.append(y-x)
 return a[0] if a else 0
put(93,POS,stones)
@functools.lru_cache(None)
def ropes(a):
 if len(a)<=1:return 0
 return min(a[i]+a[j]+ropes(tuple(sorted([v for k,v in enumerate(a) if k not in [i,j]]+[a[i]+a[j]]))) for i in range(len(a)) for j in range(i+1,len(a)))
put(94,POS,lambda a:ropes(tuple(sorted(a))))
put(95,[{'points':[[i,0],[-i,1],[0,0],[i,2]],'k':k} for i in range(1,7) for k in [1,2]],lambda d:sorted(d['points'],key=lambda p:(sum(x*x for x in p),p[0],p[1]))[:d['k']])
put(96,[[[i,i+4],[i+1,i+5],[i+2,i+6]] for i in range(-4,8)],lambda a:(lambda pairs:list(min(pairs,key=lambda p:(p[1]-p[0],p[0]))))([(min(c),max(c)) for c in it.product(*a)]))
# Graph fixtures include paths, isolated vertices, zero/negative weights where valid,
# and hand-sized grids; answers are derived from shapes or exhaustive simple paths.
CHAINS=[{'n':n,'edges':[[i,i+1] for i in range(n-1)],'start':0} for n in range(1,11)]
put([97,98],CHAINS,lambda d:list(range(d['n'])))
put(99,[{'n':n,'edges':[[i,i+1] for i in range(n-2)]} for n in range(2,12)],lambda d:2)
put(101,[{'image':[[1]*n,[1]*n],'sr':0,'sc':0,'color':c} for n in range(1,7) for c in [1,2]],lambda d:[[d['color']]*len(d['image'][0]) for _ in d['image']])
GRIDS=[[[1]*n for _ in range(n)] for n in range(1,5)]+[[[(r+c)%2 for c in range(n)] for r in range(n)] for n in range(2,6)]
put(100,GRIDS,lambda a:1 if all(all(row) for row in a) else sum(sum(row) for row in a))
put(224,GRIDS,lambda a:2*(len(a)+len(a[0])) if all(all(row) for row in a) else 4*sum(sum(row) for row in a))
put(102,[[[2]+[1]*n] for n in range(0,10)]+[[[2,0]+[1]*n] for n in range(1,4)],lambda a:len(a[0])-1 if 0 not in a[0] else -1)
put(103,[{'n':n,'edges':[[i,i+1] for i in range(n-1)]+([[n-1,0]] if n>2 else [])} for n in range(2,12)],lambda d:d['n']==2 or d['n']%2==0)
put(104,[{'n':n,'edges':[[i,i+1] for i in range(n-1)]} for n in range(1,7)]+[{'n':n,'edges':[[i,i+1] for i in range(n-1)]+[[n-1,0]]} for n in range(3,9)],lambda d:len(d['edges'])==d['n'])
COURSES=[{'n':n,'prerequisites':[[i,i-1] for i in range(1,n)]} for n in range(1,8)]+[{'n':n,'prerequisites':[[0,1],[1,0]]} for n in range(2,6)]
put(105,COURSES,lambda d:[0,1] not in d['prerequisites'])
put(106,COURSES,lambda d:list(range(d['n'])) if [0,1] not in d['prerequisites'] else [])
put(107,[[['X']*n]+[['X']+['O']*(n-2)+['X'] for _ in range(n-2)]+[['X']*n] for n in range(3,9)]+[[['O']*n] for n in range(1,5)],lambda a:[['X']*len(a[0]) for _ in a] if len(a)>1 else a)
put(216,[{'n':n,'edges':[[i,i+1] for i in range(n-1)]} for n in range(1,8)]+[{'n':n,'edges':[[0,1],[1,0]]} for n in range(2,7)],lambda d:list(range(2,d['n'])) if [1,0] in d['edges'] else list(range(d['n'])))
put(217,[[[0]*n]+[[0]+[1]*(n-2)+[0] for _ in range(n-2)]+[[0]*n] for n in range(3,10)]+[[[0,0],[0,0]],[[1]]],lambda a:sum(sum(row) for row in a) if len(a)>2 else 0)
put(218,[[[0]+[1]*n] for n in range(0,10)],lambda a:[list(range(len(a[0])))])
put(220,[{'n':n,'edges':[[i,i+1] for i in range(n-1)]} for n in range(1,7)]+[{'n':n,'edges':[[i,i+1] for i in range(n-1)]+[[n-1,0]]} for n in range(2,8)],lambda d:len(d['edges'])==d['n'])
put(223,[[[int(i==j) for i in range(n)] for j in range(n)] for n in range(1,7)]+[[[1]*n for _ in range(n)] for n in range(2,6)],lambda a:len(a) if sum(a[0])==1 else 1)
put(108,[{'begin':'a'*n,'end':'b'+'a'*(n-1),'words':['b'+'a'*(n-1)]} for n in range(1,10)]+[{'begin':'aa','end':'bb','words':['bb']}],lambda d:2 if len(d['words'][0])==sum(a==b for a,b in zip(d['begin'],d['end']))+1 else 0)
put(219,[[[1]+[0]*(n-2)+[1]]+[[0]*n for _ in range(n-1)] for n in range(3,13)],lambda a:len(a)-2)
put(109,CHAINS,lambda d:list(range(d['n'])))
def paths(d,undirected=False):
 n=d['n'];adj=[[] for _ in range(n)]
 for a,b,w in d['edges']:
  adj[a].append((b,w))
  if undirected:adj[b].append((a,w))
 dist=[None]*n
 def walk(u,cost,seen):
  dist[u]=min(dist[u],cost) if dist[u] is not None else cost
  for v,w in adj[u]:
   if v not in seen:walk(v,cost+w,seen|{v})
 walk(d.get('start',0),0,{d.get('start',0)})
 return [-1 if v is None else v for v in dist]
WEIGHTED=[{'n':n,'edges':[[i,i+1,(i%3)+1] for i in range(n-1)],'start':0} for n in range(1,10)]+[{'n':4,'edges':[[0,1,9],[0,2,2],[2,1,1]],'start':0}]
put(110,WEIGHTED,lambda d:[None if x==-1 else x for x in paths(d)])
NEGATIVE=[{'n':n,'edges':[[i,i+1,(-1)**i*(i%3+1)] for i in range(n-1)],'start':0} for n in range(1,11)]
put([111,221],NEGATIVE,paths)
put(112,[{'n':n,'edges':[[i,i+1,2] for i in range(n-1)]} for n in range(1,10)],lambda d:[[2*(j-i) if j>=i else None for j in range(d['n'])] for i in range(d['n'])])
put(113,[{'n':n,'times':[[i,i+1,2] for i in range(1,n)],'k':k} for n in range(1,8) for k in [1,n]],lambda d:2*(d['n']-1) if d['k']==1 else 0 if d['n']==1 else -1)
put(114,[{'n':n,'flights':[[i,i+1,10] for i in range(n-1)],'src':0,'dst':n-1,'k':k} for n in range(2,8) for k in [0,n-1]],lambda d:10*(d['n']-1) if d['k']>=d['n']-2 else -1)
put(115,[[list(range(n))] for n in range(1,11)],lambda a:0 if len(a[0])==1 else 1)
put(116,[{'n':n,'operations':[['connected',0,n-1],['union',0,n-1],['connected',0,n-1]]} for n in range(1,11)],lambda d:[d['n']==1,None,True])
put(117,[{'n':n,'edges':[[i,i+1,i+1] for i in range(n-1)]} for n in range(1,10)]+[{'n':4,'edges':[[0,1,1],[1,2,2],[2,3,3],[0,3,20]]}],lambda d:sum(sorted(e[2] for e in d['edges'])[:d['n']-1]))
put(118,[{'n':n,'edges':[[i,i+1] for i in range(n-1)]+[[0,n-1]]} for n in range(3,13)],lambda d:[0,d['n']-1])
put(119,[{'n':n,'edges':[[i,i+1] for i in range(n-1)]} for n in range(1,7)]+[{'n':n,'edges':[]} for n in range(2,7)],lambda d:0 if len(d['edges'])==d['n']-1 else -1)
put(120,[[[0]*n for _ in range(n)] for n in range(1,8)]+[[[1]],[[0,1],[1,1]]],lambda a:len(a) if all(not any(row) for row in a) else -1)
put(222,[{'multipliers':[2],'start':1,'end':2**i} for i in range(0,10)],lambda d:int(math.log2(d['end'])))
put(225,[[[1]*n for _ in range(n)] for n in range(1,7)]+[[[0]*n for _ in range(n)] for n in range(1,6)],lambda a:len(a)**2 if a[0][0] else 1)
# Greedy answers checked by subset enumeration or direct interval overlap counts.
put(164,[{'greed':list(range(1,n+1)),'cookies':[1]*n} for n in range(1,10)]+[{'greed':[5],'cookies':[]}],lambda d:1 if d['cookies'] else 0)
put(231,POS,lambda a:sum(max(0,b-a) for a,b in zip(a,a[1:])))
INTERVALS=[[[i,i+1] for i in range(n)] for n in range(1,7)]+[[[0,n],[1,n+1]] for n in range(2,7)]
put(248,INTERVALS,lambda a:max(len(c) for c in subsets(a) if all(x[1]<=y[0] for x,y in zip(sorted(c),sorted(c)[1:]))))
def merge_intervals(a):
 out=[]
 for l,r in sorted(a):
  if out and l<=out[-1][1]:out[-1][1]=max(out[-1][1],r)
  else:out.append([l,r])
 return out
put(157,INTERVALS,merge_intervals)
put(158,[{'intervals':[[0,1],[4,5]],'newInterval':[i,i+2]} for i in range(-4,9)],lambda d:merge_intervals(d['intervals']+[d['newInterval']]))
put(159,INTERVALS,lambda a:len(a)-max(len(c) for c in subsets(a) if all(x[1]<=y[0] for x,y in zip(sorted(c),sorted(c)[1:]))))
put(160,INTERVALS,lambda a:max(sum(l<=t<r for l,r in a) for t in sorted({t for row in a for t in row})))
def reach(a):
 levels={0:0}
 for i in range(len(a)):
  if i in levels:
   for j in range(i+1,min(len(a),i+a[i]+1)):levels[j]=min(levels.get(j,10**9),levels[i]+1)
 return levels.get(len(a)-1,-1)
put(161,POS+[[0,1],[1,0,1],[2,0,0,1]],lambda a:reach(a)>=0)
put(162,POS+[[0,1],[1,0,1],[2,0,0,1]],reach)
def station(d):
 n=len(d['gas'])
 for start in range(n):
  fuel=0;ok=True
  for k in range(n):
   i=(start+k)%n;fuel+=d['gas'][i]-d['cost'][i]
   if fuel<0:ok=False;break
  if ok:return start
 return -1
put(163,[{'gas':[0]*i+[i+1],'cost':[1]*(i+1)} for i in range(0,10)],station)
put(165,['a'*n+'b'*n+'c'*n for n in range(1,11)],lambda s:[s.count('a'),s.count('b'),s.count('c')])
put(167,[{'tasks':['A']*i+['B'],'n':c} for i in range(1,8) for c in [0,1,3]],lambda d:max(len(d['tasks']),(d['tasks'].count('A')-1)*(d['n']+1)+1))
put(168,[{'items':[{'weight':2,'value':6},{'weight':4,'value':8}],'capacity':i} for i in range(0,11)],lambda d:3*min(2,d['capacity'])+2*min(4,max(0,d['capacity']-2)))
put(247,[{'arrivals':[100+i for i in range(n)],'departures':[200+i for i in range(n)]} for n in range(1,11)],lambda d:len(d['arrivals']))
def candy(a):
 # Exhaust all assignments for small ratings arrays, with a tight finite bound.
 return min(sum(c) for c in it.product(range(1,len(a)+1),repeat=len(a)) if all((a[i]<=a[j] or c[i]>c[j]) for i in range(len(a)) for j in [i-1,i+1] if 0<=j<len(a)))
put(166,[[1],[2],[1,1],[1,2],[2,1],[1,2,1],[1,2,3],[3,2,1],[1,2,2],[2,1,2]],candy)
# DP baselines enumerate choices rather than reuse the optimized reference recurrences.
put(121,list(range(0,12)),lambda n:sum(math.comb(n-k,k) for k in range(n//2+1)))
def staircost(a):
 @functools.lru_cache(None)
 def walk(i):return 0 if i>=len(a) else a[i]+min(walk(i+1),walk(i+2))
 return min(walk(0),walk(1))
put(122,[a for a in POS if len(a)>=2]+[[1,5,1,5,1],[0,0],[2,2,2,2]],staircost)
def frog(a):
 def walk(i):return 0 if i==len(a)-1 else min(abs(a[i]-a[j])+walk(j) for j in [i+1,i+2] if j<len(a))
 return walk(0)
put(125,POS,frog)
def robber(a,circular=False):
 return max(sum(a[i] for i in s) for k in range(len(a)+1) for s in it.combinations(range(len(a)),k) if all(b-a>1 for a,b in zip(s,s[1:])) and (not circular or len(a)<2 or not(0 in s and len(a)-1 in s)))
put(123,POS,robber);put(124,POS,lambda a:robber(a,True))
put(126,[{'rows':n,'cols':k} for n in range(1,6) for k in [1,2,4]],lambda d:math.comb(d['rows']+d['cols']-2,d['rows']-1))
put(127,[[[0]*n,[0]*n] for n in range(1,9)]+[[[1,0],[0,0]],[[0,1],[1,0]]],lambda a:len(a[0]) if not any(sum(a,[])) else 0)
put(128,[[[i]*n,[i]*n] for n in range(1,6) for i in [1,3]],lambda a:(len(a[0])+1)*a[0][0])
put(129,[[[i]*(j+1) for j in range(n)] for n in range(1,7) for i in [-2,3]],lambda a:len(a)*a[0][0])
def coinmin(d):
 for n in range(d['amount']+1):
  if any(sum(c)==d['amount'] for c in it.combinations_with_replacement(d['coins'],n)):return n
 return -1
put(130,[{'coins':[2,3],'amount':n} for n in range(0,14)],coinmin)
put(131,[{'coins':[2,3],'amount':n} for n in range(0,14)],lambda d:sum(sum(c)==d['amount'] for n in range(d['amount']+1) for c in it.combinations_with_replacement(d['coins'],n)))
put(132,POS,lambda a:any(sum(s)*2==sum(a) for s in subsets(a)))
def knapsack(d,reuse=False):
 w=d['weights'];v=d['values'];cap=d['capacity'];counts=it.product(*[range(cap//x+1) if reuse else range(2) for x in w]);return max(sum(n*x for n,x in zip(c,v)) for c in counts if sum(n*x for n,x in zip(c,w))<=cap)
K=[{'weights':[2,3,4],'values':[3,4,7],'capacity':n} for n in range(0,13)]
put(226,K,knapsack);put(227,K,lambda d:knapsack(d,True))
put(228,[{'nums':a,'target':n} for a in [[0],[1],[1,1],[0,0,1],[1,2,3]] for n in [0,1,2]],lambda d:sum(sum(s*x for s,x in zip(signs,d['nums']))==d['target'] for signs in it.product([-1,1],repeat=len(d['nums']))))
put(229,POS,lambda a:min(abs(sum(a)-2*sum(s)) for s in subsets(a)))
put(230,[[i]*n for n in range(1,7) for i in [1,3]],lambda a:len(a)*a[0])
def trades(a,fee=0,cool=0,limit=100):
 def explore(day,holding,cash,bought,count):
  if day>=len(a):return cash if not holding else -10**9
  best=explore(day+1,holding,cash,bought,count)
  if holding:best=max(best,explore(day+1+cool,False,cash+a[day]-fee,-1,count+1))
  elif count<limit:best=max(best,explore(day+1,True,cash-a[day],day,count))
  return best
 return explore(0,False,0,-1,0)
put(232,POS,lambda a:trades(a,cool=1))
put(233,[{'prices':a,'fee':f} for a in POS for f in [0,1,3]],lambda d:trades(d['prices'],fee=d['fee']))
put(234,POS,lambda a:trades(a,limit=2))
put(237,[[[i]*n for _ in range(n)] for n in range(1,6) for i in [-2,3]],lambda a:len(a)*a[0][0])
def eggs(d):
 n=0
 while sum(math.comb(n,k) for k in range(1,min(n,d['eggs'])+1))<d['floors']:n+=1
 return n
put(240,[{'eggs':k,'floors':n} for k in [1,2,3] for n in [0,1,2,5,12]],eggs)
def increasing(s):return all(x<y for x,y in zip(s,s[1:]))
put(133,A,lambda a:max(len(s) for s in subsets(a) if increasing(s)))
def lcs(d):return max(len(s) for s in subsets(d['a']) if subseq(s,d['b']))
def subseq(a,b):
 itb=iter(b);return all(any(x==y for y in itb) for x in a)
PAIRS=[{'a':s,'b':t} for s,t in [('', ''),('a',''),('','ab'),('a','a'),('abc','xyz'),('abab','baba'),('aaaa','aa'),('abc','ac'),('cab','abc'),('abcd','dcba')]]
put(134,PAIRS,lcs)
put(135,PAIRS,lambda d:max([len(s) for s in ranges(d['a']) if s in d['b']]+[0]))
def edit(d):
 @functools.lru_cache(None)
 def f(a,b):
  if not a or not b:return len(a)+len(b)
  return f(a[1:],b[1:]) if a[0]==b[0] else 1+min(f(a[1:],b),f(a,b[1:]),f(a[1:],b[1:]))
 return f(d['a'],d['b'])
put(136,PAIRS,edit)
put(137,WORDS,lambda a:max(len(s) for s in subsets(a) if s==s[::-1]))
put(138,WORDS,lambda a:sum(s==s[::-1] for s in ranges(a)))
put(139,[{'s':s,'words':['a','ab','bc']} for s in WORDS],lambda d:any(all(part in d['words'] for part in p) for p in allparts(d['s'])))
def allparts(s):
 if not s:return [[]]
 return [[s[:i]]+tail for i in range(1,len(s)+1) for tail in allparts(s[i:])]
put(142,A,lambda a:max(map(math.prod,ranges(a))))
put(235,A,lambda a:(lambda valid:sum(len(s)==max(map(len,valid)) for s in valid))([s for s in subsets(a) if increasing(s)]))
def bitonic(a):
 return max(len(s) for s in subsets(a) if any(increasing(s[:i+1]) and increasing(s[i:][::-1]) for i in range(len(s))) or not s)
put(236,A,bitonic)
put(140,[{'s':d['a'],'t':d['b']} for d in PAIRS],lambda d:sum(''.join(s)==d['t'] for s in it.combinations(d['s'],len(d['t']))))
def wildcard(d):
 @functools.lru_cache(None)
 def f(s,p):
  if not p:return not s
  if p[0]=='*':return f(s,p[1:]) or bool(s) and f(s[1:],p)
  return bool(s) and (p[0]=='?' or p[0]==s[0]) and f(s[1:],p[1:])
 return bool(f(d['s'],d['p']))
put(141,[{'s':s,'p':p} for s in ['','a','ab','aa','aba'] for p in ['*','?','a*','*b','a?']],wildcard)
def mchain(a):
 def f(l,r):return 0 if r-l<=1 else min(f(l,k)+f(k,r)+a[l]*a[k]*a[r] for k in range(l+1,r))
 return f(0,len(a)-1)
put(143,[[i,2*i,3*i,4*i] for i in range(1,11)],mchain)
def balloons(a):
 if not a:return 0
 return max((a[i-1] if i else 1)*x*(a[i+1] if i+1<len(a) else 1)+balloons(a[:i]+a[i+1:]) for i,x in enumerate(a))
put(144,[a for a in POS if len(a)<=5]+[[0],[0,1,0]],balloons)
put(238,WORDS,lambda s:min(len(p)-1 for p in allparts(s) if all(x==x[::-1] for x in p)) if s else 0)
def boolean(s):
 if len(s)==1:return [s=='T']
 out=[]
 for i in range(1,len(s),2):
  for l in boolean(s[:i]):
   for r in boolean(s[i+1:]):out.append((l and r) if s[i]=='&' else (l or r) if s[i]=='|' else l!=r)
 return out
put(239,['T','F','T|F','T&F','T^F','T|T&F','T^T^T','T&F|T','F|F|F','T&T&T'],lambda s:sum(boolean(s)))
def cutstick(d):
 def f(a,b,c):return 0 if not c else b-a+min(f(a,x,[y for y in c if y<x])+f(x,b,[y for y in c if y>x]) for x in c)
 return f(0,d['length'],d['cuts'])
put(241,[{'length':n,'cuts':[1,n-1]} for n in range(3,13)],cutstick)
put(169,[[i,9,9,-3,-3] for i in range(-10,9) if i not in [9,-3]],lambda a:a[0])
put(170,[0,1,2,3,7,8,31,32,255,256,4294967295],int.bit_count)
put(171,list(range(0,13)),lambda n:[x.bit_count() for x in range(n+1)])
put(172,[0,1,2,3,4,5,8,16,31,32,1024,-2],lambda n:n>0 and n in [2**i for i in range(32)])
put(174,[0,1,2,3,4,8,255,256,2147483648,4294967295],lambda n:int(format(n,'032b')[::-1],2))
put(215,[['a'*n+'b','a'*n+'c'] for n in range(0,10)],lambda a:a[0][:-1])
put(173,[[i,i+1,99,99] for i in range(-6,6)],lambda a:sorted(a[:2]))
put(175,[{'left':l,'right':r} for l in range(0,8) for r in [l,l+3]],lambda d:functools.reduce(int.__and__,range(d['left'],d['right']+1)))
put(176,[[['insert','a'*n],['search','a'*n],['search','a'*n+'b'],['prefix','a']] for n in range(1,11)],lambda a:[None,True,False,True])
put(177,[{'roots':['cat','c','dog'],'sentence':'cattle dogmatic apple '+('z'*n)} for n in range(1,11)],lambda d:'c dog apple '+d['sentence'].split()[-1])
put(178,[[abs(x) for x in a] for a in A],lambda a:max([x^y for x in a for y in a]+[0]))
put(179,[{'capacity':1,'operations':[['put',i,i+2],['get',i],['put',i+1,0],['get',i],['get',i+1]]} for i in range(-4,8)],lambda d:[None,d['operations'][0][2],None,-1,0])
put(245,[{'n':n,'k':k} for n in range(1,8) for k in [1,2**(n-1)]],lambda d:(d['k']-1).bit_count()%2)
put(249,[[i,8,8,8] for i in range(-6,8)],lambda a:a[0])
put(250,[['a'*i for i in range(1,n+1)]+['b'*n] for n in range(1,11)],lambda a:max((w for w in a if all(w[:i] in a for i in range(1,len(w)+1))),key=lambda w:(len(w),tuple(-ord(c) for c in w)),default=''))
put(180,[{'text':s,'pattern':p} for s in WORDS for p in ['','a','ab','aaa']],lambda d:d['text'].find(d['pattern']))

def main():
 for id,(inputs,oracle) in list(CASES.items()):
  CASES[id]=[{'input':copy.deepcopy(x),'expected':oracle(copy.deepcopy(x)),'name':f'Regression {i+1}'} for i,x in enumerate(inputs)]
 problems=json.loads((ROOT/'dsa.json').read_text())
 missing=[p['id'] for p in problems if int(p['id'][4:]) not in CASES]
 assert not missing,missing
 for p in problems:
  samples=p.get('sampleTests',p['tests']);seen={json.dumps(t['input'],sort_keys=True) for t in samples};pool=[]
  for t in CASES[int(p['id'][4:])]:
   key=json.dumps(t['input'],sort_keys=True)
   if key not in seen:pool.append(t);seen.add(key)
  assert len(pool)>=6,(p['id'],len(pool))
  picked=[pool[round(i*(len(pool)-1)/5)] for i in range(6)]
  p['sampleTests']=samples;p['tests']=samples+picked;p['suiteVersion']='2.4.0'
 (ROOT/'dsa.json').write_text(json.dumps(problems,ensure_ascii=False,indent=2)+'\n')
 print(f"Built {sum(len(p['tests']) for p in problems)} cases across {len(problems)} problems; minimum {min(len(p['tests']) for p in problems)} each")
if __name__=='__main__':main()
