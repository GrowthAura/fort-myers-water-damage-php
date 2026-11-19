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
// 10x DESIGN (B-P3-1): an Article also gets `image` = the absolute URL of
// the page's own hero image (render-time only; the hero is real and
// renders on the page). $heroUrl is passed by render_page(); without it
// the schema is left exactly as the paste gave it.
function ld_normalize_given($schema, $heroUrl = null)
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
    if ($type === 'Article' && empty($schema['image']) && !empty($heroUrl)) {
        $schema['image'] = $heroUrl;
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

// --- 10x DESIGN helpers (presentation only; no new words) -----------------
// Every string below is assembled ONLY from words already on the page
// (its H1, its copy, its nav/breadcrumb labels, or the footer, which
// renders on every page). Nothing is invented.

// Plain text of a page's blocks, for "is this phrase already on the page?"
// checks. Recurses into nested segment arrays.
function page_plain_text($page)
{
    $t = $page['seo']['h1'] . ' ' . $page['seo']['title'] . ' ';
    $walk = function ($v) use (&$walk) {
        $out = '';
        if (is_string($v)) {
            return $v . ' ';
        }
        if (!is_array($v)) {
            return '';
        }
        foreach ($v as $k => $item) {
            if ($k === 'href') {
                continue;
            }
            $out .= $walk($item);
        }
        return $out;
    };
    foreach ($page['blocks'] as $b) {
        $t .= $walk($b);
    }
    return $t;
}

// Hero eyebrow (L-2). Area pages use their own nav label + Lee County;
// service/guide pages use the "Emergency Service · Answered 24/7" form
// given in the brief; everything else uses the footer place line.
function hero_eyebrow($page, $isHome)
{
    global $NAV_AREAS;
    if ($isHome) {
        return 'Fort Myers · Lee County, FL';
    }
    foreach ($NAV_AREAS as $a) {
        if ($page['slug'] === $a['href'] && $a['href'] !== '/areas/') {
            return $a['label'] . ' · Lee County, FL';
        }
    }
    if ($page['slug'] === '/areas/') {
        return 'Lee County, FL';
    }
    $group = $page['group'] ?? 'service';
    if ($group === 'service' || $group === 'guide') {
        return 'Emergency Service · Answered 24/7';
    }
    return 'Fort Myers · Lee County, FL';
}

// Hero trust row (L-2): up to 3 items, each only if its words are already
// on the page. "Answered 24/7" is on every page (footer + CTA text).
// "Moisture readings logged" needs "readings logged" in the copy;
// "Written scope before rebuild" needs "written scope" in the copy
// ("rebuild" is the how-it-works step title).
// 10x-fix-p3 V-P3-4: the old fallback put the footer place line
// ("Fort Myers · Lee County, FL") in as a third item on pages without
// "written scope" / "moisture log" — location info, not a trust signal.
// No fallback any more: those pages show only the sourced items (two),
// never an invented third item.
function hero_trust_items($page)
{
    $text = page_plain_text($page);
    $items = ['Answered 24/7'];
    if (stripos($text, 'readings logged') !== false) {
        $items[] = 'Moisture readings logged';
    } elseif (stripos($text, 'moisture readings') !== false) {
        $items[] = 'Moisture readings taken';
    }
    if (stripos($text, 'written scope') !== false) {
        $items[] = 'Written scope before rebuild';
    } elseif (stripos($text, 'moisture log') !== false) {
        $items[] = 'Photos and moisture logs';
    }
    return array_slice($items, 0, 3);
}

function hero_trust_html($page)
{
    $items = hero_trust_items($page);
    $parts = [];
    foreach ($items as $it) {
        $parts[] = '<span>' . esc($it) . '</span>';
    }
    return '<p class="hero-trust">' . implode('<span class="trust-sep" aria-hidden="true"> · </span>', $parts) . '</p>';
}

// Section kicker (L-6): the page's own group label, already on the page
// as the breadcrumb / nav label. No new words.
function page_kicker($page)
{
    $group = $page['group'] ?? 'service';
    if ($group === 'area') {
        return 'Areas';
    }
    if ($group === 'guide') {
        return 'Guide';
    }
    if ($group === 'legal') {
        return 'Fort Myers';
    }
    if ($group === 'about') {
        return 'About';
    }
    return 'Services';
}

// H1 HTML with the two worst orphan wraps hand-tuned (L-3): the place
// phrase stays on one line via a non-breaking span. Words unchanged.
function h1_html($h1, $slug)
{
    $h = esc($h1);
    if ($slug === '/drying/') {
        $h = str_replace('Fort Myers, FL', '<span class="h1-nowrap">Fort&nbsp;Myers,&nbsp;FL</span>', $h);
    } elseif ($slug === '/cost/') {
        $h = str_replace('Fort Myers?', '<span class="h1-nowrap">Fort&nbsp;Myers?</span>', $h);
    } elseif ($slug === '/contact/' || $slug === '/about/') {
        // 10x-fix V-P3-2: at 320px the H1 ended on a 1-word line ("Pros").
        // "Restoration Pros" stays together, so the last line is 2 words.
        // Presentation only; the H1 data string is unchanged. The extra
        // h1-nowrap-fit class marks these two H1s for the small-width
        // shrink in styles.css (the pair is 324px at 36px, wider than the
        // 280px content box at 320px, so the whole H1 drops to 30px
        // below 382px instead of clipping under the hero's overflow:hidden).
        $h = str_replace('Restoration Pros', '<span class="h1-nowrap h1-nowrap-fit">Restoration&nbsp;Pros</span>', $h);
    }
    return $h;
}

// Step duration chips (L-13, how-it-works steps-rich only). Each chip is
// the page's own "How Long Each Stage Takes" table row, verbatim, matched
// to the step title. Steps with no stage-time row get no chip (never
// invented): "While you wait", "Final readings and paperwork", "Repairs".
function step_duration($title)
{
    $map = [
        'You call' => 'One short phone call',
        'The inspection' => 'Usually at the first visit',
        'The written scope' => 'Usually at the first visit',
        'Water removal' => 'Usually the first day',
        "Removing what can't be saved" => 'Usually the first day',
        'Drying' => 'About 3 to 5 days',
    ];
    return $map[$title] ?? null;
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
                . '<p class="hero-eyebrow">' . esc(hero_eyebrow($page, true)) . '</p>'
                . '<h1>' . h1_html($b['h1'], $page['slug']) . '</h1>'
                . '<p class="hero-intro" id="hero-intro">' . $intro . '</p>'
                . '<p class="hero-ctas">'
                . '<a class="btn btn-call" href="tel:+12393563708">' . phone_svg() . ' Call 239-356-3708</a>'
                . '<a class="btn btn-ghost" href="/contact/">Describe your water problem</a>'
                . '</p>'
                . hero_trust_html($page)
                . '<p class="hero-areas">' . $areas . '</p>'
                . '<a class="hero-intro-more" href="#hero-intro">Read the intro ↓</a>'
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
            // L-6: kicker (page's own group label) + feature/standard class.
            // $GLOBALS['NEXT_H2_FEATURE'] is set by render_page per section:
            // the first H2 section on the page is the feature H2.
            $feat = !empty($GLOBALS['NEXT_H2_FEATURE']);
            $GLOBALS['NEXT_H2_FEATURE'] = false;
            $cls = $feat ? 'h2-feature' : 'h2-standard';
            // 10x A-2: optional 'class' on the h2 block appends to the
            // L-6 feature/standard class (e.g. 'h2-as-h3' if the design
            // wants a promoted heading at the H3 look). Unused today: the
            // 5 promoted /areas/ headings render at full H2 size.
            if (!empty($b['class'])) { $cls .= ' ' . $b['class']; }
            return '<p class="sec-kicker">' . esc(page_kicker($page)) . '</p><h2 class="' . esc($cls) . '">' . esc($b['text']) . '</h2>';
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
                // "What we help with" (homepage + /about/): the items as
                // cards, image first in each card. Images come from the
                // manifest, slug-gated (10x CLOSER): $MEDIA['help']['about']
                // on /about/ (7 cards, About order, incl. the
                // floors/cabinets photo), $MEDIA['help']['home'] elsewhere
                // (homepage order, unchanged). Indexed in list order; a
                // missing slot renders NO <img> (honestly empty, never a
                // forced photo). Item text renders through
                // render_segments() exactly as the plain <ul> did -- same
                // anchors, same hrefs, zero word changes.
                $imgs = $GLOBALS['MEDIA']['help'][$page['slug'] === '/about/' ? 'about' : 'home'] ?? [];
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
            // 10x A-2: on /areas/ ONLY, card titles are H2 (the hub outline
            // must be H1 -> H2s with no level skip). Other pages have no
            // area-cards blocks today, and the gate keeps their titles H3
            // if one is ever added. The H2 carries class="area-card-title":
            // a bare H2 would inherit 42px + the .page-body h2::before coral
            // bar inside a 474px card, so the CSS worker must size
            // .area-card h2.area-card-title like the old .area-card h3
            // (23px, 20px top margin, 28px side padding) and suppress the
            // ::before bar on it.
            $isAreasHub = ($page['slug'] ?? '') === '/areas/';
            $cards = '';
            foreach ($b['items'] as $a) {
                $m = media_for('areas', $a['slug']);
                $img = '';
                if ($m) {
                    $img = '<img class="area-card-img" src="' . esc($m['src']) . '"'
                        . ' alt="' . esc($m['alt']) . '" width="' . (int) $m['width'] . '" height="' . (int) $m['height'] . '"'
                        . ' loading="lazy" decoding="async">';
                }
                $tag = $isAreasHub ? 'h2' : 'h3';
                $tcls = $isAreasHub ? ' class="area-card-title"' : '';
                $cards .= '<article class="area-card">' . $img
                    . '<' . $tag . $tcls . '>' . esc($a['title']) . '</' . $tag . '>'
                    . '<p>' . render_segments($a['body']) . '</p></article>';
            }
            return '<div class="area-grid">' . $cards . '</div>';
        }
        case 'table': {
            $head = '';
            $headTexts = [];
            foreach ($b['head'] as $c) {
                $head .= '<th scope="col">' . render_segments($c) . '</th>';
                $ht = '';
                foreach ($c as $seg) {
                    $ht .= $seg['t'] ?? '';
                }
                $headTexts[] = plain_text($ht);
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
            // L-15: on /cost/, the first table (job size) highlights the
            // "One room" row and gets the price-range bar underneath it.
            $isCostFirst = ($page['slug'] === '/cost/' && ($GLOBALS['COST_TABLE_INDEX'] ?? 0) === 0
                && str_contains($lastHead, 'Rough area range')
                && ($headTexts[0] ?? '') === 'Size of the job');
            $GLOBALS['COST_TABLE_INDEX'] = ($GLOBALS['COST_TABLE_INDEX'] ?? 0) + 1;
            foreach ($b['rows'] as $row) {
                $cells = '';
                $firstText = '';
                foreach ($row as $ci => $c) {
                    $ct = '';
                    foreach ($c as $seg) {
                        $ct .= $seg['t'] ?? '';
                    }
                    if ($ci === 0) {
                        $firstText = plain_text($ct);
                    }
                    // C-02/C-04: data-label feeds the stacked mobile layout
                    // (CSS ::before); the label words are the table's own
                    // header words, repeated for presentation only.
                    $label = $headTexts[$ci] ?? '';
                    $chip = '';
                    if ($isCostFirst && $ci === 0 && $firstText === 'One room') {
                        $chip = ' <span class="most-common-chip">Most common</span>';
                    }
                    $cells .= '<td data-label="' . esc($label) . '">' . render_segments($c) . $chip . '</td>';
                }
                $rowCls = ($isCostFirst && $firstText === 'One room') ? ' class="cost-row-highlight"' : '';
                $rows .= '<tr' . $rowCls . '>' . $cells . '</tr>';
            }
            $out = '<div class="' . $wrapClass . '"><table><thead><tr>' . $head . '</tr></thead><tbody>' . $rows . '</tbody></table></div>';
            if ($isCostFirst) {
                // L-15 range bar: track = $500 to $15,000 (the table's own
                // range); gold marker = $1,200 to $3,500 on that scale:
                // (1200-500)/14500 = 4.8%, (3500-500)/14500 = 20.7%.
                $out .= '<div class="cost-range"><div class="cost-range-track"><div class="cost-range-fill"></div>'
                    . '<div class="cost-range-marker"></div></div>'
                    . '<div class="cost-range-axis"><span>$500</span><span>$15,000</span></div>'
                    . '<p class="cost-range-label">Most Fort Myers jobs land here</p></div>';
            }
            return $out;
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
            // L-13: duration chip from the page's own stage-time table
            // (see step_duration()); steps with no row get no chip.
            $items = '';
            foreach ($b['items'] as $k => $s) {
                $inner = '';
                foreach ($s['parts'] as $part) {
                    $inner .= render_block($part, $page);
                }
                $dur = step_duration($s['title']);
                $chip = $dur !== null ? '<span class="step-duration">' . esc($dur) . '</span>' : '';
                $items .= '<li><span class="step-num" aria-hidden="true">' . ($k + 1) . '</span>'
                    . $chip
                    . '<h3>' . esc($s['title']) . '</h3>' . $inner . '</li>';
            }
            return '<ol class="steps">' . $items . '</ol>';
        }
        case 'cta-line':
            // L-12 / L-14: render_page sets $GLOBALS['CTA_ROLE'] per block:
            // first cta-line on the page = slim utility line (post-hero);
            // last cta-line = closing band (button + ghost + trust line);
            // any middle cta-line keeps the original coral button.
            $role = $GLOBALS['CTA_ROLE'] ?? 'standard';
            if ($role === 'utility') {
                return '<p class="utility-line"><span class="utility-glyph" aria-hidden="true">' . phone_svg() . '</span> Answered 24/7 · Call <a href="tel:+12393563708">239-356-3708</a></p>';
            }
            if ($role === 'closing') {
                // 10x-fix-p3 V-P3-5: on /contact/ the ghost button would
                // link to /contact/ itself. Render it there as a non-link
                // span with the same classes (identical visuals, no href,
                // no self-link). Every other page keeps the link.
                $ghost = '<a class="btn btn-ghost" href="/contact/">Describe your water problem</a>';
                if (($page['slug'] ?? '') === '/contact/') {
                    $ghost = '<span class="btn btn-ghost" aria-disabled="true">Describe your water problem</span>';
                }
                return '<p class="cta-line closing-cta-line"><a class="btn btn-call" href="tel:+12393563708">' . phone_svg() . ' Call 239-356-3708</a>'
                    . $ghost . '</p>'
                    . '<p class="closing-trust">Answered 24/7, including holidays and the days after a storm</p>';
            }
            return '<p class="cta-line"><a class="btn btn-call" href="tel:+12393563708">' . phone_svg() . ' ' . esc($b['text']) . '</a></p>';
        case 'map':
            // Heavy map with a VISIBLE PIN on Fort Myers (city-level only:
            // Fort Myers, FL 33901 — no street address exists, none invented).
            // q=place renders Google's place pin; z=12 keeps the pin and the
            // Caloosahatchee riverfront in frame.
            // L-18: CSS-only poster fallback — the figure carries a sand/teal
            // gradient + centred caption; the iframe is transparent, so it
            // covers the poster once loaded. No fake map image is invented.
            return '<section class="map-section"><h2 class="map-caption">' . esc($b['caption']) . '</h2>'
                . '<figure class="map-figure"><figcaption class="map-poster">Map loading · Fort Myers &amp; Lee County</figcaption>'
                . '<iframe class="map-embed" title="Map: Fort Myers and the Lee County service area" '
                . 'src="https://www.google.com/maps?q=Fort%20Myers%2C%20FL%2033901&z=12&output=embed" '
                . 'width="1240" height="560" loading="lazy" '
                . 'referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></figure></section>';
        case 'area-map': {
            // L-10 (10x CLOSER): static area map strip — real OSM map image
            // + caption + "View larger map" link + 3-chip facts band.
            // Image from $MEDIA['maps'] (key in $b['map']); caption, facts
            // and link come from the data block (the spec's own words).
            // No heading: the page outline is unchanged. A missing slot
            // renders nothing (honestly empty, never a forced photo).
            $m = media_for('maps', $b['map']);
            if (!$m) {
                return '';
            }
            $chips = '';
            foreach (($b['facts'] ?? []) as $f) {
                $chips .= '<li>' . esc($f) . '</li>';
            }
            return '<figure class="area-map-strip">'
                . '<img class="area-map-img" src="' . esc($m['src']) . '"'
                . ' alt="' . esc($m['alt']) . '" width="' . (int) $m['width'] . '" height="' . (int) $m['height'] . '"'
                . ' loading="lazy" decoding="async">'
                . '<figcaption class="area-map-caption">' . esc($b['caption']) . ' <a class="area-map-link" href="' . esc($b['map_url']) . '" target="_blank" rel="noopener">View larger map ↗</a></figcaption>'
                . '<p class="area-map-attr">© OpenStreetMap contributors</p>'
                . '<ul class="area-map-facts">' . $chips . '</ul>'
                . '</figure>';
        }
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
        'ld_given' => !empty($page['seo']['schema']) ? ld_json_object(ld_normalize_given($page['seo']['schema'], $heroUrl)) : null,
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
        echo '<section class="hero hero-inner-page' . ($hero ? '' : ' hero-no-media') . ($isLocation ? ' hero-area' : '') . '">'
            . $img . '<div class="hero-scrim"></div>'
            . '<div class="container hero-inner">'
            . '<p class="hero-eyebrow">' . esc(hero_eyebrow($page, false)) . '</p>'
            . '<h1>' . h1_html($page['seo']['h1'], $slug) . '</h1>'
            . ($heroIntro ? '<p class="hero-intro" id="hero-intro">' . render_segments($heroIntro['segs']) . '</p>' : '')
            . '<p class="hero-ctas"><a class="btn btn-call" href="tel:+12393563708">' . phone_svg() . ' Call 239-356-3708</a></p>'
            . hero_trust_html($page)
            . '<a class="hero-intro-more" href="#hero-intro">Read the intro ↓</a>'
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
    // 10x DESIGN (L-4): group the flat blocks into H2-led sections so
    // the body can be banded (alternating sand, one deep-teal band).
    // A section starts at each 'h2' block; blocks before the first H2
    // (details card, opening paragraphs, the first cta-line) form the
    // intro section. Words, order and heading levels are unchanged —
    // only a <section> wrapper is added around each group.
    $GLOBALS['COST_TABLE_INDEX'] = 0;
    $ctaIdx = [];
    foreach ($blocks as $bi => $b) {
        if ($b['type'] === 'cta-line') {
            $ctaIdx[] = $bi;
        }
    }
    $firstCta = $ctaIdx ? $ctaIdx[0] : null;
    $lastCta = $ctaIdx ? $ctaIdx[count($ctaIdx) - 1] : null;
    $sections = [];
    $cur = [];
    foreach ($blocks as $bi => $b) {
        if ($b['type'] === 'h2' && $cur) {
            $sections[] = $cur;
            $cur = [];
        }
        $cur[] = ['idx' => $bi, 'block' => $b];
    }
    if ($cur) {
        $sections[] = $cur;
    }
    $featureDone = false;
    foreach ($sections as $si => $sec) {
        $hasH2 = ($sec[0]['block']['type'] === 'h2');
        $isFeature = $hasH2 && !$featureDone;
        if ($isFeature) {
            $featureDone = true;
        }
        $isDeep = false;
        foreach ($sec as $item) {
            if ($item['idx'] === $lastCta) {
                $isDeep = true;
            }
        }
        $cls = 'body-section';
        if ($si === 0) {
            $cls .= ' body-section-intro';
        }
        if ($isFeature) {
            $cls .= ' feature';
        }
        if ($isDeep) {
            $cls .= ' band-deep';
        } elseif ($si % 2 === 1) {
            $cls .= ' band-sand';
        }
        echo '<section class="' . $cls . '">';
        foreach ($sec as $item) {
            $b = $item['block'];
            if ($b['type'] === 'h2') {
                $GLOBALS['NEXT_H2_FEATURE'] = $isFeature;
            }
            if ($b['type'] === 'cta-line') {
                $GLOBALS['CTA_ROLE'] = ($item['idx'] === $firstCta) ? 'utility'
                    : (($item['idx'] === $lastCta) ? 'closing' : 'standard');
            }
            echo render_block($b, $page);
        }
        echo '</section>';
    }
    $GLOBALS['CTA_ROLE'] = 'standard';
    echo '</div></main>';
    require __DIR__ . '/footer.php';
}
