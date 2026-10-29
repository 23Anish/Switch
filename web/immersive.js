/* Small, deterministic teaching traces. Playback starts only on an explicit click. */
const LEARNING_TRACES = window.LEARNING_TRACES || [];
const homeBfs = buildBfsTrace();
let homeFrame = 0, lessonFrame = 0, lessonTraceId = null;
let playback = null, playbackTimer = null, traceDelay = 1600;

function buildBfsTrace() {
  const queue = [1], visited = [];
  const frames = [{queue:[1], visited:[], current:null, text:'Begin with the root in the queue. A node is queued once, when discovered.', line:'seed'}];
  while (queue.length) {
    const node = queue.shift(); visited.push(node);
    const children = node < 4 ? [node * 2, node * 2 + 1] : [];
    queue.push(...children);
    frames.push({queue:[...queue], visited:[...visited], current:node, line:children.length?'push':'pop',
      text:children.length ? `Remove ${node} from the front. Append children ${children.join(' and ')} at the back. Earlier discoveries keep their place.` : `Remove leaf ${node}. It has no children.${queue.length?' Continue with the next queued node.':' The queue is empty; traversal is complete.'}`});
  }
  return frames;
}
function bfsGraphic(frame) {
  const xy = [[240,38],[135,115],[345,115],[75,200],[185,200],[295,200],[405,200]];
  return `<svg viewBox="0 0 480 250" role="img" aria-label="Binary-tree BFS trace; nodes 1 through 7"><g class="bfs-edges">${[2,3,4,5,6,7].map(n=>{const a=xy[Math.floor(n/2)-1],b=xy[n-1];return `<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}"/>`}).join('')}</g>${xy.map(([x,y],i)=>`<g data-home-node="${i+1}" class="bfs-node ${frame.queue.includes(i+1)?'queued':''} ${frame.visited.includes(i+1)?'visited':''} ${frame.current===i+1?'current':''}"><circle cx="${x}" cy="${y}" r="22"/><text x="${x}" y="${y+5}" text-anchor="middle">${i+1}</text></g>`).join('')}</svg>`;
}
function traceControls(kind, index, total) {
  return `<div class="trace-controls" data-player="${kind}"><button data-trace-action="reset" aria-label="Restart ${kind} trace">↺</button><button data-trace-action="previous" aria-label="Previous ${kind} step" ${index===0?'disabled':''}>←</button><button data-trace-action="play" class="trace-play" aria-label="Play ${kind} trace">▶ Play</button><button data-trace-action="next" aria-label="Next ${kind} step" ${index===total-1?'disabled':''}>Step →</button><span class="trace-counter">${index+1} / ${total}</span></div>`;
}
function queueChips(values) { return values.length?values.map(v=>`<span>${esc(v)}</span>`).join(''):'<small>empty</small>'; }
function learningHero(next, recentWork) {
  const f=homeBfs[homeFrame];
  return `<section class="learning-hero" aria-labelledby="landing-title"><div class="learning-canvas-main"><div class="learning-hero-heading"><div><p class="eyebrow">YOUR NEXT CHAPTER / SWITCH</p><h1 id="landing-title">Understand deeply.<br><em>Build what’s next.</em></h1></div><div class="learning-counts"><span><strong>${D.length}</strong> problems</span><span><strong>${L.length}</strong> lessons</span><span><strong>${PATTERNS.length}</strong> patterns</span></div></div><div class="learning-graph">${bfsGraphic(f)}<div class="graph-key"><span>○ Undiscovered</span><span>◉ Queued</span><span>● Visited</span></div>${traceControls('home',homeFrame,homeBfs.length)}</div><div class="hero-actions">${next?`<button class="primary" data-problem="${next.id}">${recentWork?'Continue your practice':'Start your first problem'} →</button>`:''}<button data-go="visual">Explore Pattern Lab ↗</button></div></div><div class="learning-canvas-side"><div class="trace-explanation"><p class="eyebrow">BREADTH-FIRST SEARCH / C++17</p><p id="home-trace-caption" aria-live="polite">${esc(f.text)}</p></div><div class="learning-code"><p class="code-caption">Non-null root in this example</p><pre><code><span data-bfs-line="seed" class="${f.line==='seed'?'current-line':''}">queue&lt;TreeNode*&gt; frontier;
frontier.push(root);</span>
while (!frontier.empty()) {
<span data-bfs-line="pop" class="${f.line==='pop'?'current-line':''}">  auto* node = frontier.front();
  frontier.pop();</span>
<span data-bfs-line="push" class="${f.line==='push'?'current-line':''}">  if (node-&gt;left)
    frontier.push(node-&gt;left);
  if (node-&gt;right)
    frontier.push(node-&gt;right);</span>
}</code></pre><div class="queue-state"><span class="eyebrow">QUEUE / FRONT → BACK</span><div class="queue-chips" id="home-queue">${queueChips(f.queue)}</div><small>Visit order: <span id="home-visited">${f.visited.join(' → ')||'none yet'}</span></small></div></div></div></section>`;
}
function stopPlayback() {
  clearTimeout(playbackTimer); playbackTimer=null; playback=null;
  $$('[data-trace-action="play"]').forEach(b=>{b.textContent='▶ Play';b.setAttribute('aria-label','Play '+b.closest('[data-player]').dataset.player+' trace')});
}
function playerBounds(kind) {
  if(kind==='home')return [homeFrame,homeBfs.length];
  if(kind==='pattern')return [labStep,PATTERNS.find(p=>p.id===labKey).steps.length];
  const t=LEARNING_TRACES.find(t=>t.lessonId===selected);return [lessonFrame,t?.steps.length||0];
}
function changeFrame(kind,index) {
  if(kind==='home'){homeFrame=index;paintHomeFrame()}
  else if(kind==='pattern'){labStep=index;paintPatternFrame()}
  else {lessonFrame=index;paintLessonFrame()}
  updatePlayer(kind);
}
function updatePlayer(kind) {
  const control=$(`[data-player="${kind}"]`);if(!control)return;
  const [i,n]=playerBounds(kind);
  control.querySelector('[data-trace-action="previous"]').disabled=i===0;
  control.querySelector('[data-trace-action="next"]').disabled=i===n-1;
  control.querySelector('.trace-counter').textContent=`${i+1} / ${n}`;
  const b=control.querySelector('[data-trace-action="play"]');
  b.textContent=playback===kind?'Ⅱ Pause':'▶ Play';
  b.setAttribute('aria-label',(playback===kind?'Pause ':'Play ')+kind+' trace');
}
function startPlayback(kind) {
  if(playback===kind){stopPlayback();return}
  stopPlayback();const [i,n]=playerBounds(kind);if(n<2)return;if(i===n-1)changeFrame(kind,0);
  playback=kind;updatePlayer(kind);
  const advance=()=>{
    if(playback!==kind)return;
    const [index,total]=playerBounds(kind);
    if(index>=total-1){stopPlayback();return}
    changeFrame(kind,index+1);
    if(index+1===total-1)stopPlayback();else playbackTimer=setTimeout(advance,traceDelay);
  };
  playbackTimer=setTimeout(advance,traceDelay);
}
function bindTraceControls() {
  $$('[data-trace-action]').forEach(b=>b.onclick=()=>{
    const kind=b.closest('[data-player]').dataset.player,action=b.dataset.traceAction;
    if(action==='play')return startPlayback(kind);
    stopPlayback();const [i,n]=playerBounds(kind);
    changeFrame(kind,action==='reset'?0:Math.max(0,Math.min(n-1,i+(action==='next'?1:-1))));
  });
}
function paintHomeFrame() {
  const f=homeBfs[homeFrame];
  $$('[data-home-node]').forEach(el=>{const n=Number(el.dataset.homeNode);el.classList.toggle('queued',f.queue.includes(n));el.classList.toggle('visited',f.visited.includes(n));el.classList.toggle('current',f.current===n)});
  $('#home-trace-caption').textContent=f.text;$('#home-queue').innerHTML=queueChips(f.queue);$('#home-visited').textContent=f.visited.join(' → ')||'none yet';
  $$('[data-bfs-line]').forEach(el=>el.classList.toggle('current-line',el.dataset.bfsLine===f.line));
}
function paintPatternFrame() {
  const l=PATTERNS.find(p=>p.id===labKey),s=l.steps[labStep],active=new Set(s.active),values=s.values||l.values;
  $$('.pattern-graph > g').forEach((el,i)=>el.classList.toggle('node-active',active.has(String(i))));
  $$('.pattern-cell').forEach((el,i)=>{el.classList.toggle('active',active.has(String(i)));el.querySelector('strong').textContent=values[i]});
  $('.pattern-stage>.eyebrow').textContent=`${l.category} / ${labStep+1} of ${l.steps.length}`;
  $('.trace-caption h3').textContent=s.label;$('.trace-caption p').textContent=s.detail;
  $('#lab-scrub').value=labStep;$('#lab-scrub').previousElementSibling.textContent=`Step ${labStep+1} of ${l.steps.length}`;
  $('.pattern-state').innerHTML=Object.entries(s.state).map(([key,value])=>`<div><dt>${esc(key)}</dt><dd>${esc(typeof value==='object'?JSON.stringify(value):value)}</dd></div>`).join('');
}
const labBeforeImmersive=visualLab,bindLabBeforeImmersive=bindLab;
visualLab=function(){
  const html=labBeforeImmersive(),l=PATTERNS.find(p=>p.id===labKey);
  return html.replace(/<div class="actions spaced"><button id="lab-prev"[\s\S]*?<\/div>/,traceControls('pattern',labStep,l.steps.length));
};
bindLab=function(){
  bindLabBeforeImmersive();
  if($('#lab-scrub'))$('#lab-scrub').oninput=e=>{stopPlayback();changeFrame('pattern',Number(e.target.value))};
};
function lessonTraceView(t) {
  if(lessonTraceId!==t.lessonId){lessonFrame=0;lessonTraceId=t.lessonId}
  const s=t.steps[lessonFrame];
  return `<section class="lesson-trace card" aria-label="Interactive worked trace"><p class="eyebrow">INTERACTIVE WORKED TRACE</p><h2>${esc(t.title)}</h2><p>${esc(t.intro)}</p><div class="lesson-trace-nodes">${t.nodes.map((n,i)=>`<button data-lesson-node="${i}" aria-pressed="${s.active.includes(i)}" class="${s.active.includes(i)?'is-active':''}">${esc(n)}</button>`).join('')}</div><p class="subtle">Select a component to inspect its role, or step through the example.</p><p class="component-detail" id="component-detail">${esc(t.roles[s.active[0]])}</p><div class="trace-caption" aria-live="polite"><h3>${esc(s.label)}</h3><p>${esc(s.detail)}</p></div><dl class="pattern-state">${Object.entries(s.state).map(([k,v])=>`<div><dt>${esc(k)}</dt><dd>${esc(typeof v==='object'?JSON.stringify(v):v)}</dd></div>`).join('')}</dl>${traceControls('lesson',lessonFrame,t.steps.length)}<p class="subtle spaced">${esc(t.limit)}</p></section>`;
}
function paintLessonFrame() {
  const t=LEARNING_TRACES.find(t=>t.lessonId===selected),s=t.steps[lessonFrame],root=$('.lesson-trace');
  root.querySelectorAll('[data-lesson-node]').forEach((el,i)=>{el.classList.toggle('is-active',s.active.includes(i));el.setAttribute('aria-pressed',String(s.active.includes(i)))});
  root.querySelector('.trace-caption h3').textContent=s.label;root.querySelector('.trace-caption p').textContent=s.detail;
  $('#component-detail').textContent=t.roles[s.active[0]];
  root.querySelector('.pattern-state').innerHTML=Object.entries(s.state).map(([k,v])=>`<div><dt>${esc(k)}</dt><dd>${esc(typeof v==='object'?JSON.stringify(v):v)}</dd></div>`).join('');
}
const lessonBeforeImmersive=lesson;
lesson=function(){
  const html=lessonBeforeImmersive(),t=LEARNING_TRACES.find(t=>t.lessonId===selected);
  if(!t)return html;
  const firstHeading='<h2>'+esc(L.find(l=>l.id===selected).sections[0].heading)+'</h2>';
  return html.replace(firstHeading,lessonTraceView(t)+firstHeading);
};
const problemBeforeImmersive=problem;
problem=function(){
  const html=problemBeforeImmersive(),p=D.find(p=>p.id===selected);if(!p)return html;
  const related=PATTERNS.filter(x=>x.problemId===p.id);
  return related.length?html.replace('<h3>Constraints</h3>',`<div class="related-pattern"><span class="eyebrow">SEE THE IDEA MOVE</span>${related.map(l=>`<button data-open-pattern="${l.id}">${esc(l.title)} ↗</button>`).join('')}</div><h3>Constraints</h3>`):html;
};
const renderBeforeImmersive=render;
render=function(){
  stopPlayback();renderBeforeImmersive();document.body.dataset.page=page;
  bindTraceControls();
  $$('[data-open-pattern]').forEach(b=>b.onclick=()=>{labKey=b.dataset.openPattern;labStep=0;patternQuery='';patternCategory='All patterns';go('visual')});
  $$('[data-lesson-node]').forEach(b=>b.onclick=()=>{
    stopPlayback();const t=LEARNING_TRACES.find(t=>t.lessonId===selected),i=Number(b.dataset.lessonNode);
    $('#component-detail').textContent=t.roles[i];
    $$('[data-lesson-node]').forEach(el=>{const active=el===b;el.classList.toggle('is-active',active);el.setAttribute('aria-pressed',String(active))});
  });
};
document.addEventListener('visibilitychange',()=>{if(document.hidden)stopPlayback()});
render();
