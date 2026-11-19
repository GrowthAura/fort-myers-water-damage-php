<?php
// Kinds-grid card backgrounds (Task 5, homepage only). Written by the image
// worker. Shape: ['kinds' => ['home' => [card-index => [src, alt, width,
// height]]]]. Card order matches the 'kinds' block in site/data/homepage.php
// exactly (index 0 = AC leak ... index 12 = floors/cabinets). Alt text is a
// record-only honest description (CSS backgrounds take no alt attribute).
// All 13 masters: 760x864 JPEG, geotagged Fort Myers 26.6406,-81.8723,
// EXIF stripped except GPS. Coordinator: copy to site/data/manifest-kinds.php
// (or merge the 'kinds' key into $MEDIA in site/data/media-manifest.php).
return ['kinds' => ['home' => [
    0 => ['src' => '/assets/img/kinds-ac-leak.jpg', 'alt' => 'Air handler unit with a dripping condensate drain line, a water-stained wall and a puddle on the tile floor', 'width' => 760, 'height' => 864],
    1 => ['src' => '/assets/img/kinds-ceiling-leak.jpg', 'alt' => 'Brown water stain spreading across a white ceiling with a drip falling, palm trees visible through the window', 'width' => 760, 'height' => 864],
    2 => ['src' => '/assets/img/kinds-condo-leak.jpg', 'alt' => 'Condo living room with a wet patch dripping from the ceiling, sliding glass doors and palm trees outside', 'width' => 760, 'height' => 864],
    3 => ['src' => '/assets/img/kinds-sewage-backup.jpg', 'alt' => 'Murky water pooled around a floor drain in a bathroom with a toilet and bathtub', 'width' => 760, 'height' => 864],
    4 => ['src' => '/assets/img/kinds-cast-iron-pipe.jpg', 'alt' => 'Cracked, rusted cast iron drain pipe dripping into a puddle under a house', 'width' => 760, 'height' => 864],
    5 => ['src' => '/assets/img/kinds-burst-pipe.jpg', 'alt' => 'Split braided supply line spraying water under a bathroom sink', 'width' => 760, 'height' => 864],
    6 => ['src' => '/assets/img/kinds-water-heater-leak.jpg', 'alt' => 'Rusted water heater tank leaking across a garage floor with wet cardboard boxes', 'width' => 760, 'height' => 864],
    7 => ['src' => '/assets/img/kinds-appliance-leak.jpg', 'alt' => 'Dishwasher leaking water across a wood kitchen floor', 'width' => 760, 'height' => 864],
    8 => ['src' => '/assets/img/kinds-slab-leak.jpg', 'alt' => 'Swollen baseboard pulling away from a damp tile floor', 'width' => 760, 'height' => 864],
    9 => ['src' => '/assets/img/kinds-vacant-home.jpg', 'alt' => 'Empty seasonal home with sheet-covered furniture and a musty water-stained ceiling corner', 'width' => 760, 'height' => 864],
    10 => ['src' => '/assets/img/kinds-mobile-home.jpg', 'alt' => 'Manufactured home interior with sagging vinyl flooring over wet particle board and a water-stained wall base', 'width' => 760, 'height' => 864],
    11 => ['src' => '/assets/img/kinds-flood-storm.jpg', 'alt' => 'Flooded Florida residential street with murky water around stucco homes and palm trees under a storm sky', 'width' => 760, 'height' => 864],
    12 => ['src' => '/assets/img/kinds-floors-cabinets.jpg', 'alt' => 'Swollen kitchen cabinet base and cupping laminate floor planks with a puddle of water', 'width' => 760, 'height' => 864],
]]];
