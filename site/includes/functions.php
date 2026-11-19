<?php
// Fort Myers FL — NEW PHP site. Shared helpers: escaping, dash-stripping,
// segment rendering, JSON-LD builders, page rendering.
// Fresh code written for this site; no text copied from other sites.
require_once __DIR__ . '/../data/pages.php';

function esc($s)
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

// Strip em dashes and en dashes at render time WITHOUT changing any words.
function clean_dashes($s)
{
    $s = str_replace([' — ', ' – ', '— ', '– ', ' —', ' –'], ', ', $s);
    $s = str_replace(['—', '–'], ' ', $s);
    $s = preg_replace('/\s+/', ' ', $s);
    return trim($s);
}

function clean_dashes_html($html)
{
    $html = str_replace([' — ', ' – '], ', ', $html);
    $html = str_replace(['—', '–'], ' ', $html);
    return $html;
}

function plain_text($s)
{
    return clean_dashes(html_entity_decode((string) $s, ENT_QUOTES, 'UTF-8'));
}

function site_url($path)
{
    global $SITE;
    if ($path === '/') {
        return $SITE['url'] . '/';
    }
    return $SITE['url'] . $path;
}

function phone_svg()
{
    return '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>';
}

// Render segments: ['t' => text] or ['t' => anchor, 'href' => '/slug/'].
// - Phone numbers (239-356-3708) become tel: links (chrome, not content).
// - The bare domain msc.fema.gov (written in the paste) links to its https URL.
// - "Describe your water problem" is NOT in the segments: the hero renders
//   it as a link to /contact/ (carried inference from the published site,
//   flagged in the findings — the paste gives no target for it).
function render_segments($segs)
{
    global $SITE;
    $out = '';
    foreach ($segs as $s) {
        $text = $s['t'];
        if (!empty($s['href'])) {
            $out .= '<a href="' . esc($s['href']) . '">' . esc($text) . '</a>';
            continue;
        }
        // split on the phone number and on msc.fema.gov, keep both as links
        $parts = preg_split('/(239-356-3708|msc\.fema\.gov)/', $text, -1, PREG_SPLIT_DELIM_CAPTURE);
        foreach ($parts as $p) {
            if ($p === '239-356-3708') {
                $out .= '<a href="' . esc($SITE['phone_href']) . '">' . esc($p) . '</a>';
            } elseif ($p === 'msc.fema.gov') {
                $out .= '<a href="https://msc.fema.gov" target="_blank" rel="noopener">' . esc($p) . '</a>';
            } else {
                $out .= esc($p);
            }
        }
    }
    return clean_dashes_html($out);
}

function render_phone_text($text)
{
    return render_segments([['t' => $text]]);
}

// --- Media manifest -------------------------------------------------------
// Written by the image worker; may not exist yet. Shape:
// $MEDIA = ['hero' => ['home' => ['src','alt','width','height','srcset']]].
// Missing slots render NO <img> (honestly empty, never a forced photo).
function media_for($kind, $slug)
{
    global $MEDIA;
    if (empty($MEDIA[$kind][$slug])) {
        return null;
    }
    $m = $MEDIA[$kind][$slug];
    if (empty($m['src']) || empty($m['alt'])) {
        return null;
    }
    return $m;
}

function page_hero($slug)
{
    return media_for('hero', $slug === '/' ? 'home' : trim($slug, '/'));
}

// --- FAQ extraction -------------------------------------------------------
function page_faqs($page)
{
    $faqs = [];
    foreach ($page['blocks'] as $b) {
        if ($b['type'] === 'faq') {
            foreach ($b['items'] as $f) {
                $faqs[] = ['q' => plain_text($f['q']), 'a' => plain_text(render_segments_text($f['a']))];
            }
        }
    }
    return $faqs;
}

function render_segments_text($segs)
{
    $t = '';
    foreach ($segs as $s) {
        $t .= $s['t'];
    }
    return $t;
}

