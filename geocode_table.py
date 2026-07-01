import pandas as pd
import json
import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium

# 1. Transcribed cases from the user's table image
cases_data = [
    {
        "id": 1,
        "nombre": "LFL",
        "sexo": "Femenino",
        "edad": 26,
        "umf": "44",
        "domicilio": "Encinos 305, Col. Cipres",
        "institucion": "IMSS Ordinario",
        "fecha_sintomas": "18/05/2026",
        "fecha_atencion": "19/05/2026",
        "folio": "72874",
        "colonia": "Col. Cipres",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34220"
    },
    {
        "id": 2,
        "nombre": "JPO",
        "sexo": "Masculino",
        "edad": 29,
        "umf": "49",
        "domicilio": "C.Simon Bolivar 123, Col. Asentamientos Humanos",
        "institucion": "ISSSTE",
        "fecha_sintomas": "17/05/2026",
        "fecha_atencion": "20/05/2026",
        "folio": "72973",
        "colonia": "Col. Asentamientos Humanos",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34170"
    },
    {
        "id": 3,
        "nombre": "ARR",
        "sexo": "Masculino",
        "edad": 41,
        "umf": "HGZ 1",
        "domicilio": "C. Principal s/n, Col. El Presidio",
        "institucion": "IMSS Ordinario",
        "fecha_sintomas": "18/05/2026",
        "fecha_atencion": "21/05/2026",
        "folio": "73145",
        "colonia": "Col. El Presidio",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34166"
    },
    {
        "id": 4,
        "nombre": "GER",
        "sexo": "Masculino",
        "edad": 32,
        "umf": "44",
        "domicilio": "C. Morelos 206, Col. Jose Ma.Morelos",
        "institucion": "SSA",
        "fecha_sintomas": "18/05/2026",
        "fecha_atencion": "21/05/2026",
        "folio": "73098",
        "colonia": "Col. Jose Ma.Morelos",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34160"
    },
    {
        "id": 5,
        "nombre": "ARGV",
        "sexo": "Masculino",
        "edad": 34,
        "umf": "44",
        "domicilio": "C. Angeles Mena 114,Col. Legisladores",
        "institucion": "IMSS Ordinario",
        "fecha_sintomas": "17/05/2026",
        "fecha_atencion": "21/05/2026",
        "folio": "73093",
        "colonia": "Col. Legisladores",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34046"
    },
    {
        "id": 6,
        "nombre": "UNL",
        "sexo": "Masculino",
        "edad": 24,
        "umf": "44",
        "domicilio": "Conocido en el Carmen y Anexos",
        "institucion": "IMSS COPLAMAR",
        "fecha_sintomas": "18/05/2026",
        "fecha_atencion": "21/05/2026",
        "folio": "73095",
        "colonia": "El Carmen y Anexos",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34105"
    },
    {
        "id": 7,
        "nombre": "FSG",
        "sexo": "Femenino",
        "edad": 27,
        "umf": "49",
        "domicilio": "Conocido, Col. Rio Dorado",
        "institucion": "SSA",
        "fecha_sintomas": "16/05/2026",
        "fecha_atencion": "21/05/2026",
        "folio": "73117",
        "colonia": "Col. Rio Dorado",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34117"
    },
    {
        "id": 8,
        "nombre": "CHG",
        "sexo": "Femenino",
        "edad": 29,
        "umf": "49",
        "domicilio": "C. 12 de Octubre 506, Col. Constitución",
        "institucion": "SSA",
        "fecha_sintomas": "18/05/2026",
        "fecha_atencion": "21/05/2026",
        "folio": "75083",
        "colonia": "Col. Constitución",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34218"
    },
    {
        "id": 9,
        "nombre": "AEGR",
        "sexo": "Femenino",
        "edad": 34,
        "umf": "1",
        "domicilio": "C. México 408, Col. Lazaro Cardenas",
        "institucion": "IMSS Ordinario",
        "fecha_sintomas": "20/05/2026",
        "fecha_atencion": "22/05/2026",
        "folio": "73185",
        "colonia": "Col. Lazaro Cardenas",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34260"
    },
    {
        "id": 10,
        "nombre": "MCGR",
        "sexo": "Femenino",
        "edad": 29,
        "umf": "44",
        "domicilio": "Francisco Villa 407, Col. Arturo Gamiz",
        "institucion": "IMSS Ordinario",
        "fecha_sintomas": "18/05/2026",
        "fecha_atencion": "22/05/2026",
        "folio": "73163",
        "colonia": "Col. Arturo Gamiz",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34180"
    },
    {
        "id": 11,
        "nombre": "MJGC",
        "sexo": "Femenino",
        "edad": 32,
        "umf": "44",
        "domicilio": "Contadores 449, Col. 16 de Septiembre",
        "institucion": "IMSS Ordinario",
        "fecha_sintomas": "20/05/2026",
        "fecha_atencion": "22/05/2026",
        "folio": "73165",
        "colonia": "Col. 16 de Septiembre",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34100"
    },
    {
        "id": 12,
        "nombre": "YCE",
        "sexo": "Femenino",
        "edad": 33,
        "umf": "44",
        "domicilio": "Santa Catarina 148, Col. San Jose",
        "institucion": "IMSS Ordinario",
        "fecha_sintomas": "21/05/2026",
        "fecha_atencion": "22/05/2026",
        "folio": "73210",
        "colonia": "Col. San Jose",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34105"
    },
    {
        "id": 13,
        "nombre": "MMF",
        "sexo": "Masculino",
        "edad": 27,
        "umf": "44",
        "domicilio": "Hacienda Suchil 223, Frac. San Gabriel",
        "institucion": "IMSS Ordinario",
        "fecha_sintomas": "20/05/2026",
        "fecha_atencion": "22/05/2026",
        "folio": "73183",
        "colonia": "Frac. San Gabriel",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34167"
    },
    {
        "id": 14,
        "nombre": "DCLS",
        "sexo": "Femenino",
        "edad": 25,
        "umf": "IMSS",
        "domicilio": "Panama 303, Col. Francisco Zarco, CP. 34210",
        "institucion": "IMSS Ordinario",
        "fecha_sintomas": "21/05/2026",
        "fecha_atencion": "22/05/2026",
        "folio": "73193",
        "colonia": "Col. Francisco Zarco",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34210"
    },
    {
        "id": 15,
        "nombre": "ECS",
        "sexo": "Masculino",
        "edad": 24,
        "umf": "IMSS",
        "domicilio": "Geranio 417, Col. La Virgen, CP 34049",
        "institucion": "IMSS Ordinario",
        "fecha_sintomas": "22/05/2026",
        "fecha_atencion": "22/05/2026",
        "folio": "73256",
        "colonia": "Col. La Virgen",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34049"
    },
    {
        "id": 16,
        "nombre": "COCG",
        "sexo": "Masculino",
        "edad": 24,
        "umf": "44",
        "domicilio": "Luis Angel Tejada Espino 223, Col. Morga, CP. 34019",
        "institucion": "IMSS Ordinario",
        "fecha_sintomas": "24/05/2026",
        "fecha_atencion": "24/05/2026",
        "folio": "S/F",
        "colonia": "Col. Morga",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34019"
    },
    {
        "id": 17,
        "nombre": "APPV",
        "sexo": "Femenino",
        "edad": 31,
        "umf": "44",
        "domicilio": "Leo 601, Col. Valentín Gómez Farías, CP 34010",
        "institucion": "IMSS Ordinario",
        "fecha_sintomas": "23/05/2026",
        "fecha_atencion": "25/05/2026",
        "folio": "73322",
        "colonia": "Col. Valentín Gómez Farías",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34010"
    },
    {
        "id": 18,
        "nombre": "ALQA",
        "sexo": "Femenino",
        "edad": 35,
        "umf": "IMSS",
        "domicilio": "Neftali Montes 104, Fracc. Locutores CP. 34167",
        "institucion": "ISSSTE",
        "fecha_sintomas": "23/05/2026",
        "fecha_atencion": "26/05/2026",
        "folio": "73391",
        "colonia": "Fracc. Locutores",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34167"
    },
    {
        "id": 19,
        "nombre": "RARV",
        "sexo": "Masculino",
        "edad": 27,
        "umf": "IMSS",
        "domicilio": "Francisco Favela 116, Col. Miguel de la Madrid",
        "institucion": "IMSS Ordinario",
        "fecha_sintomas": "21/05/2026",
        "fecha_atencion": "26/05/2026",
        "folio": "73395",
        "colonia": "Col. Miguel de la Madrid",
        "municipio": "Durango",
        "estado": "Durango",
        "cp": "34210"
    }
]

