import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Funciones para los gráficos
def grafico_cumplimiento_entregas(df: pd.DataFrame, fecha_inicio: str, fecha_fin: str, cliente: str = None):
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d-%m-%Y')
    fecha_inicio_dt = datetime.strptime(fecha_inicio, '%d-%m-%Y')
    fecha_fin_dt = datetime.strptime(fecha_fin, '%d-%m-%Y')

    df_filtrado = df[(df['Fecha'] >= fecha_inicio_dt) & (df['Fecha'] <= fecha_fin_dt)]
    if cliente and cliente != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Cliente'] == cliente]

    agrupado = df_filtrado.groupby(['Fecha', 'CumplimientoPlazo']).size().unstack(fill_value=0)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=agrupado.index, y=agrupado.get(True, [0] * len(agrupado)), name='Cumple Plazo', marker_color='blue'))
    fig.add_trace(go.Bar(x=agrupado.index, y=agrupado.get(False, [0] * len(agrupado)), name='Fuera de Plazo', marker_color='red'))
    fig.update_layout(title='Cumplimiento de Entregas', xaxis_title='Fecha', yaxis_title='Número de Entregas', barmode='stack')
    return fig

def grafico_porcentaje_entregas(df: pd.DataFrame, fecha_inicio: str, fecha_fin: str, cliente: str = None):
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d-%m-%Y')
    fecha_inicio_dt = datetime.strptime(fecha_inicio, '%d-%m-%Y')
    fecha_fin_dt = datetime.strptime(fecha_fin, '%d-%m-%Y')

    df_filtrado = df[(df['Fecha'] >= fecha_inicio_dt) & (df['Fecha'] <= fecha_fin_dt)]
    if cliente and cliente != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Cliente'] == cliente]

    cumplimiento_counts = df_filtrado['CumplimientoPlazo'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=['Cumple Plazo', 'Fuera de Plazo'], 
                                 values=[cumplimiento_counts.get(True, 0), cumplimiento_counts.get(False, 0)],
                                 marker=dict(colors=['blue', 'red']))])
    fig.update_layout(title='Porcentaje de Entregas')
    return fig

def grafico_promedio_retraso(df: pd.DataFrame, fecha_inicio: str, fecha_fin: str, cliente: str = None):
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d-%m-%Y')
    fecha_inicio_dt = datetime.strptime(fecha_inicio, '%d-%m-%Y')
    fecha_fin_dt = datetime.strptime(fecha_fin, '%d-%m-%Y')

    df_filtrado = df[(df['Fecha'] >= fecha_inicio_dt) & (df['Fecha'] <= fecha_fin_dt)]
    if cliente and cliente != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Cliente'] == cliente]

    promedio_retraso = df_filtrado.groupby('Fecha')['RetrasoEntrega'].mean().reset_index()
    fig = go.Figure(data=[go.Scatter(x=promedio_retraso['Fecha'], y=promedio_retraso['RetrasoEntrega'], 
                                     mode='lines+markers', line=dict(color='blue', width=3))])
    fig.update_layout(title='Tiempo Promedio de Retraso', xaxis_title='Fecha', yaxis_title='Retraso Promedio (horas)')
    return fig

def grafico_variabilidad_tiempos(df: pd.DataFrame, fecha_inicio: str, fecha_fin: str, cliente: str = None):
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d-%m-%Y')
    fecha_inicio_dt = datetime.strptime(fecha_inicio, '%d-%m-%Y')
    fecha_fin_dt = datetime.strptime(fecha_fin, '%d-%m-%Y')

    df_filtrado = df[(df['Fecha'] >= fecha_inicio_dt) & (df['Fecha'] <= fecha_fin_dt)]
    if cliente and cliente != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Cliente'] == cliente]

    fig = go.Figure(data=[go.Box(x=df_filtrado['Fecha'], y=df_filtrado['TiempoEntrega'], boxpoints='outliers', marker_color='blue')])
    fig.update_layout(title='Variabilidad de Tiempos de Entrega', xaxis_title='Fecha', yaxis_title='Tiempo de Entrega (horas)')
    return fig


# Configuración de Streamlit
st.set_page_config(layout="wide", page_title="Gestión de Entregas 🚚")
st.sidebar.title("🚚 Gestión de entregas")

# Parámetros de la barra lateral
fecha_inicio = st.sidebar.date_input("Fecha de Inicio", value=datetime(2024, 11, 1), 
                                     min_value=datetime(2024, 11, 1), max_value=datetime(2024, 11, 30)).strftime('%d-%m-%Y')
fecha_fin = st.sidebar.date_input("Fecha de Fin", value=datetime(2024, 11, 30), 
                                  min_value=datetime(2024, 11, 1), max_value=datetime(2024, 11, 30)).strftime('%d-%m-%Y')
clientes = ['Todos', 'QuickLogistics', 'MegaMove', 'FoodExpress', 'PackPro', 'TechCorp', 'LogiTrans', 'SafeHaul', 'EcoDeliver', 'FastShip', 'GreenCargo']
cliente = st.sidebar.selectbox("Selecciona Cliente", clientes, index=0)

# Leer los datos desde CSV
df = pd.read_csv("entregas.csv")

# Mostrar gráficos en una cuadrícula 2x2
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(grafico_cumplimiento_entregas(df, fecha_inicio, fecha_fin, cliente), use_container_width=True)
    st.plotly_chart(grafico_promedio_retraso(df, fecha_inicio, fecha_fin, cliente), use_container_width=True)

with col2:
    st.plotly_chart(grafico_porcentaje_entregas(df, fecha_inicio, fecha_fin, cliente), use_container_width=True)
    st.plotly_chart(grafico_variabilidad_tiempos(df, fecha_inicio, fecha_fin, cliente), use_container_width=True)

