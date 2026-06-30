/* ── TourGuide Nigeria — Main JavaScript ── */

document.addEventListener('DOMContentLoaded', function () {

  // ── Auto-submit filter dropdowns ─────────────────────────────────────────
  document.querySelectorAll('.auto-submit').forEach(function (el) {
    el.addEventListener('change', function () {
      this.closest('form').submit();
    });
  });

  // ── Confirmation dialogs on destructive action forms ──────────────────────
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('submit', function (e) {
      const msg = el.getAttribute('data-confirm') || 'Are you sure?';
      if (!confirm(msg)) {
        e.preventDefault();
      }
    });
  });

  // ── Auto-dismiss alerts after 5 seconds ──────────────────────────────────
  document.querySelectorAll('.alert.alert-dismissible').forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // ── Booking date: enforce future dates client-side ────────────────────────
  const dateInputs = document.querySelectorAll('input[type="date"]');
  dateInputs.forEach(function (input) {
    const today = new Date().toISOString().split('T')[0];
    input.setAttribute('min', today);
    input.addEventListener('change', function () {
      if (this.value && this.value < today) {
        this.value = '';
        const err = document.getElementById('date-error');
        if (err) err.classList.remove('d-none');
      }
    });
  });

  // ── Active nav link highlight ─────────────────────────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(function (link) {
    if (link.getAttribute('href') && currentPath.startsWith(link.getAttribute('href')) && link.getAttribute('href') !== '/') {
      link.classList.add('active');
    }
  });

});
