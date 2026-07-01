import json
import math
import os
from collections import defaultdict

SRC = r"C:\Users\aicil\.gemini\antigravity-ide\scratch\casos_tabla.json"

with open(SRC, "r", encoding="utf-8") as f:
    cases = json.load(f)

n = len(cases)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

# --- 1. Matriz de distancias ---
print("=" * 70)
print("ANALISIS DE RELACION GEOGRAFICA - BROTE SAMA")
print("=" * 70)

print("\n--- 1. MATRIZ DE DISTANCIAS (km) ---\n")

# Header
header = "         " + "  ".join([f"{c['nombre']:>5s}" for c in cases])
print(header)

dist_matrix = []
for i in range(n):
    row = []
    line = f"{cases[i]['nombre']:>8s} "
    for j in range(n):
        d = haversine(cases[i]["lat"], cases[i]["lng"], cases[j]["lat"], cases[j]["lng"])
        row.append(d)
        if i == j:
            line += "    - "
        else:
            line += f"{d:5.1f} "
    dist_matrix.append(row)
    print(line)

# --- 2. Vecinos mas cercanos ---
print("\n--- 2. VECINO MAS CERCANO POR CASO ---\n")
print(f"{'Caso':<8} {'Colonia':<30} {'Vecino mas cercano':<8} {'Colonia vecino':<30} {'Dist (km)':>10}")
print("-" * 96)

nearest = []
for i in range(n):
    min_d = float('inf')
    min_j = -1
    for j in range(n):
        if i != j and dist_matrix[i][j] < min_d:
            min_d = dist_matrix[i][j]
            min_j = j
    nearest.append((i, min_j, min_d))
    print(f"{cases[i]['nombre']:<8} {cases[i]['colonia']:<30} {cases[min_j]['nombre']:<8} {cases[min_j]['colonia']:<30} {min_d:>8.2f} km")

avg_nearest = sum(d for _, _, d in nearest) / len(nearest)
print(f"\nDistancia promedio al vecino mas cercano: {avg_nearest:.2f} km")

# --- 3. Clusters por proximidad (< 2 km) ---
print("\n--- 3. CLUSTERS POR PROXIMIDAD (< 2 km) ---\n")

THRESHOLD = 2.0  # km
# Union-Find para clusters
parent = list(range(n))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(x, y):
    px, py = find(x), find(y)
    if px != py:
        parent[px] = py

for i in range(n):
    for j in range(i+1, n):
        if dist_matrix[i][j] < THRESHOLD:
            union(i, j)

clusters = defaultdict(list)
for i in range(n):
    clusters[find(i)].append(i)

cluster_id = 1
for root, members in sorted(clusters.items(), key=lambda x: -len(x[1])):
    if len(members) > 1:
        print(f"  CLUSTER {cluster_id} ({len(members)} casos):")
        for m in members:
            print(f"    - {cases[m]['nombre']} | {cases[m]['colonia']} | Lat: {cases[m]['lat']}, Lng: {cases[m]['lng']}")
        # Diameter of cluster
        max_d = 0
        for a in members:
            for b in members:
                if dist_matrix[a][b] > max_d:
                    max_d = dist_matrix[a][b]
        print(f"    Diametro del cluster: {max_d:.2f} km")
        print()
        cluster_id += 1

singletons = [m[0] for root, m in clusters.items() if len(m) == 1]
if singletons:
    print(f"  CASOS AISLADOS ({len(singletons)}):")
    for s in singletons:
        print(f"    - {cases[s]['nombre']} | {cases[s]['colonia']} | Dist al mas cercano: {nearest[s][2]:.2f} km")

# --- 4. Analisis de centroide y dispersion ---
print("\n--- 4. DISPERSION DESDE EL CENTROIDE ---\n")

lat_c = sum(c["lat"] for c in cases) / n
lng_c = sum(c["lng"] for c in cases) / n
print(f"Centroide geografico: Lat {lat_c:.4f}, Lng {lng_c:.4f}")

dists_centro = []
for c in cases:
    d = haversine(c["lat"], c["lng"], lat_c, lng_c)
    dists_centro.append((c["nombre"], c["colonia"], d))
    
dists_centro.sort(key=lambda x: x[2])
print(f"\n{'Caso':<8} {'Colonia':<30} {'Dist al centro (km)':>20}")
print("-" * 62)
for nombre, col, d in dists_centro:
    print(f"{nombre:<8} {col:<30} {d:>18.2f} km")

