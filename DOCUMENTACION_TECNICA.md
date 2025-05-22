# Documentación Técnica - AgroSmart Decisions MVP

---

## 1. Introducción

Este documento explica en detalle la arquitectura, lógica y funcionalidades del MVP AgroSmart Decisions.  
Se pretende facilitar la comprensión del código, su estructura, flujo y la forma en que se generan las recomendaciones agrícolas personalizadas.

---

## 2. Estructura del Proyecto

- `app1.py`  
  Archivo principal que contiene la interfaz de usuario construida con Streamlit y la lógica de interacción.  
  Aquí se reciben los datos de entrada, se ejecutan los modelos y se muestran los resultados.

- `monocultivo_module.py`  
  Módulo que contiene la función para generar propuestas de monocultivo basadas en parámetros y datos agrícolas.

- `multicultivo_module.py`  
  Módulo encargado de ejecutar el modelo de optimización multicultivo, que genera recomendaciones combinadas para múltiples cultivos.

- Carpeta `/agro/data/`  
  Contiene los datasets utilizados para alimentar el modelo, como características de cultivos, demandas, tipos de suelo y equivalencias climáticas.

- Otros archivos importantes:  
  - `requirements.txt` para gestionar dependencias.  
  - `README.md` con visión general y guía rápida.  
  - `.gitignore` para evitar subir archivos no necesarios.

---

## 3. Flujo Principal en `app1.py`

1. **Configuración y estilos:**  
   Defino configuraciones de página y CSS personalizado para mejorar la experiencia visual en la interfaz.

2. **Carga de datos de apoyo:**  
   Se cargan las equivalencias de provincias y zonas climáticas desde CSV, con manejo de errores para valores por defecto.

3. **Interfaz de usuario:**  
   Se crea un menú lateral para navegar entre Inicio, Acerca de y Formulario agrícola.

4. **Formulario agrícola:**  
   El usuario introduce parámetros: superficie, tipo de suelo, acceso a agua, provincia, y si prefiere monocultivo o multicultivo.

5. **Ejecución de modelos:**  
   Dependiendo de la elección monocultivo o multicultivo, se llama a la función correspondiente:

   - Para **Multicultivo**:
     - Se importa y ejecuta `ejecutar_modelo_multicultivo` del módulo `multicultivo_module`.
     - Se recibe un dataframe con resultados, estado y beneficio.
     - Si no hay resultados, se muestra una advertencia.
     - Si hay resultados, se calcula y muestra:
       - Calendario anual estimado de siembra y cosecha (con gráfico de timeline).
       - Treemap con distribución de superficie por cultivo.
       - Cálculo de plantas estimadas basado en unidades por m².
       - Tarjetas visuales con resumen detallado de cada cultivo.
       - Gráficos comparativos y botón para descargar resultados en Excel.

   - Para **Monocultivo**:
     - Se importa y ejecuta `generar_propuestas_monocultivo` del módulo `monocultivo_module`.
     - Se normalizan nombres para evitar discrepancias.
     - Se calculan métricas derivadas como duración, ciclos por año, producción y beneficio anual y mensual.
     - Se calcula plantas estimadas.
     - Se muestra calendario anual con fechas de siembra y cosecha.
     - Se presentan tarjetas visuales con métricas por cultivo.
     - Gráfico comparativo final y botón de descarga Excel.

---

## 4. Descripción Detallada del Bloque Multicultivo

- Importo la función `ejecutar_modelo_multicultivo` que recibe los datasets y parámetros del usuario.
- El modelo devuelve un dataframe con recomendaciones optimizadas para varios cultivos, el estado de la optimización y el beneficio total anual.
- Realizo limpieza y normalización de nombres para asegurar coincidencias con los datos de duración y unidades.
- Estimo fechas de inicio y fin para cada cultivo basándome en el mes sugerido y duración del cultivo.
- Construyo un calendario visual tipo timeline con Plotly para mostrar las ventanas óptimas de siembra y cosecha.
- Creo un treemap que representa la distribución de la superficie total por cultivo para facilitar la visualización del uso del terreno.
- Calculo el número estimado de plantas necesarias usando la superficie recomendada y unidades por metro cuadrado.
- Agrupo resultados para mostrar métricas totales y promedios en tarjetas visuales, donde destaco el cultivo con mayor beneficio.
- Incluyo gráficos de barras comparativos y un botón para descargar los datos en formato Excel.
- Finalmente, muestro un resumen destacado con el beneficio total anual optimizado.

---

## 5. Descripción Detallada del Bloque Monocultivo

- Importo la función `generar_propuestas_monocultivo` que recibe los datasets y parámetros básicos.
- Normalizo nombres de cultivos para evitar errores por tildes o mayúsculas/minúsculas.
- Calculo métricas derivadas importantes: duración, ciclos por año, producción y beneficio en formatos anual y mensual.
- Calculo el número estimado de plantas, basado en superficie y unidades por metro cuadrado.
- Construyo un calendario visual con fechas de siembra y cosecha usando datos del dataset de cultivos.
- Muestro un dataframe y gráfico timeline para facilitar la visualización de las ventanas de cultivo.
- Presento tarjetas visuales para cada cultivo con detalles completos, resaltando el cultivo más rentable.
- Agrego un gráfico comparativo con barras que muestran producción y beneficio anual.
- Ofrezco opción para descargar el resultado en Excel.

---

## 6. Consideraciones Finales

- Uso intensivo de `pandas` para manipulación de datos y `plotly` para visualización interactiva.
- La modularidad del código permite actualizar o mejorar modelos sin afectar la interfaz principal.
- Implemento validaciones y mensajes de advertencia para mejorar la robustez y experiencia del usuario.
- La interfaz está diseñada para ser intuitiva, con navegación sencilla y soporte visual para facilitar la toma de decisiones agrícolas.

---

## 7. Cómo Ejecutar el Proyecto

1. Clonar el repositorio  
   ```bash
   git clone https://github.com/CarlosRomanM/AgroSmart-Decisions-MVP.git
Crear entorno virtual e instalar dependencias

bash
Copiar
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
Ejecutar la aplicación Streamlit

bash
Copiar
streamlit run app1.py
Seguir las indicaciones en la interfaz para ingresar datos y obtener recomendaciones.

8. Contacto
Para dudas, sugerencias o colaboración, contactar a:
Carlos Román — c.roman.monje@gmail.com

yaml
Copiar

---

Si quieres, puedo ayudarte a subirlo ya a tu repositorio o ayudarte a mejorarlo con capturas, diagramas o detalles extra. ¿Qué prefieres?