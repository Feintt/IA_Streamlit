"""
Este modulo es el más importante de todos, ya que contiene las funciones que
implementan los algoritmos de búsqueda de caminos.

Los algoritmos implementados son:
- BFS (Breadth-First Search)
- Dijkstra
- DFS (Depth-First Search)
- DFS con límite
- DFS con profundización iterativa

Cada función recibe un grafo, un nodo de origen y un nodo de destino, y opcionalmente
un booleano para indicar si se debe graficar el grafo resultante.

Todos los algoritmos devuelven el número de iteraciones que tomaron para encontrar
el camino, y el tiempo que tardaron en ejecutarse (a excepción de la búsqueda con límite).

Además, cada algoritmo tiene su propia función de tiempo, que se encarga de medir el tiempo
de ejecución de la función que envuelve, y de almacenar el tiempo en un diccionario llamado
`metrics`.

El resultqdo devuelto por cada algortimo tiene el siguiente formato:
- BFS: (Número de iteraciones, tiempo de ejecución)
- Dijkstra: (Número de iteraciones, tiempo de ejecución)
- DFS: (Número de iteraciones, tiempo de ejecución)
- DFS con límite: (True si encontró el camino, False si no, número de iteraciones)
- DFS con profundización iterativa: (Número de iteraciones)

Todas las funciones de búsqueda dependen de los siguientes atributos de los nodos:
- visited: Indica si el nodo ha sido visitado.
- distance: Distancia desde el nodo de origen.
- previous: Nodo previo en el camino.
- size: Tamaño del nodo para visualización.

Además, las funciones de búsqueda utilizan los siguientes estilos para las aristas:
- Unvisited: Estilo predeterminado.
- Visited: Estilo para indicar que la arista ha sido visitada.
- Active: Estilo para indicar que la arista proviene de un nodo activo.
"""

import heapq  # Import the heapq module for priority queue
from helpers import *  # Import all the functions from the helpers module
from collections import deque  # Import the deque class for FIFO queue
from helpers import time_function  # Import the time_function decorator


@time_function
def bfs(graph, start_node, target, plot=False):
    """
    Realiza una búsqueda en amplitud (BFS) en el grafo especificado.

    Esta función explora el grafo por niveles a partir del nodo de origen hasta encontrar el nodo destino. Opcionalmente, puede graficar el grafo una vez encontrado el destino.

    Parameters
    ----------
    graph : Graph
        El grafo sobre el cual realizar la búsqueda.
    start_node : Any
        El nodo de origen de la búsqueda.
    target : Any
        El nodo destino de la búsqueda.
    plot : bool, optional
        Indica si se debe graficar el grafo al encontrar el destino (default es False).

    Returns
    -------
    int
        El número de iteraciones que tomó encontrar el camino.

    """
    # Initialize all nodes: unvisited, infinite distance, no previous node, and default size
    for node in graph.nodes:
        graph.nodes[node]["visited"] = False
        graph.nodes[node]["distance"] = float("inf")  # Set the distance to infinity
        graph.nodes[node]["previous"] = None
        graph.nodes[node]["size"] = 0

    # By default, style all edges as unvisited
    for edge in graph.edges:
        style_unvisited_edge(graph, edge)

    # Set the origin node's distance to 0 and adjust its size for visualization
    graph.nodes[start_node]["distance"] = 0
    graph.nodes[start_node]["size"] = 50
    graph.nodes[target]["size"] = 50

    # Use a deque as a FIFO queue for BFS
    queue = deque([start_node])
    step = 0

    while queue:  # Continue processing nodes while the queue is not empty
        node = queue.popleft()  # Dequeue the next node to process
        if node == target:  # Check if the destination has been reached
            if plot:  # Plot the graph if requested
                plot_graph(graph)  # Plot the graph if requested
            return step  # Return the number of iterations

        if not graph.nodes[node]["visited"]:  # Process node if it hasn't been visited
            graph.nodes[node]["visited"] = True  # Mark the node as visited, so it won't be processed again
            for edge in graph.out_edges(node):  # Process all the edges leading from this node
                style_visited_edge(graph, (edge[0], edge[1], 0))  # Style visited edges
                neighbor = edge[1]  # Get the neighbor node
                if not graph.nodes[neighbor]["visited"]:  # Process the neighbor if it hasn't been visited
                    graph.nodes[neighbor]["distance"] = graph.nodes[node]["distance"] + 1  # Increment distance
                    graph.nodes[neighbor]["previous"] = node  # Set the path to reach this neighbor
                    queue.append(neighbor)  # Enqueue the neighbor for processing
                    for edge2 in graph.out_edges(neighbor):  # Style edges leading from active nodes
                        style_active_edge(graph,
                                          (edge2[0], edge2[1], 0))  # Optional: style edges leading from active nodes
            step += 1


