import pandas as pd
import numpy as np
import streamlit as st
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, value, LpBinary, PULP_CBC_CMD

def ejecutar_modelo_multicultivo(
    cultivos_df, demanda_df, terreno_df,
    superficie_ha, tipo_suelo, acceso_agua,
    provincia_equiv, zona_climatica_usuario,
    modo_flexible=False,
    debug=False
):
    if debug:
        st.write("🔍 Iniciando modelo multicultivo...")

    agua_map = {"bajo": 1, "medio": 2, "alto": 3}
    nivel_agua_usuario = agua_map.get(acceso_agua.lower(), 2)

    if debug:
        st.write(f"🌦️ Zona climática asignada: {zona_climatica_usuario}")
        st.write(f"💧 Nivel de agua del usuario: {nivel_agua_usuario}")

    cultivos_df["Necesidad_agua_numerica"] = cultivos_df["Necesidad_agua"].str.lower().map(agua_map).fillna(2)
    cultivos_df["Tipo_suelo_requerido"] = cultivos_df["Tipo_suelo_requerido"].str.lower().str.strip()
    cultivos_df["Zona_climatica"] = cultivos_df["Zona_climatica"].str.lower().str.strip()

    if modo_flexible:
        if debug:
            st.info("🔁 Modo flexible activado: se permiten cultivos fuera de la zona climática del usuario.")
        cultivos_filtrados = cultivos_df[
            (cultivos_df["Necesidad_agua_numerica"] <= nivel_agua_usuario)
        ]
    else:
        cultivos_filtrados = cultivos_df[
            (cultivos_df["Necesidad_agua_numerica"] <= nivel_agua_usuario) &
            (cultivos_df["Zona_climatica"] == zona_climatica_usuario)
        ]

    if debug:
        st.write(f"✅ Cultivos tras filtrado por agua y clima: {len(cultivos_filtrados)}")

    productos_disponibles = demanda_df["Producto"].unique().tolist()
    cultivos_validos = cultivos_filtrados[
        cultivos_filtrados["Nombre_cultivo"].isin(productos_disponibles)
    ]
    cultivos_validos = cultivos_validos[
        cultivos_validos["Rendimiento_promedio (kg/ha)"].fillna(0) > 0
    ]

    if debug:
        st.write(f"✅ Cultivos válidos finales: {len(cultivos_validos)}")

    if cultivos_validos.empty:
        if debug:
            st.warning("⚠️ Ningún cultivo válido después del filtrado.")
        return pd.DataFrame(), "Sin solución", 0.0

    productos = cultivos_validos["Nombre_cultivo"].tolist()
    demanda_resumen = demanda_df.groupby("Producto").agg(
        demanda_total_kg=("Kg_comprados", "sum"),
        precio_medio=("Precio_kg_€", "mean")
    ).reset_index()

    coste_generico = 0.30
    demanda_resumen["beneficio_kg"] = demanda_resumen["precio_medio"] - coste_generico

    beneficios = dict(zip(demanda_resumen["Producto"], demanda_resumen["beneficio_kg"]))
    demandas = dict(zip(demanda_resumen["Producto"], demanda_resumen["demanda_total_kg"]))
    rendimientos = dict(zip(cultivos_validos["Nombre_cultivo"], cultivos_validos["Rendimiento_promedio (kg/ha)"].fillna(0) / 10000))

    duracion_dias = cultivos_validos.set_index("Nombre_cultivo")["Duración_cultivo_días"]
    duracion_meses = np.ceil(duracion_dias / 30).astype(int)
    duraciones = duracion_meses.loc[duracion_meses.index.intersection(productos)].to_dict()

    superficie_total_m2 = superficie_ha * 10000
    meses = list(range(1, 13))

    modelo = LpProblem("Optimizacion_Multicultivo_Filtrado", LpMaximize)
    x = {(p, m): LpVariable(f"x_{p}_{m}", lowBound=0) for p in productos for m in meses}
    z = {p: LpVariable(f"z_{p}", cat=LpBinary) for p in productos}

    modelo += lpSum(x[p, m] * beneficios.get(p, 0) for p in productos for m in meses)

    for p in productos:
        modelo += lpSum(x[p, m] for m in meses) <= demandas.get(p, 0) * z[p]

    # RESTRICCIÓN: uso de terreno teniendo en cuenta duración del cultivo
    for m in meses:
        uso_terreno_mes = []
        for p in productos:
            d = duraciones.get(p, 1)
            rendimiento = rendimientos.get(p, 0.0001)

            for m_inicio in meses:
                meses_ocupados = [(m_inicio + offset - 1) % 12 + 1 for offset in range(d)]
                if m in meses_ocupados:
                    if (p, m_inicio) in x:
                        uso = x[p, m_inicio] * (1 / rendimiento)
                        uso_terreno_mes.append(uso)

        modelo += lpSum(uso_terreno_mes) <= superficie_total_m2, f"rotacion_terreno_mes_{m}"

    solver = PULP_CBC_CMD(msg=False)
    modelo.solve(solver)
    estado = LpStatus[modelo.status]
    beneficio_total = round(value(modelo.objective), 2) if modelo.objective is not None else 0.0
    filas = []
    for p in productos:
        for m in meses:
            cantidad = x[p, m].varValue
            if cantidad is not None and cantidad > 0:
                rendimiento = rendimientos.get(p, 0.0001)
                beneficio_unitario = beneficios.get(p, 0.0)
                superficie_m2 = cantidad / rendimiento
                filas.append({
                    "Cultivo": p,
                    "Mes": m,
                    "Cantidad_kg": round(cantidad, 2),
                    "Beneficio_€": round(cantidad * beneficio_unitario, 2),
                    "Superficie_ha": round(superficie_m2 / 10000, 4)
                })

    resultado = pd.DataFrame(filas)

    return resultado, estado, beneficio_total
