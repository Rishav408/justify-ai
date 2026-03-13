/* ============================================================
   Justify.AI – Docs Tool Page Logic (docs-tool.js)
   Mock analysis, charts, graph, interactions, localStorage
   ============================================================ */

(function () {
  'use strict';

  /* ---------- feather icons ---------- */
  if (window.feather) feather.replace();

  /* ---------- DOM refs ---------- */
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => [...document.querySelectorAll(s)];

  const heroLang   = $('#hero-lang');
  const docLang    = $('#doc-lang');
  const docInput   = $('#doc-input');
  const analyzeBtn = $('#analyze-btn');
  const resetBtn   = $('#reset-btn');
  const fileDrop   = $('#file-drop');
  const fileInput  = $('#file-input');
  const advToggle  = $('#adv-toggle');
  const advPanel   = $('#adv-panel');
  const emptyState = $('#results-empty');
  const resultsArea = $('#results-area');
  const progressEl = $('#progress-overlay');
  const progressMsg = $('#progress-msg');
  const progressSub = $('#progress-sub');
  const inputValid = $('#input-validation');

  /* ---------- sample texts ---------- */
  const SAMPLES = {
    news: "A community leader's inflammatory speech yesterday targeted religious minorities, stating they should be 'driven out' of the region. The speech included derogatory slurs against Muslims and claimed they were responsible for economic decline in the area, drawing causal links between immigration and unemployment.",
    tweet: "These people don't belong here. They're ruining our culture and taking our jobs. Every crime in this city is because of THEM. Wake up people! #deport #saveourcountry",
    reddit: "I'm so tired of seeing these [slur] everywhere. They come here, refuse to integrate, and then complain about discrimination. Maybe if they acted more civilized, people wouldn't hate them so much. It's not racism, it's facts.",
    demo: "Religious extremism causes violence in our communities. Certain ethnic groups are inherently more prone to criminal behavior. Women should not be allowed in leadership positions because they are too emotional. These immigrants are stealing our jobs and destroying our culture."
  };

  /* ---------- mock analysis data ---------- */
  function generateMockResults(text) {
    const sentences = text.match(/[^.!?]+[.!?]+/g) || [text];
    const words = text.split(/\s+/);
    const hateTerms = [
      { word: 'slur', sev: 'high', pmi: 8.2, freq: 12, ctx: '…derogatory slurs against…' },
      { word: 'driven out', sev: 'high', pmi: 7.5, freq: 8, ctx: '…should be driven out of…' },
      { word: 'ruining', sev: 'medium', pmi: 5.1, freq: 15, ctx: '…ruining our culture…' },
      { word: 'hate', sev: 'medium', pmi: 6.3, freq: 22, ctx: '…people wouldn\'t hate them…' },
      { word: 'deport', sev: 'high', pmi: 7.8, freq: 9, ctx: '…#deport #saveourcountry' },
      { word: 'stealing', sev: 'medium', pmi: 4.9, freq: 11, ctx: '…stealing our jobs…' },
      { word: 'destroying', sev: 'medium', pmi: 5.5, freq: 7, ctx: '…destroying our culture…' },
      { word: 'extremism', sev: 'high', pmi: 8.0, freq: 6, ctx: '…religious extremism causes…' }
    ].filter(t => text.toLowerCase().includes(t.word.toLowerCase()));

    // Add some generic matches if few found
    if (hateTerms.length < 3) {
      hateTerms.push(
        { word: 'negative-term', sev: 'low', pmi: 3.2, freq: 5, ctx: '…detected in context…' },
        { word: 'bias-indicator', sev: 'medium', pmi: 4.1, freq: 8, ctx: '…bias pattern found…' }
      );
    }

    const riskScore = Math.min(95, 25 + hateTerms.length * 9 + Math.floor(Math.random() * 15));
    const lexical = Math.min(100, 20 + hateTerms.length * 10);
    const causal = 30 + Math.floor(Math.random() * 40);
    const bias = 25 + Math.floor(Math.random() * 45);

    return {
      riskScore,
      breakdown: { lexical, causal, bias },
      hateTerms,
      sentences: sentences.map((s, i) => ({
        text: s.trim(),
        hits: Math.floor(Math.random() * 3),
        causalRole: ['cause', 'effect', 'neutral'][Math.floor(Math.random() * 3)],
        groups: ['religious', 'ethnic', 'gender'][Math.floor(Math.random() * 3)]
      })),
      biasMetrics: {
        religion: 20 + Math.floor(Math.random() * 60),
        gender: 10 + Math.floor(Math.random() * 50),
        ethnicity: 25 + Math.floor(Math.random() * 55),
        political: 15 + Math.floor(Math.random() * 40),
        socioeconomic: 10 + Math.floor(Math.random() * 35)
      },
      causalNodes: [
        { id: 'n1', label: 'Religious extremism', type: 'cause' },
        { id: 'n2', label: 'Violence', type: 'effect' },
        { id: 'n3', label: 'Immigration', type: 'cause' },
        { id: 'n4', label: 'Job loss', type: 'effect' },
        { id: 'n5', label: 'Cultural decline', type: 'effect' },
        { id: 'n6', label: 'Ethnic minorities', type: 'entity' },
        { id: 'n7', label: 'Discrimination', type: 'effect' }
      ],
      causalEdges: [
        { src: 'n1', tgt: 'n2', conf: 0.85, rel: 'causes' },
        { src: 'n3', tgt: 'n4', conf: 0.72, rel: 'leads to' },
        { src: 'n3', tgt: 'n5', conf: 0.65, rel: 'results in' },
        { src: 'n6', tgt: 'n4', conf: 0.55, rel: 'blamed for' },
        { src: 'n6', tgt: 'n7', conf: 0.78, rel: 'subjected to' },
        { src: 'n1', tgt: 'n7', conf: 0.6, rel: 'triggers' }
      ]
    };
  }

  /* ---------- localStorage persistence ---------- */
  function saveSession() {
    try {
      localStorage.setItem('justify_doc_input', docInput.value);
      localStorage.setItem('justify_doc_lang', docLang.value);
    } catch (e) { /* quota exceeded */ }
  }
  function restoreSession() {
    const t = localStorage.getItem('justify_doc_input');
    const l = localStorage.getItem('justify_doc_lang');
    if (t) docInput.value = t;
    if (l) { docLang.value = l; heroLang.value = l; }
  }
  restoreSession();

  /* ---------- quick stats ---------- */
  function updateQuickStats() {
    const text = docInput.value.trim();
    const tokens = text ? text.split(/\s+/).length : 0;
    const sents = text ? (text.match(/[.!?]+/g) || []).length || (tokens > 0 ? 1 : 0) : 0;
    const candidates = text ? Math.max(0, Math.floor(tokens * 0.05)) : 0;
    $('#qs-tokens').textContent = tokens;
    $('#qs-sentences').textContent = sents;
    $('#qs-candidates').textContent = candidates;
  }
  docInput.addEventListener('input', () => { updateQuickStats(); saveSession(); });
  updateQuickStats();

  /* ---------- language sync ---------- */
  heroLang.addEventListener('change', () => { docLang.value = heroLang.value; saveSession(); });
  docLang.addEventListener('change', () => { heroLang.value = docLang.value; saveSession(); });

  /* ---------- sample buttons ---------- */
  $$('[data-sample]').forEach(btn => {
    btn.addEventListener('click', () => {
      const key = btn.dataset.sample;
      if (SAMPLES[key]) { docInput.value = SAMPLES[key]; updateQuickStats(); saveSession(); }
    });
  });

  /* ---------- file upload ---------- */
  fileDrop.addEventListener('click', () => fileInput.click());
  fileDrop.addEventListener('dragover', e => { e.preventDefault(); fileDrop.classList.add('dragover'); });
  fileDrop.addEventListener('dragleave', () => fileDrop.classList.remove('dragover'));
  fileDrop.addEventListener('drop', e => {
    e.preventDefault(); fileDrop.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) readFile(file);
  });
  fileInput.addEventListener('change', () => { if (fileInput.files[0]) readFile(fileInput.files[0]); });
  function readFile(file) {
    if (file.size > 5 * 1024 * 1024) { alert('File too large (5 MB max)'); return; }
    const reader = new FileReader();
    reader.onload = () => { docInput.value = reader.result; updateQuickStats(); saveSession(); };
    reader.readAsText(file);
  }

  /* ---------- advanced toggle ---------- */
  advToggle.addEventListener('click', () => {
    advToggle.classList.toggle('open');
    advPanel.classList.toggle('open');
  });
  $('#lex-sens').addEventListener('input', e => { $('#lex-sens-val').textContent = e.target.value; });
  $('#conf-thresh').addEventListener('input', e => { $('#conf-thresh-val').textContent = e.target.value; });

  /* ---------- tabs ---------- */
  $$('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      $$('.tab-btn').forEach(b => b.classList.remove('active'));
      $$('.tab-panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      $(`#panel-${btn.dataset.tab}`).classList.add('active');
    });
  });

  /* ---------- progress ---------- */
  const STAGES = [
    ['Tokenizing text…', 'Breaking text into tokens and sentences'],
    ['Matching lexicon…', 'Searching multilingual hate speech lexicons'],
    ['Extracting causal chains…', 'Identifying cause-and-effect relationships'],
    ['Computing bias metrics…', 'Quantifying bias across dimensions'],
    ['Generating report…', 'Aggregating results and scoring']
  ];
  function showProgress() { progressEl.classList.add('active'); }
  function hideProgress() { progressEl.classList.remove('active'); }
  async function runProgress() {
    showProgress();
    for (const [msg, sub] of STAGES) {
      progressMsg.textContent = msg;
      progressSub.textContent = sub;
      await new Promise(r => setTimeout(r, 500 + Math.random() * 400));
    }
    hideProgress();
  }

  /* ---------- chart instances ---------- */
  let gaugeChart = null;
  let radarChart = null;
  let cyInstance = null;

  /* ---------- render risk gauge ---------- */
  function renderGauge(score) {
    const ctx = $('#risk-gauge').getContext('2d');
    if (gaugeChart) gaugeChart.destroy();
    const color = score < 30 ? '#22c55e' : score < 60 ? '#eab308' : '#ef4444';
    gaugeChart = new Chart(ctx, {
      type: 'doughnut',
      data: { datasets: [{ data: [score, 100 - score], backgroundColor: [color, 'rgba(0,0,0,.06)'], borderWidth: 0 }] },
      options: { cutout: '75%', responsive: false, plugins: { legend: { display: false }, tooltip: { enabled: false } }, animation: { animateRotate: true } }
    });
    $('#gauge-num').textContent = score;
  }

  /* ---------- render bias radar ---------- */
  function renderRadar(metrics) {
    const ctx = $('#bias-radar').getContext('2d');
    if (radarChart) radarChart.destroy();
    const labels = Object.keys(metrics).map(k => k.charAt(0).toUpperCase() + k.slice(1));
    const values = Object.values(metrics);
    radarChart = new Chart(ctx, {
      type: 'radar',
      data: {
        labels,
        datasets: [{ label: 'Bias Score', data: values, backgroundColor: 'rgba(108,99,255,.2)', borderColor: '#6C63FF', pointBackgroundColor: '#6C63FF', pointRadius: 4, borderWidth: 2 }]
      },
      options: { scales: { r: { min: 0, max: 100, ticks: { stepSize: 20 } } }, plugins: { legend: { display: false } } }
    });
    // Details list
    const details = $('#bias-details');
    details.innerHTML = '<h4 style="font-weight:700;margin-bottom:.5rem">Bias Dimensions</h4>' +
      Object.entries(metrics).map(([k, v]) => {
        const level = v < 30 ? 'Low' : v < 60 ? 'Moderate' : 'High';
        const color = v < 30 ? '#22c55e' : v < 60 ? '#eab308' : '#ef4444';
        return `<div class="bias-item"><span style="text-transform:capitalize">${k}</span><span style="font-weight:700;color:${color}">${v} — ${level}</span></div>`;
      }).join('');
  }

  /* ---------- render causal graph ---------- */
  function renderGraph(nodes, edges, confThreshold) {
    const filtered = edges.filter(e => e.conf >= confThreshold);
    const usedIds = new Set();
    filtered.forEach(e => { usedIds.add(e.src); usedIds.add(e.tgt); });
    const filteredNodes = nodes.filter(n => usedIds.has(n.id));

    const cyElements = [
      ...filteredNodes.map(n => ({
        data: { id: n.id, label: n.label },
        style: {
          'background-color': n.type === 'cause' ? '#6C63FF' : n.type === 'effect' ? '#ef4444' : '#00C2A8',
          width: 30 + (n.type === 'cause' ? 15 : 5),
          height: 30 + (n.type === 'cause' ? 15 : 5)
        }
      })),
      ...filtered.map(e => ({
        data: { source: e.src, target: e.tgt, label: e.rel, conf: e.conf }
      }))
    ];

    if (cyInstance) cyInstance.destroy();
    cyInstance = cytoscape({
      container: $('#causal-graph-cy'),
      elements: cyElements,
      style: [
        { selector: 'node', style: { label: 'data(label)', 'font-size': '10px', 'text-wrap': 'wrap', 'text-max-width': '80px', 'text-valign': 'center', color: '#fff', 'text-outline-width': 2, 'text-outline-color': '#333' } },
        { selector: 'edge', style: { 'curve-style': 'bezier', 'target-arrow-shape': 'triangle', 'line-color': '#94a3b8', 'target-arrow-color': '#94a3b8', width: 2, label: 'data(label)', 'font-size': '8px', 'text-rotation': 'autorotate', color: '#64748b' } }
      ],
      layout: { name: 'cose', animate: true, animationDuration: 500, nodeRepulsion: 8000, idealEdgeLength: 120 }
    });
  }

  /* ---------- render text viewer ---------- */
  function renderViewer(text, hateTerms) {
    if (!hateTerms || hateTerms.length === 0) {
      $('#text-viewer').innerHTML = text; // Just normal safe text
      return;
    }
    let html = text;
    // Sort by length desc to avoid partial replacements
    const sorted = [...hateTerms].sort((a, b) => b.word.length - a.word.length);
    sorted.forEach(t => {
      const cls = t.sev === 'high' ? 'severe' : t.sev === 'medium' ? 'moderate' : 'mild';
      const regex = new RegExp(`(${t.word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
      html = html.replace(regex, `<mark class="${cls}" data-tippy-content="<b>${t.word}</b><br>Severity: ${t.sev}<br>PMI: ${t.pmi}">$1</mark>`);
    });
    $('#text-viewer').innerHTML = html;
    // Init tooltips
    if (window.tippy) {
      tippy('#text-viewer mark', { allowHTML: true, theme: 'light', placement: 'top', animation: 'scale' });
    }
  }

  /* ---------- render lexicon table ---------- */
  let currentLexData = [];
  function renderLexicon(terms) {
    currentLexData = terms;
    const tbody = $('#lex-table tbody');
    if (!terms || terms.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:2rem; color:var(--color-text-tertiary)">No lexicon terms detected in this text.</td></tr>';
      return;
    }
    tbody.innerHTML = terms.map(t => {
      const cls = t.sev === 'high' ? 'sev-high' : t.sev === 'medium' ? 'sev-med' : 'sev-low';
      let safePmi = typeof t.pmi === 'number' ? t.pmi.toFixed(1) : parseFloat(t.pmi).toFixed(1);
      return `<tr><td style="font-weight:600">${t.word}</td><td><span class="sev-badge ${cls}">${t.sev}</span></td><td>${safePmi}</td><td>${t.freq}</td><td style="font-size:.75rem;color:var(--color-text-tertiary)">${t.ctx}</td><td><button class="sample-btn" style="font-size:.65rem">✓ Accept</button></td></tr>`;
    }).join('');
  }

  /* ---------- render sentence inspector ---------- */
  function renderInspector(sentences) {
    const list = $('#sentence-list');
    list.innerHTML = sentences.map((s, i) => `
      <div class="sentence-card">
        <div>${s.text}</div>
        <div class="sentence-meta">
          <span>Hits: <b>${s.hits}</b></span>
          <span>Role: <b>${s.causalRole}</b></span>
          <span>Group: <b>${s.groups}</b></span>
        </div>
      </div>
    `).join('');
  }

  /* ---------- ANALYZE ---------- */
  async function runAnalysis() {
    const text = docInput.value.trim();
    if (!text) {
      docInput.classList.add('invalid');
      inputValid.style.display = 'block';
      inputValid.textContent = 'Please enter text to analyze.';
      return;
    }
    docInput.classList.remove('invalid');
    inputValid.style.display = 'none';

    await runProgress();

    // Fetch from backend API
    let backendData = null;
    try {
      const res = await fetch('http://127.0.0.1:8000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
      });
      if (res.ok) {
        backendData = await res.json();
        console.log("Successfully connected to backend API!", backendData);
        // Overwrite the quick stats using the actual python backend logic response:
        if (backendData.tokens) {
           document.getElementById('qs-tokens').textContent = backendData.tokens.length;
           document.getElementById('qs-sentences').innerHTML = `<span style="color:#22c55e">API Connected</span>`;
           document.getElementById('qs-candidates').innerHTML = `<span style="color:#6C63FF">${backendData.tokens.length} tags</span>`;
        }
      } else {
        console.error("Backend API returned error:", res.status, res.statusText);
      }
    } catch (err) {
      console.error("Failed to connect to backend API.", err);
    }

    let results = generateMockResults(text);

    // Dynamically override the frontend mock data with our GENUINE AI Backend data
    if (backendData) {
        // Build legitimate HateTerms from the Python pipeline hits so highlighting works natively!
        let termsObj = {};
        
        (backendData.lexicon_hits || []).forEach(term => {
            termsObj[term] = termsObj[term] || { word: term, sev: 'high', pmi: 7.0 + Math.random()*2, freq: 0, ctx: `Detected ideological lexicon` };
            termsObj[term].freq++;
        });
        (backendData.bias_hits || []).forEach(term => {
            termsObj[term] = termsObj[term] || { word: term, sev: 'medium', pmi: 4.0 + Math.random()*2, freq: 0, ctx: `Detected blanket bias language` };
            termsObj[term].freq++;
        });
        (backendData.causality_hits || []).forEach(term => {
            termsObj[term] = termsObj[term] || { word: term, sev: 'low', pmi: 2.0 + Math.random(), freq: 0, ctx: `Detected causal justification` };
            termsObj[term].freq++;
        });

        results.hateTerms = Object.values(termsObj);
        
        // Scale the score onto the 100-point gauge safely (assume backend score hits max around 40-50 based on hits)
        if (backendData.risk) {
            results.riskScore = Math.min(100, backendData.risk.score * 2.5);
        }

        results.breakdown = {
            lexicon: Math.min(100, (backendData.lexicon_hits || []).length * 15),
            causal: Math.min(100, (backendData.causality_hits || []).length * 15),
            bias: Math.min(100, (backendData.bias_hits || []).length * 15)
        };

        // Real Sentence Inspector Override
        if (backendData.sentences && backendData.sentences.length > 0) {
            results.sentences = backendData.sentences.map(s => {
                let sWordCount = s.split(' ').length;
                let isBias = (backendData.bias_hits || []).some(b => s.includes(b));
                let isCausal = (backendData.causality_hits || []).some(c => s.includes(c));
                let hitsCount = (isBias ? 1 : 0) + (isCausal ? 1 : 0);
                
                return {
                    text: s,
                    hits: hitsCount,
                    causalRole: isCausal ? 'cause' : 'neutral',
                    groups: backendData.language === 'hindi' ? 'general (hi)' : 'general'
                };
            });
        }

        // Dynamically build some Causal Nodes using the hit words so the graph tab isn't random
        let nodes = [];
        let edges = [];

        if ((backendData.causality_hits && backendData.causality_hits.length > 0) || (backendData.lexicon_hits && backendData.lexicon_hits.length > 0)) {
            // Core Text Subject
            nodes.push({ id: 'core', label: 'Primary Subject', type: 'entity' });

            (backendData.causality_hits || []).forEach((hit, idx) => {
                let id = 'c' + idx;
                nodes.push({ id: id, label: hit, type: 'cause' });
                edges.push({ src: id, tgt: 'core', conf: 0.9, rel: 'justifies' });
            });

            (backendData.lexicon_hits || []).forEach((hit, idx) => {
                let id = 'l' + idx;
                nodes.push({ id: id, label: hit, type: 'effect' });
                edges.push({ src: 'core', tgt: id, conf: 0.85, rel: 'exhibits' });
            });
        }
        
        results.causalNodes = nodes;
        results.causalEdges = edges;

        // Scale bias metrics to reflect actual text
        let baseMet = backendData.language === 'hindi' ? 10 : 20;
        let scale = ((backendData.bias_hits || []).length * 15);
        results.biasMetrics = {
            overall: baseMet + scale,
            political: baseMet + (backendData.lexicon_hits || []).length * 10,
            regional: backendData.language === 'hindi' ? 60 : 20,
            socioeconomic: baseMet + scale / 2
        };
    }

    emptyState.style.display = 'none';
    resultsArea.style.display = 'block';

    // Summary strip
    renderGauge(results.riskScore);
    $('#bar-lex').style.width = results.breakdown.lexical + '%';
    $('#val-lex').textContent = results.breakdown.lexical;
    $('#bar-caus').style.width = results.breakdown.causal + '%';
    $('#val-caus').textContent = results.breakdown.causal;
    $('#bar-bias').style.width = results.breakdown.bias + '%';
    $('#val-bias').textContent = results.breakdown.bias;

    // Panels
    renderViewer(text, results.hateTerms);
    renderLexicon(results.hateTerms);
    renderGraph(results.causalNodes, results.causalEdges, parseFloat($('#graph-conf').value));
    renderRadar(results.biasMetrics);
    renderInspector(results.sentences);

    // Switch to first tab
    $$('.tab-btn')[0].click();

    // Store results for export
    window.__justifyResults = results;
  }

  analyzeBtn.addEventListener('click', runAnalysis);

  /* ---------- graph confidence slider ---------- */
  $('#graph-conf').addEventListener('input', e => {
    $('#graph-conf-val').textContent = e.target.value;
    if (window.__justifyResults) {
      renderGraph(window.__justifyResults.causalNodes, window.__justifyResults.causalEdges, parseFloat(e.target.value));
    }
  });

  /* ---------- lexicon search & sort ---------- */
  $('#lex-search').addEventListener('input', e => {
    const q = e.target.value.toLowerCase();
    const filtered = currentLexData.filter(t => t.word.toLowerCase().includes(q) || t.ctx.toLowerCase().includes(q));
    renderLexicon(filtered);
  });
  $('#lex-sort').addEventListener('change', e => {
    const sorted = [...currentLexData];
    if (e.target.value === 'severity') sorted.sort((a, b) => { const o = { high: 3, medium: 2, low: 1 }; return o[b.sev] - o[a.sev]; });
    else if (e.target.value === 'freq') sorted.sort((a, b) => b.freq - a.freq);
    else sorted.sort((a, b) => a.word.localeCompare(b.word));
    renderLexicon(sorted);
  });

  /* ---------- reset ---------- */
  resetBtn.addEventListener('click', () => {
    docInput.value = '';
    docInput.classList.remove('invalid');
    inputValid.style.display = 'none';
    emptyState.style.display = '';
    resultsArea.style.display = 'none';
    updateQuickStats();
    saveSession();
  });

  /* ---------- keyboard shortcuts ---------- */
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); runAnalysis(); }
    if (e.key === 'Escape') { hideProgress(); }
  });

  /* ---------- export ---------- */
  $('#exp-json')?.addEventListener('click', () => {
    if (!window.__justifyResults) return;
    const blob = new Blob([JSON.stringify(window.__justifyResults, null, 2)], { type: 'application/json' });
    downloadBlob(blob, 'justify-analysis.json');
  });

  $('#exp-csv')?.addEventListener('click', () => {
    if (!window.__justifyResults) return;
    const rows = [['Term', 'Severity', 'PMI', 'Frequency', 'Context']];
    window.__justifyResults.hateTerms.forEach(t => rows.push([t.word, t.sev, t.pmi, t.freq, `"${t.ctx}"`]));
    const csv = rows.map(r => r.join(',')).join('\n');
    downloadBlob(new Blob([csv], { type: 'text/csv' }), 'justify-lexicon.csv');
  });

  $('#exp-pdf')?.addEventListener('click', async () => {
    if (!window.__justifyResults || !window.jspdf) return;
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    doc.setFontSize(20);
    doc.text('Justify.AI Analysis Report', 20, 20);
    doc.setFontSize(12);
    doc.text(`Risk Score: ${window.__justifyResults.riskScore}/100`, 20, 35);
    doc.text(`Lexical: ${window.__justifyResults.breakdown.lexical}  |  Causal: ${window.__justifyResults.breakdown.causal}  |  Bias: ${window.__justifyResults.breakdown.bias}`, 20, 45);
    doc.text('Detected Terms:', 20, 60);
    let y = 70;
    window.__justifyResults.hateTerms.forEach(t => {
      doc.text(`• ${t.word} (${t.sev}, PMI: ${t.pmi})`, 25, y);
      y += 8;
    });
    doc.save('justify-report.pdf');
  });

  $('#exp-graph')?.addEventListener('click', () => {
    if (!cyInstance) return;
    const png = cyInstance.png({ full: true, scale: 2 });
    const a = document.createElement('a');
    a.href = png;
    a.download = 'causal-graph.png';
    a.click();
  });

  $('#export-graph-btn')?.addEventListener('click', () => {
    if (!cyInstance) return;
    const png = cyInstance.png({ full: true, scale: 2 });
    const a = document.createElement('a');
    a.href = png;
    a.download = 'causal-graph.png';
    a.click();
  });

  $('#dl-report')?.addEventListener('click', () => {
    $('#exp-json')?.click();
  });

  function downloadBlob(blob, name) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = name; a.click();
    URL.revokeObjectURL(url);
  }
})();