@time_function
def dijkstra(graph, orig, dest, plot=False):
    """
    Realiza el algoritmo de Dijkstra en un grafo desde el nodo de origen
    hasta el nodo de destino.

    Para esto, se utiliza una cola de prioridad para procesar los nodos
    con la distancia más corta primero.

    Una cola de prioridad es una estructura de datos que permite insertar
    elementos con una prioridad asociada, y extraer el elemento con la
    prioridad más alta.

    La prioridad en este caso es la distancia desde el nodo de origen.

    Por ejemplo:
    - Si el nodo A tiene distancia 0, el nodo B tiene distancia 1, y el nodo C
        tiene distancia 2, entonces la cola de prioridad extraerá primero el nodo A,
        luego el nodo B, y finalmente el nodo C.

    Para la cola de prioridad, se utiliza la función `heapq` del módulo `heapq`,
    que permite insertar y extraer elementos de una cola de prioridad.

    :param graph: Grafo que contiene nodos y aristas.
    :param orig: Nodo de origen.
    :param dest: Nodo de destino.
    :param plot: Si es True, grafica el grafo una vez que se encuentra el destino.
    :return: Número de iteraciones que tomó encontrar el camino.
    """

    # By default set all nodes as unvisited
    for node in graph.nodes:
        graph.nodes[node]["visited"] = False
        graph.nodes[node]["distance"] = float("inf")
        graph.nodes[node]["previous"] = None
        graph.nodes[node]["size"] = 0

    # Style edges as unvisited
    for edge in graph.edges:
        style_unvisited_edge(graph, edge)

    graph.nodes[orig]["distance"] = 0
    graph.nodes[orig]["size"] = 50
    graph.nodes[dest]["size"] = 50

    pq = [(0, orig)]
    step = 0

    while pq:  # Continue processing nodes while the priority queue is not empty
        _, node = heapq.heappop(pq)  # Pop the node with the smallest distance
        if node == dest:  # Check if the destination has been reached
            if plot:
                plot_graph(graph)  # Plot the graph if requested
            return step  # Return the number of iterations
        if graph.nodes[node]["visited"]: continue  # Skip processing this node if it has been visited
        graph.nodes[node]["visited"] = True  # Mark the node as visited
        for edge in graph.out_edges(node):  # Process all the edges leading from this node
            style_visited_edge(graph, (edge[0], edge[1], 0))  # Style visited edges
            neighbor = edge[1]  # Get the neighbor node
            weight = graph.edges[(edge[0], edge[1], 0)]["weight"]  # Get the weight of the edge
            if graph.nodes[neighbor]["distance"] > graph.nodes[node]["distance"] + weight:  # Relax the edge
                graph.nodes[neighbor]["distance"] = graph.nodes[node]["distance"] + weight  # Update the distance
                graph.nodes[neighbor]["previous"] = node  # Set the path to reach this neighbor
                heapq.heappush(pq, (graph.nodes[neighbor]["distance"], neighbor))  # Push the neighbor to the queue
                for edge2 in graph.out_edges(neighbor):  # Style edges leading from active nodes
                    style_active_edge(graph, (edge2[0], edge2[1], 0))
        step += 1