// --- JSON-LD --------------------------------------------------------------
function ld_json($graph)
{
    return json_encode(
        ['@context' => 'https://schema.org', '@graph' => $graph],
        JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT
    );
}

function ld_json_object($obj)
{
    return json_encode($obj, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
}

function ld_faq_node($faqs, $canon)
{
    $entities = [];
    foreach ($faqs as $f) {
        $entities[] = [
            '@type' => 'Question',
            'name' => $f['q'],
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f['a']],
        ];
    }
    return ['@type' => 'FAQPage', '@id' => $canon . '#faq', 'mainEntity' => $entities];
}

function ld_breadcrumb_node($crumbs, $canon)
{
    // $crumbs: [['name' => 'Home', 'item' => url], ['name' => 'Services', 'item' => null], ...]
    // GOOGLE RULE (BreadcrumbList): every ListItem needs `position`, `name`
    // and `item` — `item` may be omitted ONLY on the last item. A middle
    // crumb with no URL ("Services" / "Areas" — no such route exists, and no
    // URL may be invented) triggers GSC "Missing field 'item'
    // (in 'itemListElement')" — the old site's error, found live on the new
    // site too. FIX: the JSON-LD drops item-less crumbs and renumbers
    // positions 1..n. The VISIBLE breadcrumb keeps the full trail
    // (Home » Services » H1) exactly as before — only the schema changes.
    $items = [];
    $pos = 0;
    foreach ($crumbs as $c) {
        if (empty($c['item'])) {
            continue;
        }
        $pos++;
        $items[] = ['@type' => 'ListItem', 'position' => $pos, 'name' => $c['name'], 'item' => $c['item']];
    }
    return ['@type' => 'BreadcrumbList', '@id' => $canon . '#breadcrumb', 'itemListElement' => $items];
}

// Normalize the paste's schema at RENDER time (data files stay verbatim):
// Google requires `address` on a LocalBusiness and `datePublished` on an
// Article. Both values come from the user's own pastes — the PostalAddress
// is exactly the About page's (Fort Myers, FL 33901, US; no street address
// exists, none invented), and datePublished equals the paste's own
// dateModified (first publication of this content on this site).
// Without these, GSC reports "Missing field" errors of the same class as
// the old site's "Missing field 'item'" error.
function ld_normalize_given($schema)
{
    if (!is_array($schema)) {
        return $schema;
    }
    $type = $schema['@type'] ?? '';
    if (in_array($type, ['HomeAndConstructionBusiness', 'LocalBusiness'], true) && empty($schema['address'])) {
        $schema['address'] = [
            '@type' => 'PostalAddress',
            'addressLocality' => 'Fort Myers',
            'addressRegion' => 'FL',
            'postalCode' => '33901',
            'addressCountry' => 'US',
        ];
    }
    if ($type === 'Article' && empty($schema['datePublished']) && !empty($schema['dateModified'])) {
        $schema['datePublished'] = $schema['dateModified'];
    }
    return $schema;
}

// Breadcrumb crumbs for an inner page, by group.
// service -> Home » Services » H1 ; area -> Home » Areas » H1 ; guide -> Home » H1.
function page_crumbs($page, $canon)
{
    global $SITE;
    $crumbs = [['name' => 'Home', 'item' => $SITE['url'] . '/']];
    $group = $page['group'] ?? 'service';
    if ($group === 'service') {
        $crumbs[] = ['name' => 'Services', 'item' => null];
    } elseif ($group === 'area') {
        $crumbs[] = ['name' => 'Areas', 'item' => null];
    }
    $crumbs[] = ['name' => plain_text($page['seo']['h1']), 'item' => $canon];
    return $crumbs;
}

function page_h1($page)
{
    return $page['seo']['h1'];
}

