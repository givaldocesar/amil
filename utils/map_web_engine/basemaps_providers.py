BASEMAP_PROVIDERS = {
    "google_sat": {
        "name": "Google Satellite", 
        "url": "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", 
        "attribution": "Google"
    },
    "google_hybrid": {
        "name": "Google Hybrid", 
        "url": "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", 
        "attribution": "Google"
    },
    "google_terrain": {
        "name": "Google Terrain", 
        "url": "https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}", 
        "attribution": "Google"
    },
    "osm": {
        "name": "OpenStreet Map", 
        "url": "https://tile.openstreetmap.org/{z}/{x}/{y}.png", 
        "attribution": "&copy; OpenStreetMap"
    },
    "esri": {
        "name": "Esri World Imagery", 
        "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", 
        "attribution": "Esri"
    },
    "cartodb_positron": {
        "name": "CartoDB Positron", 
        "url": "https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png", 
        "attribution": "&copy; CARTO"
    }
}