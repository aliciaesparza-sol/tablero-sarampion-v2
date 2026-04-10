import pandas as pd, os

base = os.path.expanduser('~') + '/OneDrive/Escritorio/PVU'
path = None
for root, dirs, files in os.walk(base):
    for f in files:
        if 'COMPLETO_V2' in f and f.endswith('.xlsx') and 'EE casos' in root:
            path = os.path.join(root, f); break
    if path: break

print('Usando:', path)
df = pd.read_excel(path, usecols=range(35))
filled = df.dropna(how='all')

print(f'Total filas: {len(filled)}')
print(f'  direccion: {filled["direccion"].notna().sum()}/{len(filled)}')
print(f'  colonia: {filled["colonia"].notna().sum()}/{len(filled)}')
print(f'  codigo_postal: {filled["codigo_postal"].notna().sum()}/{len(filled)}')
print(f'  municipio: {filled["municipio"].notna().sum()}/{len(filled)}')
print()

print('Municipios unicos:', filled['municipio'].dropna().unique().tolist())
print()

print('Colonias unicas:')
for c in sorted(filled['colonia'].dropna().unique()):
    print(f'  - {c}')
