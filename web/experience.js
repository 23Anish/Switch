/* The study home and practice sheet share the existing curriculum and learner data. */
(() => {
  'use strict';

  const topicOrder = [...new Set(D.map(problem => problem.topic))];
  const problemOrder = new Map(D.map((problem, index) => [problem.id, index]));
  const stageNames = ['', 'Foundations', 'Patterns', 'Composition', 'Interview stretch'];
  const difficultyOrder = { Easy: 0, Medium: 1, Hard: 2 };
  const topicOpen = new Map();
  let accordionProfile = state.active;
  const previousBindExtra = bindExtra;

  const topicDescriptions = {
    'Arrays & fundamentals': 'Build the habit of scanning, counting, and stating invariants.',
    'Hashing & prefix sums': 'Trade repeated work for fast lookups and reusable prefix information.',
    'Sorting & divide-and-conquer': 'Split a problem, order its data, and combine what you learn.',
    'Two pointers & sliding windows': 'Maintain useful boundaries instead of restarting every search.',
    'Binary search': 'Find the boundary in sorted data or a monotonic answer space.',
    'Linked lists': 'Reason about pointers, ownership, and transformations one link at a time.',
    'Stacks & queues': 'Recognize order, monotonicity, and amortized work.',
    'Recursion & backtracking': 'Define state, explore choices, and restore the path.',
    'Binary trees': 'Choose traversal order and make the recursive contract explicit.',
    'BSTs, heaps & ordered data': 'Maintain useful order for search, selection, and streaming data.',
    'Graph traversal': 'Model relationships, discover components, and explore frontiers.',
    'Shortest paths & disjoint sets': 'Check path assumptions and connect components efficiently.',
    'Dynamic programming foundations': 'Derive states and transitions from overlapping subproblems.',
    'Sequence & string dynamic programming': 'Compare prefixes, subsequences, and interval choices.',
    'Greedy algorithms & intervals': 'Prove why each local choice leaves an optimal answer possible.',
    'Bits, tries & advanced patterns': 'Use compact state and specialized structures when the pattern fits.'
  };

  function favorites() {
    const saved = profile().favorites;
    return saved && typeof saved === 'object' && !Array.isArray(saved) ? saved : {};
  }

  function hasDraft(problem) {
    const code = profile().code || {};
    return Object.keys(code).some(key => key.startsWith(problem.id + ':') && typeof code[key] === 'string' && code[key].trim());
  }

  function isDue(problem) {
    const due = profile().reviews?.[problem.id];
    return typeof due === 'number' && due <= Date.now();
  }

  function nextSessionProblem() {
    const learner = profile();
    const recent = D.find(problem => problem.id === learner.lastProblem && !learner.done[problem.id]);
    return recent || D.find(problem => !learner.done[problem.id] && hasDraft(problem)) || D.find(problem => !learner.done[problem.id]) || D[0];
  }

  function progressMeter(done, total, label, className = 'progress') {
    const percent = total ? Math.min(100, Math.round(done / total * 100)) : 0;
    return `<div class="${className}" role="progressbar" aria-label="${esc(label)}" aria-valuemin="0" aria-valuemax="${total || 1}" aria-valuenow="${done}"><i style="width:${percent}%"></i></div>`;
  }

  function lessonTrackStats(match) {
    const lessons = L.filter(match);
    return { done: lessons.filter(lesson => profile().read[lesson.id]).length, total: lessons.length };
  }

  function learningCard({ page: destination, icon, title, description, done, total, unit }) {
    return `<button class="track-tile learning-card" data-go="${destination}">
      <span class="track-icon" aria-hidden="true">${icon}</span>
      <span class="track-meta">${total} ${unit}</span>
      <h3>${esc(title)}</h3>
      <p>${esc(description)}</p>
      <div class="track-bottom"><span>${done} / ${total} complete</span><span aria-hidden="true">↗</span></div>
      ${progressMeter(done, total, title + ' progress')}
    </button>`;
  }

  function sessionProblemRow(problem, index, label) {
    return `<button class="session-row" data-problem="${problem.id}">
      <span class="session-number" aria-hidden="true">${String(index + 1).padStart(2, '0')}</span>
      <span class="session-copy"><strong>${esc(problem.title)}</strong><small>${esc(label || problem.topic)}</small></span>
      <span class="pill ${problem.difficulty}">${problem.difficulty}</span><span class="session-arrow" aria-hidden="true">↗</span>
    </button>`;
  }

  dashboard = function dashboardExperience() {
    const learner = profile();
    const completed = solved(), completedLessons = read();
    const reviews = D.filter(isDue);
    const next = nextSessionProblem();
    const recentWork = D.some(problem => hasDraft(problem)) || completed > 0;
    const core = lessonTrackStats(lesson => !isAI(lesson) && !['LLD', 'HLD'].includes(lesson.track));
    const lld = lessonTrackStats(lesson => lesson.track === 'LLD');
    const hld = lessonTrackStats(lesson => lesson.track === 'HLD');
    const ai = lessonTrackStats(isAI);
    const checklist = COMPANIES.flatMap(company => company.checklist.map((_, index) => company.id + ':' + index));
    const companyDone = checklist.filter(key => learner.companyChecks?.[key]).length;
    const tracks = [
      { page: 'dsa', icon: '⌘', title: 'Algorithms & data structures', description: 'A topic-by-topic progression from first principles to interview stretch problems.', done: completed, total: D.length, unit: 'problems' },
      { page: 'core', icon: '▤', title: 'Computer science', description: 'Understand operating systems, networks, databases, and the machinery underneath.', ...core, unit: 'lessons' },
      { page: 'lld', icon: '◇', title: 'Low-level design', description: 'Turn requirements into clear objects, contracts, and maintainable interactions.', ...lld, unit: 'lessons' },
      { page: 'hld', icon: '▦', title: 'High-level design', description: 'Reason about capacity, data flow, reliability, and the trade-offs of scale.', ...hld, unit: 'lessons' },
      { page: 'ai', icon: '✧', title: 'AI engineering', description: 'Connect model theory to retrieval, agents, MCP, evaluation, and production systems.', ...ai, unit: 'lessons' },
      { page: 'companies', icon: '◎', title: 'Company preparation', description: 'Focused Google and Microsoft tracks, interview drills, and readiness checklists.', done: companyDone, total: checklist.length, unit: 'checklist items' }
    ];
    const practice = [next, ...D.filter(problem => !learner.done[problem.id] && problem.id !== next?.id)].filter(Boolean).slice(0, 3);
    const recommendedLessons = [
      L.find(lesson => !learner.read[lesson.id] && !isAI(lesson) && !['LLD', 'HLD'].includes(lesson.track)),
      L.find(lesson => !learner.read[lesson.id] && ['LLD', 'HLD'].includes(lesson.track)),
      L.find(lesson => !learner.read[lesson.id] && isAI(lesson))
    ].filter(Boolean);

    return `<div class="experience-home">
      <section class="landing-hero" aria-labelledby="landing-title">
        <div class="landing-copy">
          <p class="hero-kicker"><span aria-hidden="true">↗</span> YOUR NEXT CHAPTER STARTS HERE</p>
          <h1 class="landing-title" id="landing-title">Build depth.<br><em>Make the switch.</em></h1>
          <p class="landing-description">One thoughtful workspace for algorithms, systems, and modern AI. Learn the idea, write the code, and build the confidence to explain it.</p>
          <div class="hero-actions">
            ${next ? `<button class="primary" data-problem="${next.id}">${recentWork ? 'Continue your practice' : 'Start your first problem'} <span aria-hidden="true">→</span></button>` : ''}
            <button data-go="plan">Explore the roadmap <span aria-hidden="true">↗</span></button>
          </div>
          <div class="hero-facts hero-metrics"><span><strong>${D.length}</strong> curated problems</span><span><strong>${L.length}</strong> study lessons</span><span><strong>C++ · Python</strong> reference code</span></div>
        </div>
        <div class="landing-route landing-visual" aria-label="A repeatable learning loop">
          <div class="route-header"><span class="eyebrow">A LITTLE BETTER, EVERY SESSION</span><span aria-hidden="true">↗</span></div>
          <button class="route-node" data-go="core"><span class="route-index">01</span><span><strong>Understand the idea</strong><small>First principles, diagrams, and examples</small></span><span aria-hidden="true">↗</span></button>
          <div class="route-connector" aria-hidden="true"></div>
          <button class="route-node route-current" data-go="dsa"><span class="route-index">02</span><span><strong>Put it into practice</strong><small>Code, test, and compare approaches</small></span><span aria-hidden="true">↗</span></button>
          <div class="route-connector" aria-hidden="true"></div>
          <button class="route-node" data-go="visual"><span class="route-index">03</span><span><strong>Explain why it works</strong><small>Trace the pattern and its trade-offs</small></span><span aria-hidden="true">↗</span></button>
          <div class="route-connector" aria-hidden="true"></div>
          <button class="route-node" data-go="review"><span class="route-index">04</span><span><strong>Make it stick</strong><small>${reviews.length ? `${reviews.length} problem${reviews.length === 1 ? '' : 's'} ready for recall` : 'Return to what you learned, over time'}</small></span><span aria-hidden="true">↗</span></button>
          <p class="route-caption">Progress comes from the loop, not the streak.</p>
        </div>
      </section>

      <section class="home-stats" aria-label="Your saved progress">
        <button class="home-stat" data-go="dsa"><span>Problems solved</span><strong>${completed}<small> / ${D.length}</small></strong>${progressMeter(completed, D.length, 'Problems completed')}</button>
        <button class="home-stat" data-go="core"><span>Lessons completed</span><strong>${completedLessons}<small> / ${L.length}</small></strong>${progressMeter(completedLessons, L.length, 'Lessons completed')}</button>
        <button class="home-stat" data-go="review"><span>Ready for review</span><strong>${reviews.length}<small> problems</small></strong><small>${reviews.length ? 'A quick recall session keeps ideas fresh.' : 'Complete a problem to start your revision queue.'}</small></button>
        <div class="home-stat"><span>Days you showed up</span><strong>${Object.keys(learner.days || {}).length}<small> study days</small></strong><small>Saved for ${esc(state.active)} on this device.</small></div>
      </section>

      <section class="home-section" aria-labelledby="tracks-heading">
        <div class="home-section-heading section-heading"><div><p class="eyebrow">THE WHOLE INTERVIEW, CONNECTED</p><h2 id="tracks-heading">Choose your next focus.</h2></div><button class="linkbutton" data-go="plan">See the 12-week plan <span aria-hidden="true">→</span></button></div>
        <div class="track-catalog learning-grid">${tracks.map(learningCard).join('')}</div>
      </section>

      <section class="home-session-grid" aria-label="A focused study session">
        <div class="session-card">
          <div class="home-section-heading section-heading"><div><p class="eyebrow">YOUR NEXT PRACTICE</p><h2>Start with one good problem.</h2></div><button class="linkbutton" data-go="dsa">Problem set <span aria-hidden="true">→</span></button></div>
          <div class="session-list">${practice.map((problem, index) => sessionProblemRow(problem, index, index === 0 && hasDraft(problem) ? 'Saved code · pick up where you left off' : '')).join('')}</div>
          <p class="session-footnote">Try a baseline first. Then ask what work you can avoid.</p>
        </div>
        <div class="session-card">
          <div class="home-section-heading section-heading"><div><p class="eyebrow">CONNECT THE DOTS</p><h2>Go beyond the coding round.</h2></div></div>
          <div class="session-list">${recommendedLessons.length ? recommendedLessons.map((lesson, index) => `<button class="session-row" data-lesson="${lesson.id}"><span class="session-number" aria-hidden="true">${String(index + 1).padStart(2, '0')}</span><span class="session-copy"><strong>${esc(lesson.title)}</strong><small>${esc(lesson.track)} · ${lesson.minutes} min</small></span><span class="session-arrow" aria-hidden="true">↗</span></button>`).join('') : `<div class="empty"><h3>You have covered every lesson.</h3><p>Revisit your notes and use the company drills to practice explaining the trade-offs.</p><button data-go="companies">Open interview drills</button></div>`}</div>
          <p class="session-footnote">Read for understanding. Close the notes and explain it aloud.</p>
        </div>
      </section>

      <section class="company-strip" aria-label="Company preparation"><div><p class="eyebrow">PREPARE WITH A DESTINATION</p><h2>Aim high. Build the foundations.</h2></div><div class="company-strip-names"><button class="linkbutton" data-go="companies">Google <span aria-hidden="true">↗</span></button><button class="linkbutton" data-go="companies">Microsoft <span aria-hidden="true">↗</span></button><span>Meta</span><span>NVIDIA</span></div><p>Focused tracks for Google and Microsoft, plus broad software and systems preparation. No claimed company question frequency.</p></section>
      <div class="workspace-note"><span aria-hidden="true">◌</span><p>Your notes, code, and progress stay in this browser or Mac app. Keep a backup to move between devices.</p><button class="linkbutton" data-go="settings">Back up your progress <span aria-hidden="true">↗</span></button></div>
    </div>`;
  };

  function matchingProblems() {
    const query = filter.query.trim().toLowerCase();
    const saved = favorites();
    const list = D.filter(problem => {
      if (query && !(problem.title + ' ' + problem.topic + ' ' + problem.id + ' ' + stageNames[problem.stage]).toLowerCase().includes(query)) return false;
      if (filter.topic !== 'All topics' && problem.topic !== filter.topic) return false;
      if (filter.difficulty !== 'All levels' && problem.difficulty !== filter.difficulty) return false;
      if (filter.status === 'Solved' && !profile().done[problem.id]) return false;
      if (filter.status === 'Unsolved' && profile().done[problem.id]) return false;
      if (filter.status === 'In progress' && (profile().done[problem.id] || !hasDraft(problem))) return false;
      if (filter.status === 'Bookmarked' && !saved[problem.id]) return false;
      if (filter.status === 'Needs review' && !isDue(problem)) return false;
      return true;
    });
    const sort = state.problemsetSort || 'progression';
    return list.sort((a, b) => {
      if (sort === 'title') return a.title.localeCompare(b.title) || problemOrder.get(a.id) - problemOrder.get(b.id);
      if (sort === 'difficulty') return difficultyOrder[a.difficulty] - difficultyOrder[b.difficulty] || problemOrder.get(a.id) - problemOrder.get(b.id);
      return problemOrder.get(a.id) - problemOrder.get(b.id);
    });
  }

  function problemRows(list, showTopic) {
    const saved = favorites();
    return list.map(problem => {
      const done = !!profile().done[problem.id], bookmarked = !!saved[problem.id];
      return `<tr class="${done ? 'problem-complete' : ''}">
        <td class="problem-done"><input type="checkbox" class="check" data-done="${problem.id}" aria-label="Mark ${esc(problem.title)} complete" ${done ? 'checked' : ''}></td>
        <td class="problem-name-cell"><span class="problem-number">${String(problemOrder.get(problem.id) + 1).padStart(3, '0')}</span><span class="problem-title-block"><button class="linkbutton rowtitle" data-problem="${problem.id}">${esc(problem.title)}</button>${showTopic ? `<small>${esc(problem.topic)}</small>` : ''}${!done && hasDraft(problem) ? '<span class="draft-label">Saved draft</span>' : ''}</span></td>
        <td><span class="pill ${problem.difficulty}">${problem.difficulty}</span></td>
        <td class="problem-stage"><span class="stage-dot stage-${problem.stage}" aria-hidden="true"></span>${esc(stageNames[problem.stage] || 'Practice')}</td>
        <td class="problem-save"><button class="bookmark-button ${bookmarked ? 'is-saved' : ''}" data-favorite="${problem.id}" aria-label="${bookmarked ? 'Remove bookmark for' : 'Bookmark'} ${esc(problem.title)}" aria-pressed="${bookmarked}" title="${bookmarked ? 'Remove bookmark' : 'Bookmark for later'}">${bookmarked ? '★' : '☆'}</button></td>
      </tr>`;
    }).join('');
  }

  function problemTable(list, showTopic = false, caption = 'Practice problems') {
    return `<div class="problem-table-wrap"><table class="problem-table practice-table"><caption class="sr-only">${esc(caption)}</caption><thead><tr><th scope="col" class="problem-done"><span class="sr-only">Completed</span><span aria-hidden="true">✓</span></th><th scope="col">Problem</th><th scope="col">Difficulty</th><th scope="col" class="problem-stage">Progression</th><th scope="col" class="problem-save"><span class="sr-only">Bookmark</span><span aria-hidden="true">☆</span></th></tr></thead><tbody>${problemRows(list, showTopic)}</tbody></table></div>`;
  }

  function hasFilters() {
    return filter.query.trim() || filter.topic !== 'All topics' || filter.difficulty !== 'All levels' || filter.status !== 'All progress';
  }

  function resultsMarkup() {
    const list = matchingProblems();
    const fullTopic = new Map(topicOrder.map(topic => [topic, D.filter(problem => problem.topic === topic)]));
    const visibleTopics = topicOrder.filter(topic => list.some(problem => problem.topic === topic));
    const mode = state.problemsetView === 'list' ? 'list' : 'sheet';
    const difficultyCounts = ['Easy', 'Medium', 'Hard'].map(level => `<span class="result-level"><i class="difficulty-dot ${level}" aria-hidden="true"></i>${list.filter(problem => problem.difficulty === level).length} ${level.toLowerCase()}</span>`).join('');
    const summary = `<div class="problemset-summary"><div aria-live="polite"><strong>${list.length}</strong> ${list.length === 1 ? 'problem' : 'problems'}${hasFilters() ? ` match your filters` : ` across ${topicOrder.length} topics`}<span class="result-difficulties">${difficultyCounts}</span></div><div class="sheet-actions">${hasFilters() ? '<button class="linkbutton" data-clear-filters>Clear filters</button>' : ''}${mode === 'sheet' && list.length ? '<button class="linkbutton" data-expand-topics>Expand all</button><span aria-hidden="true">/</span><button class="linkbutton" data-collapse-topics>Collapse all</button>' : ''}</div></div>`;
    if (!list.length) return summary + `<div class="problemset-empty empty"><span aria-hidden="true">⌕</span><h2>No problems match this view.</h2><p>Try a different keyword, topic, or difficulty. Your saved progress is unchanged.</p><button data-clear-filters>Reset filters</button></div>`;
    if (mode === 'list') return summary + problemTable(list, true, 'All matching interview practice problems');
    const firstIncomplete = visibleTopics.find(topic => fullTopic.get(topic).some(problem => !profile().done[problem.id])) || visibleTopics[0];
    return summary + `<div class="topic-sheet topic-accordion">${visibleTopics.map(topic => {
      const all = fullTopic.get(topic), matches = list.filter(problem => problem.topic === topic);
      const done = all.filter(problem => profile().done[problem.id]).length;
      const open = topicOpen.has(topic) ? topicOpen.get(topic) : hasFilters() || topic === firstIncomplete;
      return `<details class="topic-section" data-topic-section="${esc(topic)}" ${open ? 'open' : ''}>
        <summary class="topic-summary"><span class="topic-number">${String(topicOrder.indexOf(topic) + 1).padStart(2, '0')}</span><span class="topic-description topic-label"><strong>${esc(topic)}</strong><small>${esc(topicDescriptions[topic] || 'Build the pattern, then practice the variations.')}</small></span><span class="topic-count"><strong>${done}<span> / ${all.length}</span></strong><small>${matches.length !== all.length ? matches.length + ' shown' : 'completed'}</small></span>${progressMeter(done, all.length, topic + ' completion', 'topic-meter topic-progress')}<span class="topic-chevron" aria-hidden="true">⌄</span></summary>
        <div class="topic-body">${problemTable(matches, false, topic + ' practice problems')}</div>
      </details>`;
    }).join('')}</div>`;
  }

  dsa = function dsaExperience() {
    if (accordionProfile !== state.active) {
      topicOpen.clear();
      accordionProfile = state.active;
    }
    const mode = state.problemsetView === 'list' ? 'list' : 'sheet';
    const completed = solved();
    const options = (items, value) => items.map(item => `<option value="${esc(item)}" ${item === value ? 'selected' : ''}>${esc(item)}</option>`).join('');
    return `<section class="problemset-header problemset-head"><div><p class="eyebrow">THE SWITCH PRACTICE SHEET</p><h1>A pattern for every problem.</h1><p>Build a foundation, connect the patterns, then take on the stretch problems. Use the sheet to learn in order or the list for a mixed session.</p></div><div class="problemset-overview"><strong>${completed}<span> / ${D.length}</span></strong><small>problems completed</small>${progressMeter(completed, D.length, 'Overall DSA progress')}<button class="linkbutton" data-go="review">${D.filter(isDue).length} ready for review <span aria-hidden="true">→</span></button></div></section>
      <div class="problemset-toolbar">
        <label class="problem-search"><span class="sr-only">Search problems</span><span aria-hidden="true">⌕</span><input id="search" aria-label="Search problems" placeholder="Search a problem, topic, or pattern…" value="${esc(filter.query)}" autocomplete="off"></label>
        <div class="problemset-filter-row">
          <label><span>Topic</span><select id="topic" aria-label="Topic">${options(['All topics', ...topicOrder], filter.topic)}</select></label>
          <label><span>Difficulty</span><select id="difficulty" aria-label="Difficulty">${options(['All levels', 'Easy', 'Medium', 'Hard'], filter.difficulty)}</select></label>
          <label><span>Progress</span><select id="status" aria-label="Progress">${options(['All progress', 'Unsolved', 'In progress', 'Solved', 'Bookmarked', 'Needs review'], filter.status)}</select></label>
          <label><span>Sort by</span><select id="problem-sort" aria-label="Sort problems">${[['progression', 'Recommended order'], ['difficulty', 'Difficulty: easy first'], ['title', 'Title: A–Z']].map(([id, name]) => `<option value="${id}" ${(state.problemsetSort || 'progression') === id ? 'selected' : ''}>${name}</option>`).join('')}</select></label>
          <div class="view-toggle" role="group" aria-label="Problem view"><button data-problem-view="sheet" class="${mode === 'sheet' ? 'active' : ''}" aria-pressed="${mode === 'sheet'}"><span aria-hidden="true">▤</span> Topic sheet</button><button data-problem-view="list" class="${mode === 'list' ? 'active' : ''}" aria-pressed="${mode === 'list'}"><span aria-hidden="true">☷</span> All problems</button></div>
        </div>
      </div>
      <div id="problem-list">${resultsMarkup()}</div>
      <p class="problemset-footnote">The sequence is a study guide, not a company question list. Every problem includes C++ and Python reference code, approach comparisons, and practice tests.</p>`;
  };

  // The existing app also calls problemList when updating its search field.
  problemList = resultsMarkup;

  function rememberProblem(button) {
    button.onclick = () => {
      profile().lastProblem = button.dataset.problem;
      save();
      go('problem', button.dataset.problem);
    };
  }

  function resetFilters() {
    filter = { query: '', topic: 'All topics', difficulty: 'All levels', status: 'All progress' };
    topicOpen.clear();
    render();
    $('#search')?.focus();
  }

  function updateResults() {
    const list = $('#problem-list');
    if (!list) return;
    list.innerHTML = resultsMarkup();
    bindProblemResults();
    const count = $('.problemset-overview');
    if (count) {
      const completed = solved();
      count.innerHTML = `<strong>${completed}<span> / ${D.length}</span></strong><small>problems completed</small>${progressMeter(completed, D.length, 'Overall DSA progress')}<button class="linkbutton" data-go="review">${D.filter(isDue).length} ready for review <span aria-hidden="true">→</span></button>`;
      count.querySelector('[data-go]').onclick = () => go('review');
    }
  }

  function bindProblemResults() {
    const container = $('#problem-list');
    if (!container) return;
    container.querySelectorAll('[data-problem]').forEach(rememberProblem);
    container.querySelectorAll('[data-done]').forEach(checkbox => {
      checkbox.onchange = () => {
        const id = checkbox.dataset.done;
        profile().done[id] = checkbox.checked;
        if (checkbox.checked) {
          profile().reviews[id] = Date.now() + 86400000;
          touch();
        } else delete profile().reviews[id];
        save();
        const focusId = checkbox.dataset.done;
        updateResults();
        const replacement = [...container.querySelectorAll('[data-done]')].find(item => item.dataset.done === focusId);
        replacement?.focus({ preventScroll: true });
      };
    });
    container.querySelectorAll('[data-favorite]').forEach(button => {
      button.onclick = () => {
        const saved = favorites();
        profile().favorites = saved;
        const id = button.dataset.favorite;
        if (saved[id]) delete saved[id];
        else saved[id] = true;
        save();
        updateResults();
        const replacement = [...container.querySelectorAll('[data-favorite]')].find(item => item.dataset.favorite === id);
        replacement?.focus({ preventScroll: true });
      };
    });
    container.querySelectorAll('[data-topic-section]').forEach(details => {
      details.ontoggle = () => topicOpen.set(details.dataset.topicSection, details.open);
    });
    container.querySelectorAll('[data-clear-filters]').forEach(button => button.onclick = resetFilters);
    const toggleTopics = open => {
      container.querySelectorAll('[data-topic-section]').forEach(details => {
        topicOpen.set(details.dataset.topicSection, open);
        details.open = open;
      });
    };
    container.querySelector('[data-expand-topics]')?.addEventListener('click', () => toggleTopics(true));
    container.querySelector('[data-collapse-topics]')?.addEventListener('click', () => toggleTopics(false));
  }

  bindExtra = function bindExperience() {
    previousBindExtra();
    $$('[data-problem]').forEach(rememberProblem);
    if (page !== 'dsa') return;
    $('#search').oninput = event => {
      filter.query = event.target.value;
      topicOpen.clear();
      updateResults();
    };
    for (const id of ['topic', 'difficulty', 'status']) {
      $('#' + id).onchange = event => {
        filter[id] = event.target.value;
        topicOpen.clear();
        updateResults();
      };
    }
    $('#problem-sort').onchange = event => {
      state.problemsetSort = event.target.value;
      save();
      updateResults();
    };
    $$('[data-problem-view]').forEach(button => {
      button.onclick = () => {
        state.problemsetView = button.dataset.problemView;
        save();
        render();
        $(`[data-problem-view="${state.problemsetView}"]`)?.focus({ preventScroll: true });
      };
    });
    bindProblemResults();
  };

  render();
})();
