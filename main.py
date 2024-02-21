import tensorflow as tf
import numpy as np
import pandas as pd
import networkx as nx
from helpers import execution_time
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go

# Leer el CSV de nodos
nodes = pd.read_csv("data/nodes.csv")
nodes_list = nodes['Nodo'].tolist()

# Leer el CSV de aristas con pesos
df_aristas = pd.read_csv("data/aristas_con_pesos.csv")

# Crear un grafo simple con NetworkX
Graph = nx.DiGraph()
Graph.add_nodes_from(nodes_list)
Graph.add_weighted_edges_from(
    [(row['Origin'], row['Destino'], row['Peso']) for index, row in df_aristas.iterrows()])

# Dibujar el grafo con Matplotlib
plt.figure(figsize=(10, 7))
nx.draw(Graph, with_labels=True, node_color='skyblue', node_size=500, edge_color='k')
plt.title("Visualización de Grafo")

# Usar Streamlit para mostrar el grafo
st.title("Mi Aplicación de Grafo")
st.pyplot(plt)

# Crear un gráfico simple con Plotly
fig = go.Figure(data=go.Bar(y=[2, 3, 1]))
fig.update_layout(title_text='Ejemplo de visualización interactiva con Plotly')
# Mostrar el gráfico en Streamlit
st.title("Mi Aplicación de Visualización Interactiva")
st.plotly_chart(fig)
