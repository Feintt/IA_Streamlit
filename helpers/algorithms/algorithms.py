import heapq
from helpers import *
from collections import deque
from helpers import time_function


@time_function
def bfs(graph, orig, dest, plot=False):
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

    # Use a deque as a FIFO queue for BFS
    queue = deque([orig])
    step = 0

    while queue:
        node = queue.popleft()  # Dequeue the next node to process
        if node == dest:  # Check if the destination has been reached
            if plot:
                plot_graph(graph)  # Plot the graph if requested
                return step
            return

        if not graph.nodes[node]["visited"]:  # Process node if it hasn't been visited
            graph.nodes[node]["visited"] = True
            for edge in graph.out_edges(node):
                style_visited_edge(graph, (edge[0], edge[1], 0))  # Style visited edges
                neighbor = edge[1]
                if not graph.nodes[neighbor]["visited"]:
                    graph.nodes[neighbor]["distance"] = graph.nodes[node]["distance"] + 1  # Increment distance
                    graph.nodes[neighbor]["previous"] = node  # Set the path to reach this neighbor
                    queue.append(neighbor)  # Enqueue the neighbor for processing
                    for edge2 in graph.out_edges(neighbor):
                        style_active_edge(graph,
                                          (edge2[0], edge2[1], 0))  # Optional: style edges leading from active nodes
            step += 1


@time_function
def dijkstra(graph, orig, dest, plot=False):
    for node in graph.nodes:
        graph.nodes[node]["visited"] = False
        graph.nodes[node]["distance"] = float("inf")
        graph.nodes[node]["previous"] = None
        graph.nodes[node]["size"] = 0

    for edge in graph.edges:
        style_unvisited_edge(graph, edge)

    graph.nodes[orig]["distance"] = 0
    graph.nodes[orig]["size"] = 50
    graph.nodes[dest]["size"] = 50

    pq = [(0, orig)]
    step = 0

    while pq:
        _, node = heapq.heappop(pq)
        if node == dest:
            if plot:
                plot_graph(graph)
                return step
            return
        if graph.nodes[node]["visited"]: continue
        graph.nodes[node]["visited"] = True
        for edge in graph.out_edges(node):
            style_visited_edge(graph, (edge[0], edge[1], 0))
            neighbor = edge[1]
            weight = graph.edges[(edge[0], edge[1], 0)]["weight"]
            if graph.nodes[neighbor]["distance"] > graph.nodes[node]["distance"] + weight:
                graph.nodes[neighbor]["distance"] = graph.nodes[node]["distance"] + weight
                graph.nodes[neighbor]["previous"] = node
                heapq.heappush(pq, (graph.nodes[neighbor]["distance"], neighbor))
                for edge2 in graph.out_edges(neighbor):
                    style_active_edge(graph, (edge2[0], edge2[1], 0))
        step += 1


@time_function
def dfs(graph, orig, dest, plot=False):
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

    while stack:
        node = stack.pop()  # Pop the last node to process

        if node == dest:  # Check if the destination has been reached
            if plot:
                plot_graph(graph)
                return step
            return

        if not graph.nodes[node]["visited"]:
            graph.nodes[node]["visited"] = True
            for edge in graph.out_edges(node):
                style_visited_edge(graph, (edge[0], edge[1], 0))  # Style visited edges
                neighbor = edge[1]
                if not graph.nodes[neighbor]["visited"]:
                    graph.nodes[neighbor]["distance"] = graph.nodes[node]["distance"] + 1  # Increment distance
                    graph.nodes[neighbor]["previous"] = node  # Set the path to reach this neighbor
                    stack.append(neighbor)  # Push the neighbor for processing
                    for edge2 in graph.out_edges(neighbor):
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
                plot_graph(graph)
            return True, step

        if depth <= limit and not graph.nodes[node]["visited"]:
            graph.nodes[node]["visited"] = True
            for edge in graph.out_edges(node):
                style_visited_edge(graph, (edge[0], edge[1], 0))  # Style visited edges
                neighbor = edge[1]
                if not graph.nodes[neighbor]["visited"]:
                    graph.nodes[neighbor]["distance"] = graph.nodes[node]["distance"] + 1  # Increment distance
                    graph.nodes[neighbor]["previous"] = node  # Set the path to reach this neighbor
                    stack.append((neighbor, depth + 1))  # Push the neighbor and the next depth for processing
                    for edge2 in graph.out_edges(neighbor):
                        style_active_edge(graph,
                                          (edge2[0], edge2[1], 0))  # Optional: style edges leading from active nodes
            step += 1

    plot_graph(graph)
    return False, step


@time_function
def iterative_deepening_dfs(graph, orig, dest, plot=False):
    """
    Perform an iterative deepening depth-first search from orig to dest.

    :param graph: Graph object containing nodes and edges.
    :param orig: The starting node.
    :param dest: The destination node.
    :param plot: Boolean to indicate whether to plot the graph.
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
            node, depth = stack.pop()

            if depth > depth_limit:
                continue  # Skip processing this node if it exceeds the current depth limit

            if node == dest:
                if plot:
                    plot_graph(graph)
                path_found = True
                break  # Exit the loop if destination is found

            if not graph.nodes[node]["visited"]:
                graph.nodes[node]["visited"] = True
                for edge in graph.out_edges(node):
                    neighbor = edge[1]
                    if not graph.nodes[neighbor]["visited"]:
                        graph.nodes[neighbor]["distance"] = graph.nodes[node]["distance"] + 1
                        graph.nodes[neighbor]["previous"] = node
                        stack.append((neighbor, depth + 1))  # Push the neighbor with incremented depth
                        style_visited_edge(graph, (edge[0], edge[1], 0))  # Style visited edges
                        for edge2 in graph.out_edges(neighbor):
                            style_active_edge(graph, (edge2[0], edge2[1], 0))
                step += 1

        if path_found:
            break  # Break the outer loop if the path has been found
        depth_limit += 1  # Increase the depth limit for the next iteration

    if not path_found and plot:
        print("No path found within the given depth.")
        plot_graph(graph)

    return step
