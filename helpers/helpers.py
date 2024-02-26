"""
Este módulo contiene funciones auxiliares que se utilizan en el proyecto.

La mayoria de librerías que se utilizan en este módulo son importadas
en las funciones que las utilizan, para evitar errores de importación y
mejorar la eficiencia del programa (lazy import).

Las funciones en este módulo son las siguientes:
- time_function: Decorador que mide el tiempo que tarda una función en ejecutarse.
- clean_graph: Limpia el grafo para eliminar atributos innecesarios.
- style_unvisited_edge: Estiliza un arco como no visitado.
- style_visited_edge: Estiliza un arco como visitado.
- style_active_edge: Estiliza un arco como activo.
- style_path_edge: Estiliza un arco como parte de la ruta.
- plot_graph: Grafica el grafo.
- reconstruct_path: Reconstruye la ruta y estiliza los arcos que la componen.
"""

import time  # Import the time module


def time_function(func):
    """
    Decorador que mide el tiempo que tarda una función en ejecutarse.
    :param func: La función que se va a medir.
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
    Esta función limpia el grafo para eliminar atributos innecesarios.

    El grafo devuelto por OSMnx contiene muchos atributos que no son necesarios para este proyecto,
    por lo que esta función se encarga de eliminarlos para reducir el uso de memoria y mejorar la eficiencia.

    La información que se mantiene en el grafo es la siguiente:
    - Nodos:
        - latitud
        - longitud
    - Arcos:
        - longitud
        - maxspeed
        - weight

    A veces los grafos devueltos por OSMnx contienen velocidades máximas en una lista,
    por lo que se toma el primer valor de la lista y se convierte a entero, y en caso
    de que no haya un valor numérico, se asigna 40 km/h por defecto para evitar errores.
    :param graph: El grafo que se va a limpiar.
    :return:
    """
    import re  # Import the regular expressions module

    # Iterate over the edges in the graph
    # An edge looks like this: (start_node, end_node, 0)
    for edge in graph.edges:
        # Standardize the "max_speed" attribute
        max_speed = graph.edges[edge].get("maxspeed", "40")  # Default to "40" if not present
        if isinstance(max_speed, list):  # This means that there are multiple max_speeds
            max_speed = max_speed[0]  # Take the first speed if it's a list

        if isinstance(max_speed, str):  # This means there is only one max_speed
            # Extract numbers from the string. Assumes speed is in mph and needs conversion to km/h if needed.
            num = re.findall(r'\d+', max_speed)
            if num:
                # Convert the first found number to int
                max_speed = int(num[0])
            else:
                # Default to 40 km/h if no number is found
                max_speed = 40
        # Ensure max_speed is an integer
        max_speed = int(max_speed)

        # Update the edge with the standardized max_speed
        graph.edges[edge]["maxspeed"] = max_speed

        """
        En este punto, el atributo "maxspeed" de cada arco en el grafo ha sido estandarizado.
        """

        # Calculate and assign the "weight" attribute based on edge length and max_speed
        # Ensure that max_speed is not zero to avoid division by zero error
        if max_speed > 0:
            graph.edges[edge]["weight"] = graph.edges[edge]["length"] / (
                    max_speed * 1000 / 3600)  # Convert speed to m/s if length is in meters

    return graph


def style_unvisited_edge(graph, edge):
    """
    Estiliza un arco como no visitado con un color naranja y una opacidad del 20%.

    Un arco es un conjunto de dos nodos conectados por una calle,
    y se representa como una tupla (nodo_inicial, nodo_final, 0).

    Un arco no visitado es un arco que no ha sido visitado por el algoritmo de búsqueda.

    Los atributos que se modifican son:
    - color: naranja
    - alpha: 20%
    - linewidth: 0.5

    Todos los "edged" en el grafo tienen estos atributos,
    por lo que se puede modificar directamente.

    Estas son las descripciones de los atributos:
    - color: el color del arco
    - alpha: la opacidad del arco (0 es transparente, 1 es opaco)
    - linewidth: el ancho del arco

    :param graph: El grafo que se va a estilizar.
    :param edge: El arco que se va a estilizar.
    :return:

    """
    graph.edges[edge]["color"] = "#d36206"
    graph.edges[edge]["alpha"] = 0.2
    graph.edges[edge]["linewidth"] = 0.5


