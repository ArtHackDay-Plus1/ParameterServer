import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv("data/sample.csv")
df = pd.read_csv("data/perlin.csv")

df.plot(x="x",y="y")
plt.title("crab action log", size=12)
plt.show()
