import zipfile
import pdfplumber
import io
import pandas as pd
import re
import os

def extract_data_from_pdf_text(text):
    data = {}
    
    # Identificador
    match_id = re.search(r'Identificador De Caso\s*(\d+)', text)
    if match_id:
        data['id_caso'] = match_id.group(1).strip()
    
    # CLUES
    match_clues = re.search(r'CLUES:\s*(\S+)', text)
    if match_clues:
        data['rr_unidad_salud_clues'] = match_clues.group(1).strip()
        
    # Tipo de Localidad
    # Extraemos el texto literal solo por si acaso, pero luego se sobreescribirá con la lógica poblacional
    match_loc = re.search(r'Localidad:\s*(.+)', text)
    if match_loc:
        loc = match_loc.group(1).strip()
        if 'Seleccione' not in loc and loc != '':
            data['rr_tipo_localidad_text'] = loc

    # Táctica (Bloqueo)
    match_bloqueo = re.search(r'BLOQUEO\s+(Sí|No)', text, re.IGNORECASE)
    if match_bloqueo:
        data['rr_tactica_tipo'] = 'BLOQUEO ' + match_bloqueo.group(1).upper()
        
    # Fecha de táctica (Inicio)
    match_inicio = re.search(r'INICIO\s*(\d{2}/\d{2}/\d{4})', text)
    if match_inicio:
        data['rr_tactica_fecha'] = match_inicio.group(1).strip()
        
    # Total Dosis
    match_dosis = re.search(r'DOSIS:\s*(\d+)', text)
    if match_dosis:
        data['rr_total_dosis_aplicadas'] = float(match_dosis.group(1))
        
    # Cobertura Alcanzada
    match_cob = re.search(r'COBERTURA:\s*(\d+)', text)
    if match_cob:
        data['rr_cobertura_alcanzada'] = float(match_cob.group(1).strip())
        
    return data

def main():
    excel_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\CASOS NOTIFICADOS\CASOS NOTIFICADOS 2026\base_sarampion_pacientes_positivos_2026.xlsx"
    zip_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\CASOS NOTIFICADOS\CASOS NOTIFICADOS 2026\EE casos confirmados sarampion 2026-20260303T152644Z-1-001.zip"
    out_excel_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\CASOS NOTIFICADOS\CASOS NOTIFICADOS 2026\base_sarampion_pacientes_positivos_2026_updated.xlsx"

    print("Cargando Excel...")
    df = pd.read_excel(excel_path)
    
    # Crear una columna temporal de ID para el merge
    # numero_seriado ej: "1.48157" -> extraemos digitos después del punto, o cualquier grupo de 5 numeros
    def extract_id(val):
        s = str(val)
        m = re.search(r'\d+\.(\d+)', s)
        if m: return m.group(1)
        m2 = re.search(r'(\d{4,})', s)
        if m2: return m2.group(1)
        return None
        
    df['temp_id'] = df['numero_seriado'].apply(extract_id)
    
    pdf_results = []
    
    print("Abriendo ZIP y procesando PDFs...")
    with zipfile.ZipFile(zip_path, 'r') as z:
        pdf_files = [f for f in z.namelist() if f.lower().endswith('.pdf')]
        for i, file_name in enumerate(pdf_files):
            print(f"[{i+1}/{len(pdf_files)}] Procesando {file_name}")
            try:
                pdf_bytes = z.read(file_name)
                with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                    text = '\n'.join([page.extract_text() for page in pdf.pages if page.extract_text()])
                    
                    data = extract_data_from_pdf_text(text)
                    if not data.get('id_caso'):
                        # Intentar sacar el ID del nombre de archivo ej: "1. 48157 GRRH.pdf"
                        m_file = re.search(r'(\d{4,})', file_name)
                        if m_file:
                            data['id_caso'] = m_file.group(1)
                    
                    if data.get('id_caso'):
                        pdf_results.append(data)
                        
            except Exception as e:
                print(f"Error parseando {file_name}: {e}")
                
    print(f"Total de PDFs extraídos con éxito: {len(pdf_results)}")
    
    # Crear DataFrame de resultados
    df_pdfs = pd.DataFrame(pdf_results)
    if 'id_caso' in df_pdfs.columns:
        # Hacer merge actualizando solo las columnas target
        # Hacemos el match usando temp_id y id_caso
        df_pdfs = df_pdfs.set_index('id_caso')
        
        # Iteramos sobre el excel
        updated_count = 0
        for idx, row in df.iterrows():
            t_id = row['temp_id']
            if pd.notna(t_id) and str(t_id) in df_pdfs.index:
                pdf_data = df_pdfs.loc[str(t_id)]
                # loc puede devolver DataFrame si hay duplicados, tomemos la primera
                if isinstance(pdf_data, pd.DataFrame):
                    pdf_data = pdf_data.iloc[0]
                    
                # Update columns from PDF
                for col in pdf_data.index:
                    if col in df.columns and pd.notna(pdf_data[col]):
                        try:
                            df.at[idx, col] = pdf_data[col]
                        except Exception:
                            df[col] = df[col].astype(object)
                            df.at[idx, col] = pdf_data[col]
                updated_count += 1
                
        # Nueva lógica para asignar Tipo de Localidad basado en población estimada existente en el Excel guardado        
        def clasificar_localidad(pob):
            if pd.isna(pob): return None
            try:
                pob = float(pob)
                if pob >= 15000: return 'URBANA'
                elif pob >= 2500: return 'SEMIURBANA'
                else: return 'RURAL'
            except:
                return None
                
        df['rr_tipo_localidad_calc'] = df['rr_poblacion_objetivo_estimada'].apply(clasificar_localidad)
        
        # Sobreescribimos solo si hay dato
        for idx, row in df.iterrows():
            if pd.notna(row['rr_tipo_localidad_calc']):
                df.at[idx, 'rr_tipo_localidad'] = row['rr_tipo_localidad_calc']
        df = df.drop(columns=['rr_tipo_localidad_calc'])

        print(f"Registros actualizados en el Excel: {updated_count} desde PDFs.")
    else:
        print("No se encontraron identificadores de caso en los PDFs.")
        
    # Limpiamos columna temporal
    df = df.drop(columns=['temp_id'])
    
    print(f"Guardando archivo actualizado en: {out_excel_path}")
    df.to_excel(out_excel_path, index=False)
    print("¡Listo!")

if __name__ == '__main__':
    main()
