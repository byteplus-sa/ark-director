// renderer.js — reads the #showcase-data JSON and renders the page.
// Inlined into template.html by scripts/generate_showcase.py.

(function () {
  const raw = document.getElementById('showcase-data').textContent;
  const data = JSON.parse(raw);
  const viaServer = location.protocol === 'http:' || location.protocol === 'https:';

  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  };
  const projectHref = path => {
    if (typeof path !== 'string' || !path || /[\\\\?#:]/.test(path) || path.startsWith('/')) return null;
    const parts = path.split('/');
    if (parts.some(part => !part || part === '.' || part === '..')) return null;
    return parts.map(encodeURIComponent).join('/');
  };

  // ---- toast ----
  const toast = el('div', 'toast');
  document.body.appendChild(toast);
  let toastTimer = null;
  function showToast(message, type) {
    toast.textContent = message;
    toast.className = 'toast show ' + (type || '');
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.className = 'toast';
    }, 2600);
  }

  // collect selectable ASSETS: assetId -> {manifest, field, key}
  // (many cards can share one assetId; each card carries its own filename)
  const selectable = data.selectableRegistry || {};
  let sessionToken = null, expectedRevision = null;
  const selections = Object.create(null); // assetId -> filename

  // ---- nav ----
  const nav = el('nav');
  const navInner = el('div', 'inner');
  const brand = el('span', 'brand');
  brand.appendChild(document.createTextNode('Showcase'));
  const sep = el('span');
  sep.textContent = '·';
  brand.appendChild(sep);
  navInner.appendChild(brand);
  if (data.canvas) {
    const canvasLink = el('a', null, 'Production canvas');
    canvasLink.href = '#production-canvas';
    navInner.appendChild(canvasLink);
  }
  for (const s of data.sections) {
    const a = el('a', null, s.title);
    a.href = '#' + s.id;
    navInner.appendChild(a);
  }
  nav.appendChild(navInner);
  document.body.insertBefore(nav, document.body.firstChild);
  document.title = data.title;

  // ---- header ----
  const header = el('header');
  if (data.kicker) header.appendChild(el('div', 'kicker', data.kicker));
  header.appendChild(el('h1', null, data.title));
  if (data.lede) header.appendChild(el('p', 'lede', data.lede));
  if (data.badges && data.badges.length) {
    const badges = el('div', 'badges');
    for (const b of data.badges) {
      const span = el('span', 'badge');
      if (b.label) span.appendChild(document.createTextNode(b.label + ' '));
      span.appendChild(el('b', null, b.value));
      badges.appendChild(span);
    }
    header.appendChild(badges);
  }
  document.getElementById('app').appendChild(header);

  if (data.canvas) {
    document.getElementById('app').appendChild(buildProductionCanvas(data.canvas));
  }

  // ---- selection toolbar ----
  // Server mode: full select + save. Plain file:// : read-only preview.
  const selIds = Object.keys(selectable);
  let selToolbar = null, selStatus = null, selSave = null;
  if (selIds.length) {
    selToolbar = el('div', 'sel-bar');
    if (viaServer) {
      selStatus = el('span', 'sel-status', 'Pick variants, then press Ctrl+S (⌘S) to save.');
      selSave = el('button', 'sel-save', 'Save (Ctrl+S)');
      selSave.addEventListener('click', saveSelections);
      selToolbar.appendChild(selStatus);
      selToolbar.appendChild(selSave);
    } else {
      selToolbar.appendChild(el('span', 'sel-status',
        'Read-only preview — run with --serve to select and save variants.'));
    }
    document.getElementById('app').appendChild(selToolbar);
  }

  // ---- main ----
  const main = el('main');
  for (const s of data.sections) {
    main.appendChild(buildSection(s));
  }
  document.getElementById('app').appendChild(main);

  // ---- lightbox (click image to view fullscreen) ----
  const lb = el('div', 'lightbox');
  const lbImg = document.createElement('img');
  const lbClose = el('button', 'lb-close', '×');
  lbClose.setAttribute('aria-label', 'Close');
  const lbPrev = el('button', 'lb-nav lb-prev', '‹');
  const lbNext = el('button', 'lb-nav lb-next', '›');
  const lbCount = el('div', 'lb-count');
  lb.appendChild(lbImg);
  lb.appendChild(lbClose);
  lb.appendChild(lbPrev);
  lb.appendChild(lbNext);
  lb.appendChild(lbCount);
  document.body.appendChild(lb);

  const zoomable = Array.from(document.querySelectorAll('.media-frame img'));
  let zoomIdx = -1;

  function openZoom(i) {
    zoomIdx = (i + zoomable.length) % zoomable.length;
    const img = zoomable[zoomIdx];
    lbImg.src = img.src;
    lbImg.alt = img.alt || '';
    lbCount.textContent = (zoomIdx + 1) + ' / ' + zoomable.length;
    lb.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
  function closeZoom() {
    lb.style.display = 'none';
    document.body.style.overflow = '';
  }
  zoomable.forEach((img, i) => {
    img.addEventListener('click', () => openZoom(i));
  });
  lbClose.addEventListener('click', closeZoom);
  lbPrev.addEventListener('click', (e) => { e.stopPropagation(); openZoom(zoomIdx - 1); });
  lbNext.addEventListener('click', (e) => { e.stopPropagation(); openZoom(zoomIdx + 1); });
  lb.addEventListener('click', (e) => {
    if (e.target === lb) closeZoom();
  });
  document.addEventListener('keydown', (e) => {
    if (lb.style.display !== 'flex') return;
    if (e.key === 'Escape') closeZoom();
    else if (e.key === 'ArrowLeft') openZoom(zoomIdx - 1);
    else if (e.key === 'ArrowRight') openZoom(zoomIdx + 1);
  });

  if (data.footer) {
    const footer = el('footer');
    footer.appendChild(el('p', null, data.footer));
    document.getElementById('app').appendChild(footer);
  }

  function buildSection(s) {
    const section = el('section');
    section.id = s.id;

    const head = el('div', 'section-head');
    if (s.icon) {
      const ic = el('span', 'icon', s.icon);
      ic.style.background = s.iconBg || 'var(--accent-soft)';
      head.appendChild(ic);
    }
    head.appendChild(el('h2', null, s.title));
    if (s.count) head.appendChild(el('span', 'count', s.count));
    section.appendChild(head);

    if (s.desc) section.appendChild(el('div', 'section-desc', s.desc));

    if (s.kind === 'table') {
      section.appendChild(buildTable(s));
    } else if (s.kind === 'panel') {
      section.appendChild(buildPanel(s));
    } else if (s.kind === 'takes') {
      section.appendChild(buildTakes(s));
    } else {
      const grid = el('div', s.mediaOnly ? 'grid media-only' : 'grid');
      for (const c of (s.cards || [])) grid.appendChild(buildCard(c));
      section.appendChild(grid);
    }
    return section;
  }

  function buildProductionCanvas(canvas) {
    const section = el('section', 'canvas-board');
    section.id = 'production-canvas';
    const heading = el('div', 'canvas-heading');
    const headingCopy = el('div');
    headingCopy.appendChild(el('div', 'kicker', 'Live production workspace'));
    headingCopy.appendChild(el('h2', null, 'Production canvas'));
    const build = data.canvasBuild || {};
    const sync = el('div', 'canvas-sync');
    sync.appendChild(el('span', 'canvas-sync-dot'));
    sync.appendChild(document.createTextNode(
      build.generatedAt ? 'Synced ' + build.generatedAt : 'Generated canvas snapshot'
    ));
    heading.appendChild(headingCopy);
    heading.appendChild(sync);
    section.appendChild(heading);
    const mode = data.approvalMode || {};
    const modeRow = el('div', 'canvas-mode');
    modeRow.appendChild(el('strong', null,
      mode.mode === 'ask_for_approval' ? 'Ask for approval' : 'Approve for me'));
    modeRow.appendChild(el('span', null,
      mode.source === 'explicit' ? 'Explicit project setting' : 'Project default'));
    section.appendChild(modeRow);

    const stages = el('div', 'canvas-stages');
    for (const [index, stage] of (canvas.stages || []).entries()) {
      const card = el('article', 'canvas-stage status-' + (stage.status || 'pending'));
      if (stage.id === canvas.currentStage) card.classList.add('current');
      const top = el('div', 'canvas-stage-top');
      top.appendChild(el('span', 'canvas-step', String(index + 1).padStart(2, '0')));
      top.appendChild(el('h3', null, stage.label || stage.id));
      top.appendChild(el('span', 'canvas-status', stage.status || 'pending'));
      card.appendChild(top);
      if (stage.summary) card.appendChild(el('p', 'canvas-summary', stage.summary));
      if (stage.locks && Object.keys(stage.locks).length) {
        const locks = el('div', 'canvas-locks');
        for (const [kind, lock] of Object.entries(stage.locks)) {
          const row = el('div', 'canvas-lock');
          row.appendChild(el('strong', null, kind.replaceAll('_', ' ') + ': ' + (lock.result || 'pending')));
          if (lock.actor) row.appendChild(el('span', null, ' by ' + lock.actor));
          if (lock.reason) row.appendChild(el('p', null, lock.reason));
          const links = el('div', 'canvas-links');
          for (const [label, path] of [
            ['Accepted artifact', lock.artifact_path],
            ['Review', lock.review_path],
            ['Decision', lock.decision_id && 'decisions/' + lock.decision_id + '.json'],
          ]) {
            const href = projectHref(path);
            if (!href) continue;
            const link = el('a', null, label);
            link.href = href;
            links.appendChild(link);
          }
          row.appendChild(links);
          locks.appendChild(row);
        }
        card.appendChild(locks);
      }
      const counts = stage.counts || {};
      const metrics = el('div', 'canvas-metrics');
      for (const [label, value] of [
        ['sections', counts.sections || 0],
        ['sources', counts.sources || 0],
        ['media', counts.media || 0],
        ['prompts', counts.prompts || 0],
      ]) {
        const metric = el('span', 'canvas-metric');
        metric.appendChild(el('b', null, String(value)));
        metric.appendChild(document.createTextNode(' ' + label));
        metrics.appendChild(metric);
      }
      card.appendChild(metrics);
      if (stage.sectionIds && stage.sectionIds.length) {
        const links = el('div', 'canvas-links');
        for (const sectionId of stage.sectionIds) {
          const target = (data.sections || []).find(item => item.id === sectionId);
          const link = el('a', null, target ? target.title : sectionId);
          link.href = '#' + sectionId;
          links.appendChild(link);
        }
        card.appendChild(links);
      }
      if (stage.sources && stage.sources.length) {
        const sources = el('div', 'canvas-sources');
        for (const source of stage.sources) {
          const sourceRow = el('div', 'canvas-source');
          const sourceHead = el('div', 'canvas-source-head');
          sourceHead.appendChild(el('span', 'canvas-source-kind', source.kind || 'source'));
          const sourceLink = el('a', null, source.label || source.path);
          sourceLink.href = encodeURI(source.path);
          sourceHead.appendChild(sourceLink);
          if (source.sha256) {
            sourceHead.appendChild(el('code', null, source.sha256.slice(0, 10)));
          }
          sourceRow.appendChild(sourceHead);
          if (source.content != null) {
            const details = document.createElement('details');
            details.appendChild(el('summary', null, 'View in canvas'));
            const content = el('pre');
            content.textContent = source.content;
            details.appendChild(content);
            sourceRow.appendChild(details);
          } else if (['image', 'video', 'audio'].includes(source.kind)) {
            const preview = el('div', 'canvas-source-media');
            preview.appendChild(mediaNode({type: source.kind, src: source.path, alt: source.label || source.path}));
            sourceRow.appendChild(preview);
          }
          sources.appendChild(sourceRow);
        }
        card.appendChild(sources);
      }
      stages.appendChild(card);
    }
    section.appendChild(stages);
    const selected = data.currentSelections || {};
    if (Object.keys(selected).length) {
      const decisions = el('div', 'canvas-decisions');
      decisions.appendChild(el('h3', null, 'Variant decisions'));
      for (const [assetId, filename] of Object.entries(selected)) {
        const evidence = (data.selectionEvidence || {})[assetId] || {};
        const row = el('div', 'canvas-decision');
        row.appendChild(el('strong', null, assetId + ': ' + filename));
        row.appendChild(el('span', null,
          evidence.decision_id
            ? ' · ' + (evidence.result || evidence.status || 'selected') + ' by ' + (evidence.actor || 'unknown')
            : ' · legacy selection; approval evidence unavailable'));
        if (evidence.reason) row.appendChild(el('p', null, evidence.reason));
        const links = el('div', 'canvas-links');
        for (const [label, path] of [
          ['Review', evidence.review_path],
          ['Decision', evidence.decision_path],
        ]) {
          const href = projectHref(path);
          if (!href) continue;
          const link = el('a', null, label);
          link.href = href;
          links.appendChild(link);
        }
        row.appendChild(links);
        decisions.appendChild(row);
      }
      section.appendChild(decisions);
    }
    return section;
  }

  function buildCard(c) {
    const card = el('div', 'card ' + (c.type || 'video'));
    const isSelectable = viaServer && !!selectable[c.id];
    if (isSelectable) card.classList.add('selectable');
    if (c.media) {
      const frame = el('div', 'media-frame');
      if (c.kindPill) frame.appendChild(el('span', 'kind-pill', c.kindPill));
      if (isSelectable) {
        const sel = el('button', 'select-toggle', 'Select');
        sel.setAttribute('data-id', c.id);
        sel.setAttribute('data-filename', c.media.src.split('/').pop());
        sel.addEventListener('click', (e) => {
          e.stopPropagation();
          chooseVariant(c.id, c.media.src.split('/').pop(), sel);
        });
        frame.appendChild(sel);
      }
      frame.appendChild(mediaNode(c.media));
      card.appendChild(frame);
    }
    const body = el('div', 'body');
    if (c.tag) body.appendChild(el('div', 'tag', c.tag));
    if (c.title) body.appendChild(el('div', 'title', c.title));
    if (c.sub) body.appendChild(el('div', 'sub', c.sub));
    if (c.chips && c.chips.length) {
      const meta = el('div', 'meta');
      for (const ch of c.chips) meta.appendChild(el('span', 'chip', ch));
      body.appendChild(meta);
    }
    if (c.refs && c.refs.length) {
      const refs = el('div', 'refs');
      refs.appendChild(el('div', 'refs-label', 'Elements used'));
      for (const r of c.refs) {
        const ref = el('div', 'ref');
        ref.appendChild(el('span', 'dot ' + (r.kind || 'vid')));
        const name = r.path ? el('a', 'ref-name', r.name) : el('span', 'ref-name', r.name);
        if (r.path) name.href = encodeURI(r.path);
        ref.appendChild(name);
        if (r.role) ref.appendChild(el('span', 'ref-role', r.role));
        refs.appendChild(ref);
      }
      body.appendChild(refs);
    }
    if (c.prompt) {
      body.appendChild(el('div', 'prompt-label', 'Prompt'));
      const pre = el('pre');
      pre.textContent = c.prompt;
      body.appendChild(pre);
    }
    if (c.reviewPath) {
      const review = el('a', 'canvas-review-link', 'Candidate review');
      const href = projectHref(c.reviewPath);
      if (href) {
        review.href = href;
        body.appendChild(review);
      }
    }
    card.appendChild(body);
    return card;
  }

  function buildTable(s) {
    const wrap = el('div', 'table-wrap');
    const table = el('table', 'showcase');
    const thead = el('thead');
    const hr = el('tr');
    const cols = s.columns || ['Stage', 'Prompt / Input', 'Generated Result'];
    const colCls = ['col-stage', 'col-prompt', 'col-result'];
    cols.forEach((c, i) => {
      const th = el('th', colCls[i] || '', c);
      hr.appendChild(th);
    });
    thead.appendChild(hr);
    table.appendChild(thead);
    const tbody = el('tbody');
    for (const row of (s.rows || [])) {
      const tr = el('tr');
      const tdStage = el('td');
      const stageClass = row.stageClass || ((row.stage || '').toLowerCase() === 'before' ? 'before' : 'after');
      const stagePill = el('span', 'stage ' + stageClass, row.stage || '');
      tdStage.appendChild(stagePill);
      if (row.stageTitle) tdStage.appendChild(el('div', 'stage-title', row.stageTitle));
      if (row.stageSub) tdStage.appendChild(el('div', 'stage-sub', row.stageSub));
      tr.appendChild(tdStage);
      const tdPrompt = el('td');
      const pre = el('pre');
      pre.textContent = row.prompt || '';
      tdPrompt.appendChild(pre);
      tr.appendChild(tdPrompt);
      const tdResult = el('td');
      if (row.media) {
        const m = mediaNode(row.media);
        if (row.media.type === 'video') m.className = 'result-video';
        tdResult.appendChild(m);
      }
      if (row.meta) tdResult.appendChild(el('div', 'result-meta', row.meta));
      tr.appendChild(tdResult);
      tbody.appendChild(tr);
    }
    table.appendChild(tbody);
    wrap.appendChild(table);
    return wrap;
  }

  function buildPanel(s) {
    const panel = el('div', 'panel');
    if (s.media) panel.appendChild(mediaNode(s.media));
    if (s.caption) panel.appendChild(el('div', 'caption', s.caption));
    return panel;
  }

  function buildTakes(s) {
    const wrap = el('div', 'takes-wrap');
    for (const grp of (s.groups || [])) {
      const card = el('div', 'takes-card');
      const isSelectable = viaServer;

      // header
      const hdr = el('div', 'takes-header');
      hdr.appendChild(el('h3', null, grp.title || ''));
      if (grp.uc) hdr.appendChild(el('span', 'takes-uc', grp.uc));
      if (grp.meta && grp.meta.length) {
        const mc = el('div', 'takes-meta');
        for (const m of grp.meta) mc.appendChild(el('span', 'chip', m));
        hdr.appendChild(mc);
      }
      card.appendChild(hdr);

      // controls
      const videos = [];
      const ctrl = el('div', 'takes-controls');
      const playAll = el('button', 'takes-btn', '▶ Play all');
      playAll.addEventListener('click', () => {
        const anyPlaying = videos.some(v => !v.paused);
        videos.forEach(v => {
          if (anyPlaying) { v.pause(); }
          else { v.currentTime = 0; v.play().catch(() => {}); }
        });
        playAll.textContent = anyPlaying ? '▶ Play all' : '⏸ Pause all';
      });
      ctrl.appendChild(playAll);

      // prompt toggle
      let promptPre = null;
      if (grp.promptFile) {
        const promptBtn = el('button', 'takes-btn takes-btn-ghost', '📝 Prompt');
        promptBtn.addEventListener('click', () => {
          if (promptPre) {
            promptPre.style.display = promptPre.style.display === 'none' ? 'block' : 'none';
          }
        });
        ctrl.appendChild(promptBtn);
      }
      card.appendChild(ctrl);

      // prompt (lazy-loaded via fetch in server mode, embedded in file mode)
      if (grp.promptFile) {
        promptPre = el('pre', 'takes-prompt');
        promptPre.style.display = 'none';
        if (grp.prompt) {
          promptPre.textContent = grp.prompt;
        } else {
          promptPre.textContent = 'Loading…';
          fetch(grp.promptFile)
            .then(r => r.ok ? r.text() : Promise.reject())
            .then(text => { promptPre.textContent = text; })
            .catch(() => {
              promptPre.textContent = 'Prompt file: ' + grp.promptFile;
            });
        }
        card.appendChild(promptPre);
      }

      // takes grid
      const body = el('div', 'takes-body');
      for (const tk of (grp.takes || [])) {
        const col = el('div', 'takes-take');

        // video
        if (tk.media) {
          const frame = el('div', 'takes-video-frame');
          const v = document.createElement('video');
          v.controls = true;
          v.preload = 'none';
          v.playsInline = true;
          v.src = tk.media.src;
          v.addEventListener('play', () => {
            playAll.textContent = '⏸ Pause all';
          });
          v.addEventListener('pause', () => {
            if (videos.every(vv => vv.paused)) playAll.textContent = '▶ Play all';
          });
          videos.push(v);
          frame.appendChild(v);

          // pick winner button
          if (isSelectable && selectable[tk.id] && tk.filename) {
            const pick = el('button', 'select-toggle takes-pick', 'Pick winner');
            pick.setAttribute('data-id', tk.id);
            pick.setAttribute('data-filename', tk.filename);
            pick.addEventListener('click', (e) => {
              e.stopPropagation();
              chooseVariant(tk.id, tk.filename, pick);
            });
            frame.appendChild(pick);
          }

          col.appendChild(frame);
        }

        // label
        if (tk.label) col.appendChild(el('h4', null, tk.label));

        // chips
        if (tk.chips && tk.chips.length) {
          const ci = el('div', 'takes-info');
          for (const c of tk.chips) ci.appendChild(el('span', 'chip', c));
          col.appendChild(ci);
        }

        // contact sheet
        if (tk.contactSheet) {
          const cs = document.createElement('img');
          cs.className = 'takes-contact-sheet';
          cs.src = tk.contactSheet;
          cs.alt = 'Contact sheet';
          cs.loading = 'lazy';
          col.appendChild(cs);
        }
        if (tk.reviewPath) {
          const review = el('a', 'canvas-review-link', 'Candidate review');
          const href = projectHref(tk.reviewPath);
          if (href) {
            review.href = href;
            col.appendChild(review);
          }
        }

        body.appendChild(col);
      }
      card.appendChild(body);
      wrap.appendChild(card);
    }
    return wrap;
  }

  function mediaNode(m) {
    if (m.type === 'image') {
      const img = document.createElement('img');
      img.src = m.src;
      img.alt = m.alt || '';
      return img;
    }
    if (m.type === 'audio') {
      const audio = document.createElement('audio');
      audio.controls = true;
      audio.preload = 'metadata';
      audio.src = m.src;
      return audio;
    }
    const placeholder = document.createElement('button');
    placeholder.type = 'button';
    placeholder.className = 'video-lazy-placeholder';
    placeholder.textContent = '▶ Play video';
    placeholder.setAttribute('aria-label', `Play ${m.alt || 'video'}`);
    placeholder.style.alignItems = 'center';
    placeholder.style.background = '#050608';
    placeholder.style.border = '0';
    placeholder.style.color = '#fff';
    placeholder.style.cursor = 'pointer';
    placeholder.style.display = 'flex';
    placeholder.style.font = '600 14px system-ui, sans-serif';
    placeholder.style.justifyContent = 'center';
    placeholder.style.minHeight = '180px';
    placeholder.style.aspectRatio = '16 / 9';
    placeholder.style.padding = '24px';
    placeholder.style.width = '100%';
    placeholder.addEventListener('click', () => {
      const video = document.createElement('video');
      video.controls = true;
      video.preload = 'metadata';
      video.playsInline = true;
      video.src = m.src;
      placeholder.replaceWith(video);
      video.play().catch((error) => {
        video.setAttribute('data-playback-error', error.name || 'unknown');
      });
    }, {once: true});
    return placeholder;
  }

  // ---- selection helpers (manual save via Ctrl+S / Cmd+S) ----
  function chooseVariant(id, filename, btn) {
    if (selections[id] === filename) return;
    selections[id] = filename;
    // clear other selected buttons that share the same asset id
    document.querySelectorAll('.select-toggle.selected').forEach((b) => {
      if (b.getAttribute('data-id') === id && b !== btn) {
        b.classList.remove('selected');
        b.textContent = 'Select';
      }
    });
    btn.classList.add('selected');
    btn.textContent = '✓ Selected';
    updateSelStatus();
  }

  function updateSelStatus() {
    if (!selStatus) return;
    const n = Object.keys(selections).length;
    selStatus.textContent = n
      ? n + ' of ' + selIds.length + ' assets selected — press Ctrl+S (⌘S) to save.'
      : 'Pick variants, then press Ctrl+S (⌘S) to save.';
  }

  async function saveSelections() {
    if (!viaServer) return; // read-only in file:// mode
    if (!sessionToken || !expectedRevision) { showToast('Session not ready. Reload the page.', 'error'); return; }
    const n = Object.keys(selections).length;
    if (!n) { showToast('Select at least one variant first.', 'error'); return; }
    selStatus.textContent = 'Saving…';
    try {
      const res = await fetch('/api/select', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Showcase-Token': sessionToken },
        body: JSON.stringify({ selections, expected_revision: expectedRevision }),
      });
      const r = await res.json();
      if (r.ok) {
        expectedRevision = r.revision;
        if (r.canvasSynced === false) {
          selStatus.textContent = 'Selection saved; canvas refresh failed: ' + (r.canvasError || 'unknown error');
          showToast('Selection saved, but the production canvas is stale.', 'error');
          return;
        }
        const errs = r.errors.length;
        selStatus.textContent = 'Saved ' + r.applied.length + ' selection(s)' + (errs ? ' — ' + errs + ' error(s)' : '') + '.';
        if (errs) {
          showToast('Saved ' + r.applied.length + ' selection(s), ' + errs + ' error(s).', 'error');
        } else {
          showToast('Saved ' + r.applied.length + ' selection(s) successfully.', 'success');
        }
        document.dispatchEvent(new Event('showcase-saved'));
      } else {
        showToast('Save failed: ' + (r.error || 'unknown error'), 'error');
        selStatus.textContent = 'Save failed: ' + (r.error || 'unknown error');
      }
    } catch (e) {
      showToast('Save failed: ' + e.message, 'error');
      selStatus.textContent = 'Save failed (is the server running?): ' + e.message;
    }
  }

  // Ctrl+S / Cmd+S to save
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S')) {
      e.preventDefault();
      if (selSave) saveSelections();
    }
  });

  if (selIds.length && viaServer) {
    fetch('/api/session')
      .then((r) => r.json())
      .then((existing) => {
        if (!existing.token || !existing.revision) throw new Error(existing.error || "Session unavailable");
        sessionToken = existing.token;
        expectedRevision = existing.revision;
        for (const k in existing.selections) {
          if (selectable[k] && selectable[k].variants[existing.selections[k]]) selections[k] = existing.selections[k];
        }
        refreshSelectButtons();
        updateSelStatus();
      })
      .catch(error => {
        selStatus.textContent = 'Session unavailable: ' + error.message;
        showToast('Reload after resolving the selection conflict.', 'error');
      });
  }

  function refreshSelectButtons() {
    document.querySelectorAll('.select-toggle').forEach((b) => {
      const id = b.getAttribute('data-id');
      const fn = b.getAttribute('data-filename');
      if (selections[id] === fn) {
        b.classList.add('selected');
        b.textContent = '✓ Selected';
      } else {
        b.classList.remove('selected');
        b.textContent = 'Select';
      }
    });
  }

  // ---- activity log (server mode only) ----
  if (viaServer) {
    const logPanel = el('section', 'log-panel');
    logPanel.id = 'activity-log';
    const logHead = el('div', 'section-head');
    logHead.appendChild(el('h2', null, 'Activity log'));
    logHead.appendChild(el('span', 'count', 'history'));
    logPanel.appendChild(logHead);
    const logList = el('ul', 'log-list');
    logPanel.appendChild(logList);
    document.getElementById('app').appendChild(logPanel);

    function renderLog(entries) {
      logList.textContent = '';
      if (!entries.length) {
        const empty = el('li', 'log-empty', 'No activity yet — selections will appear here.');
        logList.appendChild(empty);
        return;
      }
      for (const e of entries.slice().reverse()) {
        const li = el('li', 'log-entry');
        const ts = el('span', 'log-ts', e.ts);
        const ev = el('span', 'log-event', e.event);
        ev.setAttribute('data-e', e.event || '');
        let detail = '';
        if (e.event === 'select') {
          detail = (e.manifest || '') + '  →  ' + (e.filename || '');
        } else if (e.event === 'save') {
          detail = 'applied ' + (e.applied || []).length + ' of ' + (e.total || 0) + (e.errors && e.errors.length ? ' (' + e.errors.length + ' error)' : '');
        }
        li.appendChild(ts);
        li.appendChild(ev);
        if (detail) li.appendChild(el('span', 'log-detail', detail));
        logList.appendChild(li);
      }
    }

    function refreshActivity() {
      fetch('/api/log')
        .then((r) => r.json())
        .then(renderLog)
        .catch(() => {});
    }
    document.addEventListener('showcase-saved', refreshActivity);
    refreshActivity();
  }
})();
