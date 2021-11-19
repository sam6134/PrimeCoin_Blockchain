from primeCoin.blockchain import Blockchain
import csv
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


globalChain = Blockchain()
D = int(1<<225)
miner1 = posMiner(D, 5000, globalChain)
miner2 = posMiner(D, 1000, globalChain)
w = 0.01*(miner1.stakes + miner2.stakes)
numBlocks = 0
miner1Blocks = 0
miner2Blocks = 0
prevNumBlocks = 0
csvfile = open("block_to_ratio_with_rewards.csv","w")
csvwriter = csv.writer(csvfile)
csvwriter.writerow(["block", "ratio"])
while numBlocks<5000:
    prevNumBlocks = numBlocks
    block1 = miner1.mine()
    block2 = miner2.mine()
    if block1 is not None:
        globalChain.add_block(block1)
        numBlocks += 1
        miner1Blocks += 1
        miner1.stakes += w
    elif block2 is not None:
        globalChain.add_block(block2)
        numBlocks += 1
        miner2Blocks += 1
        miner2.stakes += w
    if(numBlocks%10==0 and prevNumBlocks!=numBlocks):
        print("Mined", numBlocks, "blocks")
        csvwriter.writerow([numBlocks, miner2Blocks/miner1Blocks])

print(miner1Blocks, miner2Blocks)
csvfile.close()