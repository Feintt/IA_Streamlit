import time
import pandas as pd


def execution_time(func):
    """
    Decorator that prints the time it takes for a function to execute.
    """

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"The function {func.__name__} took {end - start} seconds to execute.")
        return result

    return wrapper


def extract_nodes_and_edges_from_csv(file_path):
    """
    Extracts the nodes and edges from a CSV file and returns them as lists.
    """
    nodes = pd.read_csv(file_path + "nodes.csv")
    edges = pd.read_csv(file_path + "edges.csv")
    return nodes, edges
