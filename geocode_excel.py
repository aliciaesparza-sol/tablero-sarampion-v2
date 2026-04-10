import pandas as pd
import os
import time
import shutil
from geopy.geocoders import Nominatim

base = os.path.expanduser('~') + '/OneDrive/Escritorio/PVU'
input_path = None
for root, dirs, files in os.walk(base):
    for f in files:
        if f == 'CASOS_NOTIFICADOS_2026_COMPLETO_ACTUALIZADO.xlsx':
            input_path = os.path.join(root, f)
            break
    if input_path: break

if not input_path:
    print("Archivo principal no encontrado.")
    exit()

print(f"Cargando archivo: {input_path}")
temp_input = input_path.replace('.xlsx', '_temp_read.xlsx')
shutil.copy2(input_path, temp_input)

# LEER SOLO 35 COLUMNAS! Para evitar pasarnos del maximo de 16384 cuando agreguemos las cooredandas
df = pd.read_excel(temp_input, usecols=range(35))
os.remove(temp_input)

if 'Latitud' not in df.columns:
    df.insert(len(df.columns), 'Latitud', None)
if 'Longitud' not in df.columns:
    df.insert(len(df.columns), 'Longitud', None)

from geopy.geocoders import ArcGIS

geolocator = ArcGIS()

unique_addresses = {}
for idx, row in df.iterrows():
    col = str(row.get('colonia', '')).strip().upper()
    mun = str(row.get('municipio', '')).strip().upper()
    if col in ('NAN', 'NONE', 'SIN COLONIA', 'NO APLICA', 'SN', 'DOMICILIO CONOCIDO', ''):
        col = ''
    if mun in ('NAN', 'NONE', ''):
        mun = ''
        
    if mun:
        parts = []
        if col: parts.append(col)
        parts.append(mun)
        parts.append("Durango")
        parts.append("Mexico")
        search_query = ", ".join(parts)
        if search_query not in unique_addresses:
            unique_addresses[search_query] = None

print(f"Buscando {len(unique_addresses)} direcciones...", flush=True)

for i, query in enumerate(unique_addresses.keys()):
    if query == ", Durango, Mexico": continue
    try:
        print(f"[{i+1}/{len(unique_addresses)}] {query}", flush=True)
        # Timeout agresivo, solo probar 1 vez.
        loc = geolocator.geocode(query, timeout=4)
        if loc:
            unique_addresses[query] = (loc.latitude, loc.longitude)
        else:
            # Fallback a municipio
            parts = query.split(", ")
            if len(parts) > 3:
                fb = ", ".join(parts[1:])
                loc2 = geolocator.geocode(fb, timeout=4)
                if loc2: unique_addresses[query] = (loc2.latitude, loc2.longitude)
        time.sleep(0.1)
    except Exception as e:
        print(f" Error en {query}: {e}", flush=True)
        time.sleep(0.1)

for idx, row in df.iterrows():
    col = str(row.get('colonia', '')).strip().upper()
    mun = str(row.get('municipio', '')).strip().upper()
    if col in ('NAN', 'NONE', 'SIN COLONIA', 'NO APLICA', 'SN', 'DOMICILIO CONOCIDO', ''): col = ''
    if mun in ('NAN', 'NONE', ''): mun = ''
    if mun:
        parts = []
        if col: parts.append(col)
        parts.append(mun)
        parts.append("Durango")
        parts.append("Mexico")
        query = ", ".join(parts)
        coords = unique_addresses.get(query)
        if coords:
            df.at[idx, 'Latitud'] = coords[0]
            df.at[idx, 'Longitud'] = coords[1]

output_path = input_path.replace('.xlsx', '_COORDENADAS.xlsx')
try:
    df.to_excel(output_path, index=False)
    print(f"\n✅ EXITO guardado en: {output_path}")
except Exception as e:
    alt = output_path.replace('.xlsx', '_v2.xlsx')
    df.to_excel(alt, index=False)
    print(f"\n✅ EXITO guardado en: {alt}")
