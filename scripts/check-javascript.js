const fs=require('fs'),vm=require('vm'),assert=require('assert');
const data=JSON.parse(fs.readFileSync(require('path').join(__dirname,'../dsa.json'),'utf8'));
let count=0;
function canon(v){return v&&typeof v==='object'?Array.isArray(v)?v.map(canon):Object.fromEntries(Object.keys(v).sort().map(k=>[k,canon(v[k])])):v}
for(const p of data)for(const t of p.tests){let context={input:structuredClone(t.input)};vm.createContext(context);let actual=vm.runInContext(p.solution+';solve(input)',context,{timeout:3000});assert.equal(JSON.stringify(canon(actual)),JSON.stringify(canon(t.expected)),p.id+' '+p.title);count++}
console.log(`${data.length} JavaScript solutions, ${count} tests passed.`);
