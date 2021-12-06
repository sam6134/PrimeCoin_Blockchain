from primeCoin.blockchain import Blockchain
from numpy.random import binomial
import progressbar
import csv

class cPosMiner:
    def __init__(self, stakes: int, v: float, w: float):
        self.stakes = stakes
        self.v = v
        self.w = w
    
    def addStakes(self, reward):
        self.stakes += reward
    
    @staticmethod
    def calculateReward(v: float, w: float, ratio: float, P: int):
        X = binomial(n= P, p = ratio, size=1)[0]
        return v*ratio + w*(X/P)
        
class cPosSimulation:
    def __init__(self, stakesA: int, stakesB: int, LIMIT: int):
        self.stakesA = stakesA
        self.stakesB = stakesB
        self.LIMIT = LIMIT
    
    def start(self, saveCSV: bool = False):
        v = 200/21 # propsor reward
        w =10/21 # attester reward

        P = 32 # number of shards
        miner1 = cPosMiner(self.stakesA, v, w)
        miner2 = cPosMiner(self.stakesB, v, w)

        numBlocks = 0
        miner1Blocks = 0
        miner2Blocks = 0
        prevNumBlocks = 0
        csvfile = open("cPos_blocks_to_ratio.csv","w")
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["block", "ratio"])

        bar = progressbar.ProgressBar(maxval=self.LIMIT, \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        
        bar.start()
        printAfter = 0
        while numBlocks<self.LIMIT:
            prevNumBlocks = numBlocks

            ratio1 = miner1.stakes/(miner1.stakes + miner2.stakes)
            ratio2 = miner2.stakes/(miner1.stakes + miner2.stakes)

            miner1Reward = cPosMiner.calculateReward(v, w, ratio1, P)
            miner2Reward = cPosMiner.calculateReward(v, w, ratio2, P)
            
            miner1.addStakes(miner1Reward)
            miner2.addStakes(miner2Reward)

            numBlocks += (miner1Reward + miner2Reward)
            miner1Blocks += miner1Reward
            miner2Blocks += miner2Reward

            if(numBlocks>=printAfter and prevNumBlocks!=numBlocks):
                bar.update(min(numBlocks, self.LIMIT))
                if(saveCSV):
                    csvwriter.writerow([numBlocks, miner2Blocks/miner1Blocks])
                printAfter += 10
        bar.finish()
        
        csvfile.close()
        return (miner1Blocks, miner2Blocks)


if __name__ == "__main__":
    simulation = cPosSimulation(1250, 1000, 1000)
    nA, nB = simulation.start(saveCSV=False)
    print(nA, nB)

