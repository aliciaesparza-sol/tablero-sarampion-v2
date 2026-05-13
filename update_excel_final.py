import pandas as pd, os, sys, unicodedata, shutil

# Helper to normalize strings (remove accents, uppercase)
def norm(s):
    if pd.isna(s):
        return ''
    s = str(s)
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s.upper().strip()

# Paths (all within the workspace)
workspace = r"C:\Users\aicil\.gemini\antigravity\scratch"
# Source files (copied to workspace)
source_excel = os.path.join(workspace, "Dosis_por_Localidad_y_Edad_Ordenado_Mezquital_09mayo2026.xlsx")
inegi_excel = os.path.join(workspace, "POBLACION_INEGI_TEMP.xlsx")
inpi_excel = os.path.join(workspace, "POBLACION_INPI_TEMP.xlsx")

# Output path (final location in OneDrive)
output_excel = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\INFORMES\Dosis_por_Localidad_y_Edad_Completo_Mezquital_10mayo2026.xlsx"

# Load main dosage data
print('Loading main dosage file...')
try:
    df = pd.read_excel(source_excel)
except Exception as e:
    print('Error loading main file:', e)
    sys.exit(1)

# Identify locality column (should be 'Localidad')
loc_col = None
for c in df.columns:
    if norm(c) == 'LOCALIDAD':
        loc_col = c
        break
if not loc_col:
    print('Localidad column not found')
    sys.exit(1)

# Load INEGI population data (Hoja1, header row = 1)
print('Loading INEGI data...')
try:
    inegi_df = pd.read_excel(inegi_excel, sheet_name=0, header=1)
except Exception as e:
    print('Error loading INEGI file:', e)
    sys.exit(1)
# Find columns for locality and population
loc_inegi_col = None
pop_inegi_col = None
for c in inegi_df.columns:
    if norm(c) in ['LOCALIDAD', 'LOCALIDAD [1]']:
        loc_inegi_col = c
    if norm(c) in ['POBLACION (2020)', 'POBLACION']:
        pop_inegi_col = c
if not loc_inegi_col or not pop_inegi_col:
    print('INEGI columns not identified')
    sys.exit(1)
# Build dict
inegi_map = {norm(loc): int(pop) for loc, pop in zip(inegi_df[loc_inegi_col], inegi_df[pop_inegi_col]) if not pd.isna(pop)}

# Load INPI approximate population data (no header, find header row similar to prior script)
print('Loading INPI data...')
try:
    inpi_df = pd.read_excel(inpi_excel, header=None)
except Exception as e:
    print('Error loading INPI file:', e)
    sys.exit(1)
# Find the row containing 'RANGO DE EDAD'
header_idx = None
for i, row in inpi_df.iterrows():
    if any(isinstance(v, str) and 'RANGO DE EDAD' in v.upper() for v in row.tolist()):
        header_idx = i
        break
if header_idx is None:
    print('Header row not found in INPI file')
    sys.exit(1)
# Row after header contains gender (skip). Row after that contains locality names.
locality_row = header_idx + 2
loc_names = inpi_df.iloc[locality_row]
# Row after locality row contains totals for each locality (population estimate)
pop_row = locality_row + 1
pop_values = inpi_df.iloc[pop_row]
# Build dict of locality -> population (total)
inpi_map = {}
for col_idx, loc in enumerate(loc_names):
    if pd.isna(loc) or str(loc).strip().upper() == 'TOTAL':
        continue
    pop_val = pop_values[col_idx]
    if not pd.isna(pop_val):
        inpi_map[norm(loc)] = int(pop_val)

# Prepare containers for new columns
pop_inegi_list = []
cov_inegi_list = []
pop_inpi_list = []
cov_inpi_list = []

# Determine which columns are age groups (numeric) and total column
# We'll consider any column after the date column (if present) that is numeric.
# Find date column (contains 'FECHA')
date_col = None
for c in df.columns:
    if 'FECHA' in norm(c):
        date_col = c
        break
# Identify numeric age columns (exclude locality and date)
numeric_cols = [c for c in df.columns if c not in [loc_col, date_col] and pd.api.types.is_numeric_dtype(df[c])]
# Ensure 'TOTAL' column is present
if 'TOTAL' not in df.columns:
    # compute total as sum of numeric cols
    df['TOTAL'] = df[numeric_cols].sum(axis=1)
    numeric_cols.append('TOTAL')

for idx, row in df.iterrows():
    loc = norm(row[loc_col])
    # total doses for locality (use TOTAL column if exists)
    total_doses = row['TOTAL'] if 'TOTAL' in row else row[numeric_cols].sum()
    # INEGI population
    pop_inegi = inegi_map.get(loc)
    if pop_inegi:
        cov_inegi = min(1.0, total_doses / pop_inegi) * 100
        cov_inegi_str = f"{cov_inegi:.2f}%"
    else:
        pop_inegi = 'S/D'
        cov_inegi_str = 'S/D'
    # INPI population
    pop_inpi = inpi_map.get(loc)
    if pop_inpi:
        cov_inpi = min(1.0, total_doses / pop_inpi) * 100
        cov_inpi_str = f"{cov_inpi:.2f}%"
    else:
        pop_inpi = 'S/D'
        cov_inpi_str = 'S/D'
    pop_inegi_list.append(pop_inegi)
    cov_inegi_list.append(cov_inegi_str)
    pop_inpi_list.append(pop_inpi)
    cov_inpi_list.append(cov_inpi_str)

# Insert new columns after the TOTAL column
cols = list(df.columns)
try:
    total_idx = cols.index('TOTAL')
except ValueError:
    total_idx = len(cols) - 1
new_order = cols[:total_idx+1] + ['POBLACION (INEGI)', 'COBERTURA (INEGI) %', 'POBLACION (INPI)', 'COBERTURA (INPI) %'] + cols[total_idx+1:]

# Build new DataFrame
new_df = pd.DataFrame(columns=new_order)
for i, row in df.iterrows():
    row_dict = row.to_dict()
    row_dict.update({
        'POBLACION (INEGI)': pop_inegi_list[i],
        'COBERTURA (INEGI) %': cov_inegi_list[i],
        'POBLACION (INPI)': pop_inpi_list[i],
        'COBERTURA (INPI) %': cov_inpi_list[i]
    })
    # Reorder according to new_order
    ordered = {col: row_dict.get(col, None) for col in new_order}
    new_df = new_df.append(ordered, ignore_index=True)

# Save result
new_df.to_excel(output_excel, index=False)
print('Excel saved to:', output_excel)
