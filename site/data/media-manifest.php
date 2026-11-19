<?php
// Media manifest — hero images (34 routes) + help cards + area cards.
// Merged 2026-11-19 by the hero-round coordinator from qa/manifest-hero-A/B/C.php,
// qa/manifest-help-E.php, qa/manifest-areas-G.php. Kinds backgrounds live in
// site/data/manifest-kinds.php (separate file, lazy-required by functions.php).
// 4 hero masters downscaled to 1600x1067 (lehigh-acres, north-fort-myers, estero,
// bonita-springs) — 24-27% lighter, same JPEG quality; srcset updated to 1600w.
// 10x round 2026-11-19 (Worker 3): 15 alts trimmed to <=125 chars; lehigh-acres +
// north-fort-myers heroes re-encoded to 1440x960 (<=250 KB) with a 640w mobile variant;
// insurance/terms/disclaimer heroes + sewage help swapped for topical photos;
// help index 6 (property types, for /about/) + maps registry added.
// 10x CLOSER 2026-11-20: $MEDIA['help']['about'] added (7 entries in About
// order; idx 5 = about-floors-cabinets.jpg, the staged floors/cabinets
// photo; the other 6 reuse the home help images).
// Every image: GPS EXIF only (Fort Myers 26.6406,-81.8723, or the area's own
// coordinates), no AI/XMP metadata. Missing slots render NO <img> (honestly empty).
$MEDIA = array (
  'hero' => 
  array (
    'home' => 
    array (
      'src' => '/assets/img/hero-home.jpg',
      'alt' => 'A restoration technician extracts standing water from a tiled living room floor in a bright Florida home',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-home-960w.jpg 960w, /assets/img/hero-home.jpg 1920w',
    ),
    'water-removal' => 
    array (
      'src' => '/assets/img/hero-water-removal.jpg',
      'alt' => 'A submersible pump and extraction wand pull standing water from a tiled floor in a Florida home',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-water-removal-960w.jpg 960w, /assets/img/hero-water-removal.jpg 1920w',
    ),
    'drying' => 
    array (
      'src' => '/assets/img/hero-drying.jpg',
      'alt' => 'A commercial dehumidifier, air movers and a moisture meter dry damp walls and tile flooring in a Florida home',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-drying-960w.jpg 960w, /assets/img/hero-drying.jpg 1920w',
    ),
    'sewage-cleanup' => 
    array (
      'src' => '/assets/img/hero-sewage-cleanup.jpg',
      'alt' => 'A technician in protective coveralls and a respirator vacuums dark water from a bathroom floor',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-sewage-cleanup-960w.jpg 960w, /assets/img/hero-sewage-cleanup.jpg 1920w',
    ),
    'ac-leak' => 
    array (
      'src' => '/assets/img/hero-ac-leak.jpg',
      'alt' => 'Water drips from an air handler condensate drain into a puddle on a tile floor',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-ac-leak-960w.jpg 960w, /assets/img/hero-ac-leak.jpg 1920w',
    ),
    'ceiling-leak' => 
    array (
      'src' => '/assets/img/hero-ceiling-leak.jpg',
      'alt' => 'A sagging, water-stained ceiling drips into a bucket while a gloved hand checks it with a moisture meter',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-ceiling-leak-960w.jpg 960w, /assets/img/hero-ceiling-leak.jpg 1920w',
    ),
    'condo-leak' => 
    array (
      'src' => '/assets/img/hero-condo-leak.jpg',
      'alt' => 'Water runs down a shared condo wall from a leaking ceiling while a technician checks it with a moisture meter',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-condo-leak-960w.jpg 960w, /assets/img/hero-condo-leak.jpg 1920w',
    ),
    'cast-iron-pipe' => 
    array (
      'src' => '/assets/img/hero-cast-iron-pipe.jpg',
      'alt' => 'A rusted cast iron drain pipe exposed in an opened wall, with a pipe wrench, wet vacuum and damp towels on the tile floor',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-cast-iron-pipe-960w.jpg 960w, /assets/img/hero-cast-iron-pipe.jpg 1920w',
    ),
    'vacant-home' => 
    array (
      'src' => '/assets/img/hero-vacant-home.jpg',
      'alt' => 'A technician enters a seasonal Florida home with covered furniture and damp, stained tile flooring',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-vacant-home-960w.jpg 960w, /assets/img/hero-vacant-home.jpg 1920w',
    ),
    'burst-pipe' => 
    array (
      'src' => '/assets/img/hero-burst-pipe.jpg',
      'alt' => 'A split supply pipe under a kitchen sink sprays water while a gloved hand reaches for the shut-off valve',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-burst-pipe-960w.jpg 960w, /assets/img/hero-burst-pipe.jpg 1920w',
    ),
    'mobile-home' => 
    array (
      'src' => '/assets/img/hero-mobile-home.jpg',
      'alt' => 'A technician checks a damp wall of a manufactured home in a Florida park with a moisture meter',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-mobile-home-960w.jpg 960w, /assets/img/hero-mobile-home.jpg 1920w',
    ),
    'slab-leak' => 
    array (
      'src' => '/assets/img/hero-slab-leak.jpg',
      'alt' => 'Gloved hands test a damp tile floor with a moisture meter beside broken tiles exposing a wet concrete slab',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-slab-leak-960w.jpg 960w, /assets/img/hero-slab-leak.jpg 1920w',
    ),
    'flood-cleanup' => 
    array (
      'src' => '/assets/img/hero-flood-cleanup.jpg',
      'alt' => 'Technician clearing floodwater from a tiled living room floor in a Florida home',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-flood-cleanup-960w.jpg 960w, /assets/img/hero-flood-cleanup.jpg 1920w',
    ),
    'water-heater-leak' => 
    array (
      'src' => '/assets/img/hero-water-heater-leak.jpg',
      'alt' => 'Water heater tank standing in a puddle on a garage floor while a gloved hand vacuums up the water',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-water-heater-leak-960w.jpg 960w, /assets/img/hero-water-heater-leak.jpg 1920w',
    ),
    'appliance-leak' => 
    array (
      'src' => '/assets/img/hero-appliance-leak.jpg',
      'alt' => 'Washing machine with water pooling on the laundry room floor and gloved hands laying towels to soak it up',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-appliance-leak-960w.jpg 960w, /assets/img/hero-appliance-leak.jpg 1920w',
    ),
    'floors' => 
    array (
      'src' => '/assets/img/hero-floors.jpg',
      'alt' => 'Lifted and curled vinyl plank flooring being checked with a moisture meter while an air mover dries the room',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-floors-960w.jpg 960w, /assets/img/hero-floors.jpg 1920w',
    ),
    'cabinets' => 
    array (
      'src' => '/assets/img/hero-cabinets.jpg',
      'alt' => 'Open kitchen cabinets with a swollen, water-stained base being checked with a moisture meter',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-cabinets-960w.jpg 960w, /assets/img/hero-cabinets.jpg 1920w',
    ),
    'commercial' => 
    array (
      'src' => '/assets/img/hero-commercial.jpg',
      'alt' => 'Technician extracting floodwater from an office floor between desks, with air movers drying the space',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-commercial-960w.jpg 960w, /assets/img/hero-commercial.jpg 1920w',
    ),
    'first-hour-checklist' => 
    array (
      'src' => '/assets/img/hero-first-hour-checklist.jpg',
      'alt' => 'Hands photographing a wet ceiling stain with a phone while water drips onto the hallway floor below',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-first-hour-checklist-960w.jpg 960w, /assets/img/hero-first-hour-checklist.jpg 1920w',
    ),
    'cost' => 
    array (
      'src' => '/assets/img/hero-cost.jpg',
      'alt' => 'Technician measuring moisture in a water-stained wall with a blank clipboard nearby during a damage assessment',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-cost-960w.jpg 960w, /assets/img/hero-cost.jpg 1920w',
    ),
    'insurance' => 
    array (
      'src' => '/assets/img/hero-insurance.jpg',
      'alt' => 'A technician photographs a water-stained wall with a phone to document damage for an insurance claim in a Florida home',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-insurance-960w.jpg 960w, /assets/img/hero-insurance.jpg 1920w',
    ),
    'how-it-works' => 
    array (
      'src' => '/assets/img/hero-how-it-works.jpg',
      'alt' => 'Technician setting up air movers and a dehumidifier beside a damp wall in a Florida home',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-how-it-works-960w.jpg 960w, /assets/img/hero-how-it-works.jpg 1920w',
    ),
    'contact' => 
    array (
      'src' => '/assets/img/hero-contact.jpg',
      'alt' => 'Office front desk with a telephone and a potted palm, with a plain white van outside the glass door',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-contact-960w.jpg 960w, /assets/img/hero-contact.jpg 1920w',
    ),
    'about' => 
    array (
      'src' => '/assets/img/hero-about.jpg',
      'alt' => 'Three technicians loading drying fans and a dehumidifier into a plain white van outside a Florida home',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-about-960w.jpg 960w, /assets/img/hero-about.jpg 1920w',
    ),
    'cape-coral' => 
    array (
      'src' => '/assets/img/hero-cape-coral.jpg',
      'alt' => 'Canal-front homes with screened pool enclosures and private docks along a canal in Cape Coral, Florida',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-cape-coral-960w.jpg 960w, /assets/img/hero-cape-coral.jpg 1920w',
    ),
    'lehigh-acres' => 
    array (
      'src' => '/assets/img/hero-lehigh-acres.jpg',
      'alt' => 'Single-story concrete-block homes on large grassy lots along a quiet street in Lehigh Acres, Florida',
      'width' => 1440,
      'height' => 960,
      'srcset' => '/assets/img/hero-lehigh-acres-640w.jpg 640w, /assets/img/hero-lehigh-acres-960w.jpg 960w, /assets/img/hero-lehigh-acres.jpg 1440w',
    ),
    'areas' => 
    array (
      'src' => '/assets/img/hero-areas.jpg',
      'alt' => 'Historic brick riverfront buildings and royal palm trees along the Caloosahatchee River in downtown Fort Myers',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-areas-960w.jpg 960w, /assets/img/hero-areas.jpg 1920w',
    ),
    'north-fort-myers' => 
    array (
      'src' => '/assets/img/hero-north-fort-myers.jpg',
      'alt' => 'Manufactured home with carport beside the Caloosahatchee River in North Fort Myers, Florida',
      'width' => 1440,
      'height' => 960,
      'srcset' => '/assets/img/hero-north-fort-myers-640w.jpg 640w, /assets/img/hero-north-fort-myers-960w.jpg 960w, /assets/img/hero-north-fort-myers.jpg 1440w',
    ),
    'fort-myers-beach' => 
    array (
      'src' => '/assets/img/hero-fort-myers-beach.jpg',
      'alt' => 'Elevated beach house on wooden pilings behind white sand and sea oats on the Gulf shore at Fort Myers Beach, Florida',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-fort-myers-beach-960w.jpg 960w, /assets/img/hero-fort-myers-beach.jpg 1920w',
    ),
    'estero' => 
    array (
      'src' => '/assets/img/hero-estero.jpg',
      'alt' => 'Mediterranean-style condo buildings with tile roofs around a landscaped courtyard with a fountain in Estero, Florida',
      'width' => 1600,
      'height' => 1067,
      'srcset' => '/assets/img/hero-estero-960w.jpg 960w, /assets/img/hero-estero.jpg 1600w',
    ),
    'bonita-springs' => 
    array (
      'src' => '/assets/img/hero-bonita-springs.jpg',
      'alt' => 'Riverfront condos and homes with tile roofs beside a mangrove-lined river in Bonita Springs, Florida',
      'width' => 1600,
      'height' => 1067,
      'srcset' => '/assets/img/hero-bonita-springs-960w.jpg 960w, /assets/img/hero-bonita-springs.jpg 1600w',
    ),
    'privacy-policy' => 
    array (
      'src' => '/assets/img/hero-privacy-policy.jpg',
      'alt' => 'Blank papers, a small brass padlock, a closed laptop and a pen on a bright wooden desk',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-privacy-policy-960w.jpg 960w, /assets/img/hero-privacy-policy.jpg 1920w',
    ),
    'terms' => 
    array (
      'src' => '/assets/img/hero-terms.jpg',
      'alt' => 'A homeowner and a technician review a written scope of work at a kitchen table in a Florida home',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-terms-960w.jpg 960w, /assets/img/hero-terms.jpg 1920w',
    ),
    'disclaimer' => 
    array (
      'src' => '/assets/img/hero-disclaimer.jpg',
      'alt' => 'A technician shows moisture meter readings to a homeowner beside a water-stained wall in a Florida home',
      'width' => 1920,
      'height' => 1280,
      'srcset' => '/assets/img/hero-disclaimer-960w.jpg 960w, /assets/img/hero-disclaimer.jpg 1920w',
    ),
  ),
  'help' => 
  array (
    'home' => 
    array (
      0 => 
      array (
        'src' => '/assets/img/help-emergency-water-removal.jpg',
        'alt' => 'A wet-vacuum extracting standing water from a tiled floor in a Fort Myers home',
        'width' => 474,
        'height' => 267,
      ),
      1 => 
      array (
        'src' => '/assets/img/help-structural-drying.jpg',
        'alt' => 'Air movers and a dehumidifier drying an opened wall cavity in a Fort Myers home, with a moisture meter on a tripod',
        'width' => 474,
        'height' => 267,
      ),
      2 => 
      array (
        'src' => '/assets/img/help-sewage-cleanup.jpg',
        'alt' => 'A technician in protective coveralls and a respirator vacuums dark contaminated water from a bathroom floor',
        'width' => 474,
        'height' => 267,
      ),
      3 => 
      array (
        'src' => '/assets/img/help-flood-storm-cleanup.jpg',
        'alt' => 'A flooded residential street lined with palm trees and stucco houses in Fort Myers after a storm, with sandbags at a driveway',
        'width' => 474,
        'height' => 267,
      ),
      4 => 
      array (
        'src' => '/assets/img/help-leaks-every-kind.jpg',
        'alt' => 'A leaking air handler with water in its drip pan and a bucket catching drips, with a water heater in the garage behind it',
        'width' => 474,
        'height' => 267,
      ),
      5 => 
      array (
        'src' => '/assets/img/help-every-property.jpg',
        'alt' => 'A Fort Myers street with a stucco single-family home, a low-rise condo building and a manufactured home with a carport',
        'width' => 474,
        'height' => 267,
      ),
      6 => 
      array (
        'src' => '/assets/img/help-property-types.jpg',
        'alt' => 'A stucco home, a three-story condo building and a manufactured home with a carport on a palm-lined Fort Myers street',
        'width' => 474,
        'height' => 267,
      ),
    ),
    'about' => 
    array (
      0 => 
      array (
        'src' => '/assets/img/help-emergency-water-removal.jpg',
        'alt' => 'A wet-vacuum extracting standing water from a tiled floor in a Fort Myers home',
        'width' => 474,
        'height' => 267,
      ),
      1 => 
      array (
        'src' => '/assets/img/help-structural-drying.jpg',
        'alt' => 'Air movers and a dehumidifier drying an opened wall cavity in a Fort Myers home, with a moisture meter on a tripod',
        'width' => 474,
        'height' => 267,
      ),
      2 => 
      array (
        'src' => '/assets/img/help-sewage-cleanup.jpg',
        'alt' => 'A technician in protective coveralls and a respirator vacuums dark contaminated water from a bathroom floor',
        'width' => 474,
        'height' => 267,
      ),
      3 => 
      array (
        'src' => '/assets/img/help-flood-storm-cleanup.jpg',
        'alt' => 'A flooded residential street lined with palm trees and stucco houses in Fort Myers after a storm, with sandbags at a driveway',
        'width' => 474,
        'height' => 267,
      ),
      4 => 
      array (
        'src' => '/assets/img/help-leaks-every-kind.jpg',
        'alt' => 'A leaking air handler with water in its drip pan and a bucket catching drips, with a water heater in the garage behind it',
        'width' => 474,
        'height' => 267,
      ),
      5 => 
      array (
        'src' => '/assets/img/about-floors-cabinets.jpg',
        'alt' => 'A swollen cabinet base and curled wet vinyl plank flooring checked with a moisture meter in a Fort Myers home',
        'width' => 474,
        'height' => 267,
      ),
      6 => 
      array (
        'src' => '/assets/img/help-property-types.jpg',
        'alt' => 'A stucco home, a three-story condo building and a manufactured home with a carport on a palm-lined Fort Myers street',
        'width' => 474,
        'height' => 267,
      ),
    ),
  ),
  'maps' => 
  array (
    'cape-coral' => 
    array (
      'src' => '/assets/img/map-cape-coral.jpg',
      'alt' => 'Map of Cape Coral and the Lee County service area, showing the Caloosahatchee River, Fort Myers and Lehigh Acres',
      'width' => 1200,
      'height' => 560,
    ),
    'fort-myers-beach' => 
    array (
      'src' => '/assets/img/map-fort-myers-beach.jpg',
      'alt' => 'Map of Fort Myers Beach on Estero Island and the Lee County service area, showing Sanibel, Estero Bay and San Carlos Park',
      'width' => 1200,
      'height' => 560,
    ),
  ),
  'areas' => 
  array (
    'cape-coral' => 
    array (
      'src' => '/assets/img/area-cape-coral.jpg',
      'alt' => 'Canal-front homes with screened lanais and boat docks in Cape Coral, Florida',
      'width' => 474,
      'height' => 316,
    ),
    'lehigh-acres' => 
    array (
      'src' => '/assets/img/area-lehigh-acres.jpg',
      'alt' => 'Concrete block homes on flat lots along a quiet street in Lehigh Acres, Florida',
      'width' => 474,
      'height' => 316,
    ),
    'north-fort-myers' => 
    array (
      'src' => '/assets/img/area-north-fort-myers.jpg',
      'alt' => 'Riverfront manufactured homes and houses along the Caloosahatchee River in North Fort Myers, Florida',
      'width' => 474,
      'height' => 316,
    ),
    'fort-myers-beach' => 
    array (
      'src' => '/assets/img/area-fort-myers-beach.jpg',
      'alt' => 'White sand beach and elevated beachfront homes on the Gulf at Fort Myers Beach, Florida',
      'width' => 474,
      'height' => 316,
    ),
    'estero' => 
    array (
      'src' => '/assets/img/area-estero.jpg',
      'alt' => 'Gated condo and coach-home community around a lake in Estero, Florida',
      'width' => 474,
      'height' => 316,
    ),
    'bonita-springs' => 
    array (
      'src' => '/assets/img/area-bonita-springs.jpg',
      'alt' => 'Condos and homes along a river waterway with docks in Bonita Springs, Florida',
      'width' => 474,
      'height' => 316,
    ),
  ),
);
