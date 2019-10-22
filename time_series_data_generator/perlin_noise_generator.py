import pandas as pd
import matplotlib.pyplot as plt
import time
import noise
from numpy.random import *
import csv

import config

def generate_perlin_noise():

    arg = config.pattern_num/config.sample_num
    x_list = [(1+noise.pnoise1(arg*i,octaves=1,base=0))/2*config.x_max_scale+config.frame_margin for i in range(config.sample_num)]
    y_list = [(1+noise.pnoise1(arg*i,octaves=1,persistence=0.5,base=1))/2*config.y_max_scale+config.frame_margin for i in range(config.sample_num)]

    return x_list,y_list;

f = open('data/perlin.csv', 'w')
writer = csv.writer(f)
writer.writerow(["index","x","y"])

x_list,y_list = generate_perlin_noise()

for index in range(config.sample_num):
    print("x:{0} / y:{1}".format(x_list[index],y_list[index]))
    writer.writerow([index,x_list[index],y_list[index]])

# ファイルクローズ
f.close()
