from primeCoin.blockchain import Blockchain
from hashlib import sha256
import json
import csv

def getHash(s):
    return sha256(s).hexdigest()

class slPosMiner:
    def __init__(self, stakes, publicKey: str, chain: Blockchain):
        self.stakes = stakes
        self.publicKey = publicKey
        self.chain = chain
    
    def proposeTime(self):
        baseTime = self.chain.chain[-1]["timestamp"]
        last_block = self.chain.chain[-1].copy()
        last_block.pop("hash")
        last_block["publicKey"] = self.publicKey
        myHash = getHash(json.dumps(last_block, sort_keys=True).encode())
        time = (baseTime*int(myHash,16))/self.stakes
        return time


globalChain = Blockchain()

miner1 = slPosMiner(5000, "x9ce", globalChain)
miner2 = slPosMiner(1000, "xdfg", globalChain)
w = 0
numBlocks = 0
miner1Blocks = 0
miner2Blocks = 0
prevNumBlocks = 0
csvfile = open("SL_block_to_ratio.csv","w")
csvwriter = csv.writer(csvfile)
csvwriter.writerow(["block", "ratio"])
while numBlocks<5000:
    prevNumBlocks = numBlocks
    block1TimeStamp = miner1.proposeTime()
    block2TimeStamp = miner2.proposeTime()
    if block1TimeStamp < block2TimeStamp:
        block1 = globalChain.new_block()
        globalChain.add_block(block1)
        numBlocks += 1
        miner1Blocks += 1
        miner1.stakes += w
    else:
        block2 = globalChain.new_block()
        globalChain.add_block(block2)
        numBlocks += 1
        miner2Blocks += 1
        miner2.stakes += w
    if(numBlocks%10==0 and prevNumBlocks!=numBlocks):
        print("Mined", numBlocks, "blocks")
        csvwriter.writerow([numBlocks, miner2Blocks/miner1Blocks])

print(miner1Blocks, miner2Blocks)
csvfile.close()