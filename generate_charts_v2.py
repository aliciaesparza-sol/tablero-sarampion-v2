import pandas as pd
import matplotlib.pyplot as plt
import os
import json

csv_path = r"C:\Users\aicil\.gemini\antigravity\scratch\SRP-SR-2028.csv"
excel_adult_path = r"C:\Users\aicil\.gemini\antigravity\scratch\COBERTURAS_UPDATED_2025.xlsx"
excel_infant_path = r"C:\Users\aicil\.gemini\antigravity\scratch\coverage_infants_copy.xlsx"
output_dir = r"C:\Users\aicil\.gemini\antigravity\scratch\charts"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Loading data...")
df_csv = pd.read_csv(csv_path, encoding='latin1', low_memory=False)

# Define all target age groups and their keywords
age_groups = {
    '12 Meses': ['1 ANIO'],
    '18 Meses': ['18 MESES'],
    '6 Años': ['6 ANIO'],
    '10-12 a': ['10 A 12'],
    '13-19 a': ['13 A 19'],
    '20-39 a': ['20 A 39'],
    '40-49 a': ['40 A 49']
}

all_cols = df_csv.columns.tolist()
group_cols = {}
all_dose_cols = []
for name, keywords in age_groups.items():
    cols = [c for c in all_cols if any(k in c.upper() for k in keywords)]
    group_cols[name] = cols
    all_dose_cols.extend(cols)

# Ensure numeric and fill NaNs
df_csv[all_dose_cols] = df_csv[all_dose_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
df_csv['Total_Applied'] = df_csv[all_dose_cols].sum(axis=1)

# Extract Metas (Population Targets)
print("Extracting Metas...")

def to_num(val):
    try:
        return float(pd.to_numeric(val, errors='coerce'))
    except:
        return 0.0

# State Metas
meta_sheet_adult = pd.read_excel(excel_adult_path, sheet_name='SE20', header=None)
adult_meta = to_num(meta_sheet_adult.iloc[6, 1])

meta_sheet_infant = pd.read_excel(excel_infant_path, sheet_name='SE 53', header=None)
intant_metas_state = {
    '12 Meses': to_num(meta_sheet_infant.iloc[6, 1]),
    '18 Meses': to_num(meta_sheet_infant.iloc[6, 4]),
    '6 Años': to_num(meta_sheet_infant.iloc[6, 7])
}

# Municipal Metas
def get_muni_metas(df, col_meta, start_row=7):
    m_data = {}
    row_count = len(df)
    for r in range(start_row, row_count):
        name = str(df.iloc[r, 0]).strip().upper()
        if name and name not in ['NAN', 'TOTAL', 'UNIDAD']:
            # Evitar filas de sumatoria final si existen
            if 'TOTAL' in name: continue
            m_data[name] = to_num(df.iloc[r, col_meta])
    return m_data

muni_metas_adult = get_muni_metas(meta_sheet_adult, 1)
muni_metas_12m = get_muni_metas(meta_sheet_infant, 1)
muni_metas_18m = get_muni_metas(meta_sheet_infant, 4)
muni_metas_6a = get_muni_metas(meta_sheet_infant, 7)

# Consolidate Municipal Metas
muni_names = sorted(list(set(muni_metas_adult.keys()) | set(muni_metas_12m.keys())))
muni_total_metas = {}
for m in muni_names:
    total = muni_metas_adult.get(m, 0) + muni_metas_12m.get(m, 0) + \
            muni_metas_18m.get(m, 0) + muni_metas_6a.get(m, 0)
    if total > 0:
        muni_total_metas[m] = total

state_total_meta = sum(muni_total_metas.values())
print(f"Total Municipalities with meta: {len(muni_total_metas)}")

# Aggregate doses by Week
weeks = list(range(1, 54))
coverage_data = []

cumulative_totals = {name: 0 for name in age_groups.keys()}
cumulative_grand_total = 0

for week in weeks:
    week_df = df_csv[df_csv['SEMANA'] == week]
    group_weekly = {}
    week_total = 0
    
    for name, cols in group_cols.items():
        doses = week_df[cols].sum().sum()
        group_weekly[name] = doses
        cumulative_totals[name] += doses
        week_total += doses
    
    cumulative_grand_total += week_total
    
    # Coverage calculation
    adult_doses_accum = sum(cumulative_totals[k] for k in ['10-12 a', '13-19 a', '20-39 a', '40-49 a'])
    
    week_record = {
        'Week': f"SE{week}",
        'Semana_Num': week,
        'Weekly_Total': week_total,
        'Cumulative_Grand_Total': cumulative_grand_total,
        'Total_Coverage': float((cumulative_grand_total / state_total_meta) * 100 if state_total_meta > 0 else 0),
        '12M_Coverage': float((cumulative_totals['12 Meses'] / intant_metas_state['12 Meses']) * 100 if intant_metas_state['12 Meses'] > 0 else 0),
        '18M_Coverage': float((cumulative_totals['18 Meses'] / intant_metas_state['18 Meses']) * 100 if intant_metas_state['18 Meses'] > 0 else 0),
        '6A_Coverage': float((cumulative_totals['6 Años'] / intant_metas_state['6 Años']) * 100 if intant_metas_state['6 Años'] > 0 else 0),
        'Adult_Coverage': float((adult_doses_accum / adult_meta) * 100 if adult_meta > 0 else 0)
    }
    week_record.update({k: float(v) for k, v in group_weekly.items()})
    coverage_data.append(week_record)

df_plot = pd.DataFrame(coverage_data)

# Municipal Coverage and Semáforo Calculation
import unicodedata
def normalize(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.upper()) if unicodedata.category(c) != 'Mn').strip()