@time_function
def dfs(graph, orig, dest, plot=False):
    """
    Realiza una búsqueda en profundidad en un grafo desde el nodo de origen
    hasta el nodo de destino.

    :param graph: Grafo que contiene nodos y aristas.
    :param orig: Nodo de origen.
    :param dest: Nodo de destino.
    :param plot: Si es True, grafica el grafo una vez que se encuentra el destino.
    :return: Número de iteraciones que tomó encontrar el camino.
    """
    # Initialize all nodes: unvisited, infinite distance, no previous node, and default size
    for node in graph.nodes:
        graph.nodes[node]["visited"] = False
        graph.nodes[node]["distance"] = float("inf")
        graph.nodes[node]["previous"] = None
        graph.nodes[node]["size"] = 0

    # Style edges as unvisited
    for edge in graph.edges:
        style_unvisited_edge(graph, edge)

    # Set the origin node's distance to 0 and adjust its size for visualization
    graph.nodes[orig]["distance"] = 0
    graph.nodes[orig]["size"] = 50
    graph.nodes[dest]["size"] = 50

    # Use a stack as a LIFO queue for DFS
    stack = [orig]
    step = 0

    while stack:  # Continue processing nodes while the stack is not empty
        node = stack.pop()  # Pop the last node to process

        if node == dest:  # Check if the destination has been reached
            if plot:  # Plot the graph if requested
                plot_graph(graph)  # Plot the graph if requested
            return step

        if not graph.nodes[node]["visited"]:  # Process node if it hasn't been visited
            graph.nodes[node]["visited"] = True  # Mark the node as visited so it won't be processed again
            for edge in graph.out_edges(node):  # Process all the edges leading from this node
                style_visited_edge(graph, (edge[0], edge[1], 0))  # Style visited edges
                neighbor = edge[1]  # Get the neighbor node
                if not graph.nodes[neighbor]["visited"]:  # Process the neighbor if it hasn't been visited
                    graph.nodes[neighbor]["distance"] = graph.nodes[node]["distance"] + 1  # Increment distance
                    graph.nodes[neighbor]["previous"] = node  # Set the path to reach this neighbor
                    stack.append(neighbor)  # Push the neighbor for processing
                    for edge2 in graph.out_edges(neighbor):  # Style edges leading from active nodes
                        style_active_edge(graph,
                                          (edge2[0], edge2[1], 0))  # Optional: style edges leading from active nodes
            step += 1


@time_function
def dfs_with_limit(graph, orig, dest, limit, plot=False):
    """
    Perform depth-first search on a graph from orig to dest with a depth limit.

    :param graph: Graph object containing nodes and edges.
    :param orig: Starting node.
    :param dest: Destination node.
    :param limit: Maximum depth to search.
    :param plot: If True, plot the graph once the destination is found or the limit is reached.
    """
    # Initialize all nodes: unvisited, infinite distance, no previous node, and default size
    for node in graph.nodes:
        graph.nodes[node]["visited"] = False
        graph.nodes[node]["distance"] = float("inf")
        graph.nodes[node]["previous"] = None
        graph.nodes[node]["size"] = 0

    # Style edges as unvisited
    for edge in graph.edges:
        style_unvisited_edge(graph, edge)

    # Set the origin node's distance to 0 and adjust its size for visualization
    graph.nodes[orig]["distance"] = 0
    graph.nodes[orig]["size"] = 50
    graph.nodes[dest]["size"] = 50

    # Use a stack as a LIFO queue for DFS, including the current depth
    stack = [(orig, 0)]  # (node, depth)
    step = 0

    while stack:
        node, depth = stack.pop()  # Pop the last node to process along with its depth

        if node == dest:  # Check if the destination has been reached
            if plot:
                plot_graph(graph)  # Plot the graph if requested
            return True, step  # Return a flag indicating the path was found and the number of iterations

        if depth <= limit and not graph.nodes[node][
            "visited"]:  # Process node if it hasn't been visited and depth is within limit
            graph.nodes[node]["visited"] = True  # Mark the node as visited so it won't be processed again
            for edge in graph.out_edges(node):  # Process all the edges leading from this node
                style_visited_edge(graph, (edge[0], edge[1], 0))  # Style visited edges
                neighbor = edge[1]  # Get the neighbor node
                if not graph.nodes[neighbor]["visited"]:  # Process the neighbor if it hasn't been visited
                    graph.nodes[neighbor]["distance"] = graph.nodes[node]["distance"] + 1  # Increment distance
                    graph.nodes[neighbor]["previous"] = node  # Set the path to reach this neighbor
                    stack.append((neighbor, depth + 1))  # Push the neighbor and the next depth for processing
                    for edge2 in graph.out_edges(neighbor):  # Style edges leading from active nodes
                        style_active_edge(graph,
                                          (edge2[0], edge2[1], 0))  # Optional: style edges leading from active nodes
            step += 1

    plot_graph(graph)  # Plot the graph if the limit is reached and the destination is not found
    return False, step  # Return a flag indicating the path was not found and the number of iterations