// --- Block rendering ------------------------------------------------------
function render_block($b, $page)
{
    switch ($b['type']) {
        case 'hero': {
            $hero = page_hero($page['slug']);
            $img = '';
            if ($hero) {
                $srcset = !empty($hero['srcset'])
                    ? ' srcset="' . esc($hero['srcset']) . '" sizes="100vw"'
                    : '';
                $img = '<img class="hero-img" src="' . esc($hero['src']) . '"' . $srcset
                    . ' alt="' . esc($hero['alt']) . '" width="' . (int) $hero['width'] . '" height="' . (int) $hero['height'] . '"'
                    . ' fetchpriority="high" decoding="async">';
            }
            $areas = render_segments($b['areas']);
            $intro = render_segments($b['intro']);
            return '<section class="hero' . ($hero ? '' : ' hero-no-media') . '">'
                . $img
                . '<div class="hero-scrim"></div>'
                . '<div class="container hero-inner">'
                . '<h1>' . esc($b['h1']) . '</h1>'
                . '<p class="hero-intro">' . $intro . '</p>'
                . '<p class="hero-ctas">'
                . '<a class="btn btn-call" href="tel:+12393563708">' . phone_svg() . ' Call 239-356-3708</a>'
                . '<a class="btn btn-ghost" href="/contact/">Describe your water problem</a>'
                . '</p>'
                . '<p class="hero-areas">' . $areas . '</p>'
                . '</div></section>';
        }
        case 'details':
            $rows = '';
            foreach ($b['rows'] as $r) {
                $rows .= '<div class="detail-row"><dt>' . esc($r['label']) . '</dt><dd>' . render_segments($r['value']) . '</dd></div>';
            }
            return '<section class="details-card"><h2>' . esc($b['heading']) . '</h2>'
                . '<p class="details-sub">' . esc($b['sub']) . '</p>'
                . '<dl class="details-grid">' . $rows . '</dl></section>';
        case 'h2':
            return '<h2>' . esc($b['text']) . '</h2>';
        case 'h3':
            return '<h3>' . esc($b['text']) . '</h3>';
        case 'p':
            return '<p>' . render_segments($b['segs']) . '</p>';
        case 'ul': {
            $items = '';
            foreach ($b['items'] as $it) {
                $items .= '<li>' . render_segments($it) . '</li>';
            }
            return '<ul>' . $items . '</ul>';
        }
        case 'kinds': {
            $cards = '';
            foreach ($b['items'] as $k) {
                $cards .= '<article class="kind-card"><h3>' . esc($k['title']) . '</h3>'
                    . '<p>' . render_segments($k['body']) . '</p></article>';
            }
            return '<div class="kinds-grid">' . $cards . '</div>';
        }
        case 'table': {
            $head = '';
            foreach ($b['head'] as $c) {
                $head .= '<th scope="col">' . render_segments($c) . '</th>';
            }
            // 10x fix D-12: only tables whose last header is a price header
            // ("Rough area range") get the prices class — right-aligned,
            // nowrap price column. Tables whose last column is prose
            // ("Effect on the price", "What to check", ...) are untouched.
            $lastHead = '';
            $lastCell = end($b['head']);
            if (is_array($lastCell)) {
                foreach ($lastCell as $seg) {
                    $lastHead .= $seg['t'] ?? '';
                }
            }
            $wrapClass = str_contains($lastHead, 'Rough area range') ? 'table-wrap prices' : 'table-wrap';
            $rows = '';
            foreach ($b['rows'] as $row) {
                $cells = '';
                foreach ($row as $c) {
                    $cells .= '<td>' . render_segments($c) . '</td>';
                }
                $rows .= '<tr>' . $cells . '</tr>';
            }
            return '<div class="' . $wrapClass . '"><table><thead><tr>' . $head . '</tr></thead><tbody>' . $rows . '</tbody></table></div>';
        }
        case 'steps': {
            $items = '';
            foreach ($b['items'] as $k => $s) {
                $items .= '<li><span class="step-num" aria-hidden="true">' . ($k + 1) . '</span>'
                    . '<h3>' . esc($s['title']) . '</h3>'
                    . '<p>' . render_segments($s['body']) . '</p></li>';
            }
            return '<ol class="steps">' . $items . '</ol>';
        }
        case 'steps-numbered': {
            $items = '';
            foreach ($b['items'] as $k => $s) {
                $items .= '<li><span class="step-num" aria-hidden="true">' . ($k + 1) . '</span>'
                    . '<p>' . render_segments($s) . '</p></li>';
            }
            return '<ol class="steps steps-inline">' . $items . '</ol>';
        }
        case 'steps-rich': {
            // How-it-works: each step is a title + any mix of paras and
            // bullet lists, rendered inside the numbered <li>.
            $items = '';
            foreach ($b['items'] as $k => $s) {
                $inner = '';
                foreach ($s['parts'] as $part) {
                    $inner .= render_block($part, $page);
                }
                $items .= '<li><span class="step-num" aria-hidden="true">' . ($k + 1) . '</span>'
                    . '<h3>' . esc($s['title']) . '</h3>' . $inner . '</li>';
            }
            return '<ol class="steps">' . $items . '</ol>';
        }
        case 'cta-line':
            return '<p class="cta-line"><a class="btn btn-call" href="tel:+12393563708">' . phone_svg() . ' ' . esc($b['text']) . '</a></p>';
        case 'map':
            // Heavy map with a VISIBLE PIN on Fort Myers (city-level only:
            // Fort Myers, FL 33901 — no street address exists, none invented).
            // q=place renders Google's place pin; z=12 keeps the pin and the
            // Caloosahatchee riverfront in frame.
            return '<section class="map-section"><h2 class="map-caption">' . esc($b['caption']) . '</h2>'
                . '<iframe class="map-embed" title="Map: Fort Myers and the Lee County service area" '
                . 'src="https://www.google.com/maps?q=Fort%20Myers%2C%20FL%2033901&z=12&output=embed" '
                . 'width="1240" height="560" loading="lazy" '
                . 'referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></section>';
        case 'faq': {
            $items = '';
            foreach ($b['items'] as $f) {
                $items .= '<details class="faq-item"><summary>' . esc($f['q']) . '</summary>'
                    . '<p>' . render_segments($f['a']) . '</p></details>';
            }
            return '<div class="faq-list">' . $items . '</div>';
        }
        default:
            return '<!-- unknown block: ' . esc($b['type']) . ' -->';
    }
}