# Accurate manual coordinates fallback to ensure exact geolocation in Victoria de Durango
coords_override = {
    "Col. Cipres": (24.0322, -104.6052),
    "Col. Asentamientos Humanos": (23.9961, -104.6548),
    "Col. El Presidio": (24.0152, -104.6190),
    "Col. Jose Ma.Morelos": (24.0177, -104.6465),
    "Col. Legisladores": (24.0220, -104.6547),
    "El Carmen y Anexos": (24.0535, -104.6291),
    "Col. Rio Dorado": (24.0841, -104.5950),
    "Col. Constitución": (24.0520, -104.6473),
    "Col. Lazaro Cardenas": (24.0435, -104.6300),
    "Col. Arturo Gamiz": (23.9995, -104.6432),
    "Col. 16 de Septiembre": (24.0577, -104.6644),
    "Col. San Jose": (24.0345, -104.6400),
    "Frac. San Gabriel": (24.0150, -104.6025),
    "Col. Francisco Zarco": (24.0197, -104.6853),
    "Col. La Virgen": (24.0381, -104.7042),
    "Col. Morga": (24.0494, -104.6698),
    "Col. Valentín Gómez Farías": (24.0507, -104.6989),
    "Fracc. Locutores": (24.0174, -104.6055),
    "Col. Miguel de la Madrid": (24.0041, -104.6931)
}

