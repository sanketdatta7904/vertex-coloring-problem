def ldf(graph):
    # Initialize the coloring to all -1's (i.e., uncolored)
    coloring = {v: None for v in graph}

    # Sort the vertices in decreasing order of degree
    vertices = sorted(graph.keys(), key=lambda x: len(graph[x]), reverse=True)

    # Color the vertices in order
    for v in vertices:
        # Find the smallest unused color for the vertex
        used_colors = set(coloring[n] for n in graph[v] if coloring[n] != None)
        available_colors = set(range(len(graph))) - used_colors
        color = min(available_colors)

        # Color the vertex
        coloring[v] = color

    return coloring
