// Friendly test inputs. JSON remains the runner's transport format only.
function inputSpecs(p){
  const sample=p.example.input;
  if(sample!==null&&typeof sample==='object'&&!Array.isArray(sample))return Object.entries(sample).map(([name,value])=>({name,value}));
  const match=p.cpp?.signature.match(/(?:&|\*|\s)([A-Za-z_]\w*)\s*\)$/);
  return [{name:match?.[1]||'input',value:sample}];
}
function numericList(value){return Array.isArray(value)&&value.every(x=>typeof x==='number'||x===null)}
function inputKind(value){
  if(typeof value==='number')return 'number';
  if(typeof value==='boolean')return 'boolean';
  if(typeof value==='string')return 'string';
  if(numericList(value))return 'numbers';
  if(Array.isArray(value)&&value.every(numericList))return 'matrix';
  if(Array.isArray(value)&&value.every(x=>typeof x==='string'))return 'strings';
  return 'structured';
}
function formatArgument(value,kind){
  if(kind==='numbers')return value.map(x=>x===null?'null':x).join(', ');
  if(kind==='matrix')return value.map(row=>row.map(x=>x===null?'null':x).join(', ')).join('\n');
  // Quoted strings preserve empty values, embedded newlines, and spacing.
  if(kind==='strings')return JSON.stringify(value);
  if(kind==='string')return value;
  return typeof value==='object'?JSON.stringify(value,null,2):String(value);
}
function parseArgument(text,kind,name){
  const fail=message=>{throw Error(name+': '+message)};
  if(kind==='string')return text;
  if(kind==='number'){
    if(!text.trim()||!Number.isFinite(Number(text)))fail('enter a number.');
    if(!Number.isSafeInteger(Number(text)))fail('enter a whole number within the safe integer range.');
    return Number(text);
  }
  if(kind==='boolean')return text==='true';
  if(kind==='numbers'||kind==='matrix'){
    const parseRow=row=>row.trim()?row.trim().split(/[\s,]+/).map(token=>{
      if(token==='null')return null;
      if(!/^-?\d+$/.test(token)||!Number.isSafeInteger(Number(token)))fail('use whole numbers separated by spaces or commas, or null.');
      return Number(token);
    }):[];
    let result;
    if(text.trim().startsWith('[')){
      try{result=JSON.parse(text)}catch{fail('check the brackets and commas in this array.')}
    }else result=kind==='numbers'?parseRow(text):text.trim()?text.trim().split(/\n|;/).map(parseRow):[];
    if(kind==='numbers'?!numericList(result):!Array.isArray(result)||!result.every(numericList))fail(kind==='numbers'?'enter a list of numbers.':'enter one row of numbers per line.');
    if(result.flat().some(x=>x!==null&&!Number.isSafeInteger(x)))fail('use whole numbers within the safe integer range.');
    return result;
  }
  if(kind==='strings'&&!text.trim().startsWith('['))return text===''?[]:text.split('\n');
  let result;try{result=JSON.parse(text)}catch{fail('enter a valid '+(kind==='strings'?'list of strings.':'structured value.'))}
  if(kind==='strings'&&(!Array.isArray(result)||result.some(x=>typeof x!=='string')))fail('enter a list of strings.');
  return result;
}
function inputValues(p){
  try{return JSON.parse(profile().inputs?.[p.id]??JSON.stringify(p.example.input))}catch{return p.example.input}
}
function customInputEditor(p){
  const mode=state.inputMode||'arguments',value=inputValues(p),object=p.example.input!==null&&typeof p.example.input==='object'&&!Array.isArray(p.example.input);
  const help={number:'Whole number',boolean:'True or false',string:'Text · no quotation marks needed',numbers:'Numbers separated by spaces or commas · null for missing nodes',matrix:'One row per line · separate values with spaces or commas',strings:'One string per line, or a quoted array to preserve empty strings',structured:'Structured value · use the shape shown in the example'};
  return `<div class="input-panel spaced"><div class="editorbar"><h3>Custom test case</h3><button id="reset-code" class="linkbutton">Reset code</button></div><div class="input-tabs" aria-label="Test input format"><button data-input-mode="arguments" class="${mode==='arguments'?'selected':''}" aria-pressed="${mode==='arguments'}">Arguments</button><button data-input-mode="json" class="${mode==='json'?'selected':''}" aria-pressed="${mode==='json'}">JSON</button></div><div class="input-fields" ${mode!=='arguments'?'hidden':''}>${inputSpecs(p).map((spec,i)=>{
    const kind=inputKind(spec.value),raw=profile().argumentDrafts?.[p.id]?.[spec.name]??formatArgument(object?(value?.[spec.name]??spec.value):value,kind),id='argument-'+i;
    const attrs=`id="${id}" data-argument="${esc(spec.name)}" data-kind="${kind}" aria-describedby="${id}-help"`;
    return `<div class="input-field"><label for="${id}">${esc(spec.name)}</label>${kind==='boolean'?`<select ${attrs}><option value="true" ${raw==='true'?'selected':''}>true</option><option value="false" ${raw==='false'?'selected':''}>false</option></select>`:kind==='number'?`<input ${attrs} type="number" step="1" value="${esc(raw)}">`:kind==='string'?`<input ${attrs} type="text" value="${esc(raw)}" autocomplete="off" spellcheck="false">`:`<textarea ${attrs} rows="${kind==='matrix'?4:3}" spellcheck="false">${esc(raw)}</textarea>`}<small id="${id}-help">${help[kind]}</small></div>`;
  }).join('')}</div><div ${mode!=='json'?'hidden':''}><label for="stdin">Raw test data</label><textarea id="stdin" class="input" spellcheck="false" aria-label="Raw test data">${esc(profile().inputs?.[p.id]??JSON.stringify(p.example.input,null,2))}</textarea></div><p id="input-feedback" class="input-feedback" role="status"></p><p class="input-help subtle">The app passes these values to your function. Use Run tests for the included cases, or Run custom input for your own case.</p></div>`;
}
function bindArguments(){
  const p=D.find(p=>p.id===selected);if(!p||!$('#stdin'))return;
  const fields=$$('[data-argument]');
  const synchronize=()=>{
    const error=$('#input-feedback'),button=$('#run-custom');
    try{
      const entries=fields.map(el=>[el.dataset.argument,parseArgument(el.value,el.dataset.kind,el.dataset.argument)]);
      if(!entries.length)return;
      const object=p.example.input!==null&&typeof p.example.input==='object'&&!Array.isArray(p.example.input);
      const value=object?Object.fromEntries(entries):entries[0][1];
      $('#stdin').value=JSON.stringify(value);profile().inputs??={};profile().inputs[p.id]=$('#stdin').value;
      if(error){error.textContent='Ready to run.';error.classList.remove('error')}
      if(button)button.disabled=practiceRun(profile(),p.id,lang).running;
      return true;
    }catch(e){if(error){error.textContent=e.message;error.classList.add('error')}if(button)button.disabled=true;return false}
  };
  fields.forEach(el=>el.oninput=()=>{
    profile().argumentDrafts??={};profile().argumentDrafts[p.id]=Object.fromEntries(fields.map(field=>[field.dataset.argument,field.value]));synchronize();save();
  });
  $$('[data-input-mode]').forEach(button=>button.onclick=()=>{state.inputMode=button.dataset.inputMode;save();render()});
  if((state.inputMode||'arguments')==='arguments')synchronize();
  else $('#stdin').oninput=e=>{profile().inputs??={};profile().inputs[p.id]=e.target.value;if(profile().argumentDrafts)delete profile().argumentDrafts[p.id];save()};
}
function workedExamples(id){
  const examples=(window.THEORY_EXAMPLES||[]).filter(e=>e.lessonId===id);
  if(!examples.length)return '';
  return `<section class="worked-examples article"><div class="section-heading"><p class="eyebrow">Understand it by building it</p><h2>Worked examples</h2><p>Trace the idea, read the code, then try the variation yourself.</p></div>${examples.map((e,i)=>`<section class="card section"><p class="eyebrow">Example ${i+1} · ${esc(e.language)}</p><h2>${esc(e.title)}</h2><p>${esc(e.concept)}</p><div class="diagram">${(e.diagram||[]).map((step,j)=>`${j?'<b aria-hidden="true">→</b>':''}<span>${esc(step)}</span>`).join('')}</div><h3 class="spaced">Walk through it</h3><ol class="constraints">${e.walkthrough.map(step=>`<li>${esc(step)}</li>`).join('')}</ol><h3>Example code</h3>${codeBlock(e.code)}<h3>Expected output</h3>${codeBlock(e.expectedOutput)}<h3>Design trade-offs</h3><ul class="constraints">${e.tradeoffs.map(t=>`<li>${esc(t)}</li>`).join('')}</ul><div class="question"><h3>Try it yourself</h3><p>${esc(e.exercise)}</p><details class="spaced"><summary>Check your reasoning</summary><p>${esc(e.solution)}</p></details></div>${e.sources?.length?`<p class="subtle spaced">Further reading: ${e.sources.map(s=>`<a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.title)} ↗</a>`).join(' · ')}</p>`:''}</section>`).join('')}</section>`;
}
