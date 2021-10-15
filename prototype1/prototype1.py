import sys
import os
import time
import random
import threading
import subprocess
import numpy as np
from pymoo.algorithms.soo.nonconvex.de import DE
from pymoo.optimize import minimize
from pymoo.factory import get_sampling
from multiprocessing.pool import ThreadPool
from pymoo.core.problem import starmap_parallelized_eval
from pymoo.core.problem import ElementwiseProblem

#Defining problem class
class BestScore(ElementwiseProblem):

    def __init__(self, **kwargs):
        super().__init__(n_var=7,n_obj=1,n_constr=0,xl=0,xu=19,**kwargs)
    def _evaluate(self,x,out,*args,**kwargs):
        path = f"./CarlSAT -a {parameter_a[x[0]]} -b {parameter_b[x[1]]} -c {parameter_c[x[2]]} -e {parameter_e[x[3]]} -f {parameter_f[x[4]]} -r {parameter_r[x[5]]} -x {parameter_x[x[6]]} -t {solver_runtime} -v 2 -z {wcard_name}"                                                            #Formatted string which represents the terminal command needed to run carlsat with the sampled commands
        result = subprocess.Popen(path, stdout=subprocess.PIPE,shell=True)    #Output is returned to thread to ensure thread safety
        output = result.communicate()[0].splitlines()
        cost =0
        for i in range(len(output)-1,-1,-1):                                  #We parse through the output to find the best cost achieved in that run
            line = str(output[i])
            if (line.find("after") != -1):
                temp = line[line.find(")")+5::]
                cost = int(temp[0:temp.find(" ")].replace(",",""))
                break    
        out["F"] = [cost]
        

##functions

#creating the threads to run the DE algorithm in parallel
def createThreads():
    threads =6
    pool = ThreadPool(threads)
    return pool
def readEnvironmentalVariables():
    wcard_name = os.getenv('filename')
    solver_runtime = int(os.getenv('timeout'))
    return wcard_name, solver_runtime
    
################### Running program
parameter_a = [1,2,5, 12, 17, 25, 50, 100,113, 125, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000]    #values are chosen to be "random" while also covering the valid sample space as evenly as possible
parameter_b = [1,2,3,5,10,12,25,50,100,125,150,200,300,400,500,600,700,800,900,1000]
parameter_c =[10,50,100,500,1000,3000,7000,10000,25000,50000,100000,200000,300000,400000,500000,600000,700000,800000,900000,1000000]
parameter_e = [0.1,0.5,1,2,5,10,25,50,75,100,150,200,300,400,500,600,700,800,900,1000]
parameter_f = [0.1,0.2,0.5,0.75,1,5,10,25,50,100,150,200,300,400,500,600,700,800,900,1000]
parameter_r = [0,1,2,3,5,10,12,15,20,25,30,40,50,60,70,75,80,90,95,100]
parameter_x = [1,2,5,10,50,100,150,250,500,750,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]

wcard_name, solver_runtime = readEnvironmentalVariables()
pool=createThreads()     # Allows the differential evolution algorithm to run horizontal runs in parallel
problem = BestScore(runner=pool.starmap, func_eval=starmap_parallelized_eval)      #Initialises the problem class 
algorithm = DE(pop_size=36,sampling=get_sampling("int_random"))                    #Defines the parameters that the differential algorithm is going to use including a population size of 36
res = minimize(problem,algorithm,("n_gen",29),verbose=True,seed=1)                 #Performs the optimization of the single objective over 29 generations and keeps track of the set of sampled parameters which produced the best output
print("Parameters that created the best score : ",end="")
best = [parameter_a[res.X[0]],parameter_b[res.X[1]],parameter_c[res.X[2]],parameter_e[res.X[3]],parameter_f[res.X[4]],parameter_r[res.X[5]],parameter_x[res.X[6]]]
print(best)
