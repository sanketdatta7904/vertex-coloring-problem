

# This function takes input of the filename for pace challenge and return output of the adjacency list graph and sum of vertices and edges
def graph_from_file(fileName):
    graph1 = {}
    edges1 = []
    with open(fileName, 'r', encoding='utf-8') as f:
        print(f)
        firstline = True
        linecount = 0
        for line in f:
            linecount = linecount+1
            # print(line)
            if(firstline == True):
                v = line.strip().split(" ")[2]
                e = line.strip().split(" ")[3]
                firstline = False
            else:
                src = line.strip().split(" ")[0]
                dst = line.strip().split(" ")[1]
                edges1.append([src, dst])
                if (src in graph1):
                    graph1[src].append(dst)
                else:
                    graph1[src] = [dst]
                if(dst in graph1):
                    graph1[dst].append(src)
                else:
                    graph1[dst] = [src]
            # if(linecount > 100):
            #     break
    return [graph1, v+e]

        
# checks if the given vertex coloring is a valid solution for the input graph or not
def is_valid_coloring(graph, coloring):
    for node in graph:
        for neighbor in graph[node]:
            # checking if no adjacent vertices have the same color 
            if coloring[node] == coloring[neighbor]:
                # print(node, neighbor)
                return False
    return True

# This function finds the vertice with the highest degree of a graph
def findHighestDegree(graph):
    if(len(graph.keys()) == 0):
        return 0
    h = 0
    vertice = 'a'
    for v, neighbors in graph.items():
        n_size = len(neighbors)
        if (n_size > h):
            h = n_size
            vertice = v
    return h, vertice


    # q = multiprocessing.Queue()
    # res = multiprocessing.Process(target=graph_coloring_exact, name="graph_coloring_exact", args=(graph, k, q))
    # res.start()
    # res.join(10)
    # if res.is_alive():
    #     print("10 seconds passed with no response")
    #     res.terminate()
    #     res.join()
    #     res = None
    #     timeOutFlag = True
    # else:
    #     res = q.get()
