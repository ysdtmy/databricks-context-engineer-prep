/**
 * Databricks Certified Context Engineer Associate
 * Interactive Exam Prep & Study Engine (app.js)
 */

(function () {
  'use strict';

  // --- State ---
  const STORAGE_KEY = 'dbx_context_engineer_exam_state_v2';
  let state = {
    answers: {}, // { [qId]: { selectedKey: 'A', isCorrect: true } }
    starred: {}, // { [qId]: true }
    activeTab: 'quiz',
    activeFilter: 'all',
    activeDomain: 'all',
    searchQuery: '',
    drillIdx: 0,
    drillStreak: 0,
    drillAnswered: false
  };

  // Load state from localStorage
  function loadState() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        state.answers = parsed.answers || {};
        state.starred = parsed.starred || {};
      }
    } catch (e) {
      console.warn('Could not load state from localStorage', e);
    }
  }

  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        answers: state.answers,
        starred: state.starred
      }));
    } catch (e) {
      console.warn('Could not save state to localStorage', e);
    }
  }

  // --- Question Helpers ---
  function getAllQuestions() {
    if (!window.EXAM_DATA) return [];
    const mocks = window.EXAM_DATA.mockQuestions || [];
    const practice = window.EXAM_DATA.practiceQuestions || [];
    return [...mocks, ...practice];
  }

  // --- Jump to Specific Guide Section from Quiz Question ---
  window.jumpToDomainGuide = function (domainText) {
    let targetId = 'ch-overview';
    const s = (domainText || '').toLowerCase();
    if (s.includes('domain 1') || s.includes('foundation') || s.includes('基礎') || s.includes('障害')) {
      targetId = 'ch-domain1';
    } else if (s.includes('domain 2') || s.includes('prompt') || s.includes('genie')) {
      targetId = 'ch-domain2';
    } else if (s.includes('domain 3') || s.includes('retrieval') || s.includes('search') || s.includes('検索')) {
      targetId = 'ch-domain3';
    } else if (s.includes('domain 4') || s.includes('memory') || s.includes('lakebase') || s.includes('メモリ')) {
      targetId = 'ch-domain4';
    } else if (s.includes('domain 5') || s.includes('tool') || s.includes('mcp') || s.includes('ツール')) {
      targetId = 'ch-domain5';
    } else if (s.includes('domain 6') || s.includes('compact') || s.includes('compress') || s.includes('圧縮')) {
      targetId = 'ch-domain6';
    } else if (s.includes('domain 7') || s.includes('multi-agent') || s.includes('horizon') || s.includes('マルチ')) {
      targetId = 'ch-domain7';
    }

    window.switchTab('guide');
    setTimeout(() => {
      const el = document.getElementById(targetId);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        el.classList.add('chapter-highlight');
        setTimeout(() => el.classList.remove('chapter-highlight'), 2500);

        // Update TOC active state
        document.querySelectorAll('.guide-sidebar .nav-link').forEach(a => a.classList.remove('active'));
        const activeLink = document.querySelector(`.guide-sidebar a[href="#${targetId}"]`);
        if (activeLink) activeLink.classList.add('active');
      }
    }, 150);
  };

  // --- Navigation Tabs ---
  window.switchTab = function (tabName) {
    state.activeTab = tabName;
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));

    const tabBtn = document.getElementById(`tabBtn_${tabName}`);
    const panel = document.getElementById(`panel_${tabName}`);

    if (tabBtn) tabBtn.classList.add('active');
    if (panel) panel.classList.add('active');

    if (tabName === 'quiz') {
      renderQuiz();
    } else if (tabName === 'guide') {
      renderGuide();
    } else if (tabName === 'cheatsheet') {
      renderCheatsheets();
    } else if (tabName === 'drill') {
      renderDrill();
    }
  };

  // --- Search & Filters ---
  window.onSearchInput = function (val) {
    state.searchQuery = (val || '').trim().toLowerCase();
    if (state.activeTab === 'quiz') {
      renderQuiz();
    }
  };

  window.setFilter = function (filterName, btn) {
    state.activeFilter = filterName;
    document.querySelectorAll('.quiz-filters .filter-btn').forEach(b => {
      if (b.tagName === 'BUTTON' && !b.classList.contains('reset-btn')) {
        b.classList.remove('active');
      }
    });
    if (btn) btn.classList.add('active');
    renderQuiz();
  };

  window.onDomainSelect = function (val) {
    state.activeDomain = val;
    renderQuiz();
  };

  window.confirmResetProgress = function () {
    if (confirm('回答進捗とお気に入り(★)の記録をすべて初期化しますか？')) {
      state.answers = {};
      state.starred = {};
      saveState();
      updateDashboardStats();
      renderQuiz();
    }
  };

  // --- Update Dashboard Stats ---
  function updateDashboardStats() {
    const all = getAllQuestions();
    const total = all.length;
    let answered = 0;
    let correct = 0;
    let starred = 0;

    all.forEach(q => {
      if (state.answers[q.id]) {
        answered++;
        if (state.answers[q.id].isCorrect) correct++;
      }
      if (state.starred[q.id]) {
        starred++;
      }
    });

    const accuracy = answered > 0 ? Math.round((correct / answered) * 100) : 0;
    const progressPct = total > 0 ? Math.round((answered / total) * 100) : 0;

    const elAns = document.getElementById('statAnswered');
    const elAcc = document.getElementById('statAccuracy');
    const elCor = document.getElementById('statCorrect');
    const elStar = document.getElementById('statStarred');
    const elFill = document.getElementById('progressBarFill');
    const elProg = document.getElementById('statProgressPercent');
    const elBadge = document.getElementById('quizCountBadge');

    if (elAns) elAns.textContent = `${answered} / ${total}`;
    if (elAcc) elAcc.textContent = `${accuracy}%`;
    if (elCor) elCor.textContent = correct;
    if (elStar) elStar.textContent = starred;
    if (elFill) elFill.style.width = `${progressPct}%`;
    if (elProg) elProg.textContent = `${progressPct}% (${answered}/${total}問)`;
    if (elBadge) elBadge.textContent = `${total}問`;
  }

  // --- Bookmark Toggle ---
  window.toggleBookmark = function (qId, btn) {
    if (state.starred[qId]) {
      delete state.starred[qId];
      if (btn) btn.classList.remove('active');
    } else {
      state.starred[qId] = true;
      if (btn) btn.classList.add('active');
    }
    saveState();
    updateDashboardStats();
    if (state.activeFilter === 'starred') {
      renderQuiz();
    }
  };

  // --- Answer Click Handler ---
  window.selectOption = function (qId, optionKey) {
    const all = getAllQuestions();
    const q = all.find(item => item.id === qId);
    if (!q) return;

    const isCorrect = (optionKey === q.correct);
    state.answers[qId] = {
      selectedKey: optionKey,
      isCorrect: isCorrect,
      timestamp: Date.now()
    };
    saveState();
    updateDashboardStats();

    const card = document.getElementById(`card-${qId}`);
    if (card) {
      updateCardDOM(card, q, optionKey, isCorrect);
    }
  };

  // --- Card Explanation Toggle ---
  window.toggleExplanation = function (qId) {
    const expPanel = document.getElementById(`exp-${qId}`);
    const btn = document.getElementById(`toggle-btn-${qId}`);
    if (expPanel) {
      if (expPanel.classList.contains('show')) {
        expPanel.classList.remove('show');
        if (btn) btn.innerHTML = '<span>解説を表示 ▼</span>';
      } else {
        expPanel.classList.add('show');
        if (btn) btn.innerHTML = '<span>解説を隠す ▲</span>';
      }
    }
  };

  // --- Code Copy ---
  window.copyCode = function (btn) {
    const pre = btn.closest('.code-block').querySelector('pre');
    if (!pre) return;
    const text = pre.innerText;
    navigator.clipboard.writeText(text).then(() => {
      const orig = btn.textContent;
      btn.textContent = 'コピー完了！';
      btn.style.borderColor = 'var(--success)';
      btn.style.color = 'var(--success)';
      setTimeout(() => {
        btn.textContent = orig;
        btn.style.borderColor = '';
        btn.style.color = '';
      }, 1500);
    });
  };

  // --- Render Quiz Questions ---
  function renderQuiz() {
    const container = document.getElementById('questionsContainer');
    if (!container) return;

    const all = getAllQuestions();
    const query = state.searchQuery;
    const filter = state.activeFilter;
    const domainFilter = state.activeDomain;

    const filtered = all.filter(q => {
      // 1. Tab filter
      if (filter === 'mock' && q.type !== 'mock') return false;
      if (filter === 'practice' && q.type !== 'practice') return false;
      if (filter === 'starred' && !state.starred[q.id]) return false;
      if (filter === 'incorrect') {
        const ans = state.answers[q.id];
        if (!ans || ans.isCorrect) return false;
      }

      // 2. Domain dropdown filter
      if (domainFilter !== 'all') {
        const cat = (q.domain || q.category || '').toLowerCase();
        if (!cat.includes(domainFilter.toLowerCase())) return false;
      }

      // 3. Search query
      if (query) {
        const targetText = [
          q.id,
          q.title || '',
          q.question || '',
          q.code || '',
          q.explanation || '',
          ...(q.rules || []),
          ...(q.options || []).map(o => o.text + ' ' + (o.verdict || ''))
        ].join(' ').toLowerCase();

        if (!targetText.includes(query)) return false;
      }

      return true;
    });

    if (filtered.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 4rem 1rem; color: var(--text-muted);">
          <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
          <h3 style="color: var(--text-main); margin-bottom: 0.5rem;">該当する問題が見つかりませんでした</h3>
          <p>検索キーワードやドメインフィルターの条件を変更してお試しください。</p>
        </div>
      `;
      return;
    }

    container.innerHTML = filtered.map(q => renderQuestionCardHTML(q)).join('');
  }

  // Generate HTML for a single question card
  function renderQuestionCardHTML(q) {
    const ansState = state.answers[q.id];
    const isStarred = !!state.starred[q.id];
    const isAnswered = !!ansState;
    const cardClass = isAnswered
      ? (ansState.isCorrect ? 'question-card answered-correct' : 'question-card answered-incorrect')
      : 'question-card';

    const displayTitle = q.title || `${q.id}: 問題`;
    const formattedQuestion = escapeHtml(q.question || '').replace(/\n/g, '<br>');

    // Code block
    let codeHtml = '';
    if (q.code) {
      codeHtml = `
        <div class="code-block">
          <div class="code-header">
            <span>Code / Configuration</span>
            <button class="copy-btn" onclick="copyCode(this)">コピー</button>
          </div>
          <pre><code>${escapeHtml(q.code)}</code></pre>
        </div>
      `;
    }

    // Options HTML
    const optionsHtml = (q.options || []).map(opt => {
      let optClass = 'option-btn';
      if (isAnswered) {
        if (opt.key === ansState.selectedKey) {
          optClass += ansState.isCorrect ? ' selected-correct' : ' selected-incorrect';
        } else if (opt.key === q.correct) {
          optClass += ' correct-highlight';
        }
      }
      return `
        <button class="${optClass}" onclick="selectOption('${q.id}', '${opt.key}')">
          <span class="option-key">${opt.key}</span>
          <span class="option-text">${escapeHtml(opt.text)}</span>
        </button>
      `;
    }).join('');

    // Explanation Content
    const showExpClass = isAnswered ? 'explanation-panel show' : 'explanation-panel';
    const toggleBtnText = isAnswered ? '解説を隠す ▲' : '解説を表示 ▼';

    // Options Breakdown (Why correct, why incorrect)
    let breakdownHtml = '';
    if (q.options && q.options.some(o => o.verdict)) {
      breakdownHtml = `
        <div class="options-analysis-list">
          ${q.options.map(opt => {
            const isCorr = opt.key === q.correct;
            return `
              <div class="analysis-item ${isCorr ? 'correct-item' : ''}">
                <strong>選択肢 ${opt.key}:</strong> ${escapeHtml(opt.verdict || opt.text)}
              </div>
            `;
          }).join('')}
        </div>
      `;
    }

    // Rules
    let rulesHtml = '';
    if (q.rules && q.rules.length > 0) {
      rulesHtml = `
        <div class="card-rules">
          <div class="card-rules-title">⚡ 試験対策の暗記ルール / Key Takeaways</div>
          <ul class="card-rules-list">
            ${q.rules.map(r => `<li>${escapeHtml(r)}</li>`).join('')}
          </ul>
        </div>
      `;
    }

    const expText = q.explanation || '';
    const expBodyHtml = expText ? `<div style="font-size: 0.925rem; color: #cbd5e1; line-height: 1.7; margin-bottom: 1rem;">${escapeHtml(expText).replace(/\n/g, '<br>')}</div>` : '';

    return `
      <div class="${cardClass}" id="card-${q.id}">
        <div class="card-top">
          <div class="card-badges">
            <span class="badge-id">${q.id}</span>
            <span class="badge-category">${escapeHtml(q.category || q.domain || '')}</span>
            <button class="question-guide-link" title="該当ドメインの基礎知識を読む" onclick="jumpToDomainGuide('${escapeHtml(q.domain || q.category || '')}')">📖 基礎知識を確認</button>
          </div>
          <button class="bookmark-btn ${isStarred ? 'active' : ''}" title="要復習ブックマーク" onclick="toggleBookmark('${q.id}', this)">
            ★
          </button>
        </div>

        <h3 class="question-title">${escapeHtml(displayTitle)}</h3>
        <div class="question-desc">${formattedQuestion}</div>
        ${codeHtml}

        <div class="options-grid">
          ${optionsHtml}
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
          <button class="toggle-exp-btn" id="toggle-btn-${q.id}" onclick="toggleExplanation('${q.id}')">
            <span>${toggleBtnText}</span>
          </button>
          ${isAnswered ? `
            <span class="answer-feedback-label" style="font-size: 0.85rem; font-weight: 700; color: ${ansState.isCorrect ? 'var(--success)' : 'var(--danger)'}">
              ${ansState.isCorrect ? '✓ 正解！' : `✕ 不正解（正解: ${q.correct}）`}
            </span>
          ` : ''}
        </div>

        <div class="${showExpClass}" id="exp-${q.id}">
          <div class="exp-header">
            <span>解答・詳細解説</span>
            <span class="exp-verdict-tag ${isAnswered ? (ansState.isCorrect ? 'correct' : 'incorrect') : 'correct'}">
              正解：${q.correct}
            </span>
          </div>
          ${breakdownHtml}
          ${expBodyHtml}
          ${rulesHtml}
        </div>
      </div>
    `;
  }

  // Update card in place upon answer selection
  function updateCardDOM(card, q, selectedKey, isCorrect) {
    card.className = isCorrect ? 'question-card answered-correct' : 'question-card answered-incorrect';

    const optButtons = card.querySelectorAll('.option-btn');
    optButtons.forEach(btn => {
      const keySpan = btn.querySelector('.option-key');
      if (!keySpan) return;
      const k = keySpan.textContent.trim();
      btn.className = 'option-btn';
      if (k === selectedKey) {
        btn.classList.add(isCorrect ? 'selected-correct' : 'selected-incorrect');
      } else if (k === q.correct) {
        btn.classList.add('correct-highlight');
      }
    });

    const exp = card.querySelector('.explanation-panel');
    const toggleBtn = card.querySelector('.toggle-exp-btn');
    if (exp) exp.classList.add('show');
    if (toggleBtn) toggleBtn.innerHTML = '<span>解説を隠す ▲</span>';

    let label = card.querySelector('.answer-feedback-label');
    if (!label) {
      label = document.createElement('span');
      label.className = 'answer-feedback-label';
      label.style.fontSize = '0.85rem';
      label.style.fontWeight = '700';
      const bottomRow = toggleBtn.parentElement;
      if (bottomRow) bottomRow.appendChild(label);
    }
    label.style.color = isCorrect ? 'var(--success)' : 'var(--danger)';
    label.textContent = isCorrect ? '✓ 正解！' : `✕ 不正解（正解: ${q.correct}）`;
  }

  // --- Render Study Guide ---
  function renderGuide() {
    const toc = document.getElementById('guideTOC');
    const content = document.getElementById('guideContent');
    if (!toc || !content || !window.EXAM_DATA) return;

    const chapters = window.EXAM_DATA.guideChapters || [];

    // TOC
    toc.innerHTML = chapters.map(ch => `
      <a href="#${ch.id}" class="nav-link" onclick="onTOCClick(event, '${ch.id}')">
        ${escapeHtml(ch.title)}
      </a>
    `).join('');

    // Content
    content.innerHTML = chapters.map(ch => `
      <section class="guide-chapter" id="${ch.id}">
        <h2 class="chapter-title">${escapeHtml(ch.title)}</h2>
        <div class="chapter-body">
          ${ch.content}
        </div>
      </section>
    `).join('');

    if (window.mermaid && typeof window.mermaid.run === 'function') {
      try {
        window.mermaid.run({ querySelector: '.mermaid' });
      } catch (err) {
        console.warn('Mermaid run error:', err);
      }
    }
  }

  window.onTOCClick = function (e, id) {
    e.preventDefault();
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      document.querySelectorAll('.guide-sidebar .nav-link').forEach(a => a.classList.remove('active'));
      const activeLink = document.querySelector(`.guide-sidebar a[href="#${id}"]`);
      if (activeLink) activeLink.classList.add('active');
    }
  };

  // --- Render Cheatsheets ---
  function renderCheatsheets() {
    const container = document.getElementById('cheatsheetContainer');
    if (!container || !window.EXAM_DATA) return;

    const sheets = window.EXAM_DATA.cheatsheets || [];
    container.innerHTML = sheets.map(cs => `
      <div class="cheatsheet-card" id="${cs.id}">
        <div class="cs-header">
          <h2 class="cs-title">${escapeHtml(cs.title)}</h2>
          <span class="badge-category">${escapeHtml(cs.category)}</span>
        </div>
        <div class="table-container">
          <table class="guide-table">
            <thead>
              <tr>
                ${cs.headers.map(h => `<th>${escapeHtml(h)}</th>`).join('')}
              </tr>
            </thead>
            <tbody>
              ${cs.rows.map(row => `
                <tr>
                  ${row.map((cell, idx) => {
                    const isName = (idx === 0);
                    return `<td>${isName ? `<code>${escapeHtml(cell)}</code>` : escapeHtml(cell)}</td>`;
                  }).join('')}
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `).join('');
  }

  // --- Render Drill (4 Major Failures) ---
  function renderDrill() {
    const container = document.getElementById('drillContainer');
    if (!container || !window.EXAM_DATA || !window.EXAM_DATA.drillQuestions) return;

    const drills = window.EXAM_DATA.drillQuestions;
    const cur = drills[state.drillIdx];
    if (!cur) return;

    container.innerHTML = `
      <div class="drill-card">
        <div class="drill-header">
          <div style="font-size: 0.85rem; color: var(--text-muted); font-weight: 700;">
            ⚡ 4大障害スピード判定ドリル (問題 ${state.drillIdx + 1} / ${drills.length})
          </div>
          <div style="font-size: 0.9rem; font-weight: 700; color: var(--accent-cyan);">
            🔥 連続正解 (Streak): ${state.drillStreak}
          </div>
        </div>

        <div class="drill-scenario">
          <div style="font-weight: 700; color: var(--accent-primary); margin-bottom: 0.5rem;">[Scenario Trace]</div>
          ${escapeHtml(cur.scenario)}
        </div>

        <div style="font-weight: 600; margin-bottom: 1rem; color: var(--text-main);">
          ${escapeHtml(cur.question)}
        </div>

        <div class="drill-buttons">
          ${cur.options.map(opt => `
            <button class="drill-choice-btn" id="drillBtn_${opt.replace(/\s+/g, '')}" onclick="answerDrill('${opt}')">
              ${escapeHtml(opt)}
            </button>
          `).join('')}
        </div>

        <div id="drillFeedback" class="drill-feedback" style="display: none;"></div>

        <div style="margin-top: 1.5rem; text-align: right;">
          <button id="drillNextBtn" class="hero-btn primary-cta" style="display: none;" onclick="nextDrill()">
            次の問題へ進む →
          </button>
        </div>
      </div>
    `;
  }

  window.answerDrill = function (selectedChoice) {
    if (state.drillAnswered) return;
    state.drillAnswered = true;

    const drills = window.EXAM_DATA.drillQuestions;
    const cur = drills[state.drillIdx];
    const isCorrect = (selectedChoice === cur.answer);

    const fb = document.getElementById('drillFeedback');
    const nextBtn = document.getElementById('drillNextBtn');

    document.querySelectorAll('.drill-choice-btn').forEach(btn => {
      btn.disabled = true;
      if (btn.textContent.trim() === cur.answer) {
        btn.classList.add('correct');
      } else if (btn.textContent.trim() === selectedChoice && !isCorrect) {
        btn.classList.add('incorrect');
      }
    });

    if (fb) {
      fb.style.display = 'block';
      if (isCorrect) {
        state.drillStreak++;
        fb.innerHTML = `
          <div style="color: var(--success); font-weight: 800; font-size: 1.1rem; margin-bottom: 0.5rem;">
            ✅ 正解！ [${escapeHtml(cur.answer)}]
          </div>
          <div style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">
            ${escapeHtml(cur.explanation)}
          </div>
        `;
      } else {
        state.drillStreak = 0;
        fb.innerHTML = `
          <div style="color: var(--danger); font-weight: 800; font-size: 1.1rem; margin-bottom: 0.5rem;">
            ❌ 不正解... 正解は [${escapeHtml(cur.answer)}] です
          </div>
          <div style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">
            ${escapeHtml(cur.explanation)}
          </div>
        `;
      }
    }

    if (nextBtn) nextBtn.style.display = 'inline-block';
  };

  window.nextDrill = function () {
    const drills = window.EXAM_DATA.drillQuestions;
    state.drillIdx = (state.drillIdx + 1) % drills.length;
    state.drillAnswered = false;
    renderDrill();
  };

  // --- Utility ---
  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // --- Initialize ---
  document.addEventListener('DOMContentLoaded', () => {
    loadState();
    updateDashboardStats();
    renderGuide();
    renderQuiz();
  });

})();
