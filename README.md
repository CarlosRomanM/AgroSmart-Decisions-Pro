
# 🌿 AgroSmart Decisions

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-%F0%9F%93%88-red)](https://streamlit.io/)
[![Estado](https://img.shields.io/badge/Estado-En%20Desarrollo-yellow)]()
[![Licencia](https://img.shields.io/badge/Licencia-MIT-green)](LICENSE)

Plataforma inteligente de apoyo a la toma de decisiones agrícolas mediante ciencia de datos, optimización y visualización.


## 📚 Índice

- [🚀 Introducción](#-introducción)
- [🌾 Contexto y Motivación](#-contexto-y-motivación)
- [🎯 Objetivos](#-objetivos)
- [✨ Características](#-características)
- [🏗️ Arquitectura y Tecnologías](#-arquitectura-y-tecnologías)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [⚙️ Instalación](#-instalación)
- [🧪 Uso y Pruebas](#-uso-y-pruebas)
- [🛠️ Detalles Técnicos](#-detalles-técnicos)
- [🔮 Futuras Mejoras](#-futuras-mejoras)
- [👨‍💻 Autor y Contacto](#-autor-y-contacto)


---

## Introducción
AgroSmart Decisions es una plataforma web interactiva diseñada para proporcionar a agricultores, técnicos y cooperativas herramientas de análisis de datos avanzadas para la toma de decisiones en producción agrícola. El sistema combina datos reales sobre clima, suelo, demanda de mercado y recursos hídricos, junto con modelos de optimización y visualización, para generar recomendaciones personalizadas y sostenibles.



---

## 🌾 Contexto y Motivación

La agricultura moderna enfrenta desafíos como:

- Cambio climático e inestabilidad meteorológica.
- Escasez de agua y degradación de suelos.
- Necesidad de sostenibilidad con rentabilidad.

AgroSmart Decisions nace para ofrecer herramientas accesibles que combinen ciencia de datos, modelos matemáticos y visualización para transformar datos en decisiones agrícolas prácticas.

---

## 🎯 Objetivos

- 🧠 Optimizar decisiones agrícolas basadas en evidencia.
- 💧 Ajustar cultivos según tipo de suelo y disponibilidad hídrica.
- 💰 Maximizar beneficio económico con planificación mensual.
- 📊 Visualizar siembra, cosecha y rendimiento con claridad.
- 📦 Generar informes exportables para análisis posterior.
- 📦 Sentar bases para futuras expansiones hacia modelos predictivos y alertas tempranas.
---

## ✨ Características Principales

- 📍 Parámetros personalizados: ubicación, tipo de suelo, nivel de acceso al agua y flexibilidad 
     climática.
- 🌱 Selección entre **monocultivo** o **multicultivo** según preferencia del usuario.
- 🧠 Modelos de optimización que asignan automáticamente los cultivos más adecuados.
- 📐 Distribución inteligente de cultivos sobre la superficie disponible (modo multicultivo), mes a 
     mes.
- 📅 Visualización de calendarios anuales de siembra y cosecha.
- 🪴 Tarjetas con métricas clave por cultivo: producción, beneficio, duración, superficie, número de 
     plantas, etc.
- 📊 Gráficos interactivos: comparativos, treemaps de uso del terreno, barras y más.
- 📤 Exportación de resultados optimizados a Excel con formato profesional.
- 🌐 Interfaz intuitiva y responsiva desarrollada con Streamlit.

---

## 🏗️ Arquitectura y Tecnologías
- **Lenguaje principal:** Python 3.10+
- **Framework web:** Streamlit — para desarrollo ágil de interfaces interactivas.
- **Análisis de datos:** Pandas y NumPy — para procesamiento eficiente y limpieza de datos.
- **Optimización matemática:** PuLP — para definición y resolución de problemas lineales con restricciones.
- **Visualización:** Plotly — gráficos interactivos y personalizables.
- **Gestión de archivos Excel:** OpenPyXL y XlsxWriter — para creación y descarga de informes.

---

## 📁 Estructura del Proyecto

AgroSmart-Decisions-Pro/
├── app1.py # Aplicación principal Streamlit
├── app/
│ ├── monocultivo_module.py # Lógica para modo monocultivo
│ └── multicultivo_module.py # Lógica para modo multicultivo
├── agro/
│ └── data/ # Datasets agrícolas y de usuario
│ ├── cultivos_hortalizas_final.csv
│ ├── demanda_clientes.csv
│ ├── terreno_suelo_final.csv
│ └── equivalencias_provincias_clima.csv
├── images/ # Logotipos, íconos y banners
├── notebooks/ # Pruebas y experimentación
├── requirements.txt
├── runtime.txt
├── README.md
└── LICENSE


---
## ⚙️ Instalación

### Requisitos
- Python 3.10 o superior
- Git

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/CarlosRomanM/AgroSmart-Decisions-Pro.git
cd AgroSmart-Decisions-Pro

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt


---

### ✅ 10. **Uso de la Aplicación**

```markdown
## 🚀 Uso de la Aplicación

```bash
streamlit run app1.py

## Instalación y Configuración

### Requisitos previos
- Python 3.10 o superior
- Acceso a línea de comandos / terminal

Luego:
Abre http://localhost:8501

Completa el formulario con parámetros agrícolas.

Explora las recomendaciones, visualizaciones y exporta resultados.


---

### ✅ 11. **Detalles Técnicos**

```markdown
## 🛠️ Detalles Técnicos

- Validación de cultivos según suelo, agua y clima.
- Cálculo de ciclos anuales según duración de cultivo.
- Rotación mensual del terreno en multicultivo mediante restricciones.
- Visualización personalizada: cards, calendarios, gráficos interactivos.
- Exportación automatizada a Excel con formato y timestamp.
- Estructura modular (`app/`) para mantener el código limpio y escalable.

--

## 🧪 Pruebas y Validación

- Pruebas de datos reales y simulados para diversos perfiles agrícolas.
- Comparación de beneficios estimados con métricas manuales.
- Validación de restricciones (agua, clima, superficie).
- Comprobación de consistencia visual y funcionamiento de descarga.

--

## 🔮 Futuras Mejoras

- 🌦️ Integración con APIs meteorológicas en tiempo real.
- 🧠 Modelos predictivos con Machine Learning.
- 🗺️ Visualizaciones geoespaciales con mapas interactivos.
- 🧑‍🌾 Perfiles de usuario (experiencia, preferencias, alertas).
- 🧩 Simulación de escenarios agrícolas a largo plazo.

--

## 👨‍💻 Autor y Contacto

Desarrollado por **Carlos Román**

- 📧 c.roman.monje@gmail.com  
- 💼 [GitHub](https://github.com/CarlosRomanM/CarlosRomanM)  
- 🌱 Proyecto académico a través de Evolve Academy con una visión real y futura expansión profesional, 
     buscando apoyar la innovación en agricultura sostenible mediante la tecnología y el análisis de 
     datos.

### Agradecimientos
Quiero expresar mi sincero agradecimiento a todas las personas y entidades que han contribuido 
de forma directa o indirecta al desarrollo de este proyecto.
A la cooperativa Brot Agrològic y a la cooperativa La Rural de Collserola, por compartir su experiencia y visión sobre la agricultura sostenible y de proximidad.
A José Antonio Domínguez, agricultor de la zona, por su tiempo, disposición y valiosas aportaciones desde la práctica real del cultivo.
Y, muy especialmente, a todo el equipo de Evolve Academy por su acompañamiento y formación durante todo el proceso. En particular, a Julio Valero, por su dedicación constante, su guía clara y su implicación personal para ayudarme a llevar esta idea hasta convertirse en un MVP funcional.

Gracias a todos por haber sembrado, junto a mí, esta primera cosecha digital.

¡Gracias por visitar AgroSmart Decisions!  
Contribuciones y sugerencias son siempre bienvenidas.



