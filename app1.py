import streamlit as st
import pandas as pd
import base64
import numpy as np
import io
from datetime import datetime, timedelta
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, value, LpBinary, PULP_CBC_CMD
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go


# -------------------------------
# Configuración general de página
# -------------------------------
st.set_page_config(page_title="AgroSmart Decisions", layout="wide")

# -------------------------------
# CSS personalizado para sidebar y expanders
# -------------------------------
custom_styles = """
<style>
[data-testid="stSidebar"] > div:first-child {
    background-color: #AABFA4;
    padding: 2rem 1rem 1rem 1rem;
}
.sidebar-logo {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 1.5rem;
}
.sidebar-logo img {
    max-width: 280px;
    height: auto;
}
div[data-testid="stExpander"] {
    border: 2px solid #AABFA4;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 1em;
}
div[data-testid="stExpander"] > details > summary {
    background-color: #AABFA4 !important;
    color: black !important;
    font-weight: bold;
    padding: 0.75em 1em;
    font-size: 1.05em;
}
div[data-testid="stExpander"] > details > div {
    background-color: #f1f7ef !important;
    padding: 1em;
}
</style>
"""
st.markdown(custom_styles, unsafe_allow_html=True)

# -------------------------------
# Mostrar logo en el sidebar
# -------------------------------
def mostrar_logo_sidebar(ruta):
    with open(ruta, "rb") as f:
        imagen_base64 = base64.b64encode(f.read()).decode()
    logo_html = f"""
    <div class='sidebar-logo'>
        <img src="data:image/png;base64,{imagen_base64}" 
             alt="Logo AgroSmart"
             style="max-width: 180px; height: auto;">
    </div>
    """
    st.sidebar.markdown(logo_html, unsafe_allow_html=True)

mostrar_logo_sidebar("solo_logo1.png")

# -------------------------------
# Cargar equivalencias de provincias
# -------------------------------
try:
    equivalencias = pd.read_csv("agro/data/equivalencias_provincias_clima.csv")
    equivalencias.columns = equivalencias.columns.str.strip()
    provincias_disponibles = sorted(equivalencias["Provincia_usuario"].dropna().unique().tolist())
    provincia_equivalencias = dict(zip(equivalencias["Provincia_usuario"].str.strip(), equivalencias["Provincia_equivalente"].str.strip()))
    provincia_zonaclimatica = dict(zip(equivalencias["Provincia_usuario"].str.strip(), equivalencias["Zona_climatica"].str.strip().str.lower()))
except Exception as e:
    provincias_disponibles = ["Navarra", "Murcia", "Lleida"]
    provincia_equivalencias = {prov: prov for prov in provincias_disponibles}
    provincia_zonaclimatica = {prov: "mediterraneo" for prov in provincias_disponibles}
    st.warning(f"⚠️ No se pudo cargar el archivo de equivalencias. Usando valores por defecto. Detalle: {e}")

# -------------------------------
# Navegación lateral
# -------------------------------
menu = st.sidebar.radio("Navegacion", ["Inicio", "Acerca de", "Formulario Agricola Usuario"])

