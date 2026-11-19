<?php global $NAV_SERVICES, $FOOTER_EXPLORE, $FOOTER_AREAS, $SITE; ?>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <p class="footer-brand-name">Fort Myers Water Damage <span>Restoration Pros</span></p>
      <p>Fort Myers, FL 33901 &middot; Lee County, Florida</p>
      <p class="footer-hours">Answered 24/7, including holidays and the days after a storm.</p>
      <a class="btn btn-call" href="tel:+12393563708"><?= phone_svg() ?> Call 239-356-3708</a>
      <?php if (!$isLocation): ?>
      <iframe class="footer-map" title="Map: Fort Myers and the Lee County service area" src="https://www.google.com/maps?q=Fort%20Myers%2C%20FL%2033901&z=12&output=embed" width="560" height="280" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      <?php endif; ?>
    </div>
    <nav class="footer-col" aria-label="Services">
      <h3>Services</h3>
      <?php foreach ($NAV_SERVICES as $s): ?>
      <a href="<?= esc($s['href']) ?>"<?= ($currentSlug === $s['href']) ? ' aria-current="page"' : '' ?>><?= esc($s['label']) ?></a>
      <?php endforeach; ?>
    </nav>
    <nav class="footer-col" aria-label="Explore">
      <h3>Explore</h3>
      <?php foreach ($FOOTER_EXPLORE as $s): ?>
      <a href="<?= esc($s['href']) ?>"<?= ($currentSlug === $s['href']) ? ' aria-current="page"' : '' ?>><?= esc($s['label']) ?></a>
      <?php endforeach; ?>
    </nav>
    <nav class="footer-col" aria-label="Areas we serve">
      <h3>Areas We Serve</h3>
      <?php foreach ($FOOTER_AREAS as $s): ?>
      <a href="<?= esc($s['href']) ?>"<?= ($currentSlug === $s['href']) ? ' aria-current="page"' : '' ?>><?= esc($s['label']) ?></a>
      <?php endforeach; ?>
      <p class="footer-zips">Fort Myers ZIPs 33901 to 33967 &middot; North Fort Myers 33903, 33917</p>
    </nav>
  </div>
  <div class="footer-base">
    <div class="container footer-base-inner">
      <span>&copy; <?= date('Y') ?> Fort Myers Water Damage Restoration Pros</span>
      <span>24/7 Emergency Response &middot; Lee County, FL</span>
      <a href="tel:+12393563708">239-356-3708</a>
    </div>
  </div>
</footer>
<a class="call-bar" href="tel:+12393563708" aria-label="Call 239-356-3708 now"><span aria-hidden="true">&#9742;</span> Call 239-356-3708</a>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
