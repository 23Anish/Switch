#!/usr/bin/env node
// Exercise the shared navigation and appearance state without replacing the editor.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
let saved, renderCalls = 0;
const listeners = new Map();
function classes(initial = []) {
  const values = new Set(initial);
  return { add(...names) { names.forEach(n => values.add(n)); }, remove(...names) { names.forEach(n => values.delete(n)); }, contains(name) { return values.has(name); }, toggle(name, force) { const on = force === undefined ? !values.has(name) : !!force; if (on) values.add(name); else values.delete(name); return on; } };
}
const nodes = {}, themeButtons = [];
let document;
function element(id, options = {}) {
  return Object.assign({ id, dataset: {}, classList: classes(), attributes: {}, hidden: false, inert: false, value: '', textContent: '', setAttribute(k, v) { this.attributes[k] = String(v); }, getAttribute(k) { return this.attributes[k] ?? null; }, focus() { document.activeElement = this; }, querySelector() { return null; }, closest(selector) { return selector === '.floating-header' && this.inHeader ? nodes['.floating-header'] : null; } }, options);
}
document = { body: { classList: classes(), dataset: {} }, documentElement: { dataset: {} }, activeElement: null, addEventListener(name, callback) { if (!listeners.has(name)) listeners.set(name, []); listeners.get(name).push(callback); }, querySelector: selector => nodes[selector] ?? null, querySelectorAll: selector => selector === '[data-theme-choice]' ? themeButtons : [] };
for (const id of ['menu-trigger', 'theme-trigger', 'focus-trigger', 'focus-exit', 'broad-menu', 'theme-menu', 'profile']) nodes['#' + id] = element(id, { inHeader: id !== 'focus-exit' });
nodes['.floating-header'] = element('floating-header');
for (const id of ['broad-menu', 'theme-menu', 'focus-exit']) { nodes['#' + id].hidden = true; nodes['#' + id].inert = true; }
for (const id of ['midnight', 'retro', 'pokemon']) {
  const check = element('check-' + id), button = element('theme-' + id, { dataset: { themeChoice: id }, check, querySelector: selector => selector === '.theme-selected' ? check : null });
  themeButtons.push(button);
}
const context = vm.createContext({ console, window: {}, document, navigator: {}, location: { protocol: 'file:' }, localStorage: { getItem: () => null, setItem: (_, value) => { saved = JSON.parse(value); } }, setTimeout, clearTimeout, markRender() { renderCalls++; } });
const run = code => vm.runInContext(code, context);
run(fs.readFileSync(path.join(root, 'web/data.js'), 'utf8'));
for (const file of ['diagrams.js', 'app.js', 'study-tools.js', 'features.js', 'experience.js', 'upgrades.js', 'immersive.js']) run(fs.readFileSync(path.join(root, 'web', file), 'utf8').replace(/render\(\);\s*$/, ''));
// Isolate navigation's render wrapper from the app's unrelated page controls.
run('render = () => markRender();');
run(fs.readFileSync(path.join(root, 'web/spatial.js'), 'utf8').replace(/render\(\);\s*$/, ''));
const json = expression => JSON.parse(run(`JSON.stringify(${expression})`));
const expected = ['dashboard', 'dsa', 'visual', 'core', 'lld', 'hld', 'ai', 'companies', 'interview', 'plan', 'review', 'settings'];
const groups = json('spatialMenuGroups()');
assert.deepEqual(groups.flatMap(([, items]) => items.map(([id]) => id)), expected);
assert.equal(new Set(groups.flatMap(([, items]) => items.map(([id]) => id))).size, expected.length);
// Future routes must remain discoverable rather than disappearing from fixed groups.
run('nav.push(["future-track", "↗", "Future track"]);');
assert.equal(json('spatialMenuGroups()').at(-1)[1].at(-1)[0], 'future-track');
run('nav.pop();');
for (const [page, selected, active] of [['dashboard', null, 'dashboard'], ['problem', 'dsa-001', 'dsa'], ['lesson', 'lesson-01', 'core'], ['lesson', 'lld-01', 'lld'], ['lesson', 'hld-01', 'hld'], ['lesson', 'lesson-27', 'ai'], ['interview', null, 'interview']]) {
  run(`page=${JSON.stringify(page)};selected=${JSON.stringify(selected)};`);
  assert.equal(run('activeNavigation()'), active);
}
run('page="problem";selected="dsa-001";');
assert.equal(run('spatialPageLabel()'), 'Coding studio');
run('page="lesson";selected="lld-01";');
assert.equal(run('spatialPageLabel()'), 'Study notes');
run('page="interview";');
assert.equal(run('spatialPageLabel()'), 'Interview studio');
const unusualName = 'Brother <img src=x> "A&B"';
context.unusualName = unusualName;
run('state.profiles[unusualName]={done:{},read:{},notes:{},code:{},reviews:{},days:{}};');
const html = run('shell("<p>Workspace content</p>")');
assert.ok(!html.includes('class="sidebar"') && !html.includes('class="topbar"'));
assert.equal((html.match(/id="profile"/g) || []).length, 1);
assert.equal((html.match(/<option /g) || []).length, 2);
assert.ok(html.includes('Brother &lt;img src=x&gt; &quot;A&amp;B&quot;'));
assert.ok(!html.includes('<img src=x>'));
assert.ok(html.includes('src="icon.svg"'));
assert.equal((html.match(/data-theme-choice=/g) || []).length, 20);
assert.ok(html.includes('id="broad-menu"') && html.includes('aria-controls="broad-menu"'));
assert.ok(html.includes('id="theme-menu"') && html.includes('aria-controls="theme-menu"'));
assert.ok(html.includes('<p>Workspace content</p>'));
const broad = nodes['#broad-menu'], themeMenu = nodes['#theme-menu'], menuTrigger = nodes['#menu-trigger'], themeTrigger = nodes['#theme-trigger'];
run('bindSpatialNavigation();');
menuTrigger.onclick();
assert.equal(broad.hidden, false); assert.equal(broad.inert, false); assert.equal(menuTrigger.getAttribute('aria-expanded'), 'true');
themeTrigger.onclick();
assert.equal(broad.hidden, true); assert.equal(broad.inert, true); assert.equal(themeMenu.hidden, false); assert.equal(themeTrigger.getAttribute('aria-expanded'), 'true');
themeTrigger.onclick();
assert.equal(themeMenu.hidden, true); assert.equal(themeMenu.inert, true); assert.equal(themeTrigger.getAttribute('aria-expanded'), 'false');
menuTrigger.onclick();
let prevented = 0;
listeners.get('keydown').at(-1)({ key: 'Escape', preventDefault() { prevented++; } });
assert.equal(broad.hidden, true); assert.equal(document.activeElement, menuTrigger); assert.equal(prevented, 1);
menuTrigger.onclick();
listeners.get('click').at(-1)({ target: menuTrigger });
assert.equal(broad.hidden, false, 'Clicks inside the header leave the open menu usable');
listeners.get('click').at(-1)({ target: element('outside') });
assert.equal(broad.hidden, true, 'Outside clicks dismiss the floating menu');
// Existing profile binding must continue to update the active learner.
run('bind();');
nodes['#profile'].onchange({ target: { value: unusualName } });
assert.equal(saved.active, unusualName); assert.equal(run('state.active'), unusualName);
// The editor instance, draft, caret, and undo history must survive appearance changes.
const editor = element('code', { value: '#include <bits/stdc++.h>\nint main() {}', selectionStart: 12, selectionEnd: 17, undoHistory: ['starter', 'draft'] });
nodes['#code'] = editor;
run('page="problem";selected="dsa-001";profile().code[codeKey(D[0],"cpp")]="saved typed draft";');
const rendersBefore = renderCalls;
menuTrigger.onclick();
nodes['#focus-trigger'].onclick();
assert.equal(nodes['.floating-header'].hidden, true); assert.equal(nodes['.floating-header'].inert, true); assert.equal(nodes['#focus-exit'].hidden, false); assert.equal(nodes['#focus-exit'].inert, false);
assert.equal(document.activeElement, nodes['#focus-exit']);
assert.equal(document.body.classList.contains('focus-mode-active'), true);
assert.ok(run('shell("")').includes('aria-label="Switch navigation" hidden inert'));
nodes['#focus-exit'].onclick();
assert.equal(nodes['.floating-header'].hidden, false); assert.equal(nodes['#focus-exit'].hidden, true); assert.equal(document.activeElement, nodes['#focus-trigger']);
run('setSpatialFocus(true);');
listeners.get('keydown').at(-1)({ key: 'Escape', preventDefault() {} });
assert.equal(run('spatialFocus'), false);
run('setSpatialFocus(true);');
listeners.get('keydown').at(-1)({ key: 'Escape', isComposing: true, preventDefault() { throw Error('Composition must not be interrupted'); } });
assert.equal(run('spatialFocus'), true); run('setSpatialFocus(false);');
themeTrigger.onclick();
themeButtons[1].onclick();
assert.equal(saved.theme, 'retro'); assert.equal(document.documentElement.dataset.theme, 'retro');
assert.equal(themeButtons[1].getAttribute('aria-pressed'), 'true'); assert.equal(themeButtons[0].getAttribute('aria-pressed'), 'false'); assert.equal(themeButtons[1].check.textContent, '✓'); assert.equal(themeMenu.hidden, true);
assert.equal(document.activeElement, themeTrigger, 'A dismissed theme popover returns focus to its trigger');
// Workspace palette buttons update in place and retain their own keyboard focus.
document.activeElement = themeButtons[2];
themeButtons[2].onclick();
assert.equal(saved.theme, 'pokemon');
assert.equal(document.activeElement, themeButtons[2], 'A workspace theme choice keeps focus on the chosen card');
const themeBeforeInvalid = saved.theme;
run('applySpatialTheme("not-a-theme");');
assert.equal(saved.theme, themeBeforeInvalid, 'Unknown theme identifiers are ignored');
assert.equal(renderCalls, rendersBefore, 'Menu, focus mode, and palette changes never rerender the editor');
assert.equal(nodes['#code'], editor); assert.equal(editor.selectionStart, 12); assert.equal(editor.selectionEnd, 17); assert.deepEqual(editor.undoHistory, ['starter', 'draft']);
assert.equal(run('profile().code[codeKey(D[0],"cpp")]'), 'saved typed draft');
const keyListeners = listeners.get('keydown').length, clickListeners = listeners.get('click').length;
run('render(); render(); render();');
assert.equal(listeners.get('keydown').length, keyListeners); assert.equal(listeners.get('click').length, clickListeners);
console.log('12-route navigation, active problem/lesson/studio routes, escaped learner profiles, menu/theme exclusivity, Escape/outside dismissal, focus hide/restore, 20 themes, and editor/caret/undo preservation passed.');
