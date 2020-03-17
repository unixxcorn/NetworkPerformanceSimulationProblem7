"""
Author: Unixcorn
Description: This is a part of Network Performance problem #7 in the simulation part. the problem 
is Client creates a session on the webserver. The webserver has 2 components Server A and B. 
Server A have processing delay mean 10 seconds (exponential distributed) and Server B have 
processing delay mean 15 seconds (exponential distributed). If total times more than 40 seconds 
the system will raise system timeout error. The goal of this simulation needs to find the average 
time of this model, the probability that it timed out and optimize the failure lower than 10%.
"""

import json
from numba import njit, jit
from tools import plotter
from numpy import random, zeros
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


@jit
def simulationManyInput(n, server_A, server_B, timeout=40):
    AverageArray = [0.0] * (server_B * server_A)
    timeoutArray = [0.0] * (server_B * server_A)
    for servA in range(server_A):
        for servB in range(server_B):
            avgS = 0
            ctimeout = 0
            for i in range(n):
                A = random.exponential(servA)
                B = random.exponential(servB)
                S = A + B
                if S > timeout:
                    ctimeout = ctimeout + 1
                avgS = ((avgS * i) + S) / (i + 1)
            AverageArray[(servA * server_B) + servB] = avgS
            timeoutArray[(servA * server_B) + servB] = ctimeout / n
    return AverageArray, timeoutArray


def one_simulation(n, sampling, output="./out/output", server_A=10, server_B=15):
    print("> running : %d times \n> Starting..." % n)

    start = timer()
    avg, timeout, dic = simulation(n, server_A, server_B, sampling=sampling)

    print("> End of Simulation in %.2f sec\n> Formatting output" % (timer()-start))

    json_dic = {}
    for key in dic:
        json_dic["{:0.02f}".format(key)] = dic[key]
    json_out = json.dumps(json_dic, sort_keys=True)

    f = open(output + '.json', 'w+')
    f.write('{ "average": %.08f, "timeout": %.08f, "records": %s }' %
            (avg, timeout, json_out))

    plotter(dic, 'Histrograms from ' + str("{:.2e}".format(n)) + ' loops and sampling ' + str(
        1/sampling) + ' sec. ', 'Total processing time', '', output)

    print("> Complete %.2f sec" % (timer()-start))


def many_simulation(n, sampling, output="./out/output", server_A=10, server_B=15, interestedProb=0.1):
    print("> running : %d times \n> Starting..." % n)
    start = timer()
    server_A = server_A + 1
    server_B = server_B + 1

    avg, timeout = simulationManyInput(n, server_A, server_B)

    avg2d = zeros((server_A, server_B))
    timeout2d = zeros((server_A, server_B))
    optimaltimeout = 0
    optimalValue = [0, 0]
    for servA in range(server_A):
        for servB in range(server_B):
            avg2d[servA, servB] = avg[servA * server_B + servB]
            timeout2d[servA, servB] = timeout[servA * server_B + servB]
            if timeout[servA * server_B + servB] < interestedProb and timeout[servA * server_B + servB] > optimaltimeout:
                optimaltimeout = timeout[servA * server_B + servB]
                optimalValue[0] = servA
                optimalValue[1] = servB

    f = open(output + '_multiple.json', 'w+')
    f.write(json.dumps({"serverA": server_A, "serverB": server_B, "average": avg2d.tolist(), "timeout": timeout2d.tolist(
    ), "optimal": {"timeout": optimaltimeout, "server A": optimalValue[0], "server B": optimalValue[1], "Optimal average": avg2d[optimalValue[0], optimalValue[1]]}}))

    print("> Complete %.2f sec" % (timer()-start))
