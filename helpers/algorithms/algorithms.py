from heapq import heappop, heappush
from collections import deque


def bfs_algorithm(graph, start_node, target_node):
    # Create a queue for BFS that stores the nodes to explore and the path to each node
    queue = deque([(start_node, [start_node])])

    # Set to store the nodes already visited
    visited = set()

    while queue:
        # Remove the first node from the queue
        current_node, path = queue.popleft()

        # If this node is the target, return the path
        if current_node == target_node:
            return path

        # Otherwise, add the neighbors of this node to the queue
        if current_node not in visited:
            visited.add(current_node)
            for neighbor in graph.neighbors(current_node):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

    # If BFS ends without finding the target node
    return -1


def dfs_algorithm(graph, start_node, target_node):
    # Stack to store the nodes to explore along with the path taken to reach them
    stack = [(start_node, [start_node])]

    # Set to store the nodes already visited to avoid cycles
    visited = set()

    while stack:
        # Pop the last added node from the stack
        current_node, path = stack.pop()

        # If this node is the target, return the path
        if current_node == target_node:
            return path

        # Mark the node as visited
        if current_node not in visited:
            visited.add(current_node)

            # Add the neighbors to the stack
            for neighbor in graph.neighbors(current_node):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    # If DFS ends without finding the target node
    return -1


def dijkstra_algorithm(graph, start_node, target_node):
    # Priority queue to store (distance, node, path) tuples
    priority_queue = [(0, start_node, [start_node])]

    # Dictionary to store the shortest distance from start_node to every other node
    distances = {node: float('infinity') for node in graph.nodes}
    distances[start_node] = 0

    # Set to store visited nodes
    visited = set()

    while priority_queue:
        # Pop the node with the smallest distance
        current_distance, current_node, path = heappop(priority_queue)

        # If target node is reached, return the path
        if current_node == target_node:
            return path

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor in graph.neighbors(current_node):
            # Calculate new distance
            weight = graph[current_node][neighbor].get('weight', 1)  # Default weight is 1 if not specified
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heappush(priority_queue, (new_distance, neighbor, path + [neighbor]))

    # If Dijkstra's algorithm ends without finding the target node
    return -1