@time_function
def iterative_deepening_dfs(graph, orig, dest, plot=False):
    """
    Realiza una búsqueda en profundidad con profundización iterativa en un grafo
    desde el nodo de origen hasta el nodo de destino.

    Una búsqueda en profundidad con profundización iterativa es similar a una
    búsqueda en profundidad con límite, pero en lugar de fijar un límite, se
    incrementa el límite de profundidad en cada iteración.

    Esto garantiza que el algoritmo encuentre el camino más corto, si existe,
    ya que incrementa el límite de profundidad de manera incremental.

    :param graph: Grafo que contiene nodos y aristas.
    :param orig: Nodo de origen.
    :param dest: Nodo de destino.
    :param plot: Si es True, grafica el grafo una vez que se encuentra el destino.
    :return: Número de iteraciones que tomó encontrar el camino.
    """
    # Initialize the depth limit starting from 0 and incrementally increase
    depth_limit = 0

    while True:  # Keep increasing the depth limit until the destination is found
        # Reinitialize all nodes for each iteration
        for node in graph.nodes:
            graph.nodes[node]["visited"] = False
            graph.nodes[node]["distance"] = float("inf")
            graph.nodes[node]["previous"] = None
            graph.nodes[node]["size"] = 0

        # Style edges as unvisited
        for edge in graph.edges:
            style_unvisited_edge(graph, edge)

        # Set the origin node's distance to 0 and adjust its size for visualization
        graph.nodes[orig]["distance"] = 0
        graph.nodes[orig]["size"] = 50
        graph.nodes[dest]["size"] = 50

        # Initialize the stack with the starting node and its initial depth
        stack = [(orig, 0)]
        step = 0
        path_found = False

        while stack:
            node, depth = stack.pop()  # Pop the last node to process along with its depth

            if depth > depth_limit:  # Skip processing this node if it exceeds the current depth limit
                continue  # Skip processing this node if it exceeds the current depth limit

            if node == dest:  # Check if the destination has been reached
                if plot:
                    plot_graph(graph)  # Plot the graph if requested
                path_found = True  # Set the flag to indicate the path has been found
                break  # Exit the loop if destination is found

            if not graph.nodes[node]["visited"]:  # Process node if it hasn't been visited
                graph.nodes[node]["visited"] = True  # Mark the node as visited so it won't be processed again
                for edge in graph.out_edges(node):  # Process all the edges leading from this node
                    neighbor = edge[1]  # Get the neighbor node
                    if not graph.nodes[neighbor]["visited"]:  # Process the neighbor if it hasn't been visited
                        graph.nodes[neighbor]["distance"] = graph.nodes[node]["distance"] + 1  # Increment distance
                        graph.nodes[neighbor]["previous"] = node  # Set the path to reach this neighbor
                        stack.append((neighbor, depth + 1))  # Push the neighbor with incremented depth
                        style_visited_edge(graph, (edge[0], edge[1], 0))  # Style visited edges
                        for edge2 in graph.out_edges(neighbor):  # Style edges leading from active nodes
                            style_active_edge(graph, (edge2[0], edge2[1], 0))
                step += 1

        if path_found:
            break  # Break the outer loop if the path has been found
        depth_limit += 1  # Increase the depth limit for the next iteration

    if not path_found and plot:  # Plot the graph if the destination is not found
        print("No path found within the given depth.")
        plot_graph(graph)  # Plot the graph if the destination is not found

    return step