function render_page($slug, $page)
{
    global $SITE, $MEDIA;
    $canon = site_url($slug);
    $hero = page_hero($slug);
    $heroUrl = $hero ? site_url($hero['src']) : null;
    $faqs = page_faqs($page);
    $isHome = $slug === '/';
    $isLegal = in_array($slug, ['/privacy-policy/', '/terms/', '/disclaimer/'], true);

    $HEAD = [
        'title' => $page['seo']['title'],
        'description' => $page['seo']['meta'],
        'canonical' => $canon,
        'robots' => $isLegal ? 'noindex, follow' : 'index, follow',
        'og_type' => 'website',
        'og_image' => $heroUrl,
        // The paste's schema, emitted verbatim EXCEPT the render-time
        // normalization in ld_normalize_given() (Google-required fields
        // filled from the user's own data — see that function). Legal pages
        // carry NO schema (none given) — ld_given stays null and the
        // header skips the script entirely.
        'ld_given' => !empty($page['seo']['schema']) ? ld_json_object(ld_normalize_given($page['seo']['schema'])) : null,
        // FAQPage, built from the visible FAQs (second script) — the paste
        // gives no FAQPage node, but "FAQ visible == schema" requires one.
        'ld_faq' => $faqs ? ld_json([ld_faq_node($faqs, $canon)]) : null,
        // BreadcrumbList on inner pages (visible == schema); none on home,
        // none on legal pages (no JSON-LD at all there, per the order).
        'ld_crumb' => (!$isHome && !$isLegal) ? ld_json([ld_breadcrumb_node(page_crumbs($page, $canon), $canon)]) : null,
    ];
    $currentSlug = $slug;
    $isLocation = in_array($slug, $GLOBALS['LOCATION_PAGES'], true);
    require __DIR__ . '/header.php';
    echo '<main id="main" tabindex="-1">';
    // Inner pages: hero (H1 + intro + Call) first, then breadcrumb, then body.
    // (Matches the published site's intro-shift pattern: H1 -> intro -> Call
    // -> breadcrumb.) The first block of an inner page is 'hero-intro' and is
    // consumed by the hero, not rendered again in the body.
    $blocks = $page['blocks'];
    $heroIntro = null;
    if (!$isHome && !empty($blocks) && $blocks[0]['type'] === 'hero-intro') {
        $heroIntro = array_shift($blocks);
    }
    if (!$isHome) {
        $img = '';
        if ($hero) {
            $srcset = !empty($hero['srcset'])
                ? ' srcset="' . esc($hero['srcset']) . '" sizes="100vw"'
                : '';
            $img = '<img class="hero-img" src="' . esc($hero['src']) . '"' . $srcset
                . ' alt="' . esc($hero['alt']) . '" width="' . (int) $hero['width'] . '" height="' . (int) $hero['height'] . '"'
                . ' fetchpriority="high" decoding="async">';
        }
        echo '<section class="hero hero-inner-page' . ($hero ? '' : ' hero-no-media') . '">'
            . $img . '<div class="hero-scrim"></div>'
            . '<div class="container hero-inner">'
            . '<h1>' . esc($page['seo']['h1']) . '</h1>'
            . ($heroIntro ? '<p class="hero-intro">' . render_segments($heroIntro['segs']) . '</p>' : '')
            . '<p class="hero-ctas"><a class="btn btn-call" href="tel:+12393563708">' . phone_svg() . ' Call 239-356-3708</a></p>'
            . '</div></section>';
        // Visible breadcrumb (middle item name-only, no URL invented;
        // the last crumb is the current page: a <span>, never a link to
        // itself — a page must not link to itself from its own body).
        $crumbs = page_crumbs($page, $canon);
        $last = count($crumbs) - 1;
        echo '<nav class="breadcrumb container" aria-label="Breadcrumb"><ol>';
        foreach ($crumbs as $k => $c) {
            if ($k === $last) {
                echo '<li aria-current="page"><span>' . esc($c['name']) . '</span></li>';
            } elseif (!empty($c['item'])) {
                echo '<li><a href="' . esc($c['item']) . '">' . esc($c['name']) . '</a></li>';
            } else {
                echo '<li><span>' . esc($c['name']) . '</span></li>';
            }
            if ($k < $last) {
                echo '<li class="crumb-sep" aria-hidden="true">&raquo;</li>';
            }
        }
        echo '</ol></nav>';
    }
    // 10x fix D-04: the homepage hero was the only inset hero on the site —
    // it rendered inside <div class="container page-body">, floating with
    // white gutters on all four sides. Render it as a direct child of
    // <main> like every other page's hero (same markup, no words change).
    if ($isHome && !empty($blocks) && $blocks[0]['type'] === 'hero') {
        $homeHero = array_shift($blocks);
        echo render_block($homeHero, $page);
    }
    echo '<div class="container page-body">';
    // "Last updated" date line (legal pages only, user-supplied date —
    // chrome, not paste content). At the top of the body, as the copy
    // itself says: 'The "Last updated" date at the top shows when it
    // last changed.' No date line on pages without one (disclaimer).
    if (!empty($page['last_updated'])) {
        echo '<p class="last-updated">Last updated: ' . esc($page['last_updated']) . '</p>';
    }
    foreach ($blocks as $b) {
        echo render_block($b, $page);
    }
    echo '</div></main>';
    require __DIR__ . '/footer.php';
}
