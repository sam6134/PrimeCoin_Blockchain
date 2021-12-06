import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('simulation_results/block_to_ratio.csv')
numBlocks = list(data["block"])
ratio = list(data["ratio"])
n = len(numBlocks)
plt.plot(numBlocks,ratio)
plt.scatter(numBlocks[::40],ratio[::40])
plt.plot(numBlocks,[0.2]*n)
plt.scatter(numBlocks[::40],([0.2]*n)[::40])

plt.grid(linestyle = '--', linewidth = 0.5)
plt.legend(['Block_R', 'Block_R','Ideal','Ideal'])
plt.show()



