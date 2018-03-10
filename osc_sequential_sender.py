import pandas as pd
import matplotlib.pyplot as plt
import time
import noise
from numpy.random import *
import csv

# 更新時間管理など
import datetime
import time

# Ctrl+Cで終了時の処理のため
import signal
import sys

# モジュール変数の定義
import config

# OSC送信のため
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

# Ctrl+Cで終了時の処理
def handler(signal, frame):
        print('Exit with Ctrl+C / sys.exit(0) ')
        sys.exit(0)

# x[0:1200]
# y[0:2700]

# OSCのSender初期化
def init_osc_sender():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sender_ip", default=config.sender_ip, help="The ip of th OSC Sender")
    parser.add_argument("--sender_port", type=int, default=config.sender_port, help="The port the OSC sender is listening on")
    args = parser.parse_args()
    osc_client = udp_client.UDPClient(args.sender_ip, args.sender_port)

    # 設定のログ出し
    print("[Sender] sender_ip:{}, sender_port:{}, address:/data".format(args.sender_ip, args.sender_port))
    return osc_client

# パーリンノイズの生成
def generate_perlin_noise():

    arg = config.pattern_num/config.sample_num
    x_list = [(1+noise.pnoise1(arg*i,octaves=1,base=0))/2*config.x_max for i in range(config.sample_num)]
    y_list = [(1+noise.pnoise1(arg*i,octaves=1,persistence=0.5,base=1))/2*config.y_max for i in range(config.sample_num)]

    return x_list,y_list;

# Parameterの取得とmsgに突っ込む
def get_param(msg,arg):
    input_arg = randint(0,100)
    msg.add_arg(int(input_arg))

def task(osc_client, x, y):
    msg = osc_message_builder.OscMessageBuilder(address="/data")

    # 更新時間を送信
    update_time = str(time.asctime().split(" ")[3])
    msg.add_arg(update_time)
    print("update_time: {}".format(update_time))

    # get_param(msg,"X")
    # get_param(msg,"Y")
    msg.add_arg(int(x))
    msg.add_arg(int(y))

    z = randint(0,100)
    interaction = randint(0,100)

    msg.add_arg(int(z))
    msg.add_arg(int(interaction))

    print("send message: x[{0}],y[{1}],z[{2}],interaction[{3}]".format(x,y,z,interaction))

    msg = msg.build()
    osc_client.send(msg)

if __name__ == "__main__":

    # Ctrl+C終了時のイベント検知
    signal.signal(signal.SIGINT, handler)

    # パーリンノイズの生成
    x_list,y_list = generate_perlin_noise()

    # OSC周りの初期化
    osc_client_sender = init_osc_sender()

    index = 0
    while True:
        task(osc_client_sender, x_list[index], y_list[index])

        time.sleep(0.05)
        index += 1
        if(index >= config.sample_num): index = 0