def style_visited_edge(graph, edge):
    """
    Estiliza un arco como visitado con un color naranja y una opacidad del 100%.

    Un arco es un conjunto de dos nodos conectados por una calle,
    y se representa como una tupla (nodo_inicial, nodo_final, 0).

    Un arco visitado es un arco que ha sido visitado por el algoritmo de búsqueda.

    Los atributos que se modifican son:
    - color: naranja
    - alpha: 100%
    - linewidth: 1

    Todos los "edged" en el grafo tienen estos atributos,
    por lo que se puede modificar directamente.

    Estas son las descripciones de los atributos:
    - color: el color del arco
    - alpha: la opacidad del arco (0 es transparente, 1 es opaco)
    - linewidth: el ancho del arco

    :param graph: El grafo que se va a estilizar.
    :param edge: El arco que se va a estilizar.
    :return:
    """
    graph.edges[edge]["color"] = "#d36206"
    graph.edges[edge]["alpha"] = 1
    graph.edges[edge]["linewidth"] = 1


def style_active_edge(graph, edge):
    """
    Estiliza un arco como activo con un color amarillo y una opacidad del 100%.

    Un arco es un conjunto de dos nodos conectados por una calle,
    y se representa como una tupla (nodo_inicial, nodo_final, 0).

    Un arco activo es un arco que está siendo visitado por el algoritmo de búsqueda.

    Los atributos que se modifican son:
    - color: amarillo
    - alpha: 100%
    - linewidth: 1

    Todos los "edged" en el grafo tienen estos atributos,
    por lo que se puede modificar directamente.

    Estas son las descripciones de los atributos:
    - color: el color del arco
    - alpha: la opacidad del arco (0 es transparente, 1 es opaco)
    - linewidth: el ancho del arco

    :param graph: El grafo que se va a estilizar.
    :param edge: El arco que se va a estilizar.
    :return:
    """
    graph.edges[edge]["color"] = '#e8a900'
    graph.edges[edge]["alpha"] = 1
    graph.edges[edge]["linewidth"] = 1


def style_path_edge(graph, edge):
    """
    Estiliza un arco como parte de la ruta con un color blanco y una opacidad del 100%.

    Un arco es un conjunto de dos nodos conectados por una calle,
    y se representa como una tupla (nodo_inicial, nodo_final, 0).

    Un arco parte de la ruta es un arco que forma parte de la ruta encontrada
    por el algoritmo de búsqueda.

    Los atributos que se modifican son:
    - color: blanco
    - alpha: 100%
    - linewidth: 1

    Todos los "edged" en el grafo tienen estos atributos,
    por lo que se puede modificar directamente.

    Estas son las descripciones de los atributos:
    - color: el color del arco
    - alpha: la opacidad del arco (0 es transparente, 1 es opaco)
    - linewidth: el ancho del arco

    :param graph: El grafo que se va a estilizar.
    :param edge: El arco que se va a estilizar.
    :return:
    """
    graph.edges[edge]["color"] = "white"
    graph.edges[edge]["alpha"] = 1
    graph.edges[edge]["linewidth"] = 1


