import random
import multiprocessing

def color_chunk(graph, vertices, available_colors, color_map, lock):

    for vertex in vertices:
        #acquire a lock before accessing shared variables. ensures that shared variables are accessed atomically using a lock to prevent race conditions.
        lock.acquire()
        # Find the colors of adjacent vertices
        neighbor_colors = {color_map[neighbor] for neighbor in graph[vertex] if neighbor in color_map}
        
        # Choose the smallest available color that does not conflict with the colors of adjacent vertices
        vertex_color = min(available_colors[vertex] - neighbor_colors)

        try:
            color_map[vertex] = vertex_color
            available_colors[vertex].discard(vertex_color)
        finally:
            # Release the lock after updating color_map and available_colors. This ensures that the lock is always released, even if an exception occurs.
            lock.release()

       
        

def randomized_greedy_coloring_parallel(graph, num_processes):
    print('Will be starting parallel processing with cores of count >', num_processes)
    # Create a multiprocessing manager to share dictionaries between processes
    manager = multiprocessing.Manager()
    # Create a shared dictionary to store the vertex-color mapping
    color_map = manager.dict()
    # Create a shared dictionary to store the available colors for each vertex
    available_colors = manager.dict({vertex: set(range(len(graph))) for vertex in graph.keys()})
    vertices = list(graph.keys())
    if(num_processes>len(vertices)):
        print("graph vertices length smaller than number of cores, keeping core count restricted to 1")
        num_processes = 1
    # Shuffle the vertices randomly to balance the load across multiple processes
    random.shuffle(vertices)
    # Create a lock object for thread safety during dictionary updates so that no collision and race condition occur
    lock = manager.Lock()
    # If there are more than 1 processes, split the vertices into chunks and process each chunk in a separate process
    if num_processes >= 1:
        chunk_size = (len(vertices) + num_processes - 1) // num_processes
        # Split the vertices into chunks
        chunks = [vertices[i:i+chunk_size] for i in range(0, len(vertices), chunk_size)]
        # Create a pool of processes
        pool = multiprocessing.Pool(processes=num_processes)
        # Call the color_chunk function for each chunk of vertices and pass the shared dictionaries and lock object
        results = pool.starmap(color_chunk, [(graph, chunk, available_colors, color_map, lock) for chunk in chunks])
        pool.close()
        # Wait for all processes to finish
        pool.join()
    # If there is only 1 process, call the color_chunk function for all vertices
    else:
        color_chunk(graph, vertices, available_colors, color_map)
    # Return the final vertex-color mapping as a dictionary
    return dict(color_map)
    

# if __name__ == '__main__':
#     graph351 = {'A': ['B'],
#             'B': ['C', 'A'],
#             'C': ['B', 'D', 'E'],
#             'D': ['C', 'E', 'F', 'G'],
#             'E': ['C', 'D', 'F'],
#             'F': ['D', 'E'],
#             'G': ['D']}

#     graphBipartite = {'A': ['F', 'G'],
#                   'B': ['F'],
#                   'C': ['H', 'G'],
#                   'D': ['H', 'J'],
#                   'E': ['I', 'J'],
#                   'F': ['A', 'B'],
#                   'G': ['A', 'C'],
#                   'H': ['C', 'D'],
#                   'I': ['E'],
#                   'J': ['D', 'E']}

#     graphConnected = {'A': ['B', 'C', 'D', 'E', 'F', 'G'],
#                   'B': ['A', 'C', 'D', 'E', 'F', 'G'],
#                   'C': ['A', 'B', 'D', 'E', 'F', 'G'],
#                   'D': ['A', 'C', 'B', 'E', 'F', 'G'],
#                   'E': ['A', 'C', 'D', 'B', 'F', 'G'],
#                   'F': ['A', 'C', 'D', 'E', 'B', 'G'],
#                   'G': ['A', 'C', 'D', 'E', 'F', 'B']}


#     graphBig = {'A': ['B', 'E', 'D'],
#             'B': ['A', 'E', 'F', 'C'],
#             'C': ['B', 'F'],
#             'D': ['A', 'E', 'H', 'G'],
#             'G': ['D', 'H', 'K', 'J'],
#             'J': ['G', 'K', 'N', 'M'],
#             'M': ['J', 'N', 'Q', 'P'],
#             'P': ['M', 'Q', 'T', 'S'],
#             'F': ['E', 'B', 'C', 'I'],
#             'I': ['H', 'E', 'F', 'L'],
#             'L': ['K', 'H', 'I', 'O'],
#             'O': ['N', 'K', 'L', 'R'],
#             'R': ['Q', 'N', 'O', 'U'],
#             'E': ['D', 'A', 'B', 'F', 'I', 'H'],
#             'H': ['G', 'D', 'E', 'I', 'L', 'K'],
#             'K': ['J', 'G', 'H', 'L', 'O', 'N'],
#             'N': ['M', 'J', 'K', 'O', 'R', 'Q'],
#             'Q': ['P', 'M', 'N', 'R', 'U', 'T'],
#             'T': ['S', 'P', 'Q', 'U'],
#             'S': ['P', 'T'],
#             'U': ['T', 'Q', 'R']}

#     inputfilename = './Final-Project-Sanket/public/vc-exact_187.gr'
#     graph = graph_from_file(inputfilename)
   
#     cm_time_sta = time.time()
#     res = randomized_greedy_coloring_parallel(graph)
#     print("Approximation(Parallel) result>>", res)
#     print("Number of colors used>>", max(res.values())+1)
#     cm_time_end = time.time()
#     cm_tim = cm_time_end - cm_time_sta
#     print("Approximation graph coloring(Parallel) time(sec) = %f" %cm_tim)
#     print("Testing approximation(parallel) result >> ",is_valid_coloring(graph, res))

    

