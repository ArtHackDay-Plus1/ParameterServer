# 更新時間管理など
import datetime
import time

# Ctrl+Cで終了時の処理のため
import signal
import sys

# モジュール変数の定義
import test_config

# OSC送信のため
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

# TestデータのCSVロードのため
import pandas as pd

# Ctrl+Cで終了時の処理
def handler(signal, frame):
        print('Exit with Ctrl+C / sys.exit(0) ')
        sys.exit(0)

# OSCのSender初期化
def init_osc_sender():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kinect_sender_ip", default=test_config.kinect_sender_ip, help="The ip of th OSC Sender")
    parser.add_argument("--kinect_sender_port", type=int, default=test_config.kinect_sender_port, help="The port the OSC sender is listening on")
    args = parser.parse_args()
    osc_client = udp_client.UDPClient(args.kinect_sender_ip, args.kinect_sender_port)

    # 設定のログ出し
    print("[Sender] sender_ip:{}, sender_port:{}, address:/data".format(args.kinect_sender_ip, args.kinect_sender_port))
    return osc_client

def task(osc_client, index):
  msg = osc_message_builder.OscMessageBuilder(address="/data")
  _x = int(df.x.values[index])
  _y = int(df.y.values[index])

  msg.add_arg(int(_x)) # nearest_x
  msg.add_arg(int(_y)) # nearest_depth
  msg.add_arg(int(0)) # num_of_people
  msg = msg.build()
  osc_client.send(msg)
  print("[Kinect Sender] x:{}, y:{}".format(_x, _y))

if __name__ == "__main__":

  # Ctrl+C終了時のイベント検知
  signal.signal(signal.SIGINT, handler)

  # OSC周りの初期化
  osc_client_sender = init_osc_sender()

  # テストデータのロード
  df = pd.read_csv('test_kinect.csv')

  index = 0
  while True:

    task(osc_client_sender, index)
    time.sleep(0.01)
    index += 1

    if index >= len(df):
        index = 0
