<?php
// Fort Myers FL — NEW PHP site. Route table + nav data.
// URL structure is 10000001% the published site's: exactly these 33 routes,
// trailing slashes, same slugs. /about/ is a 34th route: the homepage paste
// links to it but its page has NOT been sent yet — it stays pending (404)
// until the user sends the About content. Do NOT invent About content.
$SITE = [
    'brand' => 'Fort Myers Water Damage Restoration Pros',
    'brand_short' => 'Fort Myers Water Damage Restoration',
    'phone' => '239-356-3708',
    'phone_display' => '(239) 356-3708',
    'phone_href' => 'tel:+12393563708',
    'phone_intl' => '+1-239-356-3708',
    'url' => 'https://fortmyerswaterdamagerestoration.us',
    'area' => 'Fort Myers, FL',
    'city_zip' => 'Fort Myers, FL 33901',
];

// All 33 published routes, sitemap order. 'content' => page data file
// (null = not sent yet; the route 404s until its page arrives).
$ROUTES = [
    '/' => 'homepage',
    '/water-removal/' => 'water-removal',
    '/drying/' => 'drying',
    '/sewage-cleanup/' => 'sewage-cleanup',
    '/ac-leak/' => 'ac-leak',
    '/ceiling-leak/' => 'ceiling-leak',
    '/condo-leak/' => 'condo-leak',
    '/cast-iron-pipe/' => 'cast-iron-pipe',
    '/vacant-home/' => 'vacant-home',
    '/first-hour-checklist/' => 'first-hour-checklist',
    '/cost/' => 'cost',
    '/insurance/' => 'insurance',
    '/burst-pipe/' => 'burst-pipe',
    '/mobile-home/' => 'mobile-home',
    '/slab-leak/' => 'slab-leak',
    '/flood-cleanup/' => 'flood-cleanup',
    '/cape-coral/' => 'cape-coral',
    '/lehigh-acres/' => 'lehigh-acres',
    '/areas/' => 'areas',
    '/water-heater-leak/' => 'water-heater-leak',
    '/appliance-leak/' => 'appliance-leak',
    '/floors/' => 'floors',
    '/cabinets/' => 'cabinets',
    '/commercial/' => 'commercial',
    '/north-fort-myers/' => 'north-fort-myers',
    '/fort-myers-beach/' => 'fort-myers-beach',
    '/estero/' => 'estero',
    '/bonita-springs/' => 'bonita-springs',
    '/how-it-works/' => 'how-it-works',
    '/contact/' => 'contact',
    '/privacy-policy/' => 'privacy-policy',
    '/terms/' => 'terms',
    '/disclaimer/' => 'disclaimer',
    '/about/' => 'about',
];

// The 7 location pages: footer map is ABSENT on these (standing rule).
$LOCATION_PAGES = [
    '/cape-coral/', '/lehigh-acres/', '/north-fort-myers/',
    '/fort-myers-beach/', '/estero/', '/bonita-springs/', '/areas/',
];

// Full service list (17) — footer Services column iterates this, so the
// footer carries EVERY service page. Five of these (cast-iron-pipe,
// vacant-home, appliance-leak, floors, cabinets) previously had no nav
// entry at all; their labels below are proposed from each page's own
// title/H1 (owner may correct). Existing 12 entries unchanged, same order.
$NAV_SERVICES = [
    ['label' => 'Emergency Water Removal', 'href' => '/water-removal/'],
    ['label' => 'Structural Drying', 'href' => '/drying/'],
    ['label' => 'Sewage Backup Cleanup', 'href' => '/sewage-cleanup/'],
    ['label' => 'Flood & Storm Cleanup', 'href' => '/flood-cleanup/'],
    ['label' => 'AC Leak Water Damage', 'href' => '/ac-leak/'],
    ['label' => 'Ceiling Leak Water Damage', 'href' => '/ceiling-leak/'],
    ['label' => 'Burst Pipe Water Damage', 'href' => '/burst-pipe/'],
    ['label' => 'Slab Leak Water Damage', 'href' => '/slab-leak/'],
    ['label' => 'Water Heater Leak Cleanup', 'href' => '/water-heater-leak/'],
    ['label' => 'Condo Water Damage', 'href' => '/condo-leak/'],
    ['label' => 'Mobile Home Water Damage', 'href' => '/mobile-home/'],
    ['label' => 'Commercial Water Damage', 'href' => '/commercial/'],
    ['label' => 'Cast Iron Pipe Water Damage', 'href' => '/cast-iron-pipe/'],
    ['label' => 'Seasonal Home Water Damage', 'href' => '/vacant-home/'],
    ['label' => 'Appliance Leak Water Damage', 'href' => '/appliance-leak/'],
    ['label' => 'Water Damaged Floors', 'href' => '/floors/'],
    ['label' => 'Water Damaged Kitchen Cabinets', 'href' => '/cabinets/'],
];

