from primeCoin.blockchain import Blockchain
import csv
import progressbar
import random

class posMiner:
    def __init__(self, stakes, difficulty, chain: Blockchain):
        self.stakes = stakes
        self.difficulty = difficulty
        self.chain = chain
    
    def mine(self):
        block = self.chain.new_block()
        if(int(block["hash"],16) < self.difficulty*self.stakes):
            return block
        else:
            return None

class mlSimulator:
    def __init__(self, stakesA: int, stakesB: int, D: int, limit: int):
        self.stakesA = stakesA
        self.stakesB = stakesB
        self.D = D
        self.limit = limit
    
    def start(self, saveCSV: bool = False, csvFileName: str = "ml_pos_ratio.csv") -> tuple:
        globalChain = Blockchain()
        D = self.D
        miner1 = posMiner(D, self.stakesA, globalChain)
        miner2 = posMiner(D, self.stakesB, globalChain)
        w = 0  #  0.01*(miner1.stakes + miner2.stakes)
        numBlocks = 0
        miner1Blocks = 0
        miner2Blocks = 0
        prevNumBlocks = 0
        csvfile = open(csvFileName,"w")
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["block", "ratio"])

        bar = progressbar.ProgressBar(maxval=self.limit, \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        while numBlocks<self.limit:
            prevNumBlocks = numBlocks
            block1 = miner1.mine()
            block2 = miner2.mine()
            if block2 is None and block1:
                globalChain.add_block(block1)
                numBlocks += 1
                miner1Blocks += 1
                miner1.stakes += w
            elif block1 is None and block2:
                globalChain.add_block(block2)
                numBlocks += 1
                miner2Blocks += 1
                miner2.stakes += w
            elif block1 and block2:
                winner = random.randint(0,1)
                if(winner == 1):
                    globalChain.add_block(block1)
                    numBlocks += 1
                    miner1Blocks += 1
                    miner1.stakes += w
                else:
                    globalChain.add_block(block2)
                    numBlocks += 1
                    miner2Blocks += 1
                    miner2.stakes += w
            if(numBlocks%10==0 and prevNumBlocks!=numBlocks):
                # print("Mined", numBlocks, "blocks")
                bar.update(numBlocks)
                if saveCSV:
                    csvwriter.writerow([numBlocks, miner2Blocks/miner1Blocks])
        csvfile.close()
        bar.finish()
        return (miner1Blocks, miner2Blocks)


if __name__ == "__main__":
    print("Starting simulation...")
    sim = mlSimulator(5000, 1000, 1<<235, 1000)
    nA, nB = sim.start()
    print(nA, nB)




