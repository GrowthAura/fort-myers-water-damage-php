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

function details_icon($label)
{
    $icons = [
        'phone' => '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
        'map-pin' => '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
        'droplet' => '<path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>',
        'home' => '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
        'clock' => '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
        'camera' => '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
        'shield-check' => '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>',
        'check-circle' => '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
        'alert-triangle' => '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
        'wind' => '<path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/>',
        'file-text' => '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>',
        'users' => '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
        'search' => '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
        'tool' => '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
        'calendar' => '<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
        'tag' => '<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>',
        'target' => '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
        'eye' => '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
        'arrow-right' => '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
        'arrow-up' => '<line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/>',
        'waves' => '<path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>',
        'cloud-rain' => '<polyline points="16 13 16 21"/><polyline points="8 13 8 21"/><polyline points="12 15 12 21"/><path d="M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25"/>',
        'ruler' => '<path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.41 2.41 0 0 1 0-3.4l2.6-2.6a2.41 2.41 0 0 1 3.4 0Z"/><path d="m14.5 12.5 2-2"/><path d="m11.5 9.5 2-2"/><path d="m8.5 6.5 2-2"/><path d="m17.5 15.5 2-2"/>',
        'scale' => '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
        'life-buoy' => '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><line x1="4.93" y1="4.93" x2="9.76" y2="9.76"/><line x1="14.24" y1="14.24" x2="19.07" y2="19.07"/><line x1="14.24" y1="9.76" x2="19.07" y2="4.93"/><line x1="4.93" y1="19.07" x2="9.76" y2="14.24"/>',
        'refresh-cw' => '<polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>',
        'trash-2' => '<polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/>',
        'briefcase' => '<rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
        'coffee' => '<path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/>',
        'layers' => '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
        'square' => '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>',
        'building' => '<rect width="16" height="20" x="4" y="2" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/>',
        'help-circle' => '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
        'info' => '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>',
        'percent' => '<line x1="19" y1="5" x2="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
        'log-in' => '<path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/>',
        'move' => '<polyline points="5 9 2 12 5 15"/><polyline points="9 5 12 2 15 5"/><polyline points="15 19 12 22 9 19"/><polyline points="19 9 22 12 19 15"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="12" y1="2" x2="12" y2="22"/>',
    ];
    $svg = function ($name) use ($icons) {
        return '<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' . $icons[$name] . '</svg>';
    };
    $l = strtolower((string) $label);
    $has = function ($words) use ($l) {
        foreach ((array) $words as $w) {
            if (strpos($l, $w) !== false) {
                return true;
            }
        }
        return false;
    };
    // Order matters: specific phrases before the generic words inside them.
    if ($has(['phone', 'real number', 'most common calls'])) { return $svg('phone'); }
    if ($has(['zip', 'service area', 'where heaters', 'where it', 'location', 'land-lease'])) { return $svg('map-pin'); }
    if ($has(['permit', 'claim', 'records'])) { return $svg('file-text'); }
    if ($has(['50%'])) { return $svg('percent'); }
    if ($has(['florida law'])) { return $svg('scale'); }
    if ($has(['insurance'])) { return $svg('shield-check'); }
    if ($has(['mold', 'sewage', 'biggest danger', 'biggest risk', 'most at risk', 'usually fails'])) { return $svg('alert-triangle'); }
    if ($has(['roof leak', 'storm flooding'])) { return $svg('cloud-rain'); }
    if ($has(['rising water', 'saltwater', 'river water', 'drainage'])) { return $svg('waves'); }
    if ($has(['burst supply', 'water category', 'water and sewer', 'services', 'usually wet', 'irrigation', 'small leak'])) { return $svg('droplet'); }
    if ($has(['drying time', 'typical time', 'extraction time', 'tank life', 'slow leak', 'weeks of water'])) { return $svg('clock'); }
    if ($has(['drying after extraction', 'drying method', 'drying involves', 'gets dried'])) { return $svg('wind'); }
    if ($has(['can the floor be dried'])) { return $svg('help-circle'); }
    if ($has(['what can often be saved', 'what usually stays', 'what it covers', 'what the work covers', 'when it\'s done'])) { return $svg('check-circle'); }
    if ($has(['what usually gets replaced'])) { return $svg('refresh-cw'); }
    if ($has(['what comes out'])) { return $svg('trash-2'); }
    if ($has(['what usually comes up'])) { return $svg('arrow-up'); }
    if ($has(['how far it spreads'])) { return $svg('move'); }
    if ($has(['confirmed', 'quickest check', 'where the water', 'where water hides'])) { return $svg('search'); }
    if ($has(['telltale'])) { return $svg('eye'); }
    if ($has(['who ', 'what each owner gets'])) { return $svg('users'); }
    if ($has(['first move'])) { return $svg('arrow-right'); }
    if ($has(['before going in'])) { return $svg('log-in'); }
    if ($has(['before tear-out', 'repair options', 'broken pipe', 'equipment'])) { return $svg('tool'); }
    if ($has(['before new flooring', 'two or three rooms'])) { return $svg('layers'); }
    if ($has(['most common cause', 'most common sources'])) { return $svg('target'); }
    if ($has(['most jobs'])) { return $svg('tag'); }
    if ($has(['one room'])) { return $svg('square'); }
    if ($has(['condo'])) { return $svg('building'); }
    if ($has(['common homes', 'homes', 'properties', 'elevated homes'])) { return $svg('home'); }
    if ($has(['restaurants'])) { return $svg('coffee'); }
    if ($has(['staying open'])) { return $svg('briefcase'); }
    if ($has(['flood cut'])) { return $svg('ruler'); }
    if ($has(['what you keep'])) { return $svg('camera'); }
    if ($has(['empty season'])) { return $svg('calendar'); }
    if ($l === 'help') { return $svg('life-buoy'); }
    return $svg('info'); // fallback — any future label still gets a sane icon
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
                $rows .= '<div class="detail-row"><dt><span class="detail-icon">' . details_icon($r['label']) . '</span><span class="detail-label">' . esc($r['label']) . '</span></dt><dd>' . render_segments($r['value']) . '</dd></div>';
            }
            return '<section class="details-card"><h2>' . esc($b['heading']) . '</h2>'
                . '<p class="details-sub">' . esc($b['sub']) . '</p>'
                . '<dl class="details-grid">' . $rows . '</dl></section>';
        case 'h2':
            return '<h2>' . esc($b['text']) . '</h2>';
        case 'h3':
            return '<h3>' . esc($b['text']) . '</h3>';
        case 'p':
            if (($b['variant'] ?? '') === 'about-buttons') {
                // Homepage closing line (the only place this text appears):
                // lead text + the two links as ghost buttons. The ' · '
                // separator segment is dropped -- punctuation, not a word
                // (recorded in qa/FINDINGS-help-cards.md). All other segments
                // render exactly: same link texts, same hrefs.
                $out = '';
                foreach ($b['segs'] as $s) {
                    if (($s['t'] ?? '') === ' · ') {
                        continue;
                    }
                    if (!empty($s['href'])) {
                        $out .= '<a class="btn btn-ghost-dark" href="' . esc($s['href']) . '">' . esc($s['t']) . '</a>';
                    } else {
                        $out .= esc($s['t']);
                    }
                }
                return '<p class="about-buttons">' . clean_dashes_html($out) . '</p>';
            }
            if (($b['variant'] ?? '') === 'call-button') {
                // "Not sure your street is covered? Call 239-356-3708 with
                // your ZIP code." (homepage only): the phone number becomes
                // a .btn-call button with the phone SVG (same markup as the
                // hero call button; href tel:+12393563708, as hardcoded in
                // the hero and cta-line cases); the rest stays as
                // surrounding text. The trailing "Call " moves into the
                // button label so the word "Call" appears once, not twice.
                // Zero word changes: every word of the original sentence is
                // present exactly once in the rendered line.
                $text = '';
                foreach ($b['segs'] as $s) {
                    $text .= $s['t'];
                }
                $phone = '239-356-3708';
                $pos = strpos($text, $phone);
                $before = $pos === false ? $text : substr($text, 0, $pos);
                $after = $pos === false ? '' : substr($text, $pos + strlen($phone));
                if (substr($before, -5) === 'Call ') {
                    $before = substr($before, 0, -5);
                }
                return '<p class="call-zip-line">' . clean_dashes_html(esc($before))
                    . '<a class="btn btn-call" href="tel:+12393563708">' . phone_svg() . ' Call ' . esc($phone) . '</a>'
                    . clean_dashes_html(esc($after)) . '</p>';
            }
            return '<p>' . render_segments($b['segs']) . '</p>';
        case 'ul': {
            if (($b['variant'] ?? '') === 'help-cards') {
                // "What we help with" (homepage only): the 6 items as cards,
                // image first in each card. Images come from the manifest
                // ($MEDIA['help']['home'], indexed in list order); a missing
                // slot renders NO <img> (honestly empty, never a forced photo).
                // Item text renders through render_segments() exactly as the
                // plain <ul> did -- same anchors, same hrefs, zero word changes.
                $imgs = $GLOBALS['MEDIA']['help']['home'] ?? [];
                $cards = '';
                foreach ($b['items'] as $k => $it) {
                    $img = '';
                    $m = $imgs[$k] ?? null;
                    if (!empty($m['src']) && !empty($m['alt'])) {
                        $img = '<img class="help-card-img" src="' . esc($m['src']) . '"'
                            . ' alt="' . esc($m['alt']) . '" width="' . (int) $m['width'] . '" height="' . (int) $m['height'] . '"'
                            . ' loading="lazy" decoding="async">';
                    }
                    $cards .= '<article class="kind-card help-card">' . $img
                        . '<p>' . render_segments($it) . '</p></article>';
                }
                return '<div class="kinds-grid help-grid">' . $cards . '</div>';
            }
            $items = '';
            foreach ($b['items'] as $it) {
                $items .= '<li>' . render_segments($it) . '</li>';
            }
            return '<ul>' . $items . '</ul>';
        }
        case 'kinds': {
            $cards = '';
            // Task 5: card backgrounds from qa/manifest-kinds-F.php (copied
            // to site/data/manifest-kinds.php by the coordinator). Indexed
            // by card order; a missing entry renders the card with no photo.
            $kindsMedia = $GLOBALS['KINDS_MEDIA'] ?? null;
            if ($kindsMedia === null) {
                $kindsFile = __DIR__ . '/../data/manifest-kinds.php';
                $kindsMedia = is_file($kindsFile) ? require $kindsFile : [];
                $GLOBALS['KINDS_MEDIA'] = $kindsMedia;
            }
            $ki = 0;
            foreach ($b['items'] as $k) {
                $km = $kindsMedia['kinds']['home'][$ki] ?? null;
                $cls = 'kind-card';
                $style = '';
                $scrim = '';
                if (!empty($km['src'])) {
                    $cls .= ' has-photo';
                    $style = ' style="background-image:url(' . esc($km['src']) . ')"';
                    $scrim = '<div class="kind-scrim" aria-hidden="true"></div>';
                }
                $cards .= '<article class="' . $cls . '"' . $style . '>' . $scrim . '<h3>' . esc($k['title']) . '</h3>'
                    . '<p>' . render_segments($k['body']) . '</p></article>';
                $ki++;
            }
            return '<div class="kinds-grid">' . $cards . '</div>';
        }
        case 'area-cards': {
            $cards = '';
            foreach ($b['items'] as $a) {
                $m = media_for('areas', $a['slug']);
                $img = '';
                if ($m) {
                    $img = '<img class="area-card-img" src="' . esc($m['src']) . '"'
                        . ' alt="' . esc($m['alt']) . '" width="' . (int) $m['width'] . '" height="' . (int) $m['height'] . '"'
                        . ' loading="lazy" decoding="async">';
                }
                $cards .= '<article class="area-card">' . $img
                    . '<h3>' . esc($a['title']) . '</h3>'
                    . '<p>' . render_segments($a['body']) . '</p></article>';
            }
            return '<div class="area-grid">' . $cards . '</div>';
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