// Header menu services (7) — the ONLY services in the header Services
// dropdown (desktop) and the mobile-menu Services list. Owner order
// 2026-11-19: menu = 7 services, the rest go in the footer. These are the
// first 7 of $NAV_SERVICES, in the same order; footer still lists all 17.
$NAV_SERVICES_MENU = [
    ['label' => 'Emergency Water Removal', 'href' => '/water-removal/'],
    ['label' => 'Structural Drying', 'href' => '/drying/'],
    ['label' => 'Sewage Backup Cleanup', 'href' => '/sewage-cleanup/'],
    ['label' => 'Flood & Storm Cleanup', 'href' => '/flood-cleanup/'],
    ['label' => 'AC Leak Water Damage', 'href' => '/ac-leak/'],
    ['label' => 'Ceiling Leak Water Damage', 'href' => '/ceiling-leak/'],
    ['label' => 'Burst Pipe Water Damage', 'href' => '/burst-pipe/'],
];

// Header Areas dropdown (7) — mirrors the published site's nav, minus the
// old "Fort Myers" -> "/" entry: it duplicated the brand link (fix round:
// header carries important items only).
$NAV_AREAS = [
    ['label' => 'Cape Coral', 'href' => '/cape-coral/'],
    ['label' => 'Lehigh Acres', 'href' => '/lehigh-acres/'],
    ['label' => 'North Fort Myers', 'href' => '/north-fort-myers/'],
    ['label' => 'Fort Myers Beach', 'href' => '/fort-myers-beach/'],
    ['label' => 'Estero', 'href' => '/estero/'],
    ['label' => 'Bonita Springs', 'href' => '/bonita-springs/'],
    ['label' => 'All Service Areas', 'href' => '/areas/'],
];

// Footer Explore links (includes pages the header omits: Insurance, About,
// How it works, Cost, First-hour checklist, legal). "Home" removed in the
// fix round: it duplicated the brand link (footer carries important items only).
$FOOTER_EXPLORE = [
    ['label' => 'How It Works', 'href' => '/how-it-works/'],
    ['label' => 'About Us', 'href' => '/about/'],
    ['label' => 'Cost of Water Damage Restoration', 'href' => '/cost/'],
    ['label' => 'Insurance Claims', 'href' => '/insurance/'],
    ['label' => 'First-Hour Checklist', 'href' => '/first-hour-checklist/'],
    ['label' => 'Contact', 'href' => '/contact/'],
    ['label' => 'Privacy Policy', 'href' => '/privacy-policy/'],
    ['label' => 'Terms of Service', 'href' => '/terms/'],
    ['label' => 'Disclaimer', 'href' => '/disclaimer/'],
];

// Footer Areas column (plain text + links to the area pages).
// "Fort Myers" -> "/" removed in the fix round: it duplicated the brand link.
$FOOTER_AREAS = [
    ['label' => 'Cape Coral', 'href' => '/cape-coral/'],
    ['label' => 'Lehigh Acres', 'href' => '/lehigh-acres/'],
    ['label' => 'North Fort Myers', 'href' => '/north-fort-myers/'],
    ['label' => 'Fort Myers Beach', 'href' => '/fort-myers-beach/'],
    ['label' => 'Estero', 'href' => '/estero/'],
    ['label' => 'Bonita Springs', 'href' => '/bonita-springs/'],
    ['label' => 'All Service Areas', 'href' => '/areas/'],
];

function build_pages()
{
    global $ROUTES;
    $pages = [];
    foreach ($ROUTES as $slug => $key) {
        $pages[$slug] = ['slug' => $slug, 'key' => $key];
    }
    return $pages;
}
