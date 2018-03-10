import pandas as pd
import matplotlib.pyplot as plt
import time
import noise
from numpy.random import *
import csv

# x[0:1200]
# y[0:2700]

x_max = 1200
y_max = 2700

f = open('data/perlin.csv', 'w')
writer = csv.writer(f)
writer.writerow(["index","x","y"])

sample_num = 1000
pattern_num = 10
arg = pattern_num/sample_num
x_list = [(1+noise.pnoise1(arg*i,octaves=1,base=0))/2*x_max for i in range(sample_num)]
y_list = [(1+noise.pnoise1(arg*i,octaves=1,persistence=0.5,base=1))/2*y_max for i in range(sample_num)]

for index in range(sample_num):
    # time.sleep(0.1)
    print("x:{0} / y:{1}".format(x_list[index],y_list[index]))
    writer.writerow([index,x_list[index],y_list[index]])

# ファイルクローズ
f.close()
