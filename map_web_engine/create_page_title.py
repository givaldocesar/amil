def create_page_title(title):
    head_tags = f"""
    <title>{title or "Amil WebGIS - Leaflet"}</title>
    <style>
        html, body {{ 
            width: 100%; 
            height: 100%; 
            margin: 0; 
            padding: 0; 
            display: flex; 
            flex-direction: column;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}
        
        #map-header {{ 
            background-color: #1a1a1a; 
            color: #ffffff; 
            padding: 12px 20px; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.3); 
            z-index: 1000; 
        }}
        
        #map-header h1 {{ 
            margin: 0; 
            font-size: 1.3rem; 
            font-weight: 600; 
            letter-spacing: 0.5px;
            text-align: center;
        }}
        
        #map {{ 
            flex: 1; 
            width: 100%; 
        }}
    </style>
    """

    body_tags = f"""
    <div id="map-header">
        <h1>{title}</h1>
    </div>"""
    
    return head_tags, body_tags