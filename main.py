import networkx as nx
import streamlit as st
from helpers.algorithms import bfs_algorithm, dijkstra_algorithm, dfs_algorithm
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
bfs_path = bfs_algorithm(Graph, start_node, target_node)
# Find the path with Dijkstra
dijkstra_path = dijkstra_algorithm(Graph, start_node, target_node)
# Find the path with DFS
dfs_path = dfs_algorithm(Graph, start_node, target_node)

# Prepare the edges for Plotly
edge_x, edge_y = get_edge_x_y(pos, Graph)
node_x = [pos[node][0] for node in Graph.nodes()]
node_y = [pos[node][1] for node in Graph.nodes()]
node_degree = [Graph.degree(node) for node in Graph.nodes()]

# Display the results
# Assuming bfs_path, dijkstra_path, dfs_path are already defined along with
# Graph, pos, edge_x, edge_y, node_x, node_y, node_degree, start_node, target_node
display_algorithm_results("BFS", bfs_path, Graph, pos, edge_x, edge_y, node_x, node_y, node_degree, start_node, target_node)
display_algorithm_results("Dijkstra's", dijkstra_path, Graph, pos, edge_x, edge_y, node_x, node_y, node_degree, start_node, target_node)
display_algorithm_results("DFS", dfs_path, Graph, pos, edge_x, edge_y, node_x, node_y, node_degree, start_node, target_node)