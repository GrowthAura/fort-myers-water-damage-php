<?php
// Fort Myers FL — NEW PHP site. Front controller / router.
// Clean URLs WITH trailing slashes (the published site's URL structure).
// No-slash forms of a slashed route answer 308 to the slash form.
// Local only: no deploy, no domain, no external service calls.
$ROOT = __DIR__;
require $ROOT . '/data/pages.php';
if (is_file($ROOT . '/data/media-manifest.php')) {
    require $ROOT . '/data/media-manifest.php';
}
require $ROOT . '/includes/functions.php';

$SITE_URL = 'https://fortmyerswaterdamagerestoration.us';

// Load a page's data file. Returns the page array or null (not sent yet).
function load_page($slug)
{
    global $ROOT, $ROUTES;
    if (!isset($ROUTES[$slug])) {
        return null;
    }
    $key = $ROUTES[$slug];
    if ($key === null) {
        return null; // page not sent yet — pending
    }
    $file = $ROOT . '/data/' . $key . '.php';
    if (!is_file($file)) {
        return null;
    }
    $page = require $file;
    $page['slug'] = $slug;
    $page['group'] = group_for($slug);
    return $page;
}

function group_for($slug)
{
    global $LOCATION_PAGES;
    if (in_array($slug, $LOCATION_PAGES, true)) {
        return 'area';
    }
    if (in_array($slug, ['/cost/', '/insurance/', '/first-hour-checklist/', '/how-it-works/', '/contact/'], true)) {
        return 'guide';
    }
    if (in_array($slug, ['/privacy-policy/', '/terms/', '/disclaimer/'], true)) {
        return 'legal';
    }
    if ($slug === '/about/') {
        // About is not a service page: breadcrumb is Home » H1, no middle crumb.
        return 'about';
    }
    return 'service';
}

// Do NOT use parse_url() for the path — it treats a leading "//" as a
// scheme-relative URL (host, no path), so "//" would collapse to "/" and
// serve the homepage with 200. Split on "?" directly.
$uri = $_SERVER['REQUEST_URI'] ?? '/';
$rawPath = strtok($uri, '?') ?: '/';
$path = rawurldecode($rawPath);

// 0. Any path containing a double slash must not serve content with 200.
if (str_contains($path, '//')) {
    header('Location: /', true, 308);
    exit;
}

// 1. No-slash form of a slashed route -> 308 to the slash form.
if ($path !== '/' && strlen($path) > 1 && !str_ends_with($path, '/')) {
    $slashed = $path . '/';
    if (isset($ROUTES[$slashed])) {
        header('Location: ' . $slashed, true, 308);
        exit;
    }
}

// 2. Static files (assets, favicon, robots, sitemap, llms, IndexNow key).
$MIME = [
    'css' => 'text/css', 'js' => 'text/javascript', 'jpg' => 'image/jpeg',
    'jpeg' => 'image/jpeg', 'webp' => 'image/webp', 'png' => 'image/png',
    'ico' => 'image/x-icon', 'svg' => 'image/svg+xml', 'woff2' => 'font/woff2',
    'txt' => 'text/plain', 'xml' => 'application/xml',
];
$isStatic = str_starts_with($path, '/assets/') ||
    in_array($path, ['/favicon.ico', '/favicon.svg', '/robots.txt', '/sitemap.xml', '/llms.txt', '/5aacacd72541e41a25cbc83799292d44.txt'], true); // last: IndexNow key file (public by design, Bing fetches it)
if ($isStatic) {
    $file = $ROOT . $path;
    if (is_file($file)) {
        $ext = strtolower(pathinfo($file, PATHINFO_EXTENSION));
        header('Content-Type: ' . ($MIME[$ext] ?? 'application/octet-stream'));
        header('Content-Length: ' . filesize($file));
        readfile($file);
        exit;
    }
    http_response_code(404);
    echo 'Not found';
    exit;
}

// 3. Routes.
if ($path === '/' || isset($ROUTES[$path])) {
    $page = load_page($path);
    if ($page !== null) {
        render_page($path, $page);
        exit;
    }
}

// 4. 404.
http_response_code(404);
$HEAD = [
    'title' => 'Page Not Found | Fort Myers Water Damage Restoration Pros',
    'description' => 'The page you asked for is not here. Call 239-356-3708 for 24/7 emergency water damage help in Fort Myers, FL.',
    'canonical' => null,
    // 20x-fixes: 404 carries no canonical (it must not claim a real page),
    // but og:url still needs the requested URL — supplied separately so the
    // header emits og:url without a <link rel="canonical">.
    'og_url' => $SITE['url'] . $path,
    'robots' => 'noindex, follow',
    'og_type' => 'website',
    'og_image' => null,
    'ld_given' => ld_json([['@type' => 'WebSite', '@id' => $SITE['url'] . '/#website', 'name' => $SITE['brand'], 'url' => $SITE['url'] . '/']]),
    'ld_faq' => null,
    'ld_crumb' => null,
];
$currentSlug = $path;
$isLocation = false;
require $ROOT . '/includes/header.php';
echo '<main id="main" tabindex="-1"><div class="container page-body not-found">'
    . '<h1>Page Not Found</h1>'
    . '<p>The page you asked for is not here. If water is coming into your home right now, call <a href="tel:+12393563708">239-356-3708</a>, the line is answered 24/7.</p>'
    . '<p><a class="btn btn-call" href="tel:+12393563708">' . phone_svg() . ' Call 239-356-3708</a> '
    . '<a class="btn btn-ghost-dark" href="/">Back to the homepage</a></p>'
    . '</div></main>';
require $ROOT . '/includes/footer.php';
