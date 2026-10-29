#!/usr/bin/env node
// Regression checks for C++ draft migration and the native runner bridge.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { webcrypto } = require('node:crypto');
const root = path.resolve(__dirname, '..');
const problem = JSON.parse(fs.readFileSync(path.join(root, 'dsa.json'), 'utf8')).find(p => p.id === 'dsa-002');
const nodes = Object.fromEntries(['#code', '#stdin', '#run', '#run-custom', '#reset-code', '#load-solution', '#output'].map(k => [k, {}]));
let saved;
const context = vm.createContext({
  window: { DSA: [problem], LESSONS: [] },
  document: { querySelector: s => nodes[s] || null, querySelectorAll: () => [] },
  navigator: {}, location: { protocol: 'file:' },
  localStorage: { getItem: () => null, setItem: (_, value) => { saved = JSON.parse(value); } },
  setTimeout, clearTimeout, crypto: webcrypto, console
});
const evaluate = code => vm.runInContext(code, context);
evaluate(fs.readFileSync(path.join(root, 'web/app.js'), 'utf8'));
evaluate(fs.readFileSync(path.join(root, 'web/study-tools.js'), 'utf8'));
evaluate(fs.readFileSync(path.join(root, 'web/features.js'), 'utf8').replace(/render\(\);\s*$/, ''));
evaluate(fs.readFileSync(path.join(root, 'web/upgrades.js'), 'utf8').replace(/render\(\);\s*$/, ''));
assert.equal(evaluate('lang'), 'cpp', 'C++ is the default');
evaluate('render = () => {}; page = "problem"; selected = "dsa-002"; profile().code["dsa-002:cpp"] = "old JSON draft";');
assert.equal(evaluate('codeKey(D[0], "cpp")'), 'dsa-002:cpp:v2');
assert.equal(evaluate('codeKey(D[0], "python")'), 'dsa-002:python');
let html = evaluate('problem()');
assert.ok(html.includes('Previous C++ draft') && html.includes('old JSON draft'));
assert.ok(!html.match(/<textarea id="code"[^>]*>[^<]*old JSON draft/));
assert.ok(!problem.starters.cpp.includes('json'));
assert.ok(!problem.solutions.cpp.includes('json'));
evaluate('bind();');
nodes['#code'].oninput({ target: { value: 'new typed draft' } });
assert.equal(saved.profiles.Learner.code['dsa-002:cpp:v2'], 'new typed draft');
assert.equal(saved.profiles.Learner.code['dsa-002:cpp'], 'old JSON draft');
nodes['#reset-code'].onclick();
assert.equal(saved.profiles.Learner.code['dsa-002:cpp:v2'], undefined);
assert.equal(saved.profiles.Learner.code['dsa-002:cpp'], 'old JSON draft');
evaluate('lang = "python"; solutionLang = "cpp"; bind();');
nodes['#load-solution'].onclick();
assert.equal(saved.language, 'cpp');
assert.equal(saved.profiles.Learner.code['dsa-002:cpp:v2'], problem.solutions.cpp);

(async () => {
  nodes['#code'].value = problem.solutions.cpp;
  nodes['#stdin'].value = JSON.stringify(problem.example.input);
  let message;
  context.window.webkit = { messageHandlers: { runCode: { postMessage(value) { message = value; context.window.switchNativeResult(value.id, 'TEST 1: PASS'); } } } };
  await evaluate('run(false)');
  assert.equal(message, undefined, 'Old native apps must not receive typed code');
  assert.ok(nodes['#output'].textContent.includes('Switch 2.1'));
  context.window.switchCapabilities = { cppApiVersion: 2 };
  await evaluate('run(false)');
  assert.equal(message.problemId, problem.id);
  assert.equal(message.cppApiVersion, 2);
  assert.equal(message.code, problem.solutions.cpp);
  assert.equal(message.practice, true);
  assert.equal(message.input, JSON.stringify(problem.sampleTests||problem.tests));
  assert.equal(nodes['#output'].textContent, 'TEST 1: PASS');
  assert.equal(nodes['#run'].disabled, false);
  await evaluate('run(true)');
  assert.deepEqual(JSON.parse(message.input), [{ input: problem.example.input }]);
  console.log('C++ default, old/new draft isolation, reset/load, native version gate, typed bridge, and custom input passed.');
})().catch(error => { console.error(error); process.exitCode = 1; });
