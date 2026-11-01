/* Shared floating navigation. Appearance changes never replace a learner's editor. */
let spatialFocus = false;
const spatialGroups = [
  ['Learning', ['dashboard', 'dsa', 'visual']],
  ['Curriculum', ['core', 'lld', 'hld', 'ai', 'companies']],
  ['Tools', ['interview', 'plan', 'review', 'settings']]
];

function activeNavigation() {
  if (page === 'problem') return 'dsa';
  if (page === 'lesson') return lessonPage(L.find(l => l.id === selected));
  return page;
}
function spatialPageLabel() {
  return page === 'problem' ? 'Coding studio' : page === 'lesson' ? 'Study notes' : nav.find(n => n[0] === page)?.[2] || 'Overview';
}
function spatialMenuGroups() {
  const known = new Set(spatialGroups.flatMap(([, ids]) => ids));
  return spatialGroups.map(([name, ids]) => [name, nav.filter(n => ids.includes(n[0]) || (name === 'Tools' && !known.has(n[0])))]);
}
function spatialRouteButton([id, icon, name]) {
  const active = activeNavigation() === id;
  return `<button class="menu-btn ${active ? 'active' : ''}" data-go="${id}" ${active ? 'aria-current="page"' : ''}><span class="icon" aria-hidden="true">${icon}</span><span>${esc(name)}</span></button>`;
}
function spatialThemeButtons() {
  return Object.entries(themes).map(([id, label]) => {
    const [name, tone] = label.split(' · '), chosen = (state.theme || 'midnight') === id;
    return `<button class="theme-btn theme-card ${chosen ? 'chosen active' : ''}" data-theme="${id}" data-theme-choice="${id}" aria-pressed="${chosen}"><i class="theme-swatch" aria-hidden="true"></i><span>${esc(name)}<small>${esc(tone)}</small></span><span class="theme-selected" aria-hidden="true">${chosen ? '✓' : ''}</span></button>`;
  }).join('');
}

shell = function(body) {
  const active = activeNavigation();
  return `<div class="layout spatial-layout">
    <header class="floating-header" aria-label="Switch navigation" ${spatialFocus ? 'hidden inert' : ''}>
      <button id="menu-trigger" class="brand menu-trigger" aria-label="Open navigation menu" aria-controls="broad-menu" aria-expanded="false"><img src="icon.svg" alt="" width="28" height="28"><span class="brand-word">switch</span><span class="menu-label">Menu <span aria-hidden="true">⌄</span></span></button>
      <nav class="dock" aria-label="Quick navigation">${[['dashboard', 'Overview'], ['dsa', 'Practice'], ['visual', 'Pattern lab']].map(([id, label]) => `<button data-go="${id}" class="${active === id ? 'active' : ''}" ${active === id ? 'aria-current="page"' : ''}>${label}</button>`).join('')}</nav>
      <div class="header-actions"><button id="theme-trigger" class="icon-btn" aria-label="Choose theme" aria-controls="theme-menu" aria-expanded="false"><span aria-hidden="true">◑</span><span class="action-label">Themes</span></button><button id="focus-trigger" class="icon-btn focus-trigger" aria-label="Hide navigation for focus mode"><span aria-hidden="true">⛶</span><span class="action-label">Focus</span></button></div>
      <nav id="broad-menu" class="broad-menu" aria-label="All learning sections" hidden inert>${spatialMenuGroups().map(([name, items]) => `<section class="menu-group"><p class="menu-eyebrow">${name}</p><div class="menu-grid">${items.map(spatialRouteButton).join('')}</div></section>`).join('')}<div class="menu-footer"><label for="profile">Learner profile<select id="profile" class="profile">${Object.keys(state.profiles).map(name => `<option value="${esc(name)}" ${name === state.active ? 'selected' : ''}>${esc(name)}</option>`).join('')}</select></label><span class="local">Progress saved on this device</span></div></nav>
      <section id="theme-menu" class="theme-menu" aria-label="Twenty themes" hidden inert><div class="theme-menu-heading"><p class="menu-eyebrow">Make it yours</p><span>20 gradient palettes</span></div><div class="theme-menu-grid">${spatialThemeButtons()}</div></section>
    </header>
    <button id="focus-exit" class="focus-toggle-pill" ${spatialFocus ? '' : 'hidden inert'} aria-label="Show navigation menu"><span aria-hidden="true">☰</span> Show menu</button>
    <main class="main"><div class="content">${page !== 'dashboard' ? `<div class="spatial-breadcrumb"><span>Workspace <span aria-hidden="true">/</span> <strong>${esc(spatialPageLabel())}</strong></span><button class="linkbutton" data-go="dashboard">Overview <span aria-hidden="true">↗</span></button></div>` : ''}${body}</div></main>
  </div>`;
};

