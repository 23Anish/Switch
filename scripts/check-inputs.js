#!/usr/bin/env node
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const problems=JSON.parse(fs.readFileSync(path.join(root,'dsa.json'),'utf8'));
const context=vm.createContext({});
vm.runInContext(fs.readFileSync(path.join(root,'web/study-tools.js'),'utf8'),context);
function evaluate(code,args){context.args=args;return vm.runInContext(code,context)}
let count=0;
for(const problem of problems){
 const specs=evaluate('inputSpecs(args)',problem);
 for(const spec of specs){
  const actual=evaluate('parseArgument(formatArgument(args.value,inputKind(args.value)),inputKind(args.value),args.name)',spec);
  assert.equal(JSON.stringify(actual),JSON.stringify(spec.value),problem.id+' '+spec.name);
  count++;
 }
}
assert.equal(JSON.stringify(evaluate('parseArgument(args,"numbers","nums")','1, 2 -3 null')),'[1,2,-3,null]');
assert.equal(JSON.stringify(evaluate('parseArgument(args,"matrix","grid")','1 2\n3,4')),'[[1,2],[3,4]]');
assert.equal(JSON.stringify(evaluate('parseArgument(args,"strings","words")','["", "a b"]')),'["","a b"]');
assert.throws(()=>evaluate('parseArgument(args,"number","n")',''));
assert.throws(()=>evaluate('parseArgument(args,"numbers","nums")','1,two'));
assert.throws(()=>evaluate('parseArgument(args,"number","n")','1.3'));
console.log(`${count} named arguments across all 250 problems round-trip; numeric, matrix, string, empty and invalid-input cases pass.`);
