import json

questions2 = [
    {
        "q": "Señala la afirmación correcta respecto al número total de consultas que debe recibir de seguimiento un menor de cinco a nueve años:",
        "opts": ["A. Una consulta trimestral", "B. Una consulta semestral", "C. Una consulta anual", "D. Dos consultas anuales", "E. No requiere consulta obligatoria una vez escolarizado"],
        "a": "C"
    },
    {
        "q": "Al calcular el indicador antropométrico Peso/Edad (P/E) utilizando la clasificación de Federico Gómez, obtenemos un valor de 65%. Este porcentaje corresponde a:",
        "opts": ["A. Normal", "B. Desnutrición Leve", "C. Desnutrición Moderada", "D. Desnutrición Severa", "E. Obesidad"],
        "a": "C"
    },
    {
        "q": "¿Qué indica clínico refleja el indicador de Peso para Talla (P/T) bajo?",
        "opts": ["A. Desmedro o talla baja", "B. Desnutrición crónica sin agudización", "C. Desnutrición aguda o emaciación", "D. Retraso puberal inminente", "E. Riesgo de obesidad visceral"],
        "a": "C"
    },
    {
        "q": "¿En qué etapa se alcanza el 75-80% de filtración glomerular respecto al adulto en la función renal del lactante?",
        "opts": ["A. En el recién nacido", "B. A los 3-4 meses", "C. A los 6 meses", "D. A los 12 meses", "E. A los 2 años"],
        "a": "C"
    },
    {
        "q": "De acuerdo a la norma oficial (NOM-034-SSA2-2013), ¿a qué edad gestacional debe considerarse la detección para patologías de tamiz metabólico neonatal (ERRORES INNATOS DEL METABOLISMO)?",
        "opts": ["A. Menores a las 32 SDG", "B. Recién nacidos independientemente de su vía de nacimiento y SDG (tamizaje universal)", "C. Solo recién nacidos prematuros", "D. Solo recién nacidos producto de madre diabética", "E. Recién nacidos con Apgar menor a 6 a los 5 minutos"],
        "a": "B"
    },
    {
        "q": "La velocidad de crecimiento ponderal del perímetro cefálico entre el cuarto y doceavo mes es el indicador clínico del desarrollo tisular nervioso. ¿Cuánto crece desde los 3 hasta la vida adulta?",
        "opts": ["A. 1 a 2 cm", "B. 2 a 4 cm", "C. 5 a 7 cm", "D. 10 a 12 cm", "E. 15 cm"],
        "a": "C"
    },
    {
        "q": "En el caso de un lactante con introducción temprana de sólidos grumosos (previo o inmediatamente cercano a los 9-10 meses), el principal beneficio en la adolescencia y vida adulta será:",
        "opts": ["A. Mayor talla blanco familiar", "B. Menor selectividad alimentaria y mayor aceptación de frutas / verduras", "C. Regulación hepática del hierro endógeno", "D. Disminución de riesgo genético atópico", "E. Producción aumentada de linfocitos T intraepiteliales"],
        "a": "B"
    },
    {
        "q": "De los Diez Pasos Hacia Una Feliz Lactancia (OMS/UNICEF), ¿cuál paso fomenta que se deje a la madre cohabitar con el lactante garantizando que estén juntos permanentemente?",
        "opts": ["A. Paso 3", "B. Paso 4", "C. Paso 7", "D. Paso 8", "E. Paso 10"],
        "a": "C"
    },
    {
        "q": "Causa infecciosa con riesgo del 8.2% de producir muerte materna en embarazo cuando se adquiere en el 2º y 3º trimestre, la cual cuenta con prevención vacunal:",
        "opts": ["A. Rubéola endémica", "B. Hepatitis C", "C. Toxoplasmosis", "D. Influenza", "E. VPH"],
        "a": "D"
    },
    {
        "q": "¿A qué edad (o entre qué año) del desarrollo infantil la velocidad de crecimiento se estabiliza de 4-4.5 cm por año hasta el inicio del estirón puberal?",
        "opts": ["A. De 2 a 3 años", "B. De 4 a 12 años", "C. Los primeros 2 años", "D. Después de los 14 años", "E. Durante el primer año de vida"],
        "a": "B"
    },
    {
        "q": "Sobre la técnica estándar de punción capilar para el tamiz neonatal, la profundidad de la lanceta no debe sobrepasar:",
        "opts": ["A. Los 1.0 mm de profundidad", "B. Los 2.4 mm de profundidad", "C. Los 4.0 mm de profundidad", "D. Los 5.0 mm de profundidad", "E. Puede ser cualquier medida siempre que se consiga buen sangrado capilar"],
        "a": "B"
    },
    {
        "q": "Cifra de incremento total de longitud corporal aproximado durante el primer año de vida posnatal (promedio general estimado):",
        "opts": ["A. 12 cm", "B. 15 cm", "C. 24 cm", "D. 35 cm", "E. 50 cm"],
        "a": "C"
    },
    {
        "q": "Cifra de incremento total de longitud corporal en el segundo año de vida posnatal (promedio general estimado):",
        "opts": ["A. 6 cm", "B. 10 cm", "C. 12 cm", "D. 18 cm", "E. 20 cm"],
        "a": "C"
    },
    {
        "q": "¿Qué es la 'ablactación' en concepto estricto de acuerdo a la etimología de su definición en la clase?",
        "opts": ["A. La introducción de derivados lácteos vacunos", "B. El abandono temporal del calostro materno", "C. La acción de privar, separar o quitar al hijo pequeño de la leche materna", "D. El aumento calórico de alimentos exentos de proteínas complejas", "E. La transición de lactancia suplementaria a lactancia base de fórmula artificial"],
        "a": "C"
    },
    {
        "q": "¿Qué grupo etario pediátrico asiste a revisión médica (crecimiento y niño sano) con regularidad de una evaluación completa cada seis meses obligatoria por la NOM?",
        "opts": ["A. Recién nacido primeras 4 semanas", "B. Lactante menor de 1 año", "C. Niños entre 1 a 4 años", "D. Etapa preescolar de 5 a 6 años", "E. Etapa puberal entre 12 y 16 años"],
        "a": "C"
    },
    {
        "q": "¿El diagnóstico y tratamiento o prevención de hipoacusia debidamente canalizada tiene un impacto en la reducción de costos en la vida pediátrica económica estimado sobre:",
        "opts": ["A. 10 mil dólares", "B. 50 mil dólares", "C. 100 mil dólares", "D. 250 mil dólares", "E. 1 millón de dólares"],
        "a": "E"
    },
    {
        "q": "Si en la evaluación somatométrica un niño preescolar de 3 años, presenta diferencia entre Segmento Inferior y Segmento Superior, en qué parte fisiológicamente el segmento superior comienza a ser casi igual al segmento inferior estabilizándose en la brazada casi de modo paralelo hasta los 12 años:",
        "opts": ["A. Lactante de 6 meses", "B. Preescolar de 2 años", "C. Escolar de 7-10 años", "D. 12 meses", "E. Solo en la vejez"],
        "a": "C"
    },
    {
        "q": "Al interrogar el hábitat, una pregunta a formular a los padres debe ir orientada al patrón de hacinamiento por:",
        "opts": ["A. Transmisión genética recesiva", "B. Agrupación patológica de infecciones de contacto / transmisión aerogena", "C. Mayor ingesta nutricional de grasas saturadas trans-orgánicas", "D. Retraso puberal neurofisiológico originado en estrógenos estables", "E. Contaminación por mercurio sistémico de aguas pesadas"],
        "a": "B"
    },
    {
        "q": "¿En base a la técnica de evaluación clínica, el examen de inspección general (Hábitus Exterior) comprende evaluar?",
        "opts": ["A. Edad aparente, estado del sensorio y complexión simétrica en color, forma y actitud", "B. Exclusivamente la frecuencia cardiaca y respiratoria inicial (signos vitales en sí)", "C. Los ruidos de Korotkoff de grado medio en región torácica baja", "D. Auscultación de bases pulmonares bilateral en busca de derrame", "E. El resultado de su peso ajustado por Talla a 24 meses"],
        "a": "A"
    },
    {
        "q": "¿Patología umbilical al inspeccionar a un recién nacido donde las asas intestinales protruyen sin membrana protectora periumbilical ni restos vitelinos directos en cordón primario sano a la izquierda de la línea media en la exploración típica asumiendo hallazgos?",
        "opts": ["A. Persistencia de uraco bífido", "B. Hernia inguinal protruida hacia ombligo", "C. Gastrosquisis", "D. Onfalocele gigante", "E. Encefalocele anterior extrínseco"],
        "a": "C"
    },
    {
        "q": "Signo de sospecha neurológica al explorar los genitales y zona sacra pediátrica de recién nacido:",
        "opts": ["A. Clítoris prominente o labios mayores hipertróficos sin masa extra, fisiológicos", "B. Testículos en la cavidad o descendimiento en semanas iniciales", "C. Fosa pilonidal hundida profusa o mechón piloso lumbar al inspeccionar cara posterior", "D. Adherencia de prepucio no retráctil antes del mes de vida", "E. Transiluminación temporal testicular sugestiva de hidrocele transitorio benigno"],
        "a": "C"
    }
]

questions3 = [    
    {
        "q": "Respecto a los antecedentes infecciosos obstétricos clásicos agrupados, ¿cuál es el acrónimo para citomegalovirus, toxoplasmosis, herpes simple genital intrauterino o intraparto explorado usualmente?",
        "opts": ["A. COVID", "B. TORCH", "C. GPC", "D. APGAR", "E. BLW"],
        "a": "B"
    },
    {
        "q": "¿Cuánto se acepta de margen de error confiable en el instrumento en gramos al pesar en báscula electrónica y tarada a un niño escolar de más de diez kilogramos?",
        "opts": ["A. 1 a 2 g", "B. 5 a 10 g", "C. Hasta 100 g", "D. Al menos 500 g", "E. No hay margen técnico tolerable a la vista al pesar después del mes"],
        "a": "C"
    },
    {
        "q": "El término técnico semiológico de la interrupción en el ritmo normal respiratorio que mantiene ritmicidad alternada por apneas es:",
        "opts": ["A. Disnea paroxística intermitente nocturna", "B. Respiración periódica biótica / Respiración de Biot", "C. Tiro intercostal de grado laringotraqueíto recurrente moderada a severa", "D. Quejido espiratorio polipneico constante agudo intermitente tardío preagonal profundo doloroso", "E. Ataxia ventilatoria de grado hiperápneico intermitente moderada o severa central o asimétrico"],
        "a": "B"
    },
    {
        "q": "¿Qué se debe documentar por seguridad como prioridad temporal en antecedentes maternos de recién nacidos sobre infecciones prenatales referidas en clase?",
        "opts": ["A. Control de citología cervical a lo largo toda vida materna", "B. Infecciones de vías urinarias (IVU) reiteradas diagnosticadas y tratadas, CV (cervicovaginitis), RPM (ruptura prematura membranas), así como el esquema TORCH", "C. Historial de tuberculosis infantil personal de la madre", "D. El grupo sanguíneo propio del padre biológico en todas y sin excepción para iso-inmunización y vacunas conjugadas post 40 años o donaciones a otras mujeres u oncológicas para cirugías", "E. Solo toxoplasmosis si se expone a heces felinas y caninas rurales o citadinas"],
        "a": "B"
    },
    {
        "q": "Reflejo primitivo en base de sostén lateral y arrastre del pie o deslizamiento corporal que desaparece a las 3 a 5 semanas como máximo de manera fisiológica si hay integridad neuroespinal descendiendo por medula central:",
        "opts": ["A. Marcha automática arcaica / paso arcaico", "B. Reflejo cruzado miotático estriado rotuliano asimétrico de Golgi", "C. Babkin perioral palmomental transitorio intermitente medular profundo", "D. Búsqueda y hociqueo peribucal rotacional", "E. Galant / Encorvamiento lateral de tronco dorsal paraspinal o flexión ipsilateral de la cadera"],
        "a": "A"
    },
    {
        "q": "¿En un esquema de BLW o BLISS implementado como método de alimentación complementaria, un riesgo que la COCO 2023 advierte sin asesoramiento profesional estricto consiste potencialmente en:",
        "opts": ["A. Excesiva ganancia pondoestatural precoz (macrosomía idiopática láctea)", "B. Mayor producción saliva endógena y erupción dental acelerada o rápida por hiperpresión", "C. Menor ingesta calórica general y riesgo potencial de desnutrición/asfixia teórica", "D. Maduración neuroendócrina atípica del lóbulo anterior pituitario", "E. Hemoconcentración de hierro sérico de gran absorción intestinal en tracto digestivo superior precoz o microvellosidades del colon sigmoide en infantes menores o similares crónicos y temporales benignos pero asintomáticos prolongados en infantes"],
        "a": "C"
    },
    {
        "q": "¿Cuál de las características radiológicas listadas por el algoritmo y lineamiento general ortopédico infantil sugerido NO ES el método primario diagnóstico oportuno de DDC a realizar en primeros 2 meses sino después?",
        "opts": ["A. Radiografía anteroposterior simple de pelvis infantil rutinaria después de 4 a 6 meses de edad no como tamiz antes de 8 semanas", "B. Ultrasonido pélvico dinámico estructural", "C. Maniobras de Barlow repetidas en cunero sin imagenología o con maniobra de ortolani y signo de pliegues asimétricos o Galeazzi positivo como clínica o signo precoz", "D. Tamiz ultrasonográfico pediátrico a semana de nacimiento rutinarias en población general europea y mexicana (DDC o coxa vara) en primera opción.", "E. No usar doppler pelvifemoral bajo en la práctica hospitalaria pediátrica para medir la presión de la arteria femoral medial y colaterales"],
        "a": "A"
    },
    {
        "q": "El desarrollo puberal tardío de Talla en varones tiene una etapa veloz que contribuye del total final de la talla incrementándose a un nivel de ganancia media de:",
        "opts": ["A. Solo 5-10 cm correspondientes a un aumento modesto estrógeno-dependiente total a lo largo de pubertad", "B. 20-25 cm o su equivalente al casi 12% total pondo-estatural final con eje funcional somatotropo", "C. Solo se reafirman 30-35 cm por carga estrógeno testosterónica y hormonas tiroideas de reserva en tejido subcutáneo o estromal / mineral óseo madurado total tardíamente pre-cierre fisario absoluto en vida general tardía.", "D. 0 cm adicionales en crecimiento rápido ya que este ocurrió por completo en la edad prescolar de los 6 a los 8 años de vida media u osteogénesis y se conserva de vida adulta a senilidad.", "E. Mas de 45 cm post-16 años en varones por inicio androgénico retrasado"],
        "a": "B"
    },
    {
        "q": "Medida de somatometría antropométrica de rutina preferencial indicada y practicada estrictamente en menores de 2 años (por estatura menor a cien / 100 centímetros) que no aplican a regla ortostática usando estadímetro:",
        "opts": ["A. Cintura a piso en infantes recién nacidos a dos años pre-escolares o post natales neonatales sanos y menores prematuros de hasta 3 años de edad por peso inferior a catorce kilogramos", "B. Circunferencia bicipital torácica estática (CBTE) supina obligatoria por OMS y norma oficial de biometría rutinaria de primera mano y valoración universal anual al año y catorce años.", "C. La longitud evaluada en infantómetro de decúbito supino fijo o por tope y base rígida ortostáticamente re-adecuada horizontal de tope firme a planta podálica.", "D. Pliegue cutáneo cráneo supraescapular horizontal", "E. Evaluación del perímetro cefálico temporal longitudinal pélvica de manera sistemática y rutinariamente cada tres años."],
        "a": "C"
    },
    {
        "q": "¿A qué semana máxima ideal postparto post término neonatal sin contratiempos, debe reportar la aplicación la NORMA Oficial Mexicana de salud Tamiz visual y ocular pediátrico u oftalmológico buscando alteraciones retinianas de ceguera potencial u opacidades que obligan manejo preventivo o de intermitencia urgente resolutiva?",
        "opts": ["A. Cuarta semana de vida (o mes nominal en promedio fisiomaduracional) del nacimiento", "B. En sala o unidad parto cunero inmediatamente tras corte estéril aséptico de cordón umbilical central o distad en segundos minutos post natales transitorios estables.", "C. Desde la hora cuarenta y ocho posparto de adaptación extrauterina", "D. Al iniciar control cefálico a partir de tercer mes lactancial mayor. ", "E. Cerca de los seiscientos días (segundo año vida) infantil temprano con lenguaje en evolución oral"],
        "a": "A"
    },
    {
        "q": "¿Cuál test antropométrica detecta adiposidad abdominal superior por encima de 0.5 puntos como indicador de co-morbilidad o riesgo cardio-vaso-metabólico indirecto sensible superior al simple Índice Masa Corporal?",
        "opts": ["A. Índice Cintura-Estatura (Talla o Longitud cráneo plantar en relación directa matemática divisor a perímetro o circunferencia en cm por encima crestas)", "B. Relación Talla Blanca Familiar al Perímetro Cefálico en Pretérminos y P.E.G. o Síndrome Down / Patau / Síndrome de Edwards de línea media del cráneo anterior lateral", "C. IMC superior al percentil cincuenta con desmedro crónico moderado waterlow o índice Quetelet", "D. Z score índice Gómez", "E. Puntuación Tanner Genital / Mamaria / Vello axial y pubiano femenino"],
        "a": "A"
    },
    {
        "q": "Durante la auscultación abdominal u exploración neonatal integral, para que sugiera una patología subyacente de organomegalia (hepatomegalia hepática per se en este rubro particular sin incluir otras variables), el borde rebase hepático costal debe exeder de manera general:",
        "opts": ["A. Menos de un cuarto de un centímetro de rebase y se toma normal idiopático sano.", "B. 2 cm o más de tres centímetros de borde u delimitación que el reborde costal percutible de la parrilla anteroinferior costal general.", "C. Afectar el reborde esplénico por esplenomegalia gigante contralateral", "D. Que el borde percutido se pierda al timpanismo post-respiratorio idiopático percutido en rítmica respiración diafragmática espiratoria máxima de exhalación en niño escolar de modo patonogmónico al percutir fuerte de arriba bajo desde pezón al apéndice e higado inferior y medio en general con campana.", "E. Cinco a once milímetros en un varón."],
        "a": "B"
    },
    {
        "q": "¿Qué refleja o busca determinar primordialmente si se evidencia diástasis de los rectos abdominales anteriores sobre plano sagital del recién nacido evaluado o a la inspección por simple vista si existe protrusión no traumática transitoria de manera común?",
        "opts": ["A. Falta de fuerza real o relativa o separación de fascias (debilidad o laxa) local pared anterior pared abdominal medial de origen congénito que suele cerrar o acortarse fisiomaduracionalmente de manera autolimitada per se aunque requiera vigilancia", "B. Rotura traumática aponeurótica directa transversal post parto macrosómico de urgencia en vértice cesárea transpelvica forzada o forcep general instrumentado y lesión visceral postquirúrgica accidental transitoria tardía pre diagnosticada. ", "C. Inactivación somática postganglionar tóraco-abdominal espinal que denerva los plexos hipogástricos primarios distales abdominales anteromediales pélvicos. ", "D. Acumulación líquido pre o extraitoneal edematizado por asariasis de fase ascitis hepato patológica masiva portal de un feto y recién nacido", "E. Tumoral mioma intrarectus pélvico o hemangioma esclerosante central crónico y encapsulado indurado e hiperpigmentado de evolución incierta y rara infrecuente asintomática sin malignizar en pre termino varón. "],
        "a": "A"
    },
    {
        "q": "Al interrogatorio directo o mixto para conformar un diagnóstico de nutrición inadecuada e inspección de antecedentes no patológicos (APNP), si leemos sobre dieta o ablactación se indica preguntar y documentar a cuidadores qué punto en específico cardinal para seguimiento posterior post ablactación:",
        "opts": ["A. Si el niño convive con rumiantes y felinos o roedores exóticos", "B. Si se integra a la dieta familiar, cantidad, calidad, e impacto de frecuencia dietética global de nutrientes macro y micronutrientes", "C. Las marcas y empresas de puré embotelladas y de producción procesada embutida lácteas en su ciudad.", "D. Qué tan seguido vomita tras alimentarse (RGE de 5 años diagnosticado crónico de adulto en senectud en adultos tardíos)", "E. Las infecciones por E coli que cursan endémicamente con gastroenteritis de transmisión directa transmamaria por mal lavado del pezón periareolar idiopático endócrino."],
        "a": "B"
    },
    {
        "q": "Refiriéndonos al cálculo del Índice de Quetelet (IMC), ¿cómo medimos su sensibilidad teórica diagnóstica como estimador real del verdadero sobrepeso-obesidad clínica según las cifras de control en consulta?",
        "opts": ["A. Sensibilidad de un rango de alrededor o estimado por el setenta (70) al ochenta (80) por ciento (%). ", "B. Cien por ciento y es oro absoluto. Solo hay falsos si el equipo se daña técnica y localmente en calibración.", "C. Cercana al diez u once por ciento ya que subestima el tejido adiposo a menos que exceda o que haya desnutrición marasmática.", "D. Más elevado que TAC, DEXA y de la pletismografía hidrostática en porcentaje y predicción corporal masa y panículo celular.", "E. Escasa a la hora inicial por sesgar a pacientes mayores de cincuenta años con osteoporosis tardía a perfiles anoréxicos o bulímicos e inanición general neurogénica."],
        "a": "A"
    },
    {
        "q": "¿Desde qué o cuál SDG a calcular e iniciar de base inicial u origen gestacional intraútero formativo es capaz o ya se reporta en ecografía prenatal dinámica visible que puede integrarse inicialmente o de forma fisiológica la presencia intrauterina arcaica de REFLEJO de búsqueda y/u de HOCIQUEO-SUCCIÓN y reflejos vitales primarios al perioral o tocar peribucal?",
        "opts": ["A. Desde la fecundación in vitro embrionaria o tercera semana blastular germinal neural de notocorda y de surco ectodérmico e inicio somítico primario.", "B. De las de treinta y cuatro semanas de evolución del desarrollo embrionario neurofisiológico gestacional de viabilidad fetal de succión / deglución maduros básicos de manera precoz pero efectiva para vida ex utero si nace pre término funcional u arcaico", "C. En horas después o periparto de fase latente de recién nacido termino maduro 41 SDG post maduro en decúbito. ", "D. Doceavo y decimo séptimo día embrional general y precoz. ", "E. Aparece por impronta genética en lactantes solo post cuarenta días postparto de maduración cerebral en encéfalo frontal de Broca"],
        "a": "B"
    },
    {
        "q": "Aparte de valorar perímetro de longitud o peso estricto o su proporción armónica en desnutrición de las tablas de clasificación Federico Gómez al catalogar Grado Ponderal Clínico (por déficit Peso para un peso a Edad); nos permite u NO permite dictaminar en esta misma escala y exclusivamente con ella:",
        "opts": ["A. Sí sabemos por este método si es totalmente desnutrición calórico proteica Marasmo o pura hipoproteinémica de tipo Kwashiorkor puro o edematoso general anasarca hipoalbuminémica asintomática de origen infeccioso endémico.", "B. No ayuda ni permite discriminar la relación exacta de si está solo o cursando en fase general crónica compensada o con impacto talla-largo, y no se sabe al catalogar por tal instrumento la agudización cronológica (D. aguda o crónica con certeza absoluta estricta como pasa en Waterlow al usar talla)", "C. Discriminar sobre un hipercrecimiento primario hipofisiario adenomatoso y sobre la densidad calcárea trabecular periférica subcondral general densitometral de la primera cérvico torácica y la radiometría carpal carpiana.", "D. Proyectar un índice T/E como factor etiológico metabólico in-utero torácico del cordón vitelino placentario.", "E. Diagnóstico directo genético cromosomal exacto e intra-citoplasmático nuclear mutaciones mitocondriales."],
        "a": "B"
    },
    {
        "q": "Indicaciones para vacuna antitetánica en situación de contacto / herida susceptibilidad riesgo punzocortante tetanogénica sucia extensa a pesar de que está expuesta una mujer gestante embarazada (que por su trimestral o falta de las bases):",
        "opts": ["A. No debe y no pondrá indicación inmunizarse si se expone y sufre de tal riesgo si está gestando un feto pues la tetanospasmina es biológicamente un patógeno linfo de alto o de grave o bajo peso y la molécula pasa al abortar letal o gravemente.", "B. Si se produce herida o es susceptible del medio o recibe y amerita profilaxis antitetánica, se puede o debe administrar la Tdpa y/o además gammaglobulina antitetánica pasiva inmediata en cualquier u momento como GPC normativa dicta y manda al caso respectivo post exposición de riesgo.", "C. Si un perro transmite la rabia se pone BCG profiláctica a esta y solo un gramo sulfadiazina de plata general pero con inmunoglobulina contra zóster en región lumbar y hombro y muslo interno bilateral.", "D. Aplicar vacuna de tipo viva anti rábica general endógena intramuscular profunda a la dosis pre parto mensual en infusión continua sin suero homólogo por seis dosis altas hasta finalizar gestación con Tdpa en la ultima cesárea.", "E. Aislar a madre infectada u contacto en cama de reposo oscuro sin ruidos estridentes para que no precipite un periodo tónico-clónico convulsivo muscular laringoespasmo o en espasmo esofágico temporal asimétrico general e iatrogénico. "],
        "a": "B"
    },
    {
        "q": "Al interrogar el hábitat, una pregunta a formular a los padres debe ir orientada a las características constructivas de casa habitación para inferir el posible vector transmisor de padecimientos:",
        "opts": ["A. Convivencia con animales o si se tiene piso de tierra (Ejemplo: enfermedad de Chagas / leishmaniasis, parásitos o zoonosis gastro y parasitosis geohelmintos).", "B. Tipo de cortinas de seda de la cocina comunal. ", "C. Relación directa de alergias a pinturas neón fluorescentes de colores oscuros hipoalergénicos", "D. Medición barométrica del aire al pie o cerca u interior de recamara y el porcentaje molecular isótopo C-14 orgánico volátil transpirable o no transpirable", "E. Diseño estético posmodernista o si es victoriana arquitectónicamente hablando en la colonia para fines neuro-estéticos parentales y su relación social inter familiar. "],
        "a": "A"
    }
]

file_path = r'C:\Users\aicil\.gemini\antigravity\scratch\Banco_Preguntas_Historia_Clinica.md'
with open(file_path, 'a', encoding='utf-8') as f:
    for idx, item in enumerate(questions2 + questions3, 21):
        f.write(f"**{idx}. {item['q']}**\n")
        for opt in item['opts']:
            f.write(f"{opt}\n")
        f.write("\n")
        f.write(f"ANSWER: {item['a']}\n")
        f.write("\n---\n\n")

print(f"Added additional 40 questions to create a full {20 + len(questions2) + len(questions3)} database.")
