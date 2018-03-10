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

# OSC受信のため
from pythonosc import dispatcher
from pythonosc import osc_server
import threading

import math

# Ctrl+Cで終了時の処理
def handler(signal, frame):
        print('Exit with Ctrl+C / sys.exit(0) ')
        sys.exit(0)

# Receive時の処理 (data/ 以降に一つのデータの際(引数一つ)であればok)
def print_handler(_data_path, arg):
    print("receive interaction : {0}".format((arg)))
    config.interaction = arg

# OSCのReceiver初期化
def receiver_thread():
    init_osc_receiver()

# OSC Receiverの初期化
def init_osc_receiver():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receiver_ip",default=config.receiver_ip, help="The ip to listen on")
    parser.add_argument("--receiver_port",type=int, default=config.receiver_port, help="The port the OSC Receiver to listen on")
    args = parser.parse_args()

    _dispatcher = dispatcher.Dispatcher()
    _dispatcher.map("/data", print_handler)

    server = osc_server.ThreadingOSCUDPServer((args.receiver_ip, args.receiver_port), _dispatcher)
    print("[Receiver] Receiving on {}".format(server.server_address))

    server.serve_forever()

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

def broadcast_parameter(osc_client, x, y):
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

def get_distance(x1, y1, x2, y2):
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return d

def main_thread():

    # OSC周りの初期化
    osc_client_sender = init_osc_sender()

    index = 0
    while True:
        x = x_list[index]
        y = y_list[index]
        broadcast_parameter(osc_client_sender, x, y)

        # # 人が近くにいるときは、遠くに行って、離れたらあまり動かないように
        if(config.interaction > config.interction_threshold):
            # 人に近い場合は素早く動く
            if(get_distance(x, y, config.x_max/2, 0) < config.prohibited_area_radius):
                time.sleep(0.001)
            # 離れたらあんまり動かない
            else:
                time.sleep(2)
        # 普段は普通通り動く
        else:
            time.sleep(0.05)

        index += 1
        if(index >= config.sample_num): index = 0


if __name__ == "__main__":

    # Ctrl+C終了時のイベント検知
    signal.signal(signal.SIGINT, handler)

    # パーリンノイズの生成
    x_list,y_list = generate_perlin_noise()

    # ReceiverのThreadを別Threadで実行
    receive_thread = threading.Thread(target=receiver_thread,name="dual_loop")
    receive_thread.start()

    # BroadCastのloop
    main_thread()
