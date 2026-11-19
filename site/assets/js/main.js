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

// 20x D4: footer "Back to top" — smooth scroll; the href="#top"
// still works without JS.
var toTop = document.querySelector('.back-to-top');
if (toTop) {
  toTop.addEventListener('click', function (e) {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// 10x fix D-14: the menu toggle reads "Menu" even when the menu is open.
// Swap it to a Close state (x icon + "Close" label) while open.
var mobileMenu = document.querySelector('.mobile-menu');
if (mobileMenu) {
  mobileMenu.addEventListener('toggle', function () {
    var open = mobileMenu.open;
    var label = mobileMenu.querySelector('.menu-label');
    var icon = mobileMenu.querySelector('summary span[aria-hidden]');
    var summary = mobileMenu.querySelector('summary');
    if (label) label.textContent = open ? 'Close' : 'Menu';
    if (icon) icon.textContent = open ? '\u00d7' : '\u2630';
    if (summary) summary.setAttribute('aria-label', open ? 'Close menu' : 'Menu');
  });
}
