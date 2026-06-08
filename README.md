# AMIL — Application for Local Interactive Maps
### *An advanced QGIS plugin to export vector layers into lightweight, fully independent Leaflet or OpenLayers WebGIS applications.*

[![QGIS Version](https://img.shields.io/badge/QGIS-3.10+-green.svg)](https://qgis.org)
[![Plugin Version](https://img.shields.io/badge/version-2.0-blue.svg)](https://github.com/givaldocesar/amil)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

---

## Overview

**AMIL (Aplicação para Mapas Interativos Locais)** is a powerful QGIS plugin designed to bridge the gap between desktop GIS workflows and interactive web mapping. It allows geologists, engineers, and GIS analysts to effortlessly export their current QGIS vector layers into standalone, responsive HTML/JS/CSS bundles. 

Whether you need a quick shareable preview or a completely autonomous offline cartographic solution for field surveys, AMIL generates production-ready web maps using either **Leaflet** or **OpenLayers** engines.

---

## Key Features

### Multi-Engine Core Architecture
* **Leaflet Engine:** Lightweight, ultra-fast, and smooth performance for standard web applications.
* **OpenLayers Engine:** Advanced object-oriented structure optimized for handling large, dense vector datasets with robust canvas-based rendering.

### Fully Autonomous Offline Mode
* Packaged with embedded core assets (`ol.js`, `ol.css`, `leaflet.js`, `leaflet.css`) copied directly into the output directory.
* Runs perfectly in isolated network environments or offline field laptops without requiring external CDN requests.

### Intelligent Visual Symbology & Collapsible Legends
* **Leaflet Control:** Native, space-saving toggle panel (`{ collapsed: true }`) that smoothly slides open on hover/interaction.
* **OpenLayers Control:** Custom-built overlay control featuring a responsive collapsible accordion (`+` / `− Legenda`).
* **Dynamic Cartographic Icons:** Generates real-time, dynamic legend markers directly derived from your QGIS `StyleConfig` without saving flat image files:
  * 🟦 **Polygons:** Matching border colors and semi-transparent fills.
  * ➖ **Lines:** Vector lines respecting QGIS stroke width and colors.
  * 🟢 **Points:** Rounded markers styled with precise radius and contours.

### Precise Popups & Smart Attribute Tables
* Interactive feature clicks display an elegant, clean tabular view of attributes.
* **Zero-Null Filtering:** Automatically filters out empty fields, nulls, undefined values, and internal structural keys (e.g., `geometry`) to keep popups professional and human-readable.
* **Per-Attribute Precision Rounding:** Reads layer-specific `AttributeConfig` attributes. For floating-point values (`is_float`), it respects custom decimal settings (`decimals`) and formats numbers to regional presentation standards (e.g., converting decimals to Brazilian `pt-BR` comma formatting).

### Enhanced User Experience (UX)
* **Auto-Extent Fitting:** Automatically computes layer bounding boxes and pans/zooms the map framework directly to your data extents upon loading. Handles mathematical reprojections from `EPSG:4326` (Degrees) to `EPSG:3857` (Web Mercator Meters) automatically.
* **Automated Browser Launch:** Gives the user full control to automatically open the generated map (`index.html`) in their operating system's default browser immediately after export.

### Global Internationalization (i18n)
* Built-in support for multiple languages including **Portuguese (Native)**, **English**, and **Spanish** using standard Qt translation lifecycles (`.ts` / `.qm`).

---

## Exported Package Structure

When you export a web map with AMIL, it generates a clean, self-contained directory:

```text
output_directory/
│
├── index.html               # The main webpage layout and map viewport
│
├── openlayers/ or leaflet/  # Offline assets (CSS and JS files cloned by the plugin)
│   ├── ol.js / leaflet.js
│   └── ol.css / leaflet.css
│
└── scripts/
    ├── style.css            # Custom UI presentation stylesheets (Legends, Popups)
    ├── core.js              # Map initialization, viewpoint configurations & extents
    ├── basemaps.js          # Google Satellite, Hybrid, OpenStreetMap layer definitions
    ├── legend.js            # Dynamic interactive layer switcher control logic
    ├── popup.js             # Pixel feature detection, data rendering and formatting logic
    └── layers/
        ├── layer_id_1.js    # Decoupled GeoJSON data layers
        └── layer_id_2.js    # Independent vector styling scripts