# Mapping doses per indicator per muni
indicators = {
    '12 Meses': group_cols['12 Meses'],
    '18 Meses': group_cols['18 Meses'],
    '6 Años': group_cols['6 Años'],
    '10-49 Años': group_cols['10-12 a'] + group_cols['13-19 a'] + group_cols['20-39 a'] + group_cols['40-49 a']
}

muni_indicator_doses = {}
for name, cols in indicators.items():
    muni_indicator_doses[name] = df_csv.groupby('MUNICIPIO')[cols].sum().sum(axis=1)

muni_semaforo = []
norm_metas_12m = {normalize(k): v for k, v in muni_metas_12m.items()}
norm_metas_18m = {normalize(k): v for k, v in muni_metas_18m.items()}
norm_metas_6a = {normalize(k): v for k, v in muni_metas_6a.items()}
norm_metas_adult = {normalize(k): v for k, v in muni_metas_adult.items()}

all_munis = sorted(df_csv['MUNICIPIO'].unique())

for m in all_munis:
    norm_m = normalize(m)
    row = {'Municipio': m}
    
    mapping = {
        '12M': (muni_indicator_doses['12 Meses'].get(m, 0), norm_metas_12m.get(norm_m, 0)),
        '18M': (muni_indicator_doses['18 Meses'].get(m, 0), norm_metas_18m.get(norm_m, 0)),
        '6A': (muni_indicator_doses['6 Años'].get(m, 0), norm_metas_6a.get(norm_m, 0)),
        'ADULT': (muni_indicator_doses['10-49 Años'].get(m, 0), norm_metas_adult.get(norm_m, 0))
    }
    
    for key, (doses, meta) in mapping.items():
        cov = (doses / meta * 100) if meta > 0 else 0
        color = 'red' if cov <= 60 else ('yellow' if cov <= 85 else 'green')
        row[f'{key}_Cov'] = cov
        row[f'{key}_Color'] = color
        
    muni_semaforo.append(row)

df_semaforo = pd.DataFrame(muni_semaforo)

# Define df_muni for top ranking (average coverage across indicators or just total)
df_semaforo['Avg_Coverage'] = df_semaforo[['12M_Cov', '18M_Cov', '6A_Cov', 'ADULT_Cov']].mean(axis=1)
df_muni = df_semaforo[['Municipio', 'Avg_Coverage']].copy().rename(columns={'Avg_Coverage': 'Coverage'}).sort_values('Coverage', ascending=False)

# Save semáforo data to JSON for HTML rendering
semaforo_json = df_semaforo.to_dict(orient='records')
with open(os.path.join(output_dir, 'semaforo.json'), 'w') as f:
    json.dump(semaforo_json, f, indent=4)

