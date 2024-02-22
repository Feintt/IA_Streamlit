import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
from helpers.algorithms import bfs_algorithm

# Assuming bfs_algorithm is correctly defined in helpers/algorithms.py

# Read the CSV of nodes
nodes = pd.read_csv("data/nodes.csv")
nodes_list = nodes['Node'].tolist()  # 'Nodo' changed to 'Node'

# Read the CSV of edges with weights
edges_with_weights = pd.read_csv("data/edges_with_weights.csv")  # 'df_aristas' changed to 'edges_with_weights'

# Create a simple graph with NetworkX
Graph = nx.DiGraph()
Graph.add_nodes_from(nodes_list)
Graph.add_weighted_edges_from(
    [(row['Origin'], row['Destination'], row['Weight']) for index, row in edges_with_weights.iterrows()])
# Changed 'Destino' to 'Destination' and 'Peso' to 'Weight'

# Generate a fixed layout for the nodes
pos = nx.kamada_kawai_layout(Graph)  # The seed argument ensures consistency in positions

# Streamlit configuration
st.title("Graph Explorer")

# Draw the graph with fixed positions
plt.figure(figsize=(10, 7))
nx.draw(Graph, pos, with_labels=True, node_color='skyblue', node_size=500, edge_color='k')
st.pyplot(plt)

# Read the CSV of nodes and edges
nodes = pd.read_csv("data/nodes.csv")
edges_with_weights = pd.read_csv("data/edges_with_weights.csv")
nodes_list = nodes['Node'].tolist()

# Streamlit configuration
st.title("Select nodes to find a path")

start_node = st.selectbox('Start node:', nodes_list)
target_node = st.selectbox('Target node:', nodes_list)
path = bfs_algorithm(Graph, start_node, target_node)

# Prepare data for Plotly
edge_x = []
edge_y = []
for edge in Graph.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)  # Necessary to create line segments between nodes
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

node_x = [pos[node][0] for node in Graph.nodes()]
node_y = [pos[node][1] for node in Graph.nodes()]

# Create figure
fig = go.Figure()

# Add edges as lines
fig.add_trace(go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines'))

# Add nodes as points
fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers', hoverinfo='text',
                         marker=dict(showscale=True, colorscale='YlGnBu', color=[], size=10),
                         text=[node for node in Graph.nodes()]))

# Highlight the found path, if it exists
if path != -1:
    path_edges = zip(path, path[1:])
    path_x = []
    path_y = []
    for edge in path_edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        path_x.extend([x0, x1, None])
        path_y.extend([y0, y1, None])
    fig.add_trace(go.Scatter(x=path_x, y=path_y, mode='lines', line=dict(color='firebrick', width=2), hoverinfo='none'))

# Update layout for better visualization
fig.update_layout(showlegend=False, hovermode='closest',
                  margin=dict(b=0, l=0, r=0, t=0), xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                  yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

# Display figure in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Show information about the found path
if path != -1:
    st.write(f"Path found from {start_node} to {target_node}: {' -> '.join(path)}")
else:
    st.write("No path found.")
