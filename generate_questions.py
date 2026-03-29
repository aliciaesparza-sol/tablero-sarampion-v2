import json

questions = [
    {
        "q": "Norma Oficial Mexicana que regula el expediente clínico en México:",
        "opts": ["A. NOM-034-SSA2-2013", "B. NOM-004-SSA3-2012", "C. NOM-008-SSA3-2010", "D. NOM-031-SSA2-1999", "E. NOM-007-SSA2-2016"],
        "a": "B"
    },
    {
        "q": "¿A partir de qué semana de gestación se recomienda la aplicación de la vacuna Tdpa en la mujer embarazada?",
        "opts": ["A. A partir de la SDG 12", "B. A partir de la SDG 20", "C. A partir de la SDG 28", "D. A partir de la SDG 32", "E. En cualquier trimestre"],
        "a": "B"
    },
    {
        "q": "Vacuna que está absolutamente contraindicada durante el embarazo:",
        "opts": ["A. Influenza", "B. Hepatitis B", "C. COVID-19", "D. Tdpa", "E. Triple vírica (SRP)"],
        "a": "E"
    },
    {
        "q": "¿A qué edad gestacional se usa como base para el cálculo de la edad corregida en niños prematuros?",
        "opts": ["A. 36 semanas", "B. 37 semanas", "C. 38 semanas", "D. 40 semanas", "E. 42 semanas"],
        "a": "D"
    },
    {
        "q": "El tamiz metabólico neonatal básico en México detecta obligatoriamente cuántas enfermedades según la norma vigente descrita en la clase:",
        "opts": ["A. 4 enfermedades", "B. 5 enfermedades", "C. 6 enfermedades", "D. 67 enfermedades", "E. 74 enfermedades"],
        "a": "C"
    },
    {
        "q": "Estudio indicado obligatorio en la primera semana de vida para detectar Cardiopatías Congénitas Críticas (CCC):",
        "opts": ["A. Ecocardiograma transtorácico", "B. Electrocardiograma", "C. Oximetría de pulso (Tamiz cardiaco)", "D. Radiografía de tórax", "E. Cateterismo cardiaco"],
        "a": "C"
    },
    {
        "q": "¿En qué momento se debe realizar el tamiz oftalmológico neonatal según la NOM-034-SSA2-2013?",
        "opts": ["A. Al nacer", "B. A la primera semana", "C. A la cuarta semana", "D. Al tercer mes", "E. Al sexto mes"],
        "a": "C"
    },
    {
        "q": "¿Cuándo se debe realizar el ultrasonido de cadera en un lactante con factores de riesgo para displasia del desarrollo de la cadera (DDC)?",
        "opts": ["A. En la primera semana de vida", "B. Previo a los 2 meses de edad, máximo a los 4 meses", "C. A los 6 meses de edad", "D. Después de los 8 meses", "E. Al año de edad"],
        "a": "B"
    },
    {
        "q": "Reflejo primitivo que aparece a las 12 SDG y se integra a los 4 meses, que se activa con la sensación de caer o un ruido fuerte:",
        "opts": ["A. Reflejo de succión", "B. Reflejo palmar", "C. Reflejo de Moro", "D. Reflejo de Babinski", "E. Reflejo tónico asimétrico del cuello"],
        "a": "C"
    },
    {
        "q": "Según el consenso COCO 2023, ¿cuál es la mejor edad para iniciar la alimentación complementaria en un lactante sano de término?",
        "opts": ["A. A los 4 meses", "B. A los 5 meses", "C. Después de los 6 meses", "D. A los 8 meses", "E. Al año de edad"],
        "a": "C"
    },
    {
        "q": "Según el consenso COCO 2023 en relación a los alimentos potencialmente alergénicos (huevo, cacahuate, pescado):",
        "opts": ["A. Deben retrasarse hasta el año de edad", "B. Deben retrasarse hasta los 2 años de edad", "C. Se deben introducir una vez iniciada la alimentación complementaria", "D. Solo introducirlos si no hay historia familiar de atopia", "E. Introducir primero la yema del huevo hasta el año de edad"],
        "a": "C"
    },
    {
        "q": "¿Cuál es la capacidad gástrica estimada de un lactante al iniciar su alimentación complementaria?",
        "opts": ["A. 10 g/kg/día", "B. 20 g/kg/día", "C. 30 g/kg/día", "D. 40 g/kg/día", "E. 50 g/kg/día"],
        "a": "C"
    },
    {
        "q": "¿Cuál es el momento límite o ventana crítica recomendada para introducir texturas grumosas en la alimentación complementaria y evitar problemas de selectividad alimentaria?",
        "opts": ["A. Antes de los 6 meses", "B. Antes de los 10 meses", "C. A los 12 meses", "D. A los 18 meses", "E. A los 2 años"],
        "a": "B"
    },
    {
        "q": "Número total de piezas dentarias temporales y permanentes en el ser humano, respectivamente:",
        "opts": ["A. 20 temporales y 32 permanentes", "B. 24 temporales y 32 permanentes", "C. 20 temporales y 28 permanentes", "D. 24 temporales y 36 permanentes", "E. 20 temporales y 30 permanentes"],
        "a": "A"
    },
    {
        "q": "Fórmula utilizada para estimar la talla en un niño de entre 4 años y pubertad:",
        "opts": ["A. Edad (en años) x 2 + 8", "B. Edad (en años) x 5 + 85", "C. Edad (en meses) x 2 + 80", "D. Edad (en años) x 6 + 77", "E. Edad (en años) x 4 + 50"],
        "a": "B"
    },
    {
        "q": "Perímetro cefálico promedio al nacimiento y su crecimiento promedio durante el primer año de vida:",
        "opts": ["A. 33 cm al nacimiento y crece 0.5 cm por mes", "B. 35 cm al nacimiento y crece 1 cm por mes en promedio el primer año", "C. 35 cm al nacimiento y crece 2 cm por mes", "D. 38 cm al nacimiento y crece 0.5 cm por mes", "E. 32 cm al nacimiento y crece 1.5 cm por mes"],
        "a": "B"
    },
    {
        "q": "Parámetro o índice de medición que tiene más sensibilidad que el IMC para detectar riesgo de síndrome metabólico tempranamente:",
        "opts": ["A. Índice Cintura/Cadera", "B. Índice Cintura/Estatura", "C. Segmento superior/Segmento inferior", "D. Talla Blanco Familiar", "E. Circunferencia de brazo derecho"],
        "a": "B"
    },
    {
        "q": "Al revisar la brazada en la evaluación somatométrica de la talla, ¿a partir de qué edad la brazada es teóricamente igual a la talla?",
        "opts": ["A. En los lactantes", "B. 2 a 3 años", "C. 4 a 6 años", "D. 7 a 10 años", "E. Adolescentes"],
        "a": "D"
    },
    {
        "q": "Escala / Clasificación antropométrica que nos permite diferenciar la intensidad y cronología de la desnutrición (aguda o crónica) evaluando Peso/Talla y Talla/Edad:",
        "opts": ["A. Clasificación de Federico Gómez", "B. Clasificación de Waterlow", "C. Tablas de la OMS", "D. Tablas de la CDC", "E. Índice de Quetelet"],
        "a": "B"
    },
    {
        "q": "En el patrón de respiración de Cheyne-Stokes, los hallazgos semiológicos característicos son:",
        "opts": ["A. Respiraciones rápidas y superficiales persistentes", "B. Inspiraciones profundas y ruidosas seguidas de pausa", "C. Apnea de 20-30 seg. seguida de amplitud que aumenta progresivamente, llega a un máximo y luego disminuye hasta otra apnea", "D. Ritmicidad mantenida interrumpida por periodos de apnea, de forma irregular", "E. Sensación de falta de aire en decúbito supino"],
        "a": "C"
    },
    {
        "q": "Temperatura mínima considerada clínicamente como fiebre según los conceptos de la presentación (con duración de al menos 1 hora o toma aislada mayor):",
        "opts": ["A. Temperatura axilar de 37.5°C", "B. Temperatura axilar > 38.0°C (o aislada >38.3°C)", "C. Temperatura rectal de 37.8°C", "D. Temperatura ótica de 37.9°C", "E. Temperatura axilar de 38.5°C"],
        "a": "B"
    },
    {
        "q": "El tamiz auditivo es clave porque el desarrollo óptimo del lenguaje termina a la edad de:",
        "opts": ["A. 1 año", "B. 2 años", "C. 3 años", "D. 5 años", "E. 8 años"],
        "a": "D"
    },
    {
        "q": "¿Qué evalúa fundamentalmente el puntaje del APGAR?",
        "opts": ["A. El daño neurológico a largo plazo", "B. Retraso mental futuro", "C. Capacidad auditiva postnatal", "D. Transición y adaptación a la vida extrauterina inmediata (no predice daño neurológico)", "E. Madurez pulmonar y producción de surfactante"],
        "a": "D"
    },
    {
        "q": "En la evaluación somatométrica de los segmentos corporales, ¿cómo obtenemos la medida del segmento superior?",
        "opts": ["A. Midiendo del vertex al borde superior de sínfisis del pubis", "B. Restando a la Talla el valor del Segmento Inferior", "C. Midiendo de la cicatriz umbilical al vertex", "D. Extensión de los brazos", "E. Midiendo del esternón al vertex"],
        "a": "B"
    },
    {
        "q": "Definición de 'Emaciación' de acuerdo a la clasificación antropométrica referida para grados de desnutrición:",
        "opts": ["A. Talla baja para la edad con peso normal", "B. Peso mayor para la talla", "C. Adelgazamiento extremo y pérdida de grasa (reflejado en déficit Peso/Talla)", "D. Edema generalizado por déficit proteico", "E. Disminución exclusiva del segmento corporal inferior"],
        "a": "C"
    },
    {
        "q": "¿Qué reflejo primitivo o arcaico desaparece habitualmente a los 4 meses de edad como indicador de maduración de la vía motora y cuya persistencia sugiere daño neurológico?",
        "opts": ["A. Marcha automática", "B. Moro", "C. Babinski", "D. Paracaídas", "E. Reflejo de anfibio"],
        "a": "B"
    },
    {
        "q": "La recomendación para prevención de displasia del desarrollo de la cadera al envolver al recién nacido es:",
        "opts": ["A. Envolver con extremidades en extensión e hiperaducción", "B. Evitar envolver al RN con extremidades en extensión y aducción prolongada", "C. Mantener la cadera extendida permanentemente los primeros 2 meses", "D. Colocar arnés de Pavlik profilácticamente en todos los RN", "E. Envolver con fajas elásticas abdominales que compriman las extremidades inferior"],
        "a": "B"
    },
    {
        "q": "Al auscultar un soplo cardíaco y sospechar coartación de la aorta en la exploración pediátrica, el signo clínico indirecto indispensable a investigar es:",
        "opts": ["A. Ausencia o disminución acentuada de los pulsos femorales", "B. Ausencia de pulso carotídeo", "C. Acropaquia", "D. Cianosis peribucal", "E. Hipertensión pulmonar aislada"],
        "a": "A"
    },
    {
        "q": "¿Cuál es la norma oficial del control profiláctico auditivo (Tamiz)? ¿Cuánto tiempo dura generalmente la prueba de emisiones otoacústicas si el bebé está dormido?",
        "opts": ["A. 1 a 2 minutos", "B. 5 a 10 minutos", "C. 30 a 45 minutos", "D. 1 a 2 horas", "E. Más de 2 horas"],
        "a": "B"
    },
    {
        "q": "Bebidas que deben evitarse durante la ablactación por contener alcaloides y polifenoles que inhiben la absorción de hierro y producen cólicos:",
        "opts": ["A. Jugos de frutas naturales", "B. Leches de fórmulas maternizadas", "C. Café, té y aguas aromáticas", "D. Agua purificada", "E. Leche humana transicional"],
        "a": "C"
    },
    {
        "q": "Dentro del esquema de seguimiento y consulta pediátrica del niño sano (NOM-008-SSA3-2010), ¿cuántas consultas como mínimo requiere un menor de un año (excluyendo el periodo neonatal de los 28 días)?",
        "opts": ["A. Tres consultas bimensuales", "B. Cuatro consultas (cada 3 meses)", "C. Cinco consultas (a los 2, 4, 6, 9 y 12 meses)", "D. Doce consultas (mensuales)", "E. Dos consultas (a los 6 y 12 meses)"],
        "a": "C"
    },
    {
        "q": "En el contexto de Talla Baja, ¿qué es la Talla Blanco Familiar?",
        "opts": ["A. Es la estatura objetivo estimada calculada en relación directa a la talla de los abuelos", "B. Es la estimación de la estatura basada 70% en la talla de ambos padres", "C. Es la longitud supina al nacer multiplicada por 2", "D. Es el percentil poblacional promedio para ciertas comunidades", "E. Es el pronóstico de talla calculado solo con RX de mano"],
        "a": "B"
    },
    {
        "q": "¿Cuál es el momento en que inicia la pubertad fisiológicamente por incremento en la velocidad de crecimiento en las mujeres de manera frecuente?",
        "opts": ["A. Entre los 7 y 8 años", "B. Entre los 10.5 y 11 años", "C. Entre los 12 y 13 años", "D. Después de los 14 años", "E. A partir de los 15 años"],
        "a": "B"
    },
    {
        "q": "Respecto a la clasificación de Desnutrición Infantil de Federico Gómez, el porcentaje de déficit Peso/Edad que indica una desnutrición de grado LEVE es:",
        "opts": ["A. 0 a 10%", "B. 11 a 24%", "C. 25 a 40%", "D. 41 a 55%", "E. Mayor a 55%"],
        "a": "B"
    },
    {
        "q": "El término 'Desmedro' en evaluación antropométrica se utiliza para hacer referencia a:",
        "opts": ["A. La disminución paulatina del tejido adiposo", "B. Talla baja para la edad con peso normal o adecuado para la talla, traduciendo deficiencia crónica", "C. El incremento agudo de peso en un mes", "D. La detención abrupta de la circunferencia cefálica", "E. Pérdida severa de masa muscular"],
        "a": "B"
    },
    {
        "q": "Según el COCO 2023, en lactantes mayores de 6 meses alimentados con esquemas veganos (lo cual se desaconseja, pero si se exige), es indispensable la suplementación con:",
        "opts": ["A. Fenilalanina y Tirosina", "B. Solo hierro y Vitamina C", "C. Vit B12, Vit D, Hierro, Zinc, Ácido fólico, Omega 3 y Calcio", "D. Solo calcio sérico", "E. No requieren suplementación"],
        "a": "C"
    },
    {
        "q": "Patología abdominal del recién nacido caracterizada por la protrusión de asas intestinales sin recubrimiento de saco membranoso por un defecto de la pared abdominal distinto al anillo umbilical:",
        "opts": ["A. Hernia umbilical protruida", "B. Onfalocele", "C. Gastrosquisis", "D. Diástasis de rectos", "E. Tumor de Wilms"],
        "a": "C"
    },
    {
        "q": "Dosis inicial recomendada de paracetamol usada en el paciente de la presentación clínica de urgencias y que se menciona como esquema antipirético estándar en pediatría:",
        "opts": ["A. 5 mg/kg/dosis", "B. 10 a 15 mg/kg/dosis", "C. 20 mg/kg/dosis", "D. 30 mg/kg/dosis", "E. 40 mg/kg/dosis"],
        "a": "B"
    },
    {
        "q": "Cuando se valora la frecuencia respiratoria, definimos apnea como:",
        "opts": ["A. FR por arriba de 2 desviaciones estándar de lo normal", "B. Sensación subjetiva de dificultad para respirar", "C. Ausencia de flujo respiratorio por > 20 segundos independiente de otra clínica, o < 20 s acompañada de bradicardia/hipoxemia", "D. Disnea en posición supina", "E. Ritmicidad mantenida interrumpida por periodos de aumento de FR"],
        "a": "C"
    },
    {
        "q": "¿Qué cantidad de agua recomienda el consenso COCO 2023 en cucharadas o ml/día para un lactante que ha iniciado alimentación complementaria a los 6-8 meses con lactancia materna exclusiva (sin fórmula)?",
        "opts": ["A. 60 - 150 ml diarios de forma complementaria. (Aunque con seno materno no aporta gran requerimiento extra pero se incentiva la formación de hábitos)", "B. 240 a 300 ml", "C. 450 a 600 ml", "D. 1 Litro exacto al día", "E. Un vaso de agua lleno acompañando cada papilla"],
        "a": "A"
    }
]

with open(r'C:\Users\aicil\.gemini\antigravity\scratch\Banco_Preguntas_Historia_Clinica.md', 'w', encoding='utf-8') as f:
    f.write("# BANCO DE PREGUNTAS: HISTORIA CLÍNICA PEDIÁTRICA\n\n")
    for idx, item in enumerate(questions, 1):
        f.write(f"**{idx}. {item['q']}**\n")
        for opt in item['opts']:
            f.write(f"{opt}\n")
        f.write("\n")
        f.write(f"ANSWER: {item['a']}\n")
        f.write("\n---\n\n")

print("Generated questions successfully")
