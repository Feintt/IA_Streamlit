def execution_time(func):
    """
    Decorator to measure the execution time of a function.
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        import time  # Lazy import
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"The function {func.__name__} took {end - start} seconds to execute.")
        return result

    return wrapper


def extract_nodes_and_edges_from_csv(nodes_path="data/nodes.csv", edges_path="data/edges_with_weights.csv"):
    """
    Extracts the nodes and edges from the CSV files.
    :param nodes_path:
    :param edges_path:
    :return:
    """
    import pandas as pd  # Lazy import
    nodes = pd.read_csv(nodes_path)['Node'].tolist()
    edges = pd.read_csv(edges_path)
    return nodes, edges


def draw_graph(graph, pos):
    """
    Draws the graph with NetworkX and Matplotlib.
    :param graph:
    :param pos:
    :return:
    """

    import streamlit as st  # Lazy import
    import networkx as nx  # Lazy import
    import matplotlib.pyplot as plt  # Lazy import
    plt.figure(figsize=(10, 7))
    nx.draw(graph, pos,
            with_labels=True,
            node_color='skyblue',
            node_size=500,
            edge_color='k')
    st.pyplot(plt)


def generate_graph(nodes, edges):
    """
    Generates a graph with NetworkX.
    :param nodes:
    :param edges:
    :return:
    """

    import networkx as nx  # Lazy import
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_weighted_edges_from(
        [(row['Origin'], row['Destination'], row['Weight']) for _index, row in edges.iterrows()])
    return graph


def add_edges_to_plotly_graph(fig, edge_x, edge_y):
    """
    Adds the edges to the Plotly graph.
    :param fig:
    :param edge_x:
    :param edge_y:
    :return:
    """
    import plotly.graph_objects as go  # Lazy import
    fig.add_trace(go.Scatter(x=edge_x,
                             y=edge_y,
                             mode='lines',
                             line=dict(width=2, color='grey'),
                             hoverinfo='none'))


def add_color_to_nodes(fig, node_x, node_y, node_degree, graph):
    """
    Adds color to the nodes based on their degree to the Plotly graph.
    :param fig:
    :param graph:
    :param node_x:
    :param node_y:
    :param node_degree:
    :return:
    """
    import plotly.graph_objects as go  # Lazy import
    fig.add_trace(go.Scatter(x=node_x,
                             y=node_y,
                             mode='markers+text',
                             text=[node for node in graph.nodes()],
                             textposition="bottom center",
                             marker=dict(size=[(deg + 1) * 5 for deg in node_degree],
                                         color=node_degree, colorscale='Blues',
                                         showscale=True, colorbar=dict(title='Node Degree')),
                             hoverinfo='text',
                             hovertext=[f'{node}<br>Degree: {deg}' for node, deg in zip(graph.nodes(), node_degree)]))


def highlight_path(path, pos, fig):
    """
    Highlights the path in the graph by changing the color of the edges and nodes.
    """
    import plotly.graph_objects as go  # Lazy import
    path_edges = zip(path, path[1:])
    path_x = []
    path_y = []
    for edge in path_edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        path_x.extend([x0, x1, None])
        path_y.extend([y0, y1, None])
    fig.add_trace(go.Scatter(x=path_x,
                             y=path_y,
                             mode='lines',
                             line=dict(color='firebrick', width=3),
                             hoverinfo='none'))


def beautify_graph(fig):
    """
    Beautifies the graph by adding edges and nodes with a color scale based on their degree.
    """
    fig.update_layout(title_text='Interactive Network Graph',
                      title_x=0.5,
                      title_font_size=24,
                      showlegend=False,
                      hovermode='closest',
                      margin=dict(b=20, l=20, r=20, t=40),
                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      paper_bgcolor='white',
                      plot_bgcolor='white',
                      font=dict(size=12, color='black'))


def get_edge_x_y(pos, graph):
    """
    Returns the x and y coordinates of the edges in the graph.
    :param pos:
    :param graph:
    :return:
    """
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    return edge_x, edge_y


def create_figure_with_highlighted_path(graph, pos, edge_x, edge_y, node_x, node_y, node_degree, path):
    """
    Creates a figure with the graph and the highlighted path.
    :param graph:
    :param pos:
    :param edge_x:
    :param edge_y:
    :param node_x:
    :param node_y:
    :param node_degree:
    :param path:
    :return:
    """
    import plotly.graph_objects as go  # Lazy import
    fig = go.Figure()
    add_edges_to_plotly_graph(fig, edge_x, edge_y)
    add_color_to_nodes(fig, node_x, node_y, node_degree, graph)
    highlight_path(path, pos, fig)
    beautify_graph(fig)
    return fig


def create_figure(graph, edge_x, edge_y, node_x, node_y, node_degree):
    """
    Creates a figure with the graph.
    :param graph:
    :param edge_x:
    :param edge_y:
    :param node_x:
    :param node_y:
    :param node_degree:
    :return:
    """
    import plotly.graph_objects as go  # Lazy import
    fig = go.Figure()
    add_edges_to_plotly_graph(fig, edge_x, edge_y)
    add_color_to_nodes(fig, node_x, node_y, node_degree, graph)
    beautify_graph(fig)
    return fig


def display_algorithm_results(algorithm_name, path, graph, pos, edge_x, edge_y, node_x, node_y, node_degree, start_node,
                              target_node):
    """
    Displays the results of the algorithm in the Streamlit app.
    :param algorithm_name:
    :param path:
    :param graph:
    :param pos:
    :param edge_x:
    :param edge_y:
    :param node_x:
    :param node_y:
    :param node_degree:
    :param start_node:
    :param target_node:
    :return:
    """
    import streamlit as st  # Lazy import
    st.title(f"{algorithm_name} algorithm")
    if path != -1:
        fig = create_figure_with_highlighted_path(graph, pos, edge_x, edge_y, node_x, node_y, node_degree, path)
        st.write(f"Path found from {start_node} to {target_node}: {' -> '.join(path)}")
    else:
        fig = create_figure(graph, pos, edge_x, edge_y, node_x, node_y)
        st.write("No path found.")
    st.plotly_chart(fig, use_container_width=True)
