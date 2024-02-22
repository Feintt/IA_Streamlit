import networkx as nx
import streamlit as st
import plotly.graph_objects as go
from helpers.algorithms import bfs_algorithm
from helpers import *

# Read the CSV of nodes
nodes, edges_with_weights = extract_nodes_and_edges_from_csv()

# Create a simple graph with NetworkX
Graph = generate_graph(nodes, edges_with_weights)

# Generate a fixed layout for the nodes
pos = nx.kamada_kawai_layout(Graph)

# Show the graph with Matplotlib
st.title("Graph Explorer")
draw_graph(Graph, pos)

# Select nodes to find a path
st.title("Select nodes to find a path")
start_node = st.selectbox('Start node:', nodes)
target_node = st.selectbox('Target node:', nodes)

# Find the path with BFS
path = bfs_algorithm(Graph, start_node, target_node)

# Prepare the edges for Plotly
edge_x, edge_y = get_edge_x_y(pos, Graph)
node_x = [pos[node][0] for node in Graph.nodes()]
node_y = [pos[node][1] for node in Graph.nodes()]
node_degree = [Graph.degree(node) for node in Graph.nodes()]

# Create a figure
fig = go.Figure()

add_edges_to_plotly_graph(fig, edge_x, edge_y)
add_color_to_nodes(fig, node_x, node_y, node_degree, Graph)

# Highlight the found path, if it exists, with better visibility
if path != -1:
    highlight_path(path, pos, fig)
    st.write(f"Path found from {start_node} to {target_node}: {' -> '.join(path)}")
else:
    st.write("No path found.")

beautify_graph(fig)
st.plotly_chart(fig, use_container_width=True)
