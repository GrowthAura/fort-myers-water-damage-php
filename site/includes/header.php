<!DOCTYPE html>
<?php global $NAV_SERVICES, $NAV_AREAS, $SITE; ?>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0A2E38">
<meta property="og:locale" content="en_US">
<title><?= esc($HEAD['title']) ?></title>
<meta name="description" content="<?= esc($HEAD['description']) ?>">
<?php if (!empty($HEAD['canonical'])): ?>
<link rel="canonical" href="<?= esc($HEAD['canonical']) ?>">
<meta property="og:url" content="<?= esc($HEAD['canonical']) ?>">
<?php endif; ?>
<meta name="robots" content="<?= esc($HEAD['robots'] ?? 'index, follow') ?>">
<meta property="og:type" content="<?= esc($HEAD['og_type'] ?? 'website') ?>">
<meta property="og:title" content="<?= esc($HEAD['title']) ?>">
<meta property="og:description" content="<?= esc($HEAD['description']) ?>">
<meta property="og:site_name" content="Fort Myers Water Damage Restoration Pros">
<?php if (!empty($HEAD['og_image'])): ?>
<meta property="og:image" content="<?= esc($HEAD['og_image']) ?>">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="<?= esc($HEAD['og_image']) ?>">
<?php else: ?>
<meta name="twitter:card" content="summary">
<?php endif; ?>
<meta name="twitter:title" content="<?= esc($HEAD['title']) ?>">
<meta name="twitter:description" content="<?= esc($HEAD['description']) ?>">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/archivoblack-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/styles.css">
<?php if (!empty($HEAD['ld_given'])): ?>
<script type="application/ld+json"><?= $HEAD['ld_given'] ?></script>
<?php endif; ?>
<?php if (!empty($HEAD['ld_faq'])): ?>
<script type="application/ld+json"><?= $HEAD['ld_faq'] ?></script>
<?php endif; ?>
<?php if (!empty($HEAD['ld_crumb'])): ?>
<script type="application/ld+json"><?= $HEAD['ld_crumb'] ?></script>
<?php endif; ?>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header" id="site-header">
  <div class="container header-inner">
    <a class="brand" href="/"<?= ($currentSlug === '/') ? ' aria-current="page"' : '' ?> aria-label="Fort Myers Water Damage Restoration Pros - home">
      <span class="brand-mark" aria-hidden="true"><svg width="34" height="34" viewBox="0 0 34 34" fill="none"><path d="M17 3C17 3 7 13.5 7 20.5a10 10 0 0 0 20 0C27 13.5 17 3 17 3Z" fill="#E8590C"/><path d="M12 21a5 5 0 0 0 5 5" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg></span>
      <span class="brand-text"><span class="brand-name">Fort Myers Water Damage <span class="brand-city">Restoration Pros</span></span>
      <span class="brand-tag">24/7 &middot; Lee County, FL</span></span>
    </a>
    <nav class="site-nav" aria-label="Main navigation">
      <details class="nav-services">
        <summary>Services</summary>
        <div class="nav-dropdown">
          <?php foreach ($NAV_SERVICES as $s): ?>
          <a href="<?= esc($s['href']) ?>"<?= ($currentSlug === $s['href']) ? ' aria-current="page"' : '' ?>><?= esc($s['label']) ?></a>
          <?php endforeach; ?>
        </div>
      </details>
      <a href="/cost/"<?= ($currentSlug === '/cost/') ? ' aria-current="page"' : '' ?>>Cost</a>
      <details class="nav-services">
        <summary>Areas</summary>
        <div class="nav-dropdown">
          <?php foreach ($NAV_AREAS as $s): ?>
          <a href="<?= esc($s['href']) ?>"<?= ($currentSlug === $s['href']) ? ' aria-current="page"' : '' ?>><?= esc($s['label']) ?></a>
          <?php endforeach; ?>
        </div>
      </details>
      <a href="/contact/"<?= ($currentSlug === '/contact/') ? ' aria-current="page"' : '' ?>>Contact</a>
    </nav>
    <a class="btn btn-call header-call" href="tel:+12393563708"><span class="call-full"><?= phone_svg() ?> Call 239-356-3708</span><span class="call-short" aria-hidden="true">239-356-3708</span></a>
    <details class="mobile-menu">
      <summary aria-label="Menu"><span aria-hidden="true">&#9776;</span><span class="menu-label">Menu</span></summary>
      <div class="mobile-menu-panel">
        <a href="/"<?= ($currentSlug === '/') ? ' aria-current="page"' : '' ?>>Home</a>
        <span class="nav-group">Services</span>
        <?php foreach ($NAV_SERVICES as $s): ?>
        <a href="<?= esc($s['href']) ?>"<?= ($currentSlug === $s['href']) ? ' aria-current="page"' : '' ?>><?= esc($s['label']) ?></a>
        <?php endforeach; ?>
        <a href="/cost/"<?= ($currentSlug === '/cost/') ? ' aria-current="page"' : '' ?>>Cost</a>
        <span class="nav-group">Areas</span>
        <?php foreach ($NAV_AREAS as $s): ?>
        <a href="<?= esc($s['href']) ?>"<?= ($currentSlug === $s['href']) ? ' aria-current="page"' : '' ?>><?= esc($s['label']) ?></a>
        <?php endforeach; ?>
        <a href="/contact/"<?= ($currentSlug === '/contact/') ? ' aria-current="page"' : '' ?>>Contact</a>
        <a class="btn btn-call" href="tel:+12393563708"><?= phone_svg() ?> Call 239-356-3708</a>
      </div>
    </details>
  </div>
</header>