avg_dc = sum(d for _, _, d in dists_centro) / n
std_dc = math.sqrt(sum((d - avg_dc)**2 for _, _, d in dists_centro) / n)
print(f"\nDistancia promedio al centroide: {avg_dc:.2f} km")
print(f"Desviacion estandar: {std_dc:.2f} km")

# --- 5. Correlacion temporal-espacial ---
print("\n--- 5. CORRELACION TEMPORAL-ESPACIAL ---\n")
from datetime import datetime

def parse_date(d):
    for fmt in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(d, fmt)
        except:
            continue
    return None

print("Casos cercanos (<3 km) con fechas de sintomas proximas (<3 dias):")
print(f"{'Caso A':<8} {'Caso B':<8} {'Dist (km)':>10} {'Fecha A':>12} {'Fecha B':>12} {'Diff dias':>10}")
print("-" * 70)

pares_relacionados = []
for i in range(n):
    for j in range(i+1, n):
        d = dist_matrix[i][j]
        fa = parse_date(cases[i]["fecha_sintomas"])
        fb = parse_date(cases[j]["fecha_sintomas"])
        if fa and fb and d < 3.0:
            diff_dias = abs((fa - fb).days)
            if diff_dias <= 3:
                pares_relacionados.append((i, j, d, fa, fb, diff_dias))
                print(f"{cases[i]['nombre']:<8} {cases[j]['nombre']:<8} {d:>8.2f} km {fa.strftime('%d/%m'):>12} {fb.strftime('%d/%m'):>12} {diff_dias:>8} dias")

print(f"\nTotal de pares espacio-temporalmente relacionados: {len(pares_relacionados)}")

# --- 6. Analisis de cuadrantes ---
print("\n--- 6. DISTRIBUCION POR CUADRANTE (respecto al centroide) ---\n")

cuadrantes = {"NE": [], "NO": [], "SE": [], "SO": []}
for c in cases:
    ns = "N" if c["lat"] >= lat_c else "S"
    ew = "E" if c["lng"] >= lng_c else "O"
    cuadrantes[ns + ew].append(c["nombre"])

for q in ["NO", "NE", "SO", "SE"]:
    print(f"  {q}: {len(cuadrantes[q])} casos - {', '.join(cuadrantes[q]) if cuadrantes[q] else 'ninguno'}")

# --- 7. Conclusion ---
print("\n" + "=" * 70)
print("CONCLUSION DEL ANALISIS GEOGRAFICO")
print("=" * 70)

# Count clusters > 1
n_clusters = sum(1 for m in clusters.values() if len(m) > 1)
n_in_clusters = sum(len(m) for m in clusters.values() if len(m) > 1)

print(f"""
HALLAZGOS:

1. Se identificaron {n_clusters} cluster(s) geografico(s) con {n_in_clusters} de {n} casos 
   dentro de un radio de {THRESHOLD} km entre si.

2. Distancia promedio al vecino mas cercano: {avg_nearest:.2f} km
   Esto {'sugiere agrupamiento espacial significativo' if avg_nearest < 2 else 'indica dispersion moderada a amplia'}.

3. La dispersion desde el centroide tiene promedio de {avg_dc:.2f} km 
   (DE: {std_dc:.2f} km), con un rango de {dists_centro[0][2]:.2f} a {dists_centro[-1][2]:.2f} km.

4. Se encontraron {len(pares_relacionados)} pares de casos relacionados 
   espacio-temporalmente (< 3 km Y < 3 dias de diferencia en sintomas),
   lo que {'SUGIERE CADENAS DE TRANSMISION COMUNITARIA' if len(pares_relacionados) > 5 else 'sugiere transmision en un punto comun (maquiladora)'}.

5. Distribucion por cuadrantes: {'balanceada' if max(len(v) for v in cuadrantes.values()) - min(len(v) for v in cuadrantes.values()) < 5 else 'asimetrica'}
   - Los casos se distribuyen {'uniformemente' if max(len(v) for v in cuadrantes.values()) - min(len(v) for v in cuadrantes.values()) < 5 else 'con concentracion'} 
     alrededor del centroide.

INTERPRETACION:
  Los 19 casos residen en 19 colonias DIFERENTES, lo que indica que NO hay
  un foco residencial comun. Sin embargo, {'la cercania espacial entre muchos' if avg_nearest < 2 else 'la dispersion'} 
  {'casos sugiere que comparten un espacio laboral comun (Maquiladora SAMA)' if avg_nearest < 2 else 'de los casos en multiples colonias refuerza la hipotesis de exposicion comun en el centro de trabajo (Maquiladora SAMA)'}
  {'como punto de exposicion/transmision.' if avg_nearest < 2 else 'mas que transmision domiciliaria/comunitaria.'}
""")
