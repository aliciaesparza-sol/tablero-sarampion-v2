import pandas as pd

# Data extraction
data = [
    ["Enero", 775, 99, 446, 73, 551, 82, 128, 28, 138, 21, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2038, 112, 19, 3, 2057, 113],
    ["Febrero", 930, 127, 533, 119, 644, 106, 301, 41, 235, 53, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2643, 151, 40, 4, 2683, 151],
    ["Marzo", 713, 120, 535, 107, 649, 105, 226, 51, 267, 51, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2390, 149, 20, 3, 2410, 149],
    ["Abril", 819, 117, 797, 108, 776, 99, 336, 52, 454, 64, 0, 1, 0, 1, 0, 1, 1, 2, 1, 2, 3184, 163, 735, 14, 3919, 163],
    ["Mayo", 1489, 151, 1704, 148, 1379, 139, 422, 57, 843, 76, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 5837, 177, 73, 9, 5910, 178]
]

columns = [
    "Mes",
    "VAC23 PRIMERA 12 MESES (Total)",
    "VAC23 PRIMERA 12 MESES (Total CLUES)",
    "VAC81 SEGUNDA 6 AÑOS (Total)",
    "VAC81 SEGUNDA 6 AÑOS (Total CLUES)",
    "VTV01 SEGUNDA 18 MESES (Total)",
    "VTV01 SEGUNDA 18 MESES (Total CLUES)",
    "VTV02 INICIAR/COMPLETAR 1RA 13M-9A (Total)",
    "VTV02 INICIAR/COMPLETAR 1RA 13M-9A (Total CLUES)",
    "VTV03 INICIAR/COMPLETAR 2DA 19M-9A (Total)",
    "VTV03 INICIAR/COMPLETAR 2DA 19M-9A (Total CLUES)",
    "VTV51 MIGRANTE 1RA 12M (Total)",
    "VTV51 MIGRANTE 1RA 12M (Total CLUES)",
    "VTV52 MIGRANTE 2DA 18M (Total)",
    "VTV52 MIGRANTE 2DA 18M (Total CLUES)",
    "VTV53 MIGRANTE 2DA 6A (Total)",
    "VTV53 MIGRANTE 2DA 6A (Total CLUES)",
    "VTV54 MIGRANTE INICIAR/COMPLETAR 1RA 13M-9A (Total)",
    "VTV54 MIGRANTE INICIAR/COMPLETAR 1RA 13M-9A (Total CLUES)",
    "VTV55 MIGRANTE INICIAR/COMPLETAR 2DA 19M-9A (Total)",
    "VTV55 MIGRANTE INICIAR/COMPLETAR 2DA 19M-9A (Total CLUES)",
    "Total SRP TRIPLE VIRAL (Total)",
    "Total SRP TRIPLE VIRAL (Total CLUES)",
    "Total SR DOBLE VIRAL (Total)",
    "Total SR DOBLE VIRAL (Total CLUES)",
    "Total General (Total)",
    "Total General (Total CLUES)"
]

df = pd.DataFrame(data, columns=columns)

# Save to Excel
output_file = r"C:\Users\aicil\.gemini\antigravity\scratch\vaccine_data_organization\Vacunacion_SRP_SR_2025.xlsx"
df.to_excel(output_file, index=False)

print(f"Excel file created: {output_file}")
