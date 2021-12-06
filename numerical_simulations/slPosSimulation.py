from typing import Tuple
from primeCoin.blockchain import Blockchain
from hashlib import sha256
import json
import csv
import progressbar


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



class slSimulator():
    def __init__(self, stakesA: int, stakesB: int, limitBlock: int):
        self.stakesA = stakesA
        self.stakesB = stakesB
        self.stopBlock = limitBlock
    
    def start(self, saveCSV: bool = False, csvFileName: str  = "slPos.csv") -> Tuple:
        globalChain = Blockchain()

        miner1 = slPosMiner(self.stakesA, "x9ce", globalChain)
        miner2 = slPosMiner(self.stakesB, "xdfg", globalChain)
        w = 0
        numBlocks = 0
        miner1Blocks = 0
        miner2Blocks = 0
        prevNumBlocks = 0
        limit = self.stopBlock

        
        csvfile = open(csvFileName,"w")
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["block", "ratio"])

        bar = progressbar.ProgressBar(maxval=limit, \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        
        bar.start()
        while numBlocks<limit:
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
                bar.update(numBlocks)
                if saveCSV:
                    csvwriter.writerow([numBlocks, miner1Blocks/miner2Blocks])
        bar.finish()
        csvfile.close()
        return (miner1Blocks, miner2Blocks)


if __name__ == "__main__":
    sim = slSimulator(5000, 1000, 5000)
    nA, nB = sim.start()
    print(nA, nB)




