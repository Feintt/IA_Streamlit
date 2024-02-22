

def execution_time(func):
    """
    Decorator that prints the time it takes for a function to execute.
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
    Extracts the nodes and edges from a CSV file and returns them as lists.
    """
    import pandas as pd  # Lazy import
    nodes = pd.read_csv(nodes_path)['Node'].tolist()
    edges = pd.read_csv(edges_path)
    return nodes, edges


def generate_graph(nodes, edges):
    """
    Generates a graph with NetworkX.
    """
    import networkx as nx  # Lazy import
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_weighted_edges_from(
        [(row['Origin'], row['Destination'], row['Weight']) for index, row in edges.iterrows()])
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
