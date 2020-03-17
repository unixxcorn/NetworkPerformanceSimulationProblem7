"""
Author: Unixcorn
Description: This is a part of Network Performance problem #7 in the simulation part. the problem 
is Client creates a session on the webserver. The webserver has 2 components Server A and B. 
Server A have processing delay mean 10 seconds (exponential distributed) and Server B have 
processing delay mean 15 seconds (exponential distributed). If total times more than 40 seconds 
the system will raise system timeout error. The goal of this simulation needs to find the average 
time of this model and the probability that it timed out.
"""

import json
from numba import njit
from tools import plotter
from numpy import random
from timeit import default_timer as timer

@njit
def simulation(n, server_A=10, server_B=15, timeout=40, sampling=10):
    avgA = 0
    avgB = 0
    avgS = 0
    ctimeout = 0
    dic = {}
    for i in range(n):
        A = random.exponential(server_A)
        B = random.exponential(server_B)
        S = A + B
        if S > timeout:
            ctimeout = ctimeout + 1
        avgA = ((avgA * i) + A) / (i + 1)
        avgB = ((avgB * i) + B) / (i + 1)
        avgS = ((avgS * i) + S) / (i + 1)
    
        S = ((S * sampling) // 1) / sampling
        if S not in dic:
            dic[S] = 0
        dic[S] += 1
    return avgS, ctimeout/n, dic

def main(n, sampling, output="./out/output"):
    print("> running : %d times \n> Starting..." % n)

    start = timer()
    avg, timeout, dic = simulation(n, sampling=sampling)

    print("> End of Simulation in %.2f sec\n> Formatting output" % (timer()-start))

    json_dic = {}
    for key in dic:
        json_dic["{:0.02f}".format(key)] = dic[key]
    json_out = json.dumps(json_dic, sort_keys=True)

    f = open(output +'.json', 'w+')
    f.write('{ "average": %.08f, "timeout": %.08f, "records": %s }' % (avg, timeout, json_out))

    plotter(dic, 'Histrograms from ' + str("{:.2e}".format(n)) + ' loops and sampling ' + str(1/sampling) + ' sec. ', 'Total processing time', '', output)

    print("> Complete %.2f sec" % (timer()-start))
