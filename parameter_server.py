import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import *

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

# Ctrl+Cで終了時の処理
def handler(signal, frame):
        print('Exit with Ctrl+C / sys.exit(0) ')
        sys.exit(0)

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

# Receive時の処理 (data/ 以降に一つのデータの際(引数一つ)であればok)
def print_handler(_data_path, arg):
    print("receive interaction : {0}".format((arg)))
    config.interction = arg

# SendするParameterの取得
def get_param(arg):
    input_arg = randint(10,100)
    return input_arg

# ParameterをBroadCastする
def broadcast_parameter(osc_client):
    msg = osc_message_builder.OscMessageBuilder(address="/data")

    # 適当なX,Y,Zを取得
    # TODO @haradama
    input_arg_x = get_param("X")
    input_arg_y = get_param("Y")
    input_arg_z = get_param("Z")

    # interactionの値を取得してるやつをServe
    input_arg_interction = config.interction

    msg.add_arg(input_arg_x)
    msg.add_arg(input_arg_y)
    msg.add_arg(input_arg_z)
    msg.add_arg(input_arg_interction)

    print("send x : {0}".format(input_arg_x))
    print("send y : {0}".format(input_arg_y))
    print("send z : {0}".format(input_arg_z))
    print("send interction : {0}".format(input_arg_interction))

    msg = msg.build()
    osc_client.send(msg)

def main_thread():

    # Sender OSC周りの初期化
    osc_client_sender = init_osc_sender()

    # SenderでParameterをBroadCast
    while True:
        broadcast_parameter(osc_client_sender)
        time.sleep(10)

if __name__ == "__main__":

    # Ctrl+C終了時のイベント検知
    signal.signal(signal.SIGINT, handler)

    # ReceiverのThreadを別Threadで実行
    receive_thread = threading.Thread(target=receiver_thread,name="dual_loop")
    receive_thread.start()

    # BroadCastのloop
    main_thread()
