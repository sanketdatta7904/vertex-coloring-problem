
import time
import multiprocessing

from helper import graph_from_file, is_valid_coloring
from heuristic import ldf
from approximation import randomized_greedy_coloring
from parallel_approximation import randomized_greedy_coloring_parallel
from exact import graph_coloring_exact
from sample_graph_small import graph351, graphBig, graphBipartite, graphConnected




def run(graph):


# Heuristic algorithm
    cm_time_sta_1 = time.time()
    res1 = ldf(graph)
    print("Heuristic result>>", res1)
    colors_used_1  = max(res1.values())+1
    print("Number of colors used in Heuristic>>", colors_used_1)
    cm_time_end_1 = time.time()
    cm_tim_1 = cm_time_end_1 - cm_time_sta_1
    print("Heuristic graph coloring time(sec) = %f" %cm_tim_1)
    print("Testing Heuristic result >> ",is_valid_coloring(graph, res1))
    # result1 = [max(res1.values())+1, cm_tim_1]

# Approximation algorithm
    cm_time_sta_2 = time.time()
    res2 = randomized_greedy_coloring(graph)
    print("Approximation result>>", res2)
    colors_used_2  = max(res2.values())+1
    print("Number of colors used in Approximation>>", colors_used_2)
    cm_time_end_2 = time.time()
    cm_tim_2 = cm_time_end_2 - cm_time_sta_2
    print("Approximation graph coloring time(sec) = %f" %cm_tim_2)
    print("Testing approximation result >> ",is_valid_coloring(graph, res2))
    # result2 = [max(res2.values())+1, cm_tim_2]
  
# PArallel approximation algorithm
    print("Enter cores to be used for parallel computing")
    num_processes = int(input())
    cm_time_sta_3 = time.time()
    if(num_processes == 0):
        num_processes = multiprocessing.cpu_count()
    res3 = randomized_greedy_coloring_parallel(graph, num_processes)
    print("Approximation(Parallel) result>>", res3)
    colors_used_3  = max(res3.values())+1
    print("Number of colors used in Heuristic>>", colors_used_3)    
    cm_time_end_3 = time.time()
    cm_tim_3 = cm_time_end_3 - cm_time_sta_3
    print("Approximation graph coloring(Parallel) time(sec) = %f" %cm_tim_3)
    print("Testing approximation(parallel) result >> ",is_valid_coloring(graph, res3))
    

# Exact algorithm using bounded search tree
    print("enter the bound to be used for bounded search tree. Suggested less than or equal to =", min(colors_used_1, colors_used_2, colors_used_3))
    k = int(input())
    timeOutFlag = False
    cm_time_sta_4 = time.time()
    # res = graph_coloring_exact(graph, k, q)

    # Using queue to  be used for storing result
    q = multiprocessing.Queue()
    res = multiprocessing.Process(target=graph_coloring_exact, name="graph_coloring_exact", args=(graph, k, q))
    res.start()
    # Setting timeout of 30 seconds for the function
    res.join(30)
    if res.is_alive():
        print("30 seconds passed with no response")
        res.terminate()
        res.join()
        res = None
        timeOutFlag = True
    else:
        res = q.get()
    
    print("Exact coloring result>>", res)
    cm_time_end_4 = time.time()
    cm_tim_4 = cm_time_end_4 - cm_time_sta_4
    print("Exact graph coloring time(sec) = %f" %cm_tim_4)

    if(res!= None):
        print("Number of colors used in exact>>", max(res.values())+1)
        print("Testing Exact algorithm result >> ",is_valid_coloring(graph, res))

    else:
        if(timeOutFlag == True):
            print("Timeout after 30 seconds")
        print("Can't color with", k, "colors")
    



if __name__ == '__main__':
    print("Please choose 1 If you want to test in small file(sample_graph_small.py) or 2 for big files(vc test cases) or 3 to test all testcases with heuristic and approximation solution")
    choice = int(input())
    if(choice == 1):
        print("You have chosen to test in small graphs available in sample_graph_small.py")
        print("Please choose any 1 out of 4 graphs(graph351(1), graphBig(2), graphBipartite(3), graphConnected(4))")
        graphno = int(input())
        if(graphno == 1):
            graph = graph351
        elif(graphno == 2):
            graph = graphBig
        if(graphno == 3):
            graph = graphBipartite
        elif(graphno == 4):
            graph = graphConnected
        run(graph)
        
    elif(choice == 2):
        print("You have chosen to test in test cases used from PACE challenge, available in pace2019_track1_vc_exact_all folder")
        print("choose the serial number of the file to be tested.for file named vc-exact_040.gr enter 40")
        graphNo = int(input())
        graphNo = f"{graphNo:03}"
        fileName = f"./Exam-Sanket/pace2019_track1_vc_exact_all/vc-exact_{graphNo}.gr"
        graph = graph_from_file(fileName)
        graph = graph[0]
        run(graph)

    
    