print("Iniciando georreferenciación...")
geolocator = Nominatim(user_agent="visor_pvu_durango_cases")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.5)

results = []
for item in cases_data:
    col = item["colonia"]
    addr = item["domicilio"]
    query = f"{col}, Victoria de Durango, Durango, Mexico"
    
    print(f"Buscando: {query}...")
    lat, lng = None, None
    
    # Try Nominatim first
    try:
        location = geocode(query)
        if location:
            # Check if coordinates are in Durango general area
            if 23.8 < location.latitude < 24.2 and -104.8 < location.longitude < -104.4:
                lat = location.latitude
                lng = location.longitude
                print(f"  Encontrado en Nominatim: {lat}, {lng}")
    except Exception as e:
        print(f"  Error Nominatim: {e}")
        
    # If not found or outside bounds, use override
    if lat is None or lng is None:
        if col in coords_override:
            lat, lng = coords_override[col]
            print(f"  Usando coordenadas manuales: {lat}, {lng}")
        else:
            lat, lng = 24.0277, -104.6532  # Centro de Durango
            print(f"  Usando centro de Durango por defecto: {lat}, {lng}")
            
    item["lat"] = lat
    item["lng"] = lng
    results.append(item)

# 2. Save as CSV
df = pd.DataFrame(results)
csv_path = "casos_tabla_coordenadas.csv"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"Archivo CSV guardado en: {csv_path}")

# 3. Save as standard JSON
json_path = "casos_tabla.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"Archivo JSON guardado en: {json_path}")

# 4. Save as GeoJSON
geojson = {
    "type": "FeatureCollection",
    "features": []
}

for item in results:
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [item["lng"], item["lat"]]
        },
        "properties": {
            "id": item["id"],
            "nombre": item["nombre"],
            "sexo": item["sexo"],
            "edad": item["edad"],
            "umf": item["umf"],
            "domicilio": item["domicilio"],
            "colonia": item["colonia"],
            "municipio": item["municipio"],
            "cp": item["cp"],
            "institucion": item["institucion"],
            "fecha_sintomas": item["fecha_sintomas"],
            "fecha_atencion": item["fecha_atencion"],
            "folio": item["folio"]
        }
    }
    geojson["features"].append(feature)