# Behavior Analysis
peak_week_row = df_plot.loc[df_plot['Weekly_Total'].idxmax()]
avg_doses = df_plot[df_plot['Weekly_Total'] > 0]['Weekly_Total'].mean()

analysis = {
    "peak_week": str(peak_week_row['Week']),
    "peak_doses": int(peak_week_row['Weekly_Total']),
    "avg_weekly_doses": float(avg_doses) if pd.notnull(avg_doses) else 0.0,
    "total_doses": int(cumulative_grand_total),
    "final_coverage": float(df_plot.iloc[-1]['Total_Coverage']),
    "meta_total": int(state_total_meta),
    "top_municipalities": df_muni.head(5)[['Municipio', 'Coverage']].to_dict(orient='records'),
    "coverage_by_indicator": {
        "12 Meses": float(df_plot.iloc[-1]['12M_Coverage']),
        "18 Meses": float(df_plot.iloc[-1]['18M_Coverage']),
        "6 Años": float(df_plot.iloc[-1]['6A_Coverage']),
        "10-49 Años": float(df_plot.iloc[-1]['Adult_Coverage'])
    },
    "semaforo_summary": {
        "green_count": int((df_semaforo[['12M_Color','18M_Color','6A_Color','ADULT_Color']] == 'green').sum().sum()),
        "yellow_count": int((df_semaforo[['12M_Color','18M_Color','6A_Color','ADULT_Color']] == 'yellow').sum().sum()),
        "red_count": int((df_semaforo[['12M_Color','18M_Color','6A_Color','ADULT_Color']] == 'red').sum().sum())
    }
}

with open(os.path.join(output_dir, 'analysis_v4.json'), 'w') as f:
    json.dump(analysis, f, indent=4)

# Chart 1: Coverage by Indicator
plt.figure(figsize=(15, 8))
plt.plot(df_plot['Semana_Num'], df_plot['12M_Coverage'], label='12 Meses', color='#e63946', linewidth=2)
plt.plot(df_plot['Semana_Num'], df_plot['18M_Coverage'], label='18 Meses', color='#f1c40f', linewidth=2)
plt.plot(df_plot['Semana_Num'], df_plot['6A_Coverage'], label='6 Años', color='#2ecc71', linewidth=2)
plt.plot(df_plot['Semana_Num'], df_plot['Adult_Coverage'], label='10-49 Años', color='#3498db', linewidth=2, linestyle='--')
plt.title('Cobertura Acumulada por Indicador de Edad (53 Semanas)', fontsize=14)
plt.xlabel('Semana Epidemiológica', fontsize=12)
plt.ylabel('Cobertura (%)', fontsize=12)
plt.xlim(1, 53)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'cobertura_por_indicador.png'))

# Chart 2: Top 15 Municipios por Cobertura (%)
plt.figure(figsize=(12, 8))
top_muni = df_muni.head(15).sort_values('Coverage', ascending=True)
plt.barh(top_muni['Municipio'], top_muni['Coverage'], color='#1d3557')
plt.title('Top 15 Municipios por % de Cobertura (Consolidado)', fontsize=14)
plt.xlabel('% Cobertura', fontsize=12)
plt.ylabel('Municipio', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.6)
for i, v in enumerate(top_muni['Coverage']):
    plt.text(v + 0.5, i, f"{v:.1f}%", va='center')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'cobertura_por_municipio_ranking.png'))

# Chart 3: Doses by Weekly Total
plt.figure(figsize=(15, 7))
plt.bar(df_plot['Semana_Num'], df_plot['Weekly_Total'], color='#457b9d', alpha=0.8)
plt.title('Dosis Aplicadas Totales por Semana Epidemiológica', fontsize=14)
plt.xlabel('Semana Epidemiológica', fontsize=12)
plt.ylabel('Dosis', fontsize=12)
plt.xticks(weeks, rotation=90, fontsize=8)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'dosis_semanales_totales.png'))

print(f"Analysis v3 and charts generated in {output_dir}")
df_plot.to_csv(os.path.join(output_dir, 'consolidated_data_v3.csv'), index=False)
