import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

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

def init_osc():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip of th OSC Server")
    parser.add_argument("--port", type=int, default=config.port_num, help="The port the OSC server is listening on")
    args = parser.parse_args()
    osc_client = udp_client.UDPClient(args.ip, args.port)

    # 設定のログ出し
    print("ip:127.0.0.1, port:" + str(config.port_num) + ", address:/data")
    return osc_client

# Parameterの取得
def get_param(arg):
    print("type {}:".format(arg))
    input_arg = input()
    return input_arg

def task(osc_client):

  input_arg_x = get_param("X")
  input_arg_y = get_param("Y")
  input_arg_z = get_param("Z")
  input_arg_interction = get_param("interction")

  msg = osc_message_builder.OscMessageBuilder(address="/data")

  msg.add_arg(input_arg_x)
  msg.add_arg(input_arg_y)
  msg.add_arg(input_arg_z)
  msg.add_arg(input_arg_interction)

  msg = msg.build()
  osc_client.send(msg)

if __name__ == "__main__":

  # Ctrl+C終了時のイベント検知
  signal.signal(signal.SIGINT, handler)

  # OSC周りの初期化
  osc_client = init_osc()

  while True:
    task(osc_client)
    time.sleep(2)
