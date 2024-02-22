import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
from helpers.algorithms import bfs_algorithm

# Read the CSV of nodes
nodes = pd.read_csv("data/nodes.csv")
edges_with_weights = pd.read_csv("data/edges_with_weights.csv")
nodes_list = nodes['Node'].tolist()

# Create a simple graph with NetworkX
Graph = nx.DiGraph()
Graph.add_nodes_from(nodes_list)
Graph.add_weighted_edges_from(
    [(row['Origin'], row['Destination'], row['Weight']) for index, row in edges_with_weights.iterrows()])

# Generate a fixed layout for the nodes
pos = nx.kamada_kawai_layout(Graph)

# Streamlit configuration
st.title("Graph Explorer")

# Draw the graph with fixed positions
plt.figure(figsize=(10, 7))
nx.draw(Graph, pos, with_labels=True, node_color='skyblue', node_size=500, edge_color='k')
st.pyplot(plt)

# Streamlit configuration
st.title("Select nodes to find a path")

start_node = st.selectbox('Start node:', nodes_list)
target_node = st.selectbox('Target node:', nodes_list)
path = bfs_algorithm(Graph, start_node, target_node)

# Prepare data for Plotly graph
edge_x = []
edge_y = []
for edge in Graph.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

node_x = [pos[node][0] for node in Graph.nodes()]
node_y = [pos[node][1] for node in Graph.nodes()]
node_degree = [Graph.degree(node) for node in Graph.nodes()]

# Create a figure
fig = go.Figure()

# Add edges as lines with improved styling
fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=2, color='grey'), hoverinfo='none'))

# Add nodes with a color scale based on their degree
fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text', text=[node for node in Graph.nodes()],
                         textposition="bottom center",
                         marker=dict(size=[(deg + 1) * 5 for deg in node_degree], color=node_degree, colorscale='Blues',
                                     showscale=True, colorbar=dict(title='Node Degree')),
                         hoverinfo='text',
                         hovertext=[f'{node}<br>Degree: {deg}' for node, deg in zip(Graph.nodes(), node_degree)]))

# Highlight the found path, if it exists, with better visibility
if path != -1:
    path_edges = zip(path, path[1:])
    path_x = []
    path_y = []
    for edge in path_edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        path_x.extend([x0, x1, None])
        path_y.extend([y0, y1, None])
    fig.add_trace(go.Scatter(x=path_x, y=path_y, mode='lines', line=dict(color='firebrick', width=3), hoverinfo='none'))

# Update the layout for a more polished look
fig.update_layout(title_text='Interactive Network Graph', title_x=0.5, title_font_size=24,
                  showlegend=False, hovermode='closest',
                  margin=dict(b=20, l=20, r=20, t=40),
                  xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                  yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                  paper_bgcolor='white', plot_bgcolor='white',
                  font=dict(size=12, color='black'))

# Display the updated figure in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Show information about the found path
if path != -1:
    st.write(f"Path found from {start_node} to {target_node}: {' -> '.join(path)}")
else:
    st.write("No path found.")