function closeSpatialPanels(restoreFocus = false) {
  let trigger = null;
  for (const [panelId, buttonId] of [['broad-menu', 'menu-trigger'], ['theme-menu', 'theme-trigger']]) {
    const panel = $('#' + panelId), button = $('#' + buttonId);
    if (!panel || !button) continue;
    if (!panel.hidden) trigger = button;
    panel.hidden = true; panel.inert = true;
    button.setAttribute('aria-expanded', 'false');
  }
  if (restoreFocus && trigger) trigger.focus();
}
function openSpatialPanel(id) {
  const panel = $('#' + id), trigger = $('#' + (id === 'broad-menu' ? 'menu-trigger' : 'theme-trigger'));
  if (!panel || !trigger) return;
  const open = panel.hidden;
  closeSpatialPanels();
  if (open) {
    panel.hidden = false; panel.inert = false;
    trigger.setAttribute('aria-expanded', 'true');
  }
}
function setSpatialFocus(on) {
  closeSpatialPanels();
  spatialFocus = !!on;
  document.body.classList.toggle('focus-mode-active', spatialFocus);
  const header = $('.floating-header'), restore = $('#focus-exit');
  if (header) { header.hidden = spatialFocus; header.inert = spatialFocus; }
  if (restore) { restore.hidden = !spatialFocus; restore.inert = !spatialFocus; }
  (spatialFocus ? restore : $('#focus-trigger'))?.focus();
}
function applySpatialTheme(id) {
  if (!Object.hasOwn(themes, id)) return;
  const restoreFocus = $('#theme-menu') && !$('#theme-menu').hidden;
  state.theme = id;
  document.documentElement.dataset.theme = id;
  save();
  $$('[data-theme-choice]').forEach(button => {
    const chosen = button.dataset.themeChoice === id;
    button.classList.toggle('chosen', chosen);
    button.classList.toggle('active', chosen);
    button.setAttribute('aria-pressed', String(chosen));
    const check = button.querySelector('.theme-selected');
    if (check) check.textContent = chosen ? '✓' : '';
  });
  if ($('#theme')) $('#theme').value = id;
  closeSpatialPanels();
  if (restoreFocus) $('#theme-trigger')?.focus();
}
function bindSpatialNavigation() {
  if ($('#menu-trigger')) $('#menu-trigger').onclick = () => openSpatialPanel('broad-menu');
  if ($('#theme-trigger')) $('#theme-trigger').onclick = () => openSpatialPanel('theme-menu');
  if ($('#focus-trigger')) $('#focus-trigger').onclick = () => setSpatialFocus(true);
  if ($('#focus-exit')) $('#focus-exit').onclick = () => setSpatialFocus(false);
  $$('[data-theme-choice]').forEach(button => button.onclick = () => applySpatialTheme(button.dataset.themeChoice));
  if ($('#theme')) $('#theme').onchange = event => applySpatialTheme(event.target.value);
}

document.addEventListener('click', event => {
  if (!event.target.closest?.('.floating-header')) closeSpatialPanels();
});
document.addEventListener('keydown', event => {
  if (event.key !== 'Escape' || event.isComposing) return;
  const hasOpenPanel = ['#broad-menu', '#theme-menu'].some(id => $(id) && !$(id).hidden);
  if (hasOpenPanel) { event.preventDefault(); closeSpatialPanels(true); }
  else if (spatialFocus) { event.preventDefault(); setSpatialFocus(false); }
});

const renderBeforeSpatial = render;
render = function() {
  renderBeforeSpatial();
  document.body.classList.toggle('focus-mode-active', spatialFocus);
  bindSpatialNavigation();
};
render();
