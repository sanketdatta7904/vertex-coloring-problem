# The function is_valid checks if the current coloring is valid by iterating over all vertices and their adjacent vertices and checking if they have the same color. If a pair of adjacent vertices have the same color, the function returns False, indicating that the current coloring is invalid.
def is_valid(graph, colors):
    for v in graph:
        if colors[v] is not None:
            for u in graph[v]:
                if colors[u] is not None and colors[u] == colors[v]:
                    return False
    return True

# The function search is a recursive function that tries all possible colorings for a given vertex and then recursively searches for a valid coloring for the next vertex
def search(graph,vertices, colors, k, v):
    # Base case: when all vertices are colored, at which point the function returns the colors.
    if v == len(graph):
        return colors
    
    # Recursive case: try all possible colors for the current vertex
    for color in range(k):
        colors[vertices[v]] = color
        if is_valid(graph, colors):
            result = search(graph,vertices, colors, k, v + 1)
            if result is not None:
                return result
    
    # Backtrack if no valid coloring is found
    colors[vertices[v]] = None
    return None

# Define the main function to solve the graph coloring problem
def graph_coloring_exact(graph, k, q):
    # Initialize the colors of all vertices to None
    colors = {}
    for vertex in graph.keys():
        colors[vertex] = None
    vertices = sorted(graph.keys(), key=lambda x: len(graph[x]), reverse=True)


        # Try all possible number of colors starting from 1
    for num_colors in range(1, k+1):
        result = search(graph,vertices, colors, num_colors, 0)
        if result is not None:
            q.put(result)
            return result
    q.put(None)
    return None
