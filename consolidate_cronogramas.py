import pandas as pd
import os
import re
from datetime import datetime

path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\CRONOGRAMAS DE VISITAS ESCUELAS'
output_file = 'CRONOGRAMA_INTEGRADO_VPH_2025.xlsx'

all_data = []

def clean_date(val):
    if pd.isna(val) or val == '':
        return None
    if isinstance(val, datetime):
        return val.date()
    # Try to parse string dates like "15 de Abril 2026"
    if isinstance(val, str):
        val = val.lower()
        # Common Spanish month replacement
        months = {'enero':'01', 'febrero':'02', 'marzo':'03', 'abril':'04', 'mayo':'05', 'junio':'06',
                  'julio':'07', 'agosto':'08', 'septiembre':'09', 'octubre':'10', 'noviembre':'11', 'diciembre':'12'}
        for m_name, m_num in months.items():
            if m_name in val:
                # Extract day
                day_match = re.search(r'(\d+)', val)
                if day_match:
                    day = day_match.group(1).zfill(2)
                    return f"2026-{m_num}-{day}"
    return val

# 1. JS1
print("Procesando JS1...")
try:
    df1 = pd.read_excel(os.path.join(path, "ESCUELAS PRIMARIAS 2026.xlsxJS1.xlsx"))
    for _, row in df1.iterrows():
        if pd.notna(row['N_CCT']):
            all_data.append({
                'Jurisdicción': '1',
                'Institución': row['INSTITUCION_SALUD'] if pd.notna(row['INSTITUCION_SALUD']) else 'SSD',
                'Escuela': row['N_CCT'],
                'Municipio / Localidad': f"{row['MUNICIPIO']} - {row['LOCALIDAD']}",
                'Fecha de Visita': clean_date(row['FECHA PROGRAMADA']),
                'Turno': row['N_TURNO'] if 'N_TURNO' in df1.columns else ''
            })
except Exception as e:
    print(f"Error JS1: {e}")

# 2. JS2
print("Procesando JS2...")
try:
    df2 = pd.read_excel(os.path.join(path, "CRONOGRAMA DE ESCUELAS JURISDCCION 2.xlsx"))
    # JS2 is tricky. Columns: UNIDADES, GUARDERIAS, KINDER, PRIMARIAS, FECHAS, PRIMARIAS.1
    for _, row in df2.iterrows():
        # Using PRIMARIAS.1 if exists, otherwise UNIDADES
        name = row['UNIDADES'] if pd.notna(row['UNIDADES']) else ''
        school = row['PRIMARIAS.1'] if 'PRIMARIAS.1' in df2.columns and pd.notna(row['PRIMARIAS.1']) else name
        
        if school:
            all_data.append({
                'Jurisdicción': '2',
                'Institución': 'SSD',
                'Escuela': school,
                'Municipio / Localidad': 'Gómez Palacio / Lerdo',
                'Fecha de Visita': row['FECHAS'], # Leaving text as is since JS2 has complex ranges
                'Turno': ''
            })
except Exception as e:
    print(f"Error JS2: {e}")

# 3. JS3
print("Procesando JS3...")
try:
    df3 = pd.read_excel(os.path.join(path, "JS3.xlsx"), skiprows=2)
    df3.columns = ['ESCUELA', 'LOCALIDAD', 'FECHA'] + list(df3.columns[3:])
    for _, row in df3.iterrows():
        if pd.notna(row['ESCUELA']):
            all_data.append({
                'Jurisdicción': '3',
                'Institución': 'SSD',
                'Escuela': row['ESCUELA'],
                'Municipio / Localidad': row['LOCALIDAD'],
                'Fecha de Visita': clean_date(row['FECHA']),
                'Turno': ''
            })
except Exception as e:
    print(f"Error JS3: {e}")

# 4. JS4
print("Procesando JS4...")
try:
    df4 = pd.read_excel(os.path.join(path, "PROGRAMACION DE ESCUELAS.xlsxJS4.xlsx"), skiprows=6)
    for _, row in df4.iterrows():
        if pd.notna(row['ESCUELA']):
            all_data.append({
                'Jurisdicción': '4',
                'Institución': 'SSD',
                'Escuela': row['ESCUELA'],
                'Municipio / Localidad': f"{row['MUNICIPIO']} - {row['LOCALIDAD']}",
                'Fecha de Visita': clean_date(row['FECHA']),
                'Turno': ''
            })
except Exception as e:
    print(f"Error JS4: {e}")

# 5. ISSSTE
print("Procesando ISSSTE...")
try:
    # Row 1 (index 1) has the headers
    df5 = pd.read_excel(os.path.join(path, "ISSSTE - Cronograma de Vacunación..xlsx"), header=1)
    # The columns are likely 'Escuela', 'Fecha programada', 'Domicilio' but might be Unnamed if shifted
    # Let's find columns by checking row content or specific names
    for _, row in df5.iterrows():
        # Escuela is likely col index 1
        escuela = row.iloc[1] if len(row) > 1 else None
        fecha = row.iloc[3] if len(row) > 3 else None
        domicilio = row.iloc[5] if len(row) > 5 else None
        
        if pd.notna(escuela) and str(escuela).strip() and "Escuela" not in str(escuela):
            all_data.append({
                'Jurisdicción': '1',
                'Institución': 'ISSSTE',
                'Escuela': escuela,
                'Municipio / Localidad': domicilio,
                'Fecha de Visita': clean_date(fecha),
                'Turno': ''
            })