geojson_path = "casos_tabla.geojson"
with open(geojson_path, "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)
print(f"Archivo GeoJSON guardado en: {geojson_path}")

# 5. Create Folium Map
m = folium.Map(location=[24.025, -104.65], zoom_start=13, tiles="cartodbpositron")

# Health institutions color mapping
inst_colors = {
    "IMSS Ordinario": "#006341",    # Verde IMSS
    "IMSS COPLAMAR": "#2d8a4e",     # Verde claro COPLAMAR
    "IMSS": "#006341",              # Verde IMSS
    "ISSSTE": "#9f2241",            # Guinda ISSSTE
    "SSA": "#071e54"                # Azul marino SSA
}

# Add cases to map
for item in results:
    inst = item["institucion"]
    color = inst_colors.get(inst, "#ff7800") # Default orange if not found
    
    popup_html = f"""
    <div style="font-family: Arial, sans-serif; font-size: 12px; width: 250px;">
        <h4 style="margin: 0 0 5px 0; color: {color}; border-bottom: 2px solid {color}; padding-bottom: 5px;">Caso #{item['id']} ({item['nombre']})</h4>
        <b>Domicilio:</b> {item['domicilio']}<br>
        <b>Colonia:</b> {item['colonia']}<br>
        <b>Código Postal:</b> {item['cp']}<br>
        <b>Edad:</b> {item['edad']} años | <b>Sexo:</b> {item['sexo']}<br>
        <b>Institución:</b> {item['institucion']} (UMF {item['umf']})<br>
        <b>F. Síntomas:</b> {item['fecha_sintomas']}<br>
        <b>F. Atención:</b> {item['fecha_atencion']}<br>
        <b>Folio:</b> {item['folio']}
    </div>
    """
    
    # 5a. Color the colony area with a circle overlay (buffer zone of 800m)
    folium.Circle(
        location=[item["lat"], item["lng"]],
        radius=800,  # 800 meters radius to highlight the colony area
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.2,
        weight=1.5,
        tooltip=f"Área de Influencia: {item['colonia']}"
    ).add_to(m)

    # 5b. Add the case marker pin
    folium.Marker(
        location=[item["lat"], item["lng"]],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"Caso {item['id']}: Col. {item['colonia']} ({inst})",
        icon=folium.Icon(color="red", icon="exclamation-circle", prefix="fa")
    ).add_to(m)

# 6. Add Legend for colored colonies (Health Institutions)
legend_html = f"""
<div style="position: fixed; 
            bottom: 30px; right: 30px; width: 250px; height: 160px; 
            border: 2px solid #ccc; z-index: 9999; font-size: 12px;
            background-color: white; opacity: 0.95; padding: 12px; 
            border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            font-family: Arial, sans-serif;">
    <b style="font-size: 13px; display: block; margin-bottom: 8px; color: #333; border-bottom: 1px solid #eee; padding-bottom: 4px;">
        Zonas de Casos por Institución
    </b>
    <div style="display: flex; align-items: center; margin-bottom: 6px;">
        <span style="display: inline-block; width: 16px; height: 16px; background-color: #006341; border-radius: 50%; margin-right: 8px; opacity: 0.7;"></span>
        <span>IMSS Ordinario / IMSS</span>
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 6px;">
        <span style="display: inline-block; width: 16px; height: 16px; background-color: #2d8a4e; border-radius: 50%; margin-right: 8px; opacity: 0.7;"></span>
        <span>IMSS COPLAMAR</span>
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 6px;">
        <span style="display: inline-block; width: 16px; height: 16px; background-color: #9f2241; border-radius: 50%; margin-right: 8px; opacity: 0.7;"></span>
        <span>ISSSTE</span>
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 6px;">
        <span style="display: inline-block; width: 16px; height: 16px; background-color: #071e54; border-radius: 50%; margin-right: 8px; opacity: 0.7;"></span>
        <span>SSA</span>
    </div>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

map_html_path = "casos_tabla_mapa.html"
m.save(map_html_path)
print(f"Mapa interactivo HTML guardado en: {map_html_path}")

