import pandas as pd
import numpy as np

file_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\CRONOGRAMA_INTEGRADO_VPH_2025_12abril2026.xlsx"
df = pd.read_excel(file_path)

# Rename columns
df.columns = ["JURISDICCION", "INSTITUCION", "ESCUELA", "N_LOCALIDAD", "FECHA_VISITA", "N_TURNO"]

# Add new columns
df["UNIDAD_MEDICA"] = np.nan

# Try to extract the day of the week from FECHA_VISITA
def get_day_name(date_val):
    if pd.isna(date_val):
        return np.nan
    try:
        if isinstance(date_val, pd.Timestamp):
            dt = date_val
        elif isinstance(date_val, str):
            dt = pd.to_datetime(date_val, errors='coerce')
        else:
            return np.nan
        
        if pd.isnull(dt):
            return np.nan
            
        days = {
            'Monday': 'LUNES',
            'Tuesday': 'MARTES',
            'Wednesday': 'MIÉRCOLES',
            'Thursday': 'JUEVES',
            'Friday': 'VIERNES',
            'Saturday': 'SÁBADO',
            'Sunday': 'DOMINGO'
        }
        return days.get(dt.day_name(), np.nan)
    except:
        return np.nan

df["DIA_VISITA"] = df["FECHA_VISITA"].apply(get_day_name)

# Make sure FECHA_VISITA keeps its date format if it's timestamp, or string if it's string
df['FECHA_VISITA'] = df['FECHA_VISITA'].apply(lambda x: x.date() if isinstance(x, pd.Timestamp) else x)


# Rearrange columns
cols = ["JURISDICCION", "INSTITUCION", "UNIDAD_MEDICA", "N_LOCALIDAD", "ESCUELA", "FECHA_VISITA", "DIA_VISITA", "N_TURNO"]
df = df[cols]

# Save to the same file
df.to_excel(file_path, index=False)

print("Process completed successfully.")
