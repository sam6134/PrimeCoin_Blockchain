from slPosSimulation import slSimulator
from mlPosSimulation import mlSimulator
from cPosSimulation import cPosSimulation
from powSimulation import powSimulation
from theoreticFunctions import getTheoreticMLPoSMV, getTheoreticSLPoSMV, getTheoreticPoWMV
from statistics import mean, variance
import json

"""
    experiment- 100 times
    Mine 1000 blocks, 
    a-sum mean SUM(reward)/100
    b-sum mean
            
    a - variance = SUM(x-meanA)^2/n (100)
    b - variance = SUM(x-meanB)^2/n 

    plot mean/variance- ratio [5 values 0.2, 0.4, 0.6, 0.8]
 """

OPT = "C" # "ML" or "SL" or "C" or "PoW"
RATIOS = [2, 4, 6, 8, 10] # for SL ratio 2 doesnot work


NUM_SIMULATIONS = 100
LIMIT = 1000
DIFFICULTY = (1<<235)

simulators = {
    "SL": slSimulator,
    "C": cPosSimulation,
    "PoW": powSimulation,
}

jsonFileNames ={
    "SL": "SLPOS_MV.json",
    "C": "CPOS_MV.json",
    "PoW": "POW_MV.json",
    "ML": "MLPOS_MV.json",
}

getTheoreticMV = {
    "ML": getTheoreticMLPoSMV,
    "PoW": getTheoreticPoWMV,
    "SL": getTheoreticSLPoSMV,
    "C": getTheoreticMLPoSMV,
}

meanVar = {}
for ratio in RATIOS:
    rewardsA  = []
    rewardsB  = []
    for simNumber in range(NUM_SIMULATIONS):
        print("Simulation number:", simNumber+1)

        if OPT == "ML":
            sim = mlSimulator(1000*ratio, 1000, DIFFICULTY, LIMIT)
        elif OPT == "C" or OPT == "SL":
            sim = simulators[OPT](1000*ratio, 1000, LIMIT)
        elif OPT == "PoW":
            sim = simulators[OPT](ratio, 1, LIMIT)
        else:
            raise Exception("Invalid option")

        nA, nB = sim.start()
        rewardsA.append(nA)
        rewardsB.append(nB)
    mvTheoreticA, mvTheoreticB = getTheoreticMV[OPT](ratio, 1, LIMIT)
    meanVar[ratio] = {"MeanA": mean(rewardsA),      
                    "VarA": variance(rewardsA), 
                    "MeanB":mean(rewardsB), 
                    "VarB": variance(rewardsB),
                    "TheoreticA": mvTheoreticA,
                    "TheoreticB": mvTheoreticB}

json.dump(meanVar, open(jsonFileNames[OPT], "w"))
    