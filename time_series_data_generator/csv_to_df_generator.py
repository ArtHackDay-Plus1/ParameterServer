import pandas as pd
import time

df = pd.read_csv("data/sample.csv")

for num in range(1000):
    argx = str(df["x"][num:num+1].get_values())
    argy = str(df["y"][num:num+1].get_values())
    print("x:{0} / y:{1}".format(argx,argy))
    time.sleep(0.1)
