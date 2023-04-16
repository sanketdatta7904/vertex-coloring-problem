

import random

def randomized_greedy_coloring(graph):
    color_map = {}
    available_colors = {vertice: set(range(len(graph))) for vertice in graph.keys()}
    vertices = list(graph.keys())
    random.shuffle(vertices)
    
    for v in vertices:
        # Find the colors of adjacent vertices
        neighbor_colors = {color_map[neighbor] for neighbor in graph[v] if neighbor in color_map}
        
        # Choose the smallest available color that does not conflict with the colors of adjacent vertices
        v_color = min(available_colors[v] - neighbor_colors)
        color_map[v] = v_color
        
        # Remove the chosen color from the available colors for the v
        available_colors[v].discard(v_color)
        
    return color_map

