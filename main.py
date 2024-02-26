import streamlit as st
from helpers.algorithms import *
from helpers import *
import osmnx as ox

# Sidebar for Place Input
place_name = st.sidebar.text_input("Place Name:", value="Benito Juarez, Mexico",
                                   help="Input the place you want to graph.")
# Sidebar for Pathfinding Settings
limit = st.sidebar.number_input('Depth Limit:', min_value=0, value=5, step=1,
                                help="Set the maximum depth for depth-limited search.")

# Attempt to load the graph for the specified place
try:
    Graph = ox.graph_from_place(place_name, network_type="drive")
    clean_graph(Graph)
    nodes_ready = True
except Exception as e:
    st.sidebar.error("Could not load graph for the specified place. Please try a different location.")
    nodes_ready = False

if nodes_ready:
    # Sidebar for Node Selection
    st.sidebar.title("Pathfinding Settings")
    start_node = st.sidebar.selectbox('Start Node:', list(Graph.nodes))
    target_node = st.sidebar.selectbox('Target Node:', list(Graph.nodes))

    # Main Interface - Tabs for Each Algorithm
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Dijkstra", "BFS", "DFS", "DLS", "IDDFS"])

    with tab1:
        st.header("Dijkstra's Algorithm")
        # Create two columns for the plots
        col1, col2 = st.columns(2)

        with col1:
            st.write("Visited Nodes")
            iterations = dijkstra(Graph, start_node, target_node, plot=True)
            st.write(f"Number of iterations: {iterations}")

        with col2:
            st.write("Shortest Path")
            distance, average_speed, total_time = reconstruct_path(Graph, start_node, target_node, plot=True)
            st.write(f"Distance: {distance} km")
            st.write(f"Average Speed: {average_speed} m/s")
            st.write(f"Total Time: {total_time} minutes")

    with tab2:
        st.header("Breadth-First Search (BFS)")

        # Create two columns for the plots
        col1, col2 = st.columns(2)

        with col1:
            st.write("Visited Nodes")
            iterations = bfs(Graph, start_node, target_node, plot=True)
            st.write(f"Number of iterations: {iterations}")

        with col2:
            st.write("Shortest Path")
            distance, average_speed, total_time = reconstruct_path(Graph, start_node, target_node, plot=True)
            st.write(f"Distance: {distance} km")
            st.write(f"Average Speed: {average_speed} m/s")
            st.write(f"Total Time: {total_time} minutes")

    with tab3:
        st.header("Depth-First Search (DFS)")

        # Create two columns for the plots
        col1, col2 = st.columns(2)

        with col1:
            st.write("Visited Nodes")
            iterations = dfs(Graph, start_node, target_node, plot=True)
            st.write(f"Number of iterations: {iterations}")

        with col2:
            st.write("Shortest Path")
            distance, average_speed, total_time = reconstruct_path(Graph, start_node, target_node, plot=True)
            st.write(f"Distance: {distance} km")
            st.write(f"Average Speed: {average_speed} m/s")
            st.write(f"Total Time: {total_time} minutes")

    with tab4:
        found = False
        st.header("Depth-Limited Search (DLS)")

        # Indicate if the limit is not set; otherwise, run the DLS
        if limit is None:
            st.write("Please set a depth limit.")
        else:
            # Create two columns for the plots
            col1, col2 = st.columns(2)

            with col1:
                st.write("Visited Nodes")
                # Assuming dls_plot is a function that plots the graph showing visited nodes
                found, steps = dfs_with_limit(Graph, start_node, target_node, limit, plot=True)
                st.write(f"Number of iterations: {steps}")

            with col2:
                st.write("Shortest Path")
                if found:
                    distance, average_speed, total_time = reconstruct_path(Graph, start_node, target_node, plot=True)
                    st.write(f"Distance: {distance} km")
                    st.write(f"Average Speed: {average_speed} m/s")
                    st.write(f"Total Time: {total_time} minutes")
                else:
                    st.write("No path found within the depth limit.")

    with tab5:
        found = False
        st.header("Iterative Depth-First Search (Iterative DFS)")

        # Create two columns for the plots
        col1, col2 = st.columns(2)

        with col1:
            st.write("Visited Nodes")
            iterations = iterative_deepening_dfs(Graph, start_node, target_node, plot=True)
            st.write(f"Number of iterations: {iterations}")

        with col2:
            st.write("Shortest Path")
            distance, average_speed, total_time = reconstruct_path(Graph, start_node, target_node, plot=True)
            st.write(f"Distance: {distance} km")
            st.write(f"Average Speed: {average_speed} m/s")
            st.write(f"Total Time: {total_time} minutes")

    # Repeat the pattern for A*, Bellman-Ford, Floyd-Warshall, and your custom algorithm
else:
    st.error("Please specify a valid location to generate the graph.")
