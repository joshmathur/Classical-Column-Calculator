/* ── homepage.js ─────────────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', () => {

  // ── Staggered row reveal ──────────────────────────────────────
  // CA_HAS_RESULTS is set inline in the template before this script loads
  if (typeof CA_HAS_RESULTS !== 'undefined' && CA_HAS_RESULTS) {
    const rows = document.querySelectorAll('.ca-row');
    rows.forEach((row, i) => {
      setTimeout(() => row.classList.add('in'), 80 + i * 45);
    });
  }

  // ── Scroll grid into view after POST ─────────────────────────
  if (typeof CA_HAS_RESULTS !== 'undefined' && CA_HAS_RESULTS) {
    const grid = document.querySelector('.ca-grid');
    if (grid) {
      setTimeout(() => {
        grid.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 100);
    }
  }

  // ── Input: remove validation styles on change ─────────────────
  const inputs = document.querySelectorAll('.ca-input');
  inputs.forEach(input => {
    input.addEventListener('input', () => {
      input.style.borderColor = '';
    });
  });

  // ── Button: loading state on submit ──────────────────────────
  const form = document.getElementById('ca-form');
  const btn  = form ? form.querySelector('.ca-btn span') : null;

  if (form && btn) {
    form.addEventListener('submit', () => {
      btn.textContent = '◆  Calculating…';
    });
  }

});