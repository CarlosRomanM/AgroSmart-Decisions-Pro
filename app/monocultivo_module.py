import pandas as pd
import numpy as np

def generar_propuestas_monocultivo(cultivos_df, demanda_df, terreno_df, superficie_ha):
    # Calcular el rendimiento en kg/m²
    cultivos_df["Rendimiento_kg_m2"] = cultivos_df["Rendimiento_promedio (kg/ha)"].fillna(0) / 10000

    # Calcular beneficio por kg
    coste_generico = 0.30  # €/kg estimado
    demanda_df["beneficio_kg"] = demanda_df["Precio_kg_€"] - coste_generico

    # Unir cultivos con la demanda
    resumen = cultivos_df.merge(
        demanda_df[["Producto", "Precio_kg_€", "beneficio_kg"]],
        left_on="Nombre_cultivo", right_on="Producto", how="inner"
    ).drop_duplicates(subset=["Nombre_cultivo"])

    # Duración del cultivo y ciclos por año
    resumen["Duración del ciclo (días)"] = resumen["Duración_cultivo_días"]
    resumen["Ciclos por año"] = (365 / resumen["Duración_cultivo_días"]).apply(np.floor).astype(int)

    # Cálculos de producción y beneficio
    resumen["Producción (kg)"] = resumen["Rendimiento_kg_m2"] * superficie_ha * 10000  # por ciclo
    resumen["Producción total anual (kg)"] = resumen["Producción (kg)"] * resumen["Ciclos por año"]
    resumen["Beneficio estimado (€)"] = resumen["Producción (kg)"] * resumen["beneficio_kg"]
    resumen["Beneficio total anual (€)"] = resumen["Producción total anual (kg)"] * resumen["beneficio_kg"]
    resumen["Beneficio mensual promedio (€)"] = resumen["Beneficio total anual (€)"] / 12
    resumen["Producción mensual promedio (kg)"] = resumen["Producción total anual (kg)"] / 12
    resumen["Superficie (ha)"] = superficie_ha

    # Selección de columnas
    resumen_final = resumen[[
        "Nombre_cultivo",
        "Duración del ciclo (días)",
        "Ciclos por año",
        "Producción (kg)",
        "Producción mensual promedio (kg)",
        "Producción total anual (kg)",
        "Precio_kg_€",
        "Beneficio estimado (€)",
        "Beneficio mensual promedio (€)",
        "Beneficio total anual (€)",
        "Superficie (ha)"
    ]].rename(columns={
        "Nombre_cultivo": "Cultivo",
        "Precio_kg_€": "Precio estimado €/kg"
    })

    # Ordenar por beneficio total anual
    resumen_final = resumen_final.sort_values("Beneficio total anual (€)", ascending=False).head(10)

    return resumen_final