def plot_graph(graph):
    """
    Grafica el grafo.

    En esta función se utilizan dos librerías:
    - Streamlit: para mostrar la gráfica en la interfaz de usuario.
    - OSMnx: para graficar el grafo.

    Los atributos que se utilizan para graficar el grafo son:
    - node_size: el tamaño de los nodos
    - edge_color: el color de los arcos
    - edge_alpha: la opacidad de los arcos
    - edge_linewidth: el ancho de los arcos
    - node_color: el color de los nodos
    - bgcolor: el color de fondo del grafo

    Se obtienen 4 listas con estos atributos de los nodos y arcos del grafo,
    y se pasan como argumentos a la función plot_graph de OSMnx.

    Las listas tienen el siguiente formato:
    - node_sizes: [10, 10, 10, 10, ...]
    - edge_colors: ["#d36206", "#d36206", "#d36206", "#d36206", ...]
    - edge_alphas: [0.2, 0.2, 0.2, 0.2, ...]
    - edge_linewidths: [0.5, 0.5, 0.5, 0.5, ...]

    ox.plot_graph por defecto muestra la gráfica en una ventana emergente,
    por lo que se utiliza el argumento show=False para evitar que se muestre.

    Utilizamos manualmente st.pyplot para mostrar la gráfica en la interfaz de usuario.

    :param graph: El grafo que se va a graficar.
    :return:
    """
    # Lazy import necessary libraries
    import streamlit as st
    import osmnx as ox

    # Extract the node sizes, edge colors, edge alphas, and edge linewidths from the graph
    node_sizes = [graph.nodes[node]["size"] for node in graph.nodes]
    edge_colors = [graph.edges[edge]["color"] for edge in graph.edges]
    edge_alphas = [graph.edges[edge]["alpha"] for edge in graph.edges]
    edge_linewidths = [graph.edges[edge]["linewidth"] for edge in graph.edges]

    # Configure and plot the graph
    fig, ax = ox.plot_graph(
        graph,
        node_size=node_sizes,  # size of the nodes: if 0, then skip plotting the nodes
        edge_color=edge_colors,  # color(s) of the edges' lines
        edge_alpha=edge_alphas,  # opacity of the edges' lines
        edge_linewidth=edge_linewidths,  # width of the edges' lines: if 0, then skip plotting the edges
        node_color="white",  # color(s) of the nodes
        bgcolor="#18080e",  # background color of plot
        show=False,  # if True, call pyplot.show() to show the figure
    )

    # Display the plot in a Streamlit app
    st.pyplot(fig, use_container_width=True)


def reconstruct_path(graph, orig, dest, plot=False):
    """
    Reconstruye la ruta y estiliza los arcos que la componen.

    Esta función toma el grafo, el nodo de origen, el nodo de destino, y reconstruye la ruta
    utilizando el atributo "previous" de los nodos.

    El atributo "previous" de un nodo es el nodo que lo visitó en la búsqueda, por lo que
    se puede iterar desde el nodo de destino hasta el nodo de origen para reconstruir la ruta.

    La ruta se reconstruye desde el nodo de destino hasta el nodo de origen, y se estilizan
    los arcos que la componen para resaltarla.

    Los atributos que se modifican son:
    - color: blanco
    - alpha: 100%
    - linewidth: 1

    Todos los "edged" en el grafo tienen estos atributos,
    por lo que se puede modificar directamente.

    Estas son las descripciones de los atributos:
    - color: el color del arco
    - alpha: la opacidad del arco (0 es transparente, 1 es opaco)
    - linewidth: el ancho del arco

    :param graph: El grafo que se va a estilizar.
    :param orig: El nodo de origen.
    :param dest: El nodo de destino.
    :param plot: Si es True, se grafica el grafo.
    :return:
    """

    # By default, set all edges to unvisited
    for edge in graph.edges:
        style_unvisited_edge(graph, edge)
    dist = 0  # Total distance
    speeds = []  # List of speeds
    curr = dest  # Start at the destination
    while curr != orig:  # While we haven't reached the origin
        prev = graph.nodes[curr]["previous"]  # Get the previous node
        dist += graph.edges[(prev, curr, 0)]["length"]  # Add the length of the edge to the total distance
        speeds.append(graph.edges[(prev, curr, 0)]["maxspeed"])  # Add the speed to the list of speeds
        style_path_edge(graph, (prev, curr, 0))  # Style the edge as part of the path
        curr = prev  # Move to the previous node
    dist /= 1000  # Convert distance to kilometers

    # If plot is True, plot the graph
    if plot:
        plot_graph(graph)

        try:
            # Return the distance, average speed, and time
            return dist, sum(speeds) / len(speeds), dist / (sum(speeds) / len(speeds)) * 60
        except ZeroDivisionError:
            return dist, 0, 0
