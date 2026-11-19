// Fort Myers PHP site - minimal progressive enhancement.
// Nav + FAQ use native <details>; this only closes menus on navigation.
document.addEventListener('click', function (e) {
  var a = e.target.closest('.mobile-menu-panel a, .nav-dropdown a');
  if (!a) return;
  document.querySelectorAll('details[open]').forEach(function (d) {
    if (d.classList.contains('mobile-menu') || d.classList.contains('nav-services')) {
      d.removeAttribute('open');
    }
  });
});
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    document.querySelectorAll('details[open]').forEach(function (d) { d.removeAttribute('open'); });
  }
});
