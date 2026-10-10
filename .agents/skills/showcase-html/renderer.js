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
  header.appendChild(el('h1', null, data.title));
  if (data.lede) header.appendChild(el('p', 'lede', data.lede));
  const badgeItems = (data.badges || [])
    .map(b => (typeof b === 'string' ? {value: b} : b || {}))
    .filter(b => b.value);
  if (badgeItems.length) {
    const badges = el('div', 'badges');
    for (const b of badgeItems) {
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

  function linkRow(pairs) {
    const links = el('div', 'canvas-links');
    for (const [label, path] of pairs) {
      const href = projectHref(path);
      if (!href) continue;
      const link = el('a', null, label);
      link.href = href;
      links.appendChild(link);
    }
    return links.childNodes.length ? links : null;
  }

  function buildLock(kind, lock) {
    const row = el('div', 'canvas-lock');
    const line = el('div', 'canvas-lock-line');
    line.appendChild(el('strong', null, kind.replaceAll('_', ' ') + ': ' + (lock.result || 'pending')));
    if (lock.actor) line.appendChild(el('span', null, ' · ' + lock.actor));
    row.appendChild(line);
    const links = linkRow([
      ['Accepted artifact', lock.artifact_path],
      ['Review', lock.review_path],
      ['Decision', lock.decision_id && 'decisions/' + lock.decision_id + '.json'],
    ]);
    if (lock.reason || links) {
      const evidence = document.createElement('details');
      evidence.className = 'canvas-evidence';
      evidence.appendChild(el('summary', null, 'Evidence'));
      if (lock.reason) evidence.appendChild(el('p', null, lock.reason));
      if (links) evidence.appendChild(links);
      row.appendChild(evidence);
    }
    return row;
  }

  function buildLockCandidate(candidate, stage, canvas, mode) {
    const row = el('div', 'canvas-lock-candidate');
    row.appendChild(el('strong', null, candidate.lock_kind.replaceAll('_', ' ') + ' candidate'));
    row.appendChild(el('p', null, candidate.reason));
    const artifactHref = projectHref(candidate.artifact_path);
    const links = linkRow([['Candidate', candidate.artifact_path], ['Review', candidate.review_path]]);
    if (links) row.appendChild(links);
    if (artifactHref) {
      const mediaType = /\.(mp4|mov|mkv|webm)$/i.test(candidate.artifact_path) ? 'video'
        : /\.(wav|mp3|m4a|aac|flac)$/i.test(candidate.artifact_path) ? 'audio' : 'image';
      const preview = el('div', 'canvas-source-media');
      preview.appendChild(mediaNode({type: mediaType, src: artifactHref, alt: candidate.artifact_path}));
      row.appendChild(preview);
    }
    if (viaServer && mode.mode === 'ask_for_approval' && stage.id === canvas.currentStage
        && !((stage.locks || {})[candidate.lock_kind])) {
      const button = el('button', 'canvas-lock-approve', 'Approve ' + candidate.lock_kind.replaceAll('_', ' '));
      button.type = 'button';
      button.addEventListener('click', () => approveStageCandidate(candidate, button));
      row.appendChild(button);
    }
    return row;
  }

  function buildDocumentSource(source) {
    const label = source.label || source.path;
    if (source.content == null) {
      const row = el('div', 'canvas-source');
      row.appendChild(el('span', 'canvas-source-kind', source.kind || 'source'));
      const link = el('a', null, label);
      link.href = encodeURI(source.path);
      row.appendChild(link);
      return row;
    }
    const row = document.createElement('details');
    row.className = 'canvas-source';
    const summary = el('summary');
    summary.appendChild(el('span', 'canvas-source-kind', source.kind || 'source'));
    summary.appendChild(el('span', 'canvas-source-label', label));
    row.appendChild(summary);
    const open = el('a', 'canvas-source-open', 'Open file');
    open.href = encodeURI(source.path);
    row.appendChild(open);
    const content = el('pre');
    content.textContent = source.content;
    row.appendChild(content);
    return row;
  }

  function buildStageBody(card, stage, canvas, mode) {
    if (stage.summary) card.appendChild(el('p', 'canvas-summary', stage.summary));
    if (stage.locks && Object.keys(stage.locks).length) {
      const locks = el('div', 'canvas-locks');
      for (const [kind, lock] of Object.entries(stage.locks)) locks.appendChild(buildLock(kind, lock));
      card.appendChild(locks);
    }
    if (Array.isArray(stage.lockCandidates) && stage.lockCandidates.length) {
      const candidates = el('div', 'canvas-lock-candidates');
      for (const candidate of stage.lockCandidates) {
        candidates.appendChild(buildLockCandidate(candidate, stage, canvas, mode));
      }
      card.appendChild(candidates);
    }
    const sources = stage.sources || [];
    const mediaSources = sources.filter(source => ['image', 'video', 'audio'].includes(source.kind));
    const documentSources = sources.filter(source => !mediaSources.includes(source));
    if (mediaSources.length) {
      const strip = el('div', 'canvas-figures');
      for (const source of mediaSources) {
        const figure = el('figure', 'canvas-figure');
        figure.appendChild(mediaNode({type: source.kind, src: source.path, alt: source.label || source.path}));
        figure.appendChild(el('figcaption', null, source.label || source.path));
        strip.appendChild(figure);
      }
      card.appendChild(strip);
    }
    if (documentSources.length) {
      const docs = document.createElement('details');
      docs.className = 'canvas-sources';
      docs.appendChild(el('summary', null, 'Documents (' + documentSources.length + ')'));
      const list = el('div', 'canvas-source-list');
      for (const source of documentSources) list.appendChild(buildDocumentSource(source));
      docs.appendChild(list);
      card.appendChild(docs);
    }
  }

  function buildDecisions() {
    const selected = data.currentSelections || {};
    const entries = Object.entries(selected);
    if (!entries.length) return null;
    const decisions = document.createElement('details');
    decisions.className = 'canvas-decisions';
    decisions.appendChild(el('summary', null, 'Selected variants (' + entries.length + ')'));
    const list = el('div', 'canvas-decision-list');
    for (const [assetId, filename] of entries) {
      const evidence = (data.selectionEvidence || {})[assetId] || {};
      const row = el('div', 'canvas-decision');
      row.appendChild(el('strong', null, assetId + ': ' + filename));
      if (evidence.decision_id) {
        row.appendChild(el('span', null,
          ' · ' + (evidence.result || evidence.status || 'selected') + ' by ' + (evidence.actor || 'unknown')));
      }
      if (evidence.reason) row.appendChild(el('p', null, evidence.reason));
      const links = linkRow([['Review', evidence.review_path], ['Decision', evidence.decision_path]]);
      if (links) row.appendChild(links);
      list.appendChild(row);
    }
    decisions.appendChild(list);
    return decisions;
  }

  function buildProductionCanvas(canvas) {
    const section = el('section', 'canvas-board');
    section.id = 'production-canvas';
    const mode = data.approvalMode || {};
    const heading = el('div', 'canvas-heading');
    heading.appendChild(el('h2', null, 'Production canvas'));
    const modeBadge = el('div', 'canvas-mode');
    modeBadge.appendChild(el('strong', null,
      mode.mode === 'ask_for_approval' ? 'Ask for approval' : 'Approve for me'));
    heading.appendChild(modeBadge);
    section.appendChild(heading);

    const stages = el('div', 'canvas-stages');
    for (const [index, stage] of (canvas.stages || []).entries()) {
      const status = stage.status || 'pending';
      const isCurrent = stage.id === canvas.currentStage;
      const card = document.createElement('details');
      card.className = 'canvas-stage status-' + status + (isCurrent ? ' current' : '');
      card.open = isCurrent || ['active', 'review', 'blocked'].includes(status);
      const top = el('summary', 'canvas-stage-top');
      top.appendChild(el('span', 'canvas-step', String(index + 1).padStart(2, '0')));
      top.appendChild(el('h3', null, stage.label || stage.id));
      top.appendChild(el('span', 'canvas-status', status));
      card.appendChild(top);
      buildStageBody(card, stage, canvas, mode);
      if (card.childNodes.length === 1) card.classList.add('canvas-stage-empty');
      stages.appendChild(card);
    }
    section.appendChild(stages);
    const decisions = buildDecisions();
    if (decisions) section.appendChild(decisions);
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
    if (c.title) body.appendChild(el('h3', 'title', c.title));
    if (c.sub) body.appendChild(el('div', 'sub', c.sub));
    const more = el('div', 'card-more');
    if (c.chips && c.chips.length) {
      const meta = el('div', 'meta');
      for (const ch of c.chips) meta.appendChild(el('span', 'chip', ch));
      more.appendChild(meta);
    }
    if (c.refs && c.refs.length) {
      const refs = el('div', 'refs');
      refs.appendChild(el('h4', 'refs-label', 'Elements used'));
      for (const r of c.refs) {
        const ref = el('div', 'ref');
        ref.appendChild(el('span', 'dot ' + (r.kind || 'vid')));
        const name = r.path ? el('a', 'ref-name', r.name) : el('span', 'ref-name', r.name);
        if (r.path) name.href = encodeURI(r.path);
        ref.appendChild(name);
        if (r.role) ref.appendChild(el('span', 'ref-role', r.role));
        refs.appendChild(ref);
      }
      more.appendChild(refs);
    }
    if (c.prompt) {
      more.appendChild(el('h4', 'prompt-label', 'Prompt'));
      const pre = el('pre');
      pre.textContent = c.prompt;
      more.appendChild(pre);
    }
    if (c.reviewPath) {
      const review = el('a', 'canvas-review-link', 'Candidate review');
      const href = projectHref(c.reviewPath);
      if (href) {
        review.href = href;
        more.appendChild(review);
      }
    }
    if (more.childNodes.length) {
      const details = document.createElement('details');
      details.className = 'card-details';
      details.appendChild(el('summary', null, c.prompt ? 'Prompt & details' : 'Details'));
      details.appendChild(more);
      body.appendChild(details);
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
      if (row.stageTitle) tdStage.appendChild(el('h3', 'stage-title', row.stageTitle));
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

        const takeMore = el('div', 'card-more');
        if (tk.chips && tk.chips.length) {
          const ci = el('div', 'takes-info');
          for (const c of tk.chips) ci.appendChild(el('span', 'chip', c));
          takeMore.appendChild(ci);
        }

        // contact sheet
        if (tk.contactSheet) {
          const cs = document.createElement('img');
          cs.className = 'takes-contact-sheet';
          cs.src = tk.contactSheet;
          cs.alt = 'Contact sheet';
          cs.loading = 'lazy';
          takeMore.appendChild(cs);
        }
        if (tk.reviewPath) {
          const review = el('a', 'canvas-review-link', 'Candidate review');
          const href = projectHref(tk.reviewPath);
          if (href) {
            review.href = href;
            takeMore.appendChild(review);
          }
        }
        if (takeMore.childNodes.length) {
          const takeDetails = document.createElement('details');
          takeDetails.className = 'card-details';
          takeDetails.appendChild(el('summary', null, 'Details'));
          takeDetails.appendChild(takeMore);
          col.appendChild(takeDetails);
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

  async function approveStageCandidate(candidate, button) {
    if (!viaServer || !data.canvasBuild) return;
    button.disabled = true;
    button.textContent = 'Approving…';
    try {
      const sessionResponse = await fetch('/api/session');
      const session = await sessionResponse.json();
      if (!sessionResponse.ok || !session.token || !session.stageRevision) {
        throw new Error(session.error || 'Session unavailable');
      }
      const response = await fetch('/api/stage-lock', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Showcase-Token': session.token },
        body: JSON.stringify({
          candidate: {lock_kind: candidate.lock_kind, artifact_path: candidate.artifact_path},
          canvas_manifest_sha256: data.canvasBuild.manifestSha256,
          expected_revision: session.stageRevision,
        }),
      });
      const result = await response.json();
      if (!response.ok || !result.ok) throw new Error(result.error || 'Approval failed');
      if (result.canvasSynced === false) {
        button.textContent = 'Approved; canvas refresh failed';
        showToast('Approval saved, but the production canvas is stale.', 'error');
        return;
      }
      showToast('Stage lock approved.', 'success');
      location.reload();
    } catch (error) {
      button.disabled = false;
      button.textContent = 'Approve ' + candidate.lock_kind.replaceAll('_', ' ');
      showToast('Approval failed: ' + error.message, 'error');
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
