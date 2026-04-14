import pandas as pd
import re
from datetime import datetime

# Path names (using local copies)
cronograma_file = 'cronograma_ver.xlsx'
top100_file = 'vph_top100.xlsx'
output_file = 'CRONOGRAMA_VPH_2025_CON_METAS.xlsx'

def normalize_school_name(name):
    if pd.isna(name):
        return ""
    name = str(name).upper().strip()
    # Remove common prefixes/suffixes
    # Using regex to match words
    patterns = [
        r'^PRIMARIA\s+', r'^ESC\.\s+', r'^ESCUELA\s+', r'^COLEGIO\s+',
        r'\s+T\.M\.$', r'\s+T\.V\.$', r'\s+MATUTINO$', r'\s+VESPERTINO$'
    ]
    for p in patterns:
        name = re.sub(p, '', name)
    
    # Remove special characters except alphanumeric
    name = re.sub(r'[^A-Z0-9\s]', '', name)
    # Remove double spaces
    name = re.sub(r'\s+', ' ', name).strip()
    return name

print("Cargando archivos...")
df_cron = pd.read_excel(cronograma_file)
df_top = pd.read_excel(top100_file)

# Normalizar nombres para el cruce
df_cron['Escuela_Clean'] = df_cron['Escuela'].apply(normalize_school_name)
df_top['Escuela_Clean'] = df_top['N_CCT'].apply(normalize_school_name)

# Cruce (Left Join)
# Solo queremos las columnas relevantes del Top 100
top_cols = ['Escuela_Clean', 'CLAVECCT', 'INSC_T', 'INSC_4', 'MUJ_4', 'ALUMNOS_FALTANTES', 'COBERTURA_EST', 'DOSIS_TOTAL.1']
# Evitar duplicados en el Top 100 si los hay (por CCT/Nombre)
df_top_unique = df_top[top_cols].drop_duplicates(subset=['Escuela_Clean'])

print("Realizando cruce de información...")
merged_df = pd.merge(df_cron, df_top_unique, on='Escuela_Clean', how='left')

# Limpiar columnas temporales
merged_df = merged_df.drop(columns=['Escuela_Clean'])

# Reordenar columnas para una mejor presentación
# Columnas base: Jurisdicción, Institución, Escuela, Municipio / Localidad, Fecha de Visita, Turno
# Columnas adicionales: CLAVECCT, INSC_T, INSC_4, MUJ_4, ALUMNOS_FALTANTES, COBERTURA_EST
final_cols = ['Jurisdicci\u00f3n', 'Instituci\u00f3n', 'Escuela', 'CLAVECCT', 'Municipio / Localidad', 
              'Fecha de Visita', 'Turno', 'INSC_4', 'MUJ_4', 'ALUMNOS_FALTANTES', 'COBERTURA_EST']

# Asegurar que existan las columnas (en caso de que alguna no haya cruzado nada)
for col in final_cols:
    if col not in merged_df.columns:
        merged_df[col] = ""

merged_df = merged_df[final_cols]

print(f"Cruce completado. Guardando en {output_file}...")

# Aplicar formato "Premium" con xlsxwriter
import xlsxwriter

with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    # No escribimos el index
    # merged_df.to_excel(writer, index=False, sheet_name='Cronograma con Metas')
    
    workbook = writer.book
    worksheet = workbook.add_worksheet('Cronograma con Metas')
    
    # Formatos
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#1F4E78', # Azul oscuro
        'font_color': 'white',
        'border': 1,
        'align': 'center'
    })
    
    cell_format = workbook.add_format({
        'border': 1,
        'valign': 'vcenter'
    })
    
    alt_cell_format = workbook.add_format({
        'border': 1,
        'valign': 'vcenter',
        'fg_color': '#F2F2F2' # Gris claro
    })
    
    date_format = workbook.add_format({
        'border': 1,
        'valign': 'vcenter',
        'num_format': 'dd/mm/yyyy'
    })
    
    pct_format = workbook.add_format({
        'border': 1,
        'valign': 'vcenter',
        'num_format': '0.0%'
    })

    alt_date_format = workbook.add_format({
        'border': 1,
        'valign': 'vcenter',
        'fg_color': '#F2F2F2',
        'num_format': 'dd/mm/yyyy'
    })
    
    alt_pct_format = workbook.add_format({
        'border': 1,
        'valign': 'vcenter',
        'fg_color': '#F2F2F2',
        'num_format': '0.0%'
    })
    
    # Escribir encabezados
    for col_num, value in enumerate(merged_df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    
    # Escribir datos
    for row_num in range(1, len(merged_df) + 1):
        is_alt = row_num % 2 == 0
        for col_num in range(len(merged_df.columns)):
            val = merged_df.iloc[row_num-1, col_num]
            
            # Formato de Fecha (columna 5: Fecha de Visita)
            if col_num == 5:
                fmt = alt_date_format if is_alt else date_format
                if isinstance(val, (datetime, pd.Timestamp)):
                    worksheet.write_datetime(row_num, col_num, val, fmt)
                else:
                    worksheet.write(row_num, col_num, val if pd.notna(val) else '', fmt)
            
            # Formato de Porcentaje (columna 10: COBERTURA_EST)
            elif col_num == 10:
                fmt = alt_pct_format if is_alt else pct_format
                if pd.notna(val) and isinstance(val, (int, float)):
                    worksheet.write_number(row_num, col_num, val, fmt)
                else:
                    worksheet.write(row_num, col_num, '', fmt)
            
            # Otros
            else:
                fmt = alt_cell_format if is_alt else cell_format
                if pd.isna(val):
                    worksheet.write(row_num, col_num, '', fmt)
                elif isinstance(val, (int, float)):
                    worksheet.write_number(row_num, col_num, val, fmt)
                else:
                    worksheet.write(row_num, col_num, val, fmt)

    # Anchos de columna
    worksheet.set_column('A:B', 12) # Jurisdicción, Institución
    worksheet.set_column('C:C', 45) # Escuela
    worksheet.set_column('D:D', 15) # CLAVECCT
    worksheet.set_column('E:E', 35) # Municipio / Localidad
    worksheet.set_column('F:F', 18) # Fecha
    worksheet.set_column('G:G', 10) # Turno
    worksheet.set_column('H:K', 12) # INSC, MUJ, FALTANTES, COBERTURA
    
    # Inmovilizar panel superior y filtros
    worksheet.freeze_panes(1, 0)
    worksheet.autofilter(0, 0, len(merged_df), len(merged_df.columns) - 1)

print("Proceso finalizado con éxito.")
