def getTheoreticPoWMV(cpuPowerA: int, cpuPowerB: int, n:int):
    p = cpuPowerA/(cpuPowerA+cpuPowerB)
    thMean1 =  n*p
    thVar1 = n*p*(1-p)

    thMean2 = n*(1-p)
    thVar2 = n*(1-p)*p

    return thMean1/thVar1, thMean2/thVar2

def getTheoreticMLPoSMV(stakesA: int, stakesB: int, n:int):
    p = stakesA/(stakesA+stakesB)
    thMean1 =  n*p
    thVar1 = n*p*(1-p)

    thMean2 = n*(1-p)
    thVar2 = n*(1-p)*p
    return thMean1/thVar1, thMean2/thVar2

def getTheoreticSLPoSMV(stakesA: int, stakesB: int, n:int):
    stakesA, stakesB = min(stakesA, stakesB), max(stakesA, stakesB)
    p = stakesA/(2*stakesB)
    thMean1 =  n*p
    thVar1 = n*p*(1-p)

    thMean2 = n*(1-p)
    thVar2 = n*(1-p)*(p)
    return thMean2/thVar2, thMean1/thVar1