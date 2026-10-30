(() => {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const fixed = (n, d = 4) => Number(n).toFixed(d);

  // -----------------------------------------------------------------------
  // KaTeX: render formulas after all deferred scripts are available
  // -----------------------------------------------------------------------
  function renderMath() {
    if (typeof window.renderMathInElement !== "function") return;
    window.renderMathInElement(document.body, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "\\[", right: "\\]", display: true },
        { left: "\\(", right: "\\)", display: false }
      ],
      throwOnError: false,
      ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"]
    });
  }

  // -----------------------------------------------------------------------
  // Scroll progress + active chapter
  // -----------------------------------------------------------------------
  const meter = $("#scrollMeter");
  const navLinks = $$("[data-nav]");
  const mobileLinks = $$(".mobile-nav a");
  const sections = $$("main section[data-section]");
  let ticking = false;

  function currentSection() {
    if (!sections.length) return null;
    const marker = window.scrollY + Math.min(180, window.innerHeight * 0.28);
    let current = sections[0];
    for (const section of sections) {
      if (section.offsetTop <= marker) current = section;
    }
    return current;
  }

  function activate(id) {
    navLinks.forEach((link) => {
      const on = link.dataset.nav === id;
      link.classList.toggle("is-active", on);
      if (on) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
    mobileLinks.forEach((link) => {
      const on = link.getAttribute("href") === `#${id}`;
      link.classList.toggle("is-active", on);
      if (on) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  }

  function updateScroll() {
    const doc = document.documentElement;
    const max = Math.max(1, doc.scrollHeight - window.innerHeight);
    const ratio = Math.min(1, Math.max(0, window.scrollY / max));
    if (meter) meter.style.width = `${(ratio * 100).toFixed(2)}%`;
    const section = currentSection();
    if (section) activate(section.dataset.section);
    ticking = false;
  }

  function requestScrollUpdate() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(updateScroll);
  }

  // -----------------------------------------------------------------------
  // Batch calculator
  // -----------------------------------------------------------------------
  const batchN = $("#batchN");
  const batchSize = $("#batchSize");
  const batchCount = $("#batchCount");
  const batchLast = $("#batchLast");
  const batchNote = $("#batchNote");

  function updateBatch() {
    if (!batchN || !batchSize || !batchCount || !batchLast || !batchNote) return;
    const n = Math.max(1, Math.min(100000, Math.floor(Number(batchN.value) || 1)));
    const b = Math.max(1, Math.min(1024, Math.floor(Number(batchSize.value) || 1)));
    batchN.value = String(n);
    batchSize.value = String(b);
    const batches = Math.ceil(n / b);
    const last = n - (batches - 1) * b;
    batchCount.textContent = String(batches);
    batchLast.textContent = String(last);
    if (batches === 1) {
      batchNote.textContent = `${n} < ${b}，只有一个 batch，末批 ${last} 条`;
    } else if (last === b) {
      batchNote.textContent = `${n} = ${batches} × ${b}，末批 ${last} 条`;
    } else {
      batchNote.textContent = `${n} = ${batches - 1} × ${b} + ${last}`;
    }
  }

  [batchN, batchSize].forEach((el) => {
    if (el) el.addEventListener("input", updateBatch);
  });

  // -----------------------------------------------------------------------
  // Threshold simulator
  // -----------------------------------------------------------------------
  const thr = $("#threshold");
  const thrOut = $("#thrOut");
  const mAcc = $("#mAcc");
  const mPrec = $("#mPrec");
  const mRec = $("#mRec");
  const mF1 = $("#mF1");
  const cells = {
    tp: $("#cellTP strong"),
    fp: $("#cellFP strong"),
    fn: $("#cellFN strong"),
    tn: $("#cellTN strong")
  };
  const predictions = Array.isArray(window.TEST_PREDICTIONS) ? window.TEST_PREDICTIONS : [];

  function updateThreshold() {
    if (!thr) return;
    const t = Number(thr.value);
    if (thrOut) thrOut.textContent = t.toFixed(2);
    if (!predictions.length) return;

    let tp = 0, fp = 0, fn = 0, tn = 0;
    for (const row of predictions) {
      const positive = row.p >= t;
      if (row.y === 1) {
        if (positive) tp += 1;
        else fn += 1;
      } else {
        if (positive) fp += 1;
        else tn += 1;
      }
    }
    const total = predictions.length;
    const acc = (tp + tn) / total;
    const precision = tp + fp ? tp / (tp + fp) : 0;
    const recall = tp + fn ? tp / (tp + fn) : 0;
    const f1 = precision + recall ? (2 * precision * recall) / (precision + recall) : 0;

    if (mAcc) mAcc.textContent = fixed(acc);
    if (mPrec) mPrec.textContent = fixed(precision);
    if (mRec) mRec.textContent = fixed(recall);
    if (mF1) mF1.textContent = fixed(f1);
    if (cells.tp) cells.tp.textContent = String(tp);
    if (cells.fp) cells.fp.textContent = String(fp);
    if (cells.fn) cells.fn.textContent = String(fn);
    if (cells.tn) cells.tn.textContent = String(tn);
  }

  if (thr) {
    thr.addEventListener("input", updateThreshold);
    const resetThr = $("#resetThr");
    if (resetThr) {
      resetThr.addEventListener("click", () => {
        thr.value = "0.5";
        updateThreshold();
      });
    }
  }

  // -----------------------------------------------------------------------
  // Prompt builder
  // -----------------------------------------------------------------------
  const promptFields = ["pRole", "pTask", "pContext", "pConstraint", "pOutput"].map((id) => $(`#${id}`));
  const promptOutput = $("#promptOutput");
  const copyPrompt = $("#copyPrompt");

  function updatePrompt() {
    if (!promptOutput) return;
    const [role, task, context, constraint, output] = promptFields.map((el) => (el ? el.value.trim() : ""));
    promptOutput.textContent =
      `角色：${role || "（未填写）"}\n` +
      `任务：${task || "（未填写）"}\n` +
      `上下文：${context || "（未填写）"}\n` +
      `约束：${constraint || "（未填写）"}\n` +
      `输出：${output || "（未填写）"}\n` +
      `自检：先复述验收标准；运行 verify_submission.py，并报告失败项。`;
  }

  promptFields.forEach((el) => {
    if (el) el.addEventListener("input", updatePrompt);
  });

  function fallbackCopy(text) {
    const area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    let ok = false;
    try { ok = document.execCommand("copy"); } catch (_) { ok = false; }
    document.body.removeChild(area);
    return ok;
  }

  if (copyPrompt) {
    copyPrompt.addEventListener("click", async () => {
      const text = promptOutput ? promptOutput.textContent : "";
      let ok = false;
      if (navigator.clipboard && window.isSecureContext) {
        try {
          await navigator.clipboard.writeText(text);
          ok = true;
        } catch (_) { ok = false; }
      }
      if (!ok) ok = fallbackCopy(text);
      const old = copyPrompt.textContent;
      copyPrompt.textContent = ok ? "已复制" : "请手动选择";
      copyPrompt.setAttribute("aria-live", "polite");
      window.setTimeout(() => { copyPrompt.textContent = old; }, 1600);
    });
  }

  // -----------------------------------------------------------------------
  // Checklist
  // -----------------------------------------------------------------------
  const checkKey = "lr-teaching-checklist-v1";
  const checks = $$("#checklist input[type='checkbox']");
  const checkCount = $("#checkCount");
  const checkBar = $("#checkBar");

  function readChecks() {
    try {
      const raw = window.localStorage.getItem(checkKey);
      return raw ? new Set(JSON.parse(raw)) : new Set();
    } catch (_) {
      return new Set();
    }
  }

  function saveChecks() {
    try {
      window.localStorage.setItem(checkKey, JSON.stringify(checks.filter((c) => c.checked).map((c) => c.dataset.key)));
    } catch (_) { /* file:// or private mode: keep in-memory only */ }
  }

  function renderChecks() {
    const done = checks.filter((c) => c.checked).length;
    if (checkCount) checkCount.textContent = `${done} / ${checks.length}`;
    if (checkBar) checkBar.style.width = `${(done / Math.max(1, checks.length)) * 100}%`;
  }

  function initChecks() {
    const saved = readChecks();
    checks.forEach((checkbox) => {
      checkbox.checked = saved.has(checkbox.dataset.key);
      checkbox.addEventListener("change", () => {
        saveChecks();
        renderChecks();
      });
    });
    renderChecks();
  }

  const resetChecks = $("#resetChecks");
  if (resetChecks) {
    resetChecks.addEventListener("click", () => {
      checks.forEach((checkbox) => { checkbox.checked = false; });
      saveChecks();
      renderChecks();
    });
  }

  // -----------------------------------------------------------------------
  // Quiz
  // -----------------------------------------------------------------------
  const quiz = $("#quiz");
  const quizResult = $("#quizResult");
  const quizReset = $("#quizReset");

  function resetQuiz() {
    if (!quiz) return;
    $$("fieldset", quiz).forEach((fieldset) => {
      fieldset.classList.remove("is-correct", "is-wrong");
      const explain = $(".explain", fieldset);
      if (explain) explain.hidden = true;
      $$("input[type='radio']", fieldset).forEach((input) => { input.checked = false; });
    });
    if (quizResult) quizResult.textContent = "";
  }

  if (quiz) {
    quiz.addEventListener("submit", (event) => {
      event.preventDefault();
      const fieldsets = $$("fieldset", quiz);
      let score = 0;
      fieldsets.forEach((fieldset) => {
        const answer = fieldset.dataset.answer;
        const checked = $("input[type='radio']:checked", fieldset);
        fieldset.classList.remove("is-correct", "is-wrong");
        const explain = $(".explain", fieldset);
        if (checked && checked.value === answer) {
          score += 1;
          fieldset.classList.add("is-correct");
        } else {
          fieldset.classList.add("is-wrong");
        }
        if (explain) explain.hidden = false;
      });
      if (quizResult) {
        quizResult.textContent = score === fieldsets.length
          ? `全对：${score} / ${fieldsets.length}。可以开始做实验了。`
          : `答对 ${score} / ${fieldsets.length}。先看错题解释，再回到对应章节。`;
      }
    });
  }

  if (quizReset) quizReset.addEventListener("click", resetQuiz);

  // -----------------------------------------------------------------------
  // Init
  // -----------------------------------------------------------------------
  document.addEventListener("DOMContentLoaded", () => {
    renderMath();
    updateBatch();
    updateThreshold();
    updatePrompt();
    initChecks();
    updateScroll();
    window.addEventListener("scroll", requestScrollUpdate, { passive: true });
    window.addEventListener("resize", requestScrollUpdate);
  });
})();
