from collections import deque


def bfs_algorithm(graph, start_node, target_node):
    # Crear una cola para BFS que almacene los nodos a explorar y el camino hasta cada nodo
    queue = deque([(start_node, [start_node])])

    # Conjunto para almacenar los nodos ya visitados
    visited = set()

    while queue:
        # Sacar el primer nodo de la cola
        current_node, path = queue.popleft()

        # Si este nodo es el objetivo, regresamos el camino
        if current_node == target_node:
            return path

        # Si no, agregamos los vecinos de este nodo a la cola
        if current_node not in visited:
            visited.add(current_node)
            for neighbor in graph.neighbors(current_node):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

    # Si el BFS termina sin encontrar el nodo objetivo
    return -1
