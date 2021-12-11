from primeCoin.blockchain import Blockchain
import random
import progressbar
import csv

class powMiner:
    def __init__(self, cpuPower: int, chain: Blockchain, difficulty: int):
        self.cpuPower = cpuPower
        self.chain = chain
        self.difficulty = difficulty

    def mine(self):
        for _ in range(self.cpuPower):
            block = self.chain.new_block()
            if(str(block["hash"])[:self.difficulty] == '0'*self.difficulty):
                return block
        return None
        
class powSimulation:
    def __init__(self, cpuPowerA: int, cpuPowerB: int, LIMIT: int):
        self.cpuPowerA = cpuPowerA
        self.cpuPowerB = cpuPowerB
        self.LIMIT = LIMIT
    
    def start(self, saveCSV: bool = False):
        globalChain = Blockchain()
        miner1 = powMiner(self.cpuPowerA, globalChain, 1)
        miner2 = powMiner(self.cpuPowerB, globalChain, 1)

        numBlocks = 0
        miner1Blocks = 0
        miner2Blocks = 0
        prevNumBlocks = 0
        csvfile = open("pow_blocks_to_ratio.csv","w")
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["block", "ratio"])

        bar = progressbar.ProgressBar(maxval=self.LIMIT, \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        
        bar.start()
        while numBlocks<self.LIMIT:
            prevNumBlocks = numBlocks
            block1 = miner1.mine()
            block2 = miner2.mine()
            if block2 is None and block1:
                globalChain.add_block(block1)
                numBlocks += 1
                miner1Blocks += 1
            elif block1 is None and block2:
                globalChain.add_block(block2)
                numBlocks += 1
                miner2Blocks += 1
            elif block1 and block2:
                winner = random.randint(0,1)
                if(winner == 1):
                    globalChain.add_block(block1)
                    numBlocks += 1
                    miner1Blocks += 1
                else:
                    globalChain.add_block(block2)
                    numBlocks += 1
                    miner2Blocks += 1
            if(numBlocks%10==0 and prevNumBlocks!=numBlocks):
                # print("Mined", numBlocks, "blocks")
                bar.update(numBlocks)
                if saveCSV:
                    csvwriter.writerow([numBlocks, miner2Blocks/miner1Blocks])
        csvfile.close()
        bar.finish()
        return (miner1Blocks, miner2Blocks)


if __name__ == "__main__":
    simulation = powSimulation(10, 1, 1000)
    nA, nB = simulation.start(saveCSV=False)
    print(nA, nB)

