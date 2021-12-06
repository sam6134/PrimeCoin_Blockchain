from slPosSimulation import slSimulator
from mlPosSimulation import mlSimulator
from cPosSimulation import cPosSimulation
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

RATIOS = [0.1, 0.2, 0.4, 0.6, 0.8]
NUM_SIMULATIONS = 100
LIMIT = 1000
DIFFICULTY = (1<<235)
meanVar = {}
for ratio in RATIOS:
    rewardsA  = []
    rewardsB  = []
    for simNumber in range(NUM_SIMULATIONS):
        print("Simulation number:", simNumber+1)
        sim = mlSimulator(int(1000/ratio), 1000, DIFFICULTY, LIMIT)
        nA, nB = sim.start()
        rewardsA.append(nA)
        rewardsB.append(nB)
    meanVar[ratio] = {"MeanA": mean(rewardsA),      
                    "VarA": variance(rewardsA), 
                    "MeanB":mean(rewardsB), 
                    "VarB": variance(rewardsB)}

json.dump(meanVar, open("MLPOS_MV.json", "w"))
    