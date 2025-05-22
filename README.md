# AgroSmart Decisions 🌾

## Índice
- [Introducción](#introducción)
- [Contexto y Motivación](#contexto-y-motivación)
- [Objetivos del Proyecto](#objetivos-del-proyecto)
- [Características Principales](#características-principales)
- [Arquitectura y Tecnologías](#arquitectura-y-tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Configuración](#instalación-y-configuración)
- [Guía de Uso](#guía-de-uso)
- [Detalles Técnicos](#detalles-técnicos)
- [Pruebas y Validación](#pruebas-y-validación)
- [Limitaciones y Futuras Mejoras](#limitaciones-y-futuras-mejoras)
- [Créditos y Contacto](#créditos-y-contacto)

---

## Introducción
AgroSmart Decisions es una plataforma web interactiva diseñada para proporcionar a agricultores, técnicos y cooperativas herramientas de análisis de datos avanzadas para la toma de decisiones en producción agrícola. El sistema combina datos reales sobre clima, suelo, demanda de mercado y recursos hídricos, junto con modelos de optimización y visualización, para generar recomendaciones personalizadas y sostenibles.

---

## Contexto y Motivación
El sector agrícola enfrenta múltiples retos contemporáneos, incluyendo:
- El impacto creciente del cambio climático.
- La necesidad imperante de optimizar recursos limitados, especialmente agua y tierra.
- La presión por aumentar la productividad y rentabilidad, manteniendo la sostenibilidad ambiental.
  
En este contexto, AgroSmart Decisions surge como una solución accesible que integra ciencia de datos, optimización matemática y visualización avanzada para apoyar decisiones basadas en evidencia.

---

## Objetivos del Proyecto
- Facilitar la planificación de cultivos a nivel pequeño y mediano.
- Proporcionar recomendaciones adaptadas a condiciones específicas de suelo, clima y disponibilidad hídrica.
- Optimizar el uso del terreno y maximizar beneficios económicos.
- Visualizar claramente los calendarios de siembra y cosecha.
- Ofrecer resultados exportables para su análisis posterior.
- Sentar bases para futuras expansiones hacia modelos predictivos y alertas tempranas.

---

## Características Principales
- **Selección de superficie cultivable** con preferencia entre monocultivo y multicultivo.
- **Parámetros personalizados**: ubicación geográfica, tipo de suelo, acceso al agua y flexibilidad climática.
- **Modelos de optimización** para maximizar beneficios y ajustar cultivos a las restricciones reales.
- **Visualizaciones interactivas**: calendarios anuales, treemaps de uso de suelo, gráficos comparativos.
- **Exportación directa** de resultados a Excel con formatos claros.
- **Interfaz amigable y responsiva** desarrollada en Streamlit.

---

## Arquitectura y Tecnologías
- **Lenguaje principal:** Python 3.10+
- **Framework web:** Streamlit — para desarrollo ágil de interfaces interactivas.
- **Análisis de datos:** Pandas y NumPy — para procesamiento eficiente y limpieza de datos.
- **Optimización matemática:** PuLP — para definición y resolución de problemas lineales con restricciones.
- **Visualización:** Plotly — gráficos interactivos y personalizables.
- **Gestión de archivos Excel:** OpenPyXL y XlsxWriter — para creación y descarga de informes.

---

## Estructura del Proyecto

AgroSmartDecisions/
├── app1.py # Aplicación principal (Streamlit)
├── multicultivo_module.py # Lógica y modelo para multicultivo
├── monocultivo_module.py # Lógica y modelo para monocultivo
├── agro/
│ └── data/
│ ├── cultivos_hortalizas_final.csv
│ ├── demanda_clientes.csv
│ ├── terreno_suelo_final.csv
│ └── equivalencias_provincias_clima.csv
├── requirements.txt # Dependencias y versiones recomendadas
└── README.md # Documentación detallada


---

## Instalación y Configuración

### Requisitos previos
- Python 3.10 o superior
- Acceso a línea de comandos / terminal

### Pasos de instalación

1. Clonar repositorio:
git clone https://github.com/CarlosRomanM/AgroSmartDecisions.git
cd AgroSmartDecisions


2. Crear y activar entorno virtual (recomendado):
```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

3. Instalar dependencias:
pip install -r requirements.txt



## Guía de Uso
1.Ejecutar aplicación:
streamlit run app1.py

Navegar a http://localhost:8501 en tu navegador.

####Utilizar el menú lateral para:

- Ver bienvenida e información.

- Consultar detalles del proyecto.

- Acceder al formulario para ingresar parámetros agrícolas.

#####Completar formulario con datos:

- Superficie cultivable.

- Preferencia monocultivo o multicultivo.

- Acceso a agua, tipo de suelo, ubicación.

- Opciones climáticas.

#####Generar recomendaciones y explorar resultados:

- Calendarios visuales.

- Tarjetas detalladas por cultivo.

- Gráficos comparativos.

- Descargar informes.

##### Detalles Técnicos

- La aplicación normaliza nombres de cultivos para asegurar coherencia.

- Calcula duración y ciclos anuales según datos de cada cultivo.

- Integra algoritmos de optimización lineal para asignar cultivos según restricciones reales.

- Visualiza resultados con Plotly, asegurando interactividad y claridad.

- Soporta exportación Excel con formatos amigables y datos completos.

- Implementa control de errores y advertencias para casos sin datos o incompatibilidades.

##### Pruebas y Validación:

- Se realizaron pruebas con datasets reales y simulados.

- Validación cruzada de resultados con datos históricos agrícolas.

- Verificación de la coherencia en fechas y producción estimada.

- Pruebas de usabilidad en la interfaz para garantizar fluidez y claridad.

##### Limitaciones y Futuras Mejoras:

- Actualmente no integra datos en tiempo real ni alertas climáticas.

- Falta soporte para cultivos especializados y modelos predictivos avanzados.

- Optimización basada en datos estáticos; se planea incluir Machine Learning para predicción.

- Ampliar interfaz con mapas geoespaciales y análisis de riesgos.

- Incorporar perfiles de usuario para recomendaciones más personalizadas.

#####Créditos y Contacto:

Desarrollador: Carlos Román
Email: c.roman.monje@gmail.com
GitHub: https://github.com/CarlosRomanM/CarlosRomanM


###### AgroSmart Decisions es un proyecto académico con visión real, buscando apoyar la innovación en agricultura sostenible mediante la tecnología y el análisis de datos.

¡Gracias por tu interés en AgroSmart Decisions!
Contribuciones, sugerencias y colaboraciones son bienvenidas.



