import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('block_to_ratio.csv')
numBlocks = list(data["block"])
ratio = list(data["ratio"])
n = len(numBlocks)
plt.plot(numBlocks,ratio)
plt.plot(numBlocks,[0.2]*n)


plt.grid(linestyle = '--', linewidth = 0.5)
plt.legend(['Block_R', 'Ideal'])
plt.show()

