from helpers.algorithms import *
from helpers import *
import osmnx as ox
import pandas as pd
import streamlit as st

# Sidebar for Place Input
place_name = st.sidebar.text_input("Place Name:", value="Benito Juarez, Mexico",
                                   help="Input the place you want to graph.")
# Sidebar for Pathfinding Settings
limit = st.sidebar.number_input('Depth Limit:', min_value=0, value=5, step=1,
                                help="Set the maximum depth for depth-limited search.")

metrics = {

}

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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        ["Dijkstra", "BFS", "DFS", "DLS", "IDDFS", "Execution Times Chart", "Distance Chart"])

    with tab1:
        st.header("Dijkstra's Algorithm")
        # Create two columns for the plots
        col1, col2 = st.columns(2)

        with col1:
            st.write("Visited Nodes")
            iterations, time_of_function = dijkstra(Graph, start_node, target_node, plot=True)
            st.write(f"The Dijkstra's algorithm took {time_of_function} seconds.")
            st.write(f"Number of iterations: {iterations}")
            metrics['Dijkstra'] = {'Execution Time': time_of_function}

        with col2:
            st.write("Shortest Path")
            distance, average_speed, total_time = reconstruct_path(Graph, start_node, target_node, plot=True)
            st.write(f"Distance: {distance} km")
            st.write(f"Average Speed: {average_speed} m/s")
            st.write(f"Total Time: {total_time} minutes")
            metrics['Dijkstra']['Distance'] = distance
            metrics['Dijkstra']['Average Speed'] = average_speed
            metrics['Dijkstra']['Total Time'] = total_time

    with tab2:
        st.header("Breadth-First Search (BFS)")

        # Create two columns for the plots
        col1, col2 = st.columns(2)

        with col1:
            st.write("Visited Nodes")
            iterations, time_of_function = bfs(Graph, start_node, target_node, plot=True)
            st.write(f"The BFS algorithm took {time_of_function} seconds.")
            st.write(f"Number of iterations: {iterations}")
            metrics['BFS'] = {'Execution Time': time_of_function}

        with col2:
            st.write("Shortest Path")
            distance, average_speed, total_time = reconstruct_path(Graph, start_node, target_node, plot=True)
            st.write(f"Distance: {distance} km")
            st.write(f"Average Speed: {average_speed} m/s")
            st.write(f"Total Time: {total_time} minutes")
            metrics['BFS']['Distance'] = distance
            metrics['BFS']['Average Speed'] = average_speed
            metrics['BFS']['Total Time'] = total_time

    with tab3:
        st.header("Depth-First Search (DFS)")

        # Create two columns for the plots
        col1, col2 = st.columns(2)

        with col1:
            st.write("Visited Nodes")
            iterations, time_of_function = dfs(Graph, start_node, target_node, plot=True)
            st.write(f"The DFS algorithm took {time_of_function} seconds.")
            st.write(f"Number of iterations: {iterations}")
            metrics['DFS'] = {'Execution Time': time_of_function}

        with col2:
            st.write("Shortest Path")
            distance, average_speed, total_time = reconstruct_path(Graph, start_node, target_node, plot=True)
            st.write(f"Distance: {distance} km")
            st.write(f"Average Speed: {average_speed} m/s")
            st.write(f"Total Time: {total_time} minutes")
            metrics['DFS']['Distance'] = distance
            metrics['DFS']['Average Speed'] = average_speed
            metrics['DFS']['Total Time'] = total_time

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
                found, steps, time_of_function = dfs_with_limit(Graph, start_node, target_node, limit, plot=True)
                st.write(f"The DLS algorithm took {time_of_function} seconds.")
                st.write(f"Number of iterations: {steps}")
                metrics['DLS'] = {'Execution Time': time_of_function}

            with col2:
                st.write("Shortest Path")
                if found:
                    distance, average_speed, total_time = reconstruct_path(Graph, start_node, target_node, plot=True)
                    st.write(f"Distance: {distance} km")
                    st.write(f"Average Speed: {average_speed} m/s")
                    st.write(f"Total Time: {total_time} minutes")
                    metrics['DLS']['Distance'] = distance
                    metrics['DLS']['Average Speed'] = average_speed
                    metrics['DLS']['Total Time'] = total_time
                else:
                    st.write("No path found within the depth limit.")
                    metrics['DLS']['Distance'] = "N/A"
                    metrics['DLS']['Average Speed'] = "N/A"
                    metrics['DLS']['Total Time'] = "N/A"

    with tab5:
        found = False
        st.header("Iterative Depth-First Search (Iterative DFS)")

        # Create two columns for the plots
        col1, col2 = st.columns(2)

        with col1:
            st.write("Visited Nodes")
            iterations, time_of_function = iterative_deepening_dfs(Graph, start_node, target_node, plot=True)
            st.write(f"The IDDFS algorithm took {time_of_function} seconds.")
            st.write(f"Number of iterations: {iterations}")
            metrics['IDDFS'] = {'Execution Time': time_of_function}

        with col2:
            st.write("Shortest Path")
            distance, average_speed, total_time = reconstruct_path(Graph, start_node, target_node, plot=True)
            st.write(f"Distance: {distance} km")
            st.write(f"Average Speed: {average_speed} m/s")
            st.write(f"Total Time: {total_time} minutes")
            metrics['IDDFS']['Distance'] = distance
            metrics['IDDFS']['Average Speed'] = average_speed
            metrics['IDDFS']['Total Time'] = total_time

    with tab6:
        st.header("Algorithm Execution Times")
        speeds = [metrics[key]['Execution Time'] for key in metrics]
        data = pd.DataFrame({
            'Algorithm': list(metrics.keys()),
            'Execution Time (s)': speeds
        })
        st.bar_chart(data.set_index('Algorithm'))

    with tab7:
        st.header("Distance Chart")
        distances = [metrics[key]['Distance'] for key in metrics]
        data = pd.DataFrame({
            'Algorithm': list(metrics.keys()),
            'Distance (km)': distances
        })
        st.bar_chart(data.set_index('Algorithm'))

    # Repeat the pattern for A*, Bellman-Ford, Floyd-Warshall, and your custom algorithm
else:
    st.error("Please specify a valid location to generate the graph.")
