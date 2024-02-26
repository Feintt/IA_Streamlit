import time


def time_function(func):
    """
    Decorator to measure the time a function takes to execute.
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)  # Call the original function and store its result
        end_time = time.time()
        duration = end_time - start_time
        print(f"Function {func.__name__} took {duration} seconds.")
        if isinstance(result, tuple):
            return *result, duration
        return result, duration  # Return a tuple containing the original result and the duration

    return wrapper


def clean_graph(graph):
    """
    Clean and prepare the graph by adjusting 'max_speed' and calculating 'weight' for each edge.
    :param graph:
    :return:
    """
    for edge in graph.edges:
        # Standardize the "max_speed" attribute
        max_speed = graph.edges[edge].get("maxspeed", 40)  # Default to 40 if not present
        if isinstance(max_speed, list):
            max_speed = min(int(speed) for speed in max_speed)
        elif isinstance(max_speed, str):
            max_speed = int(max_speed)

        # Update the edge with the standardized max_speed
        graph.edges[edge]["maxspeed"] = max_speed

        # Calculate and assign the "weight" attribute based on edge length and max_speed
        graph.edges[edge]["weight"] = graph.edges[edge]["length"] / max_speed


def style_unvisited_edge(graph, edge):
    graph.edges[edge]["color"] = "#d36206"
    graph.edges[edge]["alpha"] = 0.2
    graph.edges[edge]["linewidth"] = 0.5


def style_visited_edge(graph, edge):
    graph.edges[edge]["color"] = "#d36206"
    graph.edges[edge]["alpha"] = 1
    graph.edges[edge]["linewidth"] = 1


def style_active_edge(graph, edge):
    graph.edges[edge]["color"] = '#e8a900'
    graph.edges[edge]["alpha"] = 1
    graph.edges[edge]["linewidth"] = 1


def style_path_edge(graph, edge):
    graph.edges[edge]["color"] = "white"
    graph.edges[edge]["alpha"] = 1
    graph.edges[edge]["linewidth"] = 1


def plot_graph(graph):
    # Lazy import necessary libraries
    import streamlit as st
    import osmnx as ox

    # Define visualization attributes for the graph
    node_sizes = [graph.nodes[node]["size"] for node in graph.nodes]
    edge_colors = [graph.edges[edge]["color"] for edge in graph.edges]
    edge_alphas = [graph.edges[edge]["alpha"] for edge in graph.edges]
    edge_linewidths = [graph.edges[edge]["linewidth"] for edge in graph.edges]

    # Configure and plot the graph
    fig, ax = ox.plot_graph(
        graph,
        node_size=node_sizes,
        edge_color=edge_colors,
        edge_alpha=edge_alphas,
        edge_linewidth=edge_linewidths,
        node_color="white",
        bgcolor="#18080e",
        show=False,
    )

    # Display the plot in a Streamlit app
    st.pyplot(fig, use_container_width=True)


def reconstruct_path(graph, orig, dest, plot=False, algorithm=None):
    for edge in graph.edges:
        style_unvisited_edge(graph, edge)
    dist = 0
    speeds = []
    curr = dest
    while curr != orig:
        prev = graph.nodes[curr]["previous"]
        dist += graph.edges[(prev, curr, 0)]["length"]
        speeds.append(graph.edges[(prev, curr, 0)]["maxspeed"])
        style_path_edge(graph, (prev, curr, 0))
        if algorithm:
            graph.edges[(prev, curr, 0)][f"{algorithm}_uses"] = graph.edges[(prev, curr, 0)].get(f"{algorithm}_uses",
                                                                                                 0) + 1
        curr = prev
    dist /= 1000
    if plot:
        plot_graph(graph)
        return dist, sum(speeds) / len(speeds), dist / (sum(speeds) / len(speeds)) * 60