except Exception as e:
    print(f"Error ISSSTE: {e}")

# 6. IMSS
print("Procesando IMSS...")
try:
    df6 = pd.read_excel(os.path.join(path, "PROGRAMACION PRIMARIAS ABRIL 26 IMSS ORDINARIO.xlsx"), header=5)
    for _, row in df6.iterrows():
        # col2: UMF, col3: ESCUELA, col4: FECHA
        escuela = row.iloc[3] if len(row) > 3 else None
        fecha = row.iloc[4] if len(row) > 4 else None
        umf = row.iloc[2] if len(row) > 2 else ''
        
        if pd.notna(escuela) and str(escuela).strip() and "ESCUELA" not in str(escuela).upper():
            all_data.append({
                'Jurisdicción': '1',
                'Institución': 'IMSS',
                'Escuela': escuela,
                'Municipio / Localidad': f"UMF {umf}" if umf else '',
                'Fecha de Visita': clean_date(fecha),
                'Turno': ''
            })
except Exception as e:
    print(f"Error IMSS: {e}")

# Create Final DataFrame
final_df = pd.DataFrame(all_data)

# Filtering: Remove schools without a visit date
final_df = final_df.dropna(subset=['Fecha de Visita'])
# Also remove rows where Fecha de Visita might be an empty string if it's not NaN
final_df = final_df[final_df['Fecha de Visita'].astype(str).str.strip() != '']

# Sort for better organization
final_df = final_df.sort_values(by=['Jurisdicción', 'Institución', 'Fecha de Visita'])

# Save with Premium Formatting
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    # We don't use to_excel directly to have full control over formatting
    # final_df.to_excel(writer, index=False, sheet_name='CRONOGRAMA VPH 2025')
    
    workbook = writer.book
    worksheet = workbook.add_worksheet('CRONOGRAMA VPH 2025')
    
    # Formatos
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#1F4E78', # Dark blue
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
        'fg_color': '#F2F2F2' # Light grey
    })
    
    date_format = workbook.add_format({
        'border': 1,
        'valign': 'vcenter',
        'num_format': 'dd/mm/yyyy'
    })
    
    alt_date_format = workbook.add_format({
        'border': 1,
        'valign': 'vcenter',
        'fg_color': '#F2F2F2',
        'num_format': 'dd/mm/yyyy'
    })
    
    # Apply header format
    for col_num, value in enumerate(final_df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    
    # Apply cell formats and adjust column widths
    for row_num in range(1, len(final_df) + 1):
        is_alt = row_num % 2 == 0
        for col_num in range(len(final_df.columns)):
            val = final_df.iloc[row_num-1, col_num]
            
            # Special handling for dates
            if col_num == 4: # Fecha de Visita
                fmt = alt_date_format if is_alt else date_format
                if isinstance(val, str) and '-' in val:
                    try:
                        dt = datetime.strptime(val, '%Y-%m-%d')
                        worksheet.write_datetime(row_num, col_num, dt, fmt)
                    except:
                        worksheet.write(row_num, col_num, val, fmt)
                elif isinstance(val, (datetime, pd.Timestamp)):
                    worksheet.write_datetime(row_num, col_num, val, fmt)
                elif isinstance(val, (int, float)): # Excel serial date
                    if pd.isna(val):
                        worksheet.write(row_num, col_num, '', fmt)
                    else:
                        worksheet.write(row_num, col_num, val, fmt)
                else:
                    worksheet.write(row_num, col_num, val if pd.notna(val) else '', fmt)
            else:
                fmt = alt_cell_format if is_alt else cell_format
                # Cleanup "UMF UMF"
                if col_num == 3 and isinstance(val, str):
                    val = val.replace('UMF UMF', 'UMF ')
                
                if pd.isna(val):
                    worksheet.write(row_num, col_num, '', fmt)
                else:
                    worksheet.write(row_num, col_num, val, fmt)
                
    # Column widths
    worksheet.set_column('A:A', 15) # Jurisdicción
    worksheet.set_column('B:B', 15) # Institución
    worksheet.set_column('C:C', 50) # Escuela
    worksheet.set_column('D:D', 40) # Localidad
    worksheet.set_column('E:E', 25) # Fecha
    worksheet.set_column('F:F', 15) # Turno
    
    # Freeze top row
    worksheet.freeze_panes(1, 0)
    
    # Add filters
    worksheet.autofilter(0, 0, len(final_df), len(final_df.columns) - 1)

print(f"Archivo guardado exitosamente como {output_file}")
