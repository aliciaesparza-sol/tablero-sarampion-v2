import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

excel_path = r"C:\Users\aicil\.gemini\antigravity\scratch\Formato_Concentrado_Mezquital_2026_Updated.xlsx"

try:
    df = pd.read_excel(excel_path, sheet_name="Concentrado", header=None)
    
    # Extract locality and Alcance %
    # Col 4: Loc, Col 83: Alcance
    data = []
    for i in range(4, len(df)):
        loc = df.iloc[i, 4]
        alcance = df.iloc[i, 83]
        if pd.notna(loc) and pd.notna(alcance) and isinstance(alcance, (int, float)) and alcance > 0:
            data.append([str(loc), float(alcance)])
    
    # Sort and take top 15-20 for a clear heatmap
    data.sort(key=lambda x: x[1], reverse=True)
    plot_data = data[:25] # Top 25 localities
    
    # Convert to DataFrame
    plot_df = pd.DataFrame(plot_data, columns=['Localidad', 'Alcance'])
    plot_df['Alcance'] = plot_df['Alcance'] * 100 # Convert to percentage values
    
    # Prepare data for heatmap (matrix style)
    # We'll just do a bar chart style heatmap or a single column heatmap
    plt.figure(figsize=(10, 12))
    sns.set_theme(style="white")
    
    # Creating a matrix for the heatmap
    matrix_data = plot_df.set_index('Localidad')
    
    ax = sns.heatmap(matrix_data, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={'label': 'Alcance %'})
    
    plt.title('Mapa de Calor: Alcance de Vacunación por Localidad\n(Mezquital, Durango - Mayo 2026)', fontsize=14, pad=20)
    plt.xlabel('Indicador: Alcance (%)')
    plt.ylabel('Localidad')
    
    plt.tight_layout()
    output_img = r"C:\Users\aicil\.gemini\antigravity\scratch\heatmap_vacunacion.png"
    plt.savefig(output_img, dpi=300)
    print(f"Heatmap saved to {output_img}")

except Exception as e:
    print(f"Error: {e}")
