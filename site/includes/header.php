<!DOCTYPE html>
<?php global $NAV_SERVICES, $NAV_SERVICES_MENU, $NAV_AREAS, $SITE;
// 20x-fixes D-V2: which dropdown section (if any) the current page sits
// in, so the closed Services/Areas summary can show the current-section
// marker. Pages not in either dropdown (guides, legal, about, home)
// get no section marker.
$inServices = false; $inAreas = false;
foreach ($NAV_SERVICES as $s) { if ($currentSlug === $s['href']) { $inServices = true; break; } }
foreach ($NAV_AREAS as $s) { if ($currentSlug === $s['href']) { $inAreas = true; break; } }
?>
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
<?php endif; ?>
<?php $ogUrl = $HEAD['canonical'] ?? ($HEAD['og_url'] ?? null); ?>
<?php if (!empty($ogUrl)): ?>
<meta property="og:url" content="<?= esc($ogUrl) ?>">
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
<link rel="preload" href="/assets/fonts/archivoblack-400.woff2" as="font" type="font/woff2" crossorigin fetchpriority="high">
<link rel="preload" href="/assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin fetchpriority="high">
<!-- Stylesheet cache-bust: assets are served Cache-Control 1 year
     immutable (out/_headers), so a CSS-only change NEVER reaches a
     browser that already cached the file, the 2026-11-19 kinds-text
     and details-icon defects were exactly this (new HTML + old CSS).
     Bump the ?v= number on EVERY CSS change, or the fix stays local. -->
<link rel="stylesheet" href="/assets/css/styles.css?v=5">
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
<body id="top">
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header" id="site-header">
  <div class="container header-inner">
    <?php if ($currentSlug === '/'): ?>
    <span class="brand" aria-current="page" aria-label="Fort Myers Water Damage - home">
    <?php else: ?>
    <a class="brand" href="/" aria-label="Fort Myers Water Damage - home">
    <?php endif; ?>
      <span class="brand-mark" aria-hidden="true"><svg width="34" height="34" viewBox="0 0 34 34" fill="none"><path d="M17 3C17 3 7 13.5 7 20.5a10 10 0 0 0 20 0C27 13.5 17 3 17 3Z" fill="#E8590C"/><path d="M12 21a5 5 0 0 0 5 5" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg></span>
      <span class="brand-text"><span class="brand-name">Fort Myers Water Damage</span>
      <span class="brand-tag">24/7 &middot; FL</span></span>
    <?php if ($currentSlug === '/'): ?>
    </span>
    <?php else: ?>
    </a>
    <?php endif; ?>
    <nav class="site-nav" aria-label="Main navigation">
      <details class="nav-services<?= $inServices ? ' nav-section-current' : '' ?>">
        <summary<?= $inServices ? ' aria-current="true"' : '' ?>>Services</summary>
        <div class="nav-dropdown">
          <?php foreach ($NAV_SERVICES_MENU as $s): ?>
          <?php if ($currentSlug === $s['href']): ?>
          <span class="nav-current" aria-current="page"><?= esc($s['label']) ?></span>
          <?php else: ?>
          <a href="<?= esc($s['href']) ?>"><?= esc($s['label']) ?></a>
          <?php endif; ?>
          <?php endforeach; ?>
        </div>
      </details>
      <?php if ($currentSlug === '/cost/'): ?>
      <span class="nav-current-top" aria-current="page">Cost</span>
      <?php else: ?>
      <a href="/cost/">Cost</a>
      <?php endif; ?>
      <details class="nav-services<?= $inAreas ? ' nav-section-current' : '' ?>">
        <summary<?= $inAreas ? ' aria-current="true"' : '' ?>>Areas</summary>
        <div class="nav-dropdown">
          <?php foreach ($NAV_AREAS as $s): ?>
          <?php if ($currentSlug === $s['href']): ?>
          <span class="nav-current" aria-current="page"><?= esc($s['label']) ?></span>
          <?php else: ?>
          <a href="<?= esc($s['href']) ?>"><?= esc($s['label']) ?></a>
          <?php endif; ?>
          <?php endforeach; ?>
        </div>
      </details>
      <?php if ($currentSlug === '/contact/'): ?>
      <span class="nav-current-top" aria-current="page">Contact</span>
      <?php else: ?>
      <a href="/contact/">Contact</a>
      <?php endif; ?>
    </nav>
    <a class="btn btn-call header-call" href="tel:+12393563708"><span class="call-full"><?= phone_svg() ?> Call 239-356-3708</span><span class="call-short" aria-hidden="true">239-356-3708</span></a>
    <a class="header-call-icon" href="tel:+12393563708" aria-label="Call 239-356-3708"><?= phone_svg() ?></a>
    <details class="mobile-menu">
      <summary aria-label="Menu"><span aria-hidden="true">&#9776;</span><span class="menu-label">Menu</span></summary>
      <div class="mobile-menu-panel">
        <?php if ($currentSlug === '/'): ?>
        <span class="nav-current" aria-current="page">Home</span>
        <?php else: ?>
        <a href="/">Home</a>
        <?php endif; ?>
        <span class="nav-group">Services</span>
        <?php foreach ($NAV_SERVICES_MENU as $s): ?>
        <?php if ($currentSlug === $s['href']): ?>
        <span class="nav-current" aria-current="page"><?= esc($s['label']) ?></span>
        <?php else: ?>
        <a href="<?= esc($s['href']) ?>"><?= esc($s['label']) ?></a>
        <?php endif; ?>
        <?php endforeach; ?>
        <?php if ($currentSlug === '/cost/'): ?>
        <span class="nav-current" aria-current="page">Cost</span>
        <?php else: ?>
        <a href="/cost/">Cost</a>
        <?php endif; ?>
        <span class="nav-group">Areas</span>
        <?php foreach ($NAV_AREAS as $s): ?>
        <?php if ($currentSlug === $s['href']): ?>
        <span class="nav-current" aria-current="page"><?= esc($s['label']) ?></span>
        <?php else: ?>
        <a href="<?= esc($s['href']) ?>"><?= esc($s['label']) ?></a>
        <?php endif; ?>
        <?php endforeach; ?>
        <?php if ($currentSlug === '/contact/'): ?>
        <span class="nav-current" aria-current="page">Contact</span>
        <?php else: ?>
        <a href="/contact/">Contact</a>
        <?php endif; ?>
        <a class="btn btn-call" href="tel:+12393563708"><?= phone_svg() ?> Call 239-356-3708</a>
      </div>
    </details>
  </div>
</header>