# -------------------------------
# Mostrar logo principal centrado
# -------------------------------
with open("logo_transp_verde.png", "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()

st.markdown(f"""
    <div style='
        display: flex;
        justify-content: center;
        align-items: center;
        height: 240px;
        margin-top: -4rem;
        margin-bottom: 0.5rem;
    '>
        <img src="data:image/png;base64,{logo_base64}"
             alt="AgroSmart Decisions"
             style="max-width: 500px; height: auto;">
    </div>
""", unsafe_allow_html=True)


# -------------------------------
# Contenido dinámico
# -------------------------------
if menu == "Inicio":
    st.subheader("🌱 ¡Bienvenido agricultor del futuro!")
    st.write("Selecciona una sección en el menú lateral para:")



    # Imagen portada con marco verde
    def mostrar_imagen_con_marco_verde(ruta_imagen, caption=""):
        with open(ruta_imagen, "rb") as f:
            img_bytes = f.read()
            encoded = base64.b64encode(img_bytes).decode()

        st.markdown(f"""
        <div style="padding: 1rem; background-color: #AABFA4; border-radius: 16px;
                    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
                    text-align: center; margin-top: 2rem; margin-bottom: 2rem;">
            <img src="data:image/png;base64,{encoded}" style="max-width: 100%; height: auto; border-radius: 8px;">
            <p style="color: #ffffff; font-size: 1.1em; margin-top: 0.5rem;">{caption}</p>
        </div>
        """, unsafe_allow_html=True)

    mostrar_imagen_con_marco_verde("PORTADA_AGRO.png", caption="Cultivos en campo abierto")

elif menu == "Acerca de":
    st.subheader("📘 Sobre AgroSmart Decisions")
    st.markdown("""
    <p style='font-size: 1.1em;'>
        <strong>AgroSmart Decisions</strong> es una herramienta innovadora desarrollada con el objetivo de empoderar a agricultores, técnicos y cooperativas a través del análisis inteligente de datos. 
        En un contexto marcado por el cambio climático, la escasez de recursos y la necesidad de producir de manera más eficiente, AgroSmart ofrece un enfoque práctico y accesible para la toma de decisiones agrícolas.
    </p>

    <p style='font-size: 1.1em;'>
        Esta aplicación integra información real y actualizada sobre condiciones climáticas, características del suelo, demanda del mercado y disponibilidad de recursos como el agua y la maquinaria. 
        A través de algoritmos de optimización y análisis de datos, permite a los usuarios recibir recomendaciones de cultivo personalizadas y basadas en evidencia.
    </p>

    <ul style='padding-left: 1.2em; font-size: 1.05em;'>
        <li>📊 <strong>Análisis y procesamiento de datos agrícolas</strong></li>
        <li>🌾 <strong>Recomendaciones personalizadas según condiciones reales</strong></li>
        <li>💧 <strong>Optimización del uso del agua y recursos</strong></li>
        <li>🧠 <strong>Modelos inteligentes para maximizar beneficios</strong></li>
        <li>📥 <strong>Exportación de informes personalizables</strong></li>
    </ul>

    <p style='font-size: 1.05em;'>
        AgroSmart Decisions nace como un proyecto académico con vocación real. Su diseño modular y escalable permite integrarlo en múltiples contextos regionales o productivos.
    </p>

    <hr style='border: 1px solid #AABFA4; margin-top: 2em; margin-bottom: 1em;'>

    <h4 style='color: #4E5B48;'>📬 Contacto</h4>
    <p style='font-size: 1em;'>
        ¿Tienes dudas, sugerencias o deseas colaborar?<br>
        Puedes escribirme a: <strong>c.roman.monje@gmail.com</strong><br>
        También puedes seguir el proyecto en 
        <a href='https://github.com/CarlosRomanM/CarlosRomanM' target='_blank' style='color:#4E5B48; text-decoration: underline;'>GitHub</a>
    </p>
    """, unsafe_allow_html=True)


if menu == "Formulario Agricola Usuario":
    st.subheader("Formulario del Usuario Agrícola")
    st.markdown("Introduce los siguientes datos para generar recomendaciones:")

    with st.expander("📏 Superficie y tipo de cultivo", expanded=True):
        superficie_ha = st.number_input(
            "Superficie total (ha)",
            min_value=0.1,
            max_value=10.0,
            step=0.1,
            value=0.5
        )
        cultivo_unico = st.radio("¿Preferencia por monocultivo o multicultivo?", ["Monocultivo", "Multicultivo"])

    with st.expander("🚰 Condiciones de agua", expanded=True):
        acceso_agua = st.selectbox("Acceso a agua", ["bajo", "medio", "alto"])

    with st.expander("📍 Ubicación y suelo", expanded=True):
        provincia = st.selectbox("Provincia", provincias_disponibles)
        provincia_equiv = provincia_equivalencias.get(provincia)
        tipo_suelo = st.selectbox("Tipo de suelo", ["franco", "arcilloso", "arenoso", "franco-arcilloso", "franco-arenoso"])

    

    modo_flexible = st.checkbox("¿Permitir recomendaciones fuera de tu zona climática?", value=False)
    zona_climatica = provincia_zonaclimatica.get(provincia, "mediterraneo")



    if st.button("Generar recomendaciones"):
        st.session_state["recomendaciones_generadas"] = True
        st.success("Datos guardados correctamente. Recomendaciones disponibles más abajo.")

    # Asegurarse que se haya generado antes de mostrar resultados
    if st.session_state.get("recomendaciones_generadas"):
        # Aquí va todo lo que ya tienes:
        # ejecutar modelo, mostrar calendario, tarjetas, gráficos, treemap...


        st.markdown(f"""
        <div style='
            border: 2px solid #AABFA4;
            border-radius: 12px;
            padding: 1.5em;
            background-color: #f9fdf7;
            margin-bottom: 1.5em;'>
            <h4 style='color: #4E5B48;'>🌿 Parámetros del usuario</h4>
            <ul style='list-style-type: none; padding-left: 0; font-size: 1.1em;'>
                <li><strong>Provincia:</strong> {provincia}</li>
                <li><strong>Tipo de suelo:</strong> {tipo_suelo}</li>
                <li><strong>Superficie:</strong> {superficie_ha} ha</li>
                <li><strong>Opción de cultivo:</strong> {cultivo_unico}</li>
                <li><strong>Zona climática:</strong> {zona_climatica}</li>
                <li><strong>Filtro climático flexible:</strong> {'Sí' if modo_flexible else 'No'}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        cultivos_df = pd.read_csv("/Users/kardiahq/Desktop/33.final_proyect/agro/data/cultivos_hortalizas_final.csv")
        demanda_df = pd.read_csv("/Users/kardiahq/Desktop/33.final_proyect/agro/data/demanda_clientes.csv")
        terreno_df = pd.read_csv("/Users/kardiahq/Desktop/33.final_proyect/agro/data/terreno_suelo_final.csv")
        cultivos_df["Rendimiento_kg_m2"] = cultivos_df["Rendimiento_promedio (kg/ha)"].fillna(0) / 10000

        # Activar o desactivar modo depuración
        modo_debug = False  # Cambiar a True si quieres ver los mensajes internos

  # ===============================  # ===============================  # ===============================  # ===============================
        
        if cultivo_unico == "Multicultivo":
            from multicultivo_module import ejecutar_modelo_multicultivo
            df_resultados, estado, beneficio = ejecutar_modelo_multicultivo(
                cultivos_df, demanda_df, terreno_df,
                superficie_ha, tipo_suelo, acceso_agua,
                provincia_equiv, zona_climatica,
                modo_flexible,
                debug=modo_debug  # 👈 Pasa el valor del flag
            )

            if df_resultados is None or df_resultados.empty:
                st.warning("⚠️ No hay cultivos que coincidan con tus condiciones actuales o el modelo no encontró solución óptima.")
            else:
                # 🔍 Mensajes técnicos solo si modo_debug está activado
                if modo_debug:
                    st.markdown("🔍 Iniciando modelo multicultivo...")
                    st.markdown(f"🌦️ Zona climática asignada: {zona_climatica}")
                    st.markdown(f"💧 Nivel de agua del usuario: {acceso_agua}")
                    st.markdown(f"📌 Estado del modelo: {estado}")
                    st.markdown(f"💰 Beneficio total anual optimizado: € {beneficio:,.2f}")

                # Aquí continúa el resto de tu flujo: calendario, tarjetas, resumen, treemap...

                # ===============================

                # Calendario estimado de siembra y cosecha
                st.markdown("### 🗓️ Calendario estimado anual de siembra y cosecha")

                cultivos_df["Nombre_cultivo"] = cultivos_df["Nombre_cultivo"].str.strip().str.lower()
                df_resultados["Cultivo"] = df_resultados["Cultivo"].str.strip().str.lower()

                df_duracion = cultivos_df.set_index("Nombre_cultivo")["Duración_cultivo_días"].to_dict()
                df_resultados["Duracion_dias"] = df_resultados["Cultivo"].map(df_duracion)

                def estimar_inicio(mes):
                    try:
                        return datetime(2025, int(mes), 1)
                    except:
                        return pd.NaT

                df_resultados["Inicio"] = df_resultados["Mes"].apply(estimar_inicio)
                df_resultados["Fin"] = df_resultados.apply(
                    lambda row: row["Inicio"] + timedelta(days=int(row["Duracion_dias"])) if pd.notnull(row["Inicio"]) else pd.NaT,
                    axis=1
                )

                calendario_multi = df_resultados.dropna(subset=["Inicio", "Fin"])[["Cultivo", "Inicio", "Fin"]].copy()
                calendario_multi["Cultivo"] = calendario_multi["Cultivo"].str.capitalize()
                calendario_multi = calendario_multi.sort_values("Inicio")

                if not calendario_multi.empty:
                    fig2 = px.timeline(
                        calendario_multi,
                        x_start="Inicio",
                        x_end="Fin",
                        y="Cultivo",
                        color="Cultivo",
                        title="Calendario anual Multicultivo"
                    )
                    fig2.update_yaxes(autorange="reversed")
                    fig2.update_layout(height=420, margin=dict(l=0, r=0, t=50, b=0))
                    st.plotly_chart(fig2, use_container_width=True)

                    calendario_mostrar = calendario_multi.copy()
                    calendario_mostrar["Inicio"] = calendario_mostrar["Inicio"].dt.strftime("%d/%m")
                    calendario_mostrar["Fin"] = calendario_mostrar["Fin"].dt.strftime("%d/%m")

                    st.markdown("### 📅 Fechas de siembra y cosecha ", unsafe_allow_html=True)
                    st.markdown("#####  Recomendación de fechas válidas ", unsafe_allow_html=True)
                    st.markdown("""
                        <style>
                        thead tr th {
                            background-color: #AABFA4;
                            color: #1e1e1e;
                            font-weight: bold;
                            text-align: center;
                        }
                        tbody tr td {
                            text-align: center;
                        }
                        </style>
                    """, unsafe_allow_html=True)
                    st.dataframe(calendario_mostrar, use_container_width=True)
                else:
                    st.warning("⚠️ No se pudieron estimar fechas para los cultivos seleccionados.")
                
                # 🌾 Visualización de uso del terreno (Treemap)
                # ===============================
                st.markdown("### 🌾 Visualización de uso del terreno por cultivo")

                import plotly.express as px

                # Agrupamos superficie por cultivo desde el df_resultados
                superficie_por_cultivo = df_resultados.groupby("Cultivo")["Superficie_ha"].sum().reset_index()
                superficie_por_cultivo["Cultivo"] = superficie_por_cultivo["Cultivo"].str.capitalize()

                # Creamos el treemap
                fig_treemap = px.treemap(
                    superficie_por_cultivo,
                    path=["Cultivo"],
                    values="Superficie_ha", 
                    color="Superficie_ha",
                    color_continuous_scale="Greens",
                    title="🧭 Distribución de la superficie total por cultivo."
                )

                fig_treemap.update_traces(textinfo="label+value+percent entry")
                fig_treemap.update_layout(margin=dict(t=50, l=10, r=10, b=10))

                # Mostramos el gráfico
                st.plotly_chart(fig_treemap, use_container_width=True, key="grafico_treemap")

                resumen = df_resultados.groupby("Cultivo").agg(
                    Total_kg=("Cantidad_kg", "sum"),
                    Total_beneficio=("Beneficio_€", "sum"),
                    Total_superficie_ha=("Superficie_ha", "sum"),
                    Duracion_dias=("Duracion_dias", "mean")
                ).reset_index()

                # ===============================
                # 🪴 Recomendaciones visuales por cultivo (Multicultivo)
                # ===============================
                st.markdown("### 🪴 Resultados personalizados por cultivo")
                st.markdown("#####  🎋 Tarjetas de cultivo ")
               
                iconos_por_cultivo = {
                    "Tomate": "🍅", "Lechuga": "🥬", "Zanahoria": "🥕", "Cebolla": "🧅", "Ajo": "🧄", "Pimiento": "🌶️",
                    "Pepino": "🥒", "Calabacín": "🥒", "Berenjena": "🍆", "Espinaca": "🥬", "Repollo": "🥬", "Brócoli": "🥦",
                    "Coliflor": "🥦", "Alcachofa": "🥬", "Guisante": "🌱", "Habas": "🌱", "Nabo": "🌰", "Rábano": "🌰",
                    "Apio": "🥬", "Remolacha": "🫒", "Judía verde": "🌿", "Escarola": "🥬", "Endivia": "🥬", "Acelga": "🥬",
                    "Col rizada": "🥬", "Pepinillo": "🥒", "Puerro": "🧅", "Bledo": "🌿", "Mostaza verde": "🌿", "Berro": "🌿",
                    "Acelga de verano": "🥬", "Achicoria": "🥬", "Berza": "🥬", "Canónigos": "🥬", "Cardo": "🌿",
                    "Coles de Bruselas": "🥬", "Mizuna": "🌿", "Pak Choi": "🥬", "Rúcula": "🌿"
                }

                cultivo_top = resumen.loc[resumen["Total_beneficio"].idxmax(), "Cultivo"]
                n_col = 4
                filas = [resumen[i:i + n_col] for i in range(0, resumen.shape[0], n_col)]

                for fila in filas:
                    cols = st.columns(len(fila))
                    for i, (_, row) in enumerate(fila.iterrows()):
                        cultivo = row["Cultivo"].capitalize()
                        icono = iconos_por_cultivo.get(cultivo, "🌿")
                        estrella = " ⭐" if cultivo == cultivo_top else ""
                        duracion = int(row["Duracion_dias"]) if not pd.isna(row["Duracion_dias"]) else 90
                        ciclos = int(365 / duracion)
                        produccion_mensual = row["Total_kg"] / 12
                        beneficio_mensual = row["Total_beneficio"] / 12

                        with cols[i]:
                            st.markdown(f"""
                            <div style="background-color: #B0C8B4; border: 3px solid #2f4030; border-radius: 16px; padding: 1.2rem; color: white; text-align: center;
                                        box-shadow: 1px 1px 6px rgba(0,0,0,0.1); height: 580px; font-family: 'Segoe UI', sans-serif;">
                            <div style='font-size: 1.2rem;'>{icono}{estrella}</div>
                            <h4 style="margin: 0.5rem 0 0.8rem;">{cultivo}</h4>
                            <div style="margin-bottom: 0.6rem;">
                                <p style="margin-bottom: 0.2rem; color: #2f4030; font-weight: bold;">Duración del ciclo</p>
                                <p>{duracion} días</p>
                            </div>
                            <div style="margin-bottom: 0.6rem;">
                                <p style="margin-bottom: 0.2rem; color: #2f4030; font-weight: bold;">Ciclos por año</p>
                                <p>{ciclos}</p>
                            </div>
                            <div style="margin-bottom: 0.6rem;">
                                <p style="margin-bottom: 0.2rem; color: #2f4030; font-weight: bold;">Producción mensual</p>
                                <p>{produccion_mensual:,.0f} kg</p>
                            </div>
                            <div style="margin-bottom: 0.6rem;">
                                <p style="margin-bottom: 0.2rem; color: #2f4030; font-weight: bold;">Producción total</p>
                                <p>{row['Total_kg']:,.0f} kg</p>
                            </div>
                            <div style="margin-bottom: 0.6rem;">
                                <p style="margin-bottom: 0.2rem; color: #2f4030; font-weight: bold;">Beneficio mensual</p>
                                <p>€ {beneficio_mensual:,.2f}</p>
                            </div>
                            <div>
                                <p style="margin-bottom: 0.2rem; color: #2f4030; font-weight: bold;">Beneficio Anual</p>
                                <p>€ {row['Total_beneficio']:,.2f}</p>
                            </div>
                            </div>
                            """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

                # ===============================
                # Gráfico de resumen por cultivo
                # ===============================
                st.markdown("### 📊 Datos Obtenidos por cultivo")
                st.dataframe(resumen, use_container_width=True)

                st.markdown("### 📊 Comparativa visual por cultivo")

                resumen_melted = resumen.melt(id_vars="Cultivo", value_vars=["Total_kg", "Total_beneficio"])
                fig_resumen = px.bar(
                    resumen_melted,
                    x="Cultivo",
                    y="value",
                    color="variable",
                    barmode="group",
                    title="Representación por cultivo"
                )
                fig_resumen.update_layout(xaxis_title="Cultivo", yaxis_title="Valor", height=420)
                st.plotly_chart(fig_resumen, use_container_width=True)

                output = io.BytesIO()
                nombre_archivo = f"recomendacion_multicultivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df_resultados.to_excel(writer, index=False, sheet_name="Multicultivo")
                st.download_button(
                    label="🗓️ Descargar resultados en Excel",
                    data=output.getvalue(),
                    file_name=nombre_archivo,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                st.markdown(f"""
                <div style='
                    background-color: #DCEFD9;
                    border: 2px solid #37572F;
                    border-radius: 10px;
                    padding: 1.2rem;
                    text-align: center;
                    font-size: 1.4em;
                    font-weight: bold;
                    color: #2f4030;
                    box-shadow: 1px 2px 6px rgba(0,0,0,0.1);'>

                💰 Beneficio total anual optimizado: € {beneficio:,.2f}
                </div>
                """, unsafe_allow_html=True)

 # =============================== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====                

        elif cultivo_unico == "Monocultivo":
            from monocultivo_module import generar_propuestas_monocultivo
            df_monocultivo = generar_propuestas_monocultivo(
                cultivos_df, demanda_df, terreno_df, superficie_ha
            )

            st.markdown("## 🌾 Propuestas de monocultivo más rentables")

            if df_monocultivo is None or df_monocultivo.empty:
                st.warning("⚠️ No se encontraron cultivos válidos para monocultivo con las condiciones actuales.")
            else:
                # Normalizar nombres de cultivos para garantizar coincidencias
                import unicodedata
                def quitar_tildes(texto):
                    if isinstance(texto, str):
                        return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
                    return texto

                cultivos_df["Nombre_cultivo"] = cultivos_df["Nombre_cultivo"].str.strip().str.lower().apply(quitar_tildes)
                df_monocultivo["Cultivo"] = df_monocultivo["Cultivo"].str.strip().str.lower().apply(quitar_tildes)

                # Duración del ciclo y métricas derivadas
                if "Duración del ciclo (días)" not in df_monocultivo.columns:
                    if "Duración_cultivo_días" in cultivos_df.columns:
                        duraciones = cultivos_df.set_index("Nombre_cultivo")["Duración_cultivo_días"].to_dict()
                        df_monocultivo["Duración del ciclo (días)"] = df_monocultivo["Cultivo"].map(duraciones)
                    else:
                        st.warning("⚠️ No se encontró la columna 'Duración_cultivo_días'. Se usará 90 días por defecto.")
                        df_monocultivo["Duración del ciclo (días)"] = 90

                    df_monocultivo["Ciclos por año"] = (365 / df_monocultivo["Duración del ciclo (días)"]).apply(np.floor).astype(int)
                    df_monocultivo["Producción total anual (kg)"] = df_monocultivo["Producción (kg)"] * df_monocultivo["Ciclos por año"]
                    df_monocultivo["Beneficio total anual (€)"] = df_monocultivo["Beneficio estimado (€)"] * df_monocultivo["Ciclos por año"]
                    df_monocultivo["Producción mensual promedio (kg)"] = df_monocultivo["Producción total anual (kg)"] / 12
                    df_monocultivo["Beneficio mensual promedio (€)"] = df_monocultivo["Beneficio total anual (€)"] / 12

                # Calcular Plantas estimadas
                if "Unidades_m2" in cultivos_df.columns:
                    unidades_dict = cultivos_df.set_index("Nombre_cultivo")["Unidades_m2"].to_dict()
                    df_monocultivo["Unidades_m2"] = df_monocultivo["Cultivo"].map(unidades_dict)
                    df_monocultivo["Plantas estimadas"] = (df_monocultivo["Superficie (ha)"] * 10000 * df_monocultivo["Unidades_m2"]).astype(int)
                else:
                    st.warning("⚠️ No se encontró la columna 'Unidades_m2'. No se puede calcular plantas estimadas.")
                    df_monocultivo["Plantas estimadas"] = 0


                # =======================
                # Calendario visual monocultivo
                # =======================
                st.markdown("### 📅 Fechas de siembra y cosecha")

                def convertir_fecha(fecha_texto, año_base=2025):
                    try:
                        if isinstance(fecha_texto, str):
                            fecha_texto = fecha_texto.strip().replace("/", "-")
                            dia, mes = map(int, fecha_texto.split("-"))
                            return datetime(año_base, mes, dia)
                    except:
                        return pd.NaT
                    return pd.NaT

                cultivos_df["Nombre_cultivo"] = cultivos_df["Nombre_cultivo"].str.strip().str.lower()
                df_monocultivo["Cultivo"] = df_monocultivo["Cultivo"].str.strip().str.lower()

                cultivos_df["Fecha_siembra"] = cultivos_df["Fecha_siembra"].astype(str).str.strip()
                cultivos_df["Fecha_cosecha"] = cultivos_df["Fecha_cosecha"].astype(str).str.strip()
                cultivos_df["Fecha_siembra_dt"] = cultivos_df["Fecha_siembra"].apply(convertir_fecha)
                cultivos_df["Fecha_cosecha_dt"] = cultivos_df["Fecha_cosecha"].apply(convertir_fecha)

                cultivos_usados = df_monocultivo["Cultivo"].unique()
                df_calendario = cultivos_df[cultivos_df["Nombre_cultivo"].isin(cultivos_usados)].copy()
                df_calendario = df_calendario[["Nombre_cultivo", "Fecha_siembra_dt", "Fecha_cosecha_dt"]]
                df_calendario.columns = ["Cultivo", "Inicio", "Fin"]
                df_calendario = df_calendario.dropna()


                
                df_mostrar = df_calendario.copy()
                df_mostrar["Inicio"] = df_mostrar["Inicio"].dt.strftime("%d/%m")
                df_mostrar["Fin"] = df_mostrar["Fin"].dt.strftime("%d/%m")
                st.markdown("""
                    <style>
                    thead tr th {
                        background-color: #AABFA4;
                        color: #1e1e1e;
                        font-weight: bold;
                        text-align: center;
                    }
                    tbody tr td {
                        text-align: center;
                    }
                    </style>
                """, unsafe_allow_html=True)
                st.dataframe(df_mostrar)

                st.markdown("### 📅 Calendario anual de siembra y cosecha")
                if not df_calendario.empty:
                    fig = px.timeline(
                        df_calendario,
                        x_start="Inicio",
                        x_end="Fin",
                        y="Cultivo",
                        color="Cultivo",
                        title="Calendario anual Monocultivo",
                    )
                    fig.update_yaxes(autorange="reversed")
                    fig.update_layout(height=420, margin=dict(l=0, r=0, t=50, b=0))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ No se encontraron cultivos con fechas válidas para mostrar el calendario.")

                output_mono = io.BytesIO()
                nombre_archivo_mono = f"recomendacion_monocultivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                with pd.ExcelWriter(output_mono, engine="xlsxwriter") as writer:
                    df_monocultivo.to_excel(writer, index=False, sheet_name="Monocultivo")

                st.download_button(
                    label="📥 Descargar resultados en Excel",
                    data=output_mono.getvalue(),
                    file_name=nombre_archivo_mono,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )


                st.markdown("## 🪴 Recomendaciones visuales por cultivo")
                st.markdown("##### 🎋 Tarjetas de cultivo")
                iconos_por_cultivo = {
                    "Tomate": "🍅", "Lechuga": "🥬", "Zanahoria": "🥕", "Cebolla": "🧅", "Ajo": "🧄", "Pimiento": "🌶️",
                    "Pepino": "🥒", "Calabacín": "🥒", "Berenjena": "🍆", "Espinaca": "🥬", "Repollo": "🥬", "Brócoli": "🥦",
                    "Coliflor": "🥦", "Alcachofa": "🥬", "Guisante": "🌱", "Habas": "🌱", "Nabo": "🌰", "Rábano": "🌰",
                    "Apio": "🥬", "Remolacha": "🫒", "Judía verde": "🌿", "Escarola": "🥬", "Endivia": "🥬", "Acelga": "🥬",
                    "Col rizada": "🥬", "Pepinillo": "🥒", "Puerro": "🧅", "Bledo": "🌿", "Mostaza verde": "🌿", "Berro": "🌿",
                    "Acelga de verano": "🥬", "Achicoria": "🥬", "Berza": "🥬", "Canónigos": "🥬", "Cardo": "🌿",
                    "Coles de Bruselas": "🥬", "Mizuna": "🌿", "Pak Choi": "🥬", "Rúcula": "🌿"
                }

                cultivo_top = df_monocultivo.loc[df_monocultivo["Beneficio total anual (€)"].idxmax(), "Cultivo"]
                n_col = 4
                rows = [df_monocultivo[i:i + n_col] for i in range(0, df_monocultivo.shape[0], n_col)]

                for fila in rows:
                    cols = st.columns(len(fila))
                    for i, (_, row) in enumerate(fila.iterrows()):
                        cultivo = row["Cultivo"]
                        icono = iconos_por_cultivo.get(cultivo, "🌿")
                        estrella = " ⭐" if cultivo == cultivo_top else ""

                        with cols[i]:
                            st.markdown(f"""
                            <div style="background-color: #AABFA4; border: 3px solid #2f4030; border-radius: 16px; padding: 1.2rem; color: white; text-align: center;
                                        box-shadow: 1px 1px 6px rgba(0,0,0,0.1); height: 650px; font-family: 'Segoe UI', sans-serif;">

                            <div style='font-size: 1.2rem;'>{icono}{estrella}</div>
                            <h4 style="margin: 0.5rem 0 0.8rem;">{cultivo}</h4>

                            <div style="margin-bottom: 0.6rem;">
                                <p style="margin-bottom: 0.2rem; color: #2f4030; font-weight: bold;">Duración del ciclo</p>
                                <p>{int(row['Duración del ciclo (días)'])} días</p>
                            </div>
                            <div style="margin-bottom: 0.6rem;">
                                <p style="margin-bottom: 0.2rem; color: #2f4030; font-weight: bold;">Ciclos por año</p>
                                <p>{int(row['Ciclos por año'])}</p>
                            </div>
                            <div style="margin-bottom: 0.6rem;">
                                <p style="margin-bottom: 0.2rem; color: #2f4030; font-weight: bold;">Plantas estimadas</p>
                                <p>{int(row.get('Plantas estimadas', 0)):,} unidades</p>
                            </div>
                            <div style="margin-bottom: 0.6rem;">
                                <p style="margin-bottom: 0.2rem; color: #2f4030; font-weight: bold;">Producción mensual</p>
                                <p>{row['Producción mensual promedio (kg)']:,.0f} kg</p>
                            </div>
                            <div style="margin-bottom: 0.6rem;">
                                <p style="margin-bottom: 0.2rem; color: #2f4030; font-weight: bold;">Producción total</p>
                                <p>{row['Producción total anual (kg)']:,.0f} kg</p>
                            </div>
                            <div style="margin-bottom: 0.6rem;">
                                <p style="margin-bottom: 0.2rem; color: #2f4030; font-weight: bold;">Beneficio mensual</p>
                                <p>€ {row['Beneficio mensual promedio (€)']:,.2f}</p>
                            </div>
                            <div>
                                <p style="margin-bottom: 0.2rem; color: #2f4030; font-weight: bold;">Beneficio Anual</p>
                                <p>€ {row['Beneficio total anual (€)']:,.2f}</p>
                            </div>
                            </div>
                            """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

                

        # === Gráfico resumen agregado al final ===
                st.markdown("### 📊 Comparativa visual por cultivo")
                resumen_mono = df_monocultivo[[
                    "Cultivo", 
                    "Producción total anual (kg)", 
                    "Beneficio total anual (€)", 
                   
                ]].copy()

                resumen_melted = resumen_mono.melt(
                    id_vars="Cultivo", 
                    value_vars=[
                        "Producción total anual (kg)", 
                        "Beneficio total anual (€)", 
                       
                    ],
                    var_name="Variable", 
                    value_name="Valor"
                )

                fig_resumen_mono = px.bar(
                    resumen_melted,
                    x="Cultivo",
                    y="Valor",
                    color="Variable",
                    barmode="group",
                    title=" Cultivos monocultivos"
                )

                fig_resumen_mono.update_layout(
                    xaxis_title="Cultivo",
                    yaxis_title="Valor",
                    height=420,
                    plot_bgcolor='#F2F7F1',      # Fondo igual que el sidebar
                    paper_bgcolor='#F2F7F1',     # También el lienzo externo
                    font=dict(color="#2f4030"),
                    margin=dict(l=0, r=0, t=50, b=0)
                )

                st.plotly_chart(fig_resumen_mono, use_container_width=True)
                