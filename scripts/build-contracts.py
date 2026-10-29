"""Derive named test contracts from the existing, tested examples without changing inputs."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
problems=json.loads((root/'dsa.json').read_text())
def compact(value):return json.dumps(value,ensure_ascii=False,separators=(', ', ': '))
def tree_graph(values):
    if not values or values[0] is None:return {'kind':'tree','nodes':[],'edges':[]}
    nodes=[{'id':0,'value':values[0],'x':50,'y':22}];edges=[];queue=[(0,50,25,0)];i=1
    while queue and i<len(values):
        parent,x,span,depth=queue.pop(0)
        for side in [-1,1]:
            if i>=len(values):break
            value=values[i];i+=1
            if value is not None:
                index=len(nodes);nx=x+side*span
                nodes.append({'id':index,'value':value,'x':nx,'y':22+(depth+1)*24});edges.append([parent,index]);queue.append((index,nx,span/2,depth+1))
    return {'kind':'tree','nodes':nodes,'edges':edges}
def describe(key,value,problem):
    if key in ['tree','root','subRoot'] or ('TreeNode' in problem['cpp']['signature'] and not isinstance(problem['example']['input'],dict)):
        return 'Binary tree · level-order node values','null marks a missing child. Consume child slots only for existing parents; trailing nulls may be omitted.'
    if isinstance(value,list):
        if value and all(isinstance(x,list) for x in value):
            if key in ['edges','flights','times']:
                return 'Edge list',('[from, to, weight] per row.' if len(value[0])==3 else '[from, to] per row.')+' Direction and weight rules follow the statement.'
            if key=='prerequisites':return 'Prerequisite pairs','Each row is [course, prerequisite]: complete the second course before the first. Course IDs run from 0 to n−1.'
            if key in ['intervals','meetings']:return 'Intervals · [start, end]','Each row is one interval. Endpoint overlap rules follow this problem’s statement.'
            if key=='operations':return 'Ordered operation stream','Each row begins with an operation name, followed by its arguments. Apply rows from top to bottom to the same data structure.'
            if key=='queries':return 'Query pairs','Each row is one query. The statement specifies the index convention and whether the endpoints are inclusive.'
            if key=='points':return 'Points · [x, y]','Each row is a separate two-dimensional point, not a row of a grid.'
            if key=='lists':return 'Sorted sequences','Each inner array is one sorted sequence. Keep the sequences separate; do not flatten them before calling the function.'
            return 'Matrix / list of rows','Each inner array is one row. Preserve row order; use the statement’s shape and adjacency rules.'
        if 'ListNode' in problem['cpp']['signature'] and (key in ['head','a','b','listA','listB','input','values','prefixA','prefixB','shared'] or not isinstance(problem['example']['input'],dict)):
            return 'Linked list · head-to-tail values','The runner constructs ListNode objects in this order. Your C++ function receives a node pointer.'
        if all(isinstance(x,str) for x in value):return 'List of strings','Keep each quoted string as a separate item; empty strings and spaces are meaningful.'
        return 'Array of values','Entries stay in the shown order. Its length is inferred; do not add a separate length value.'
    if isinstance(value,str):return 'String','Enter the text itself in the Arguments tab. Quotation marks here identify a string in the example.'
    if isinstance(value,bool):return 'Boolean','Choose true or false.'
    if isinstance(value,int):return 'Integer','One whole number. Refer to the constraints for its valid range and meaning.'
    if value is None:return 'Optional value','null means the value is absent under this problem’s contract.'
    return 'Structured value','Use the named fields shown in the example.'
for p in problems:
    example=p['example']['input'];obj=isinstance(example,dict)
    raw=p['cpp']['signature'].split('(',1)[1].rsplit(')',1)[0]
    chunks=[];start=0;depth=0
    for i,char in enumerate(raw):
        if char=='<': depth+=1
        elif char=='>': depth-=1
        elif char==',' and depth==0: chunks.append(raw[start:i]);start=i+1
    chunks.append(raw[start:])
    params=[re.search(r'([A-Za-z_]\w*)\s*$',chunk).group(1) for chunk in chunks if chunk.strip()]
    name=(params[-1] if len(params)==1 else 'input')
    entries=list(example.items()) if obj else [(name,example)]
    args=[];diagrams=[]
    for key,value in entries:
        rep,desc=describe(key,value,p)
        if p['id'] in ['dsa-053','dsa-054'] and key=='pos':desc='Zero-based index of the node to which the tail connects. Use −1 for no cycle; this field builds the list and is not passed as a separate C++ argument.'
        if p['id']=='dsa-205' and key in ['prefixA','prefixB','shared']:desc={'prefixA':'Private nodes before the shared tail in list A.','prefixB':'Private nodes before the shared tail in list B.','shared':'Nodes created once and attached to both lists. Intersection means the same node object, not merely equal values.'}[key]
        if p['id'] in ['dsa-083','dsa-213'] and key in ['p','q','target']:desc='Value identifying an existing node in this example tree. The runner finds that node and passes its TreeNode pointer to C++.'
        if p['id']=='dsa-113' and key=='k':desc='The source vertex, numbered from 1 through n. The C++ function calls this argument source.'
        if p['id']=='dsa-203' and key=='x':desc='Partition value, passed to the C++ function as pivot.'
        args.append({'name':key,'representation':rep,'example':value,'description':desc})
        if rep.startswith('Binary tree'):
            g=tree_graph(value);g['label']=key;diagrams.append(g)
        elif rep.startswith('Linked list'):
            diagram={'kind':'list','label':key,'values':value[:14],'truncated':len(value)>14}
            if p['id'] in ['dsa-053','dsa-054']:diagram['cycleTo']=example['pos']
            if p['id']=='dsa-205' and key in ['prefixA','prefixB']:diagram['suffix']='shared tail'
            diagrams.append(diagram)
        elif rep.startswith('Matrix') and len(value)<=6 and all(len(row)<=8 for row in value):diagrams.append({'kind':'matrix','label':key,'rows':value})
    notes=['Implement the supplied function. The runner calls it with these arguments; no main function or separate size prefix is required.']
    if 'TreeNode' in p['cpp']['signature']:notes.append('The array is a test representation of a pointer-based tree. It is not a heap-indexed array: missing nodes do not receive children.')
    if 'ListNode' in p['cpp']['signature']:notes.append('Node identity, cycle positions, and shared tails are described by the statement when relevant; an array by itself describes node values only.')
    if p['id']=='dsa-205':notes.append('Construct headA as prefixA followed by shared, and headB as prefixB followed by the exact same shared nodes.')
    if p['id']=='dsa-113':notes.append('Network delay uses 1-based vertices, 1 through n. Each times row is a directed [from, to, travelTime] edge.')
    if obj and 'n' in example and 'edges' in example:notes.append('For this graph input, n is the vertex count; vertex identifiers run from 0 through n−1. The statement defines directedness and edge weights.')
    p['contract']={'arguments':args,'namedInput':'\n'.join(key+' = '+compact(value) for key,value in entries),'expectedOutput':p['example']['output'],'notes':notes,'diagrams':diagrams}
(root/'dsa.json').write_text(json.dumps(problems,ensure_ascii=False,indent=2)+'\n')
print('Built clear named contracts for',len(problems),'problems')
