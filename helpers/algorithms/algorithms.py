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
