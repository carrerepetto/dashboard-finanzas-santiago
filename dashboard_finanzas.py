
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Dashboard Finanzas Santiago', layout='wide')

st.title("Dashboard Financiero - Santiago")

st.markdown("""
Bienvenido a tu dashboard financiero personal.

Desde aquí podés visualizar y analizar tus ingresos, egresos, ahorros y compras a plazos.  
Este espacio está diseñado para que tengas el control total de tus finanzas de forma clara y visual.

Subí tu archivo Excel con tus movimientos o usá el archivo de ejemplo incluido en el repositorio.

""")

archivo = st.file_uploader("Subí tu archivo de control financiero (.xlsx)", type=["xlsx"])

if archivo:
    registro = pd.read_excel(archivo, sheet_name="Registro Diario")
    compras = pd.read_excel(archivo, sheet_name="Compras a Plazos")

    st.header("Resumen general")

    saldo_actual = registro["Saldo Restante"].dropna().iloc[-1]
    ingresos = registro[registro["Tipo (Ingreso/Egreso)"] == "Ingreso"]["Monto"].sum()
    egresos = registro[registro["Tipo (Ingreso/Egreso)"] == "Egreso"]["Monto"].sum()
    ahorro_total = registro["Ahorro"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Saldo Actual", f"${saldo_actual:,.0f}")
    col2.metric("Ingresos Totales", f"${ingresos:,.0f}")
    col3.metric("Egresos Totales", f"${egresos:,.0f}")
    col4.metric("Ahorro Total", f"${ahorro_total:,.0f}")

    st.subheader("Egresos por Categoría")
    egresos_df = registro[registro["Tipo (Ingreso/Egreso)"] == "Egreso"]
    egresos_categoria = egresos_df.groupby("Categoría")["Monto"].sum().sort_values()

    fig, ax = plt.subplots()
    egresos_categoria.plot(kind='barh', ax=ax)
    ax.set_xlabel("Monto ($)")
    ax.set_title("Egresos por Categoría")
    st.pyplot(fig)

    st.subheader("Compras a Plazos")
    compras_filtradas = compras[compras["Estado"] == "Activa"]
    st.dataframe(compras_filtradas)

else:
    st.info("Por favor, subí tu archivo Excel para ver el dashboard.")
