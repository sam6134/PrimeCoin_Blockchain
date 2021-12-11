import pandas as pd
import matplotlib.pyplot as plt
import json
from typing import List

def getMeanByVariance(data: List[dict], minerType: str) -> List[int]:
    """
        Finds the mean of the data by the variance.
    """
    meanByVariance = []
    for dataPoint in data:
        if(minerType == 'A'):
            meanByVariance.append(dataPoint['MeanA']/dataPoint['VarA'])
        else:
            meanByVariance.append(dataPoint['MeanB']/dataPoint['VarB'])
    return meanByVariance



if __name__ == '__main__':

    OPT = 'ML' # change this to 'ML' or 'C' or 'SL' 
    # depending on the type of staking

    OPTIONS = {
        'ML': 'MLPOS_MV.json',
        'SL': 'SLPOS_MV.json',
        'C': 'CPOS_MV.json',
        'PoW': 'PoW_MV.json'
    }    

    data = json.loads(open(OPTIONS[OPT]).read())
    plotA = True
    plotB = True

    # plot mean/variance for each Miner
    plt.title('Mean/Variance for each Miner for ' + OPT )
    plt.ylabel('Mean/Variance')
    if plotA:
        xValues = list(data.keys())
        yValues = getMeanByVariance(list(data.values()), 'A')
        plt.plot(xValues, yValues, color='red', marker='o', linestyle='solid',linewidth=2)
        yValues = [data[key]['TheoreticA'] for key in data.keys()]
        plt.plot(xValues, yValues, color='green', marker='x', linestyle='dashed',linewidth=2)
        
    if plotB:
        xValues = list(data.keys())
        yValues = getMeanByVariance(list(data.values()), 'B')
        plt.plot(xValues, yValues, color='blue', marker='o', linestyle='solid',linewidth=2)
        yValues = [data[key]['TheoreticB'] for key in data.keys()]
        plt.plot(xValues, yValues, color='orange', marker='x', linestyle='dashed',linewidth=2)
    
    if plotA and plotB:
        plt.legend(['Miner A',  "TheoreticA" ,'Miner B', "TheoreticB"])
    elif plotA:
        plt.legend(['Miner A', 'TheoreticA'])
    else:
        plt.legend(['Miner B', 'TheoreticB'])

    plt.show()