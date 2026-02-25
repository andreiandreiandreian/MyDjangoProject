(function () {
  function toMinutes(hhmm) {
    const [h, m] = hhmm.split(":").map(Number);
    return h * 60 + m;
  }

  function refreshEndOptions() {
    const startEl = document.querySelector('select[name="start_time"]');
    const endEl = document.querySelector('select[name="end_time"]');
    if (!startEl || !endEl) return;

    const startVal = startEl.value;
    if (!startVal) return;

    const minEnd = toMinutes(startVal) + 60;

    let firstValid = null;
    for (const opt of endEl.options) {
      const optMin = toMinutes(opt.value);
      const valid = optMin >= minEnd;
      opt.disabled = !valid;
      if (valid && firstValid === null) firstValid = opt.value;
    }

    if (endEl.value && endEl.selectedOptions.length) {
      const cur = toMinutes(endEl.value);
      if (cur < minEnd && firstValid) endEl.value = firstValid;
    } else if (firstValid) {
      endEl.value = firstValid;
    }
  }

  document.addEventListener("change", (e) => {
    if (e.target && e.target.matches('select[name="start_time"]')) {
      refreshEndOptions();
    }
  });

  document.addEventListener("DOMContentLoaded", () => {
    refreshEndOptions();
  });
})();