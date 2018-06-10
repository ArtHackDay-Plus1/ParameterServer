# Motion生成のため
import time
import noise
from numpy.random import *

# 更新時間管理など
import datetime
import time

# Ctrl+Cで終了時の処理のため
import signal
import sys

# モジュール変数の定義
import config
import received_data

# OSC送信のため
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

# OSC受信のため
from pythonosc import dispatcher
from pythonosc import osc_server

# 受信は別スレッドで行うため
import threading

# Kinectで取得したデータでインタラクションの計算を行うため
import math

# Ctrl+Cで終了時の処理
def handler(signal, frame):
        print('Exit with Ctrl+C / sys.exit(0) ')
        sys.exit(0)

# Receive時の処理 (data/ 以降に一つのデータの際(引数一つ)であればok)
def print_handler(_data_path, nearest_x, nearest_depth, num_of_people):
    print("receive : {0},{1},{2}".format(nearest_x, nearest_depth, num_of_people))
    received_data.nearest_x = nearest_x
    received_data.nearest_depth = nearest_depth
    received_data.num_of_people = num_of_people

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
def init_osc_sender(ip,port):
    osc_client = udp_client.UDPClient(ip,port)

    # 設定のログ出し
    print("[Sender] sender_ip:{}, sender_port:{}, address:/data".format(ip,port))
    return osc_client

# パーリンノイズの生成
def generate_perlin_noise():

    arg = config.pattern_num/config.sample_num
    x_list = [(1+noise.pnoise1(arg*i,octaves=1,base=0))/2*config.x_max_scale+config.frame_margin for i in range(config.sample_num)]
    y_list = [(1+noise.pnoise1(arg*i,octaves=1,persistence=0.5,base=1))/2*config.y_max_scale+config.frame_margin for i in range(config.sample_num)]

    return x_list,y_list;

# Parameterの取得とmsgに突っ込む
# def get_param(msg,arg):
#     input_arg = randint(0,100)
#     msg.add_arg(int(input_arg))

def broadcast_parameter(osc_client, x, y, z, interaction):
    try:
        msg = osc_message_builder.OscMessageBuilder(address="/data")

        # 更新時間を送信
        update_time = str(time.asctime().split(" ")[3])
        msg.add_arg(update_time)
        # print("update_time: {}".format(update_time))

        msg.add_arg(int(x))
        msg.add_arg(int(y))
        msg.add_arg(int(z))
        msg.add_arg(int(interaction))

        print("send message: x[{0}],y[{1}],z[{2}],interaction[{3}]".format(x,y,z,interaction))

        msg = msg.build()
        osc_client.send(msg)

    except OSError:
        print("[OS Error] OSC disconnected")

def get_distance(x1, y1, x2, y2):
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return d

#検知したInteractionの0~2700の位置をもとに、ルンバの逃げる位置を決定
def get_farthest_xy(target_x):
    if target_x < 1350:
        f_x = 0 + frame_margin
    else:
        f_x = 2700 - frame_margin
    f_y = 0 + frame_margin # 一番壁側
    return f_x,f_y

# 任意の点(x,y)最近傍の 生成済み経路の点のindexを取得
def calculate_nearest_index(x, y):
    index = -1
    min_distance = 10000
    for i in range(config.sample_num):
        if get_distance(x, y, x_list[i], y_list[i]) < min_distance :
            min_distance = get_distance(x, y, x_list[i], y_list[i])
            index = i
    return nearest_index

def main_thread():

    # OSC周りの初期化
    macmini_osc_client_sender = init_osc_sender(config.macmini_sender_ip,config.macmini_sender_port)
    pd_osc_client_sender = init_osc_sender(config.pd_sender_ip,config.pd_sender_port)
    roomba_osc_client_sender = init_osc_sender(config.roomba_sender_ip,config.roomba_sender_port)

    # 更新パラメータ
    index = 0

    while True:
        x = x_list[index]
        y = y_list[index]
        # zに何かしらインタラクション入れたい
        z = randint(0,config.z_max)

        # 人が多い場合はinteraction度合いをあげる
        interaction = received_data.num_of_people

        # 一番展示に近い人のy方向の値をmapで取得
        target_x = received_data.nearest_x

        # 一番展示に近い人の展示までの距離をmapで取得
        target_y = received_data.nearest_depth

        # この時Interactionの検知なし(誰も見てないだろうから更新もほぼしない)
        if(target_x<0 or target_y<0):
            # 普段の時、Interactionは検知しているが、ある程度遠い時
            time.sleep(5)

        # Interaction検知してる時、roombaと人がある程度近いと逃げる
        elif(get_distance(x, y, target_x, target_y) < config.prohibited_area_radius):
            print("NEAR")
            # 以降しばらくは特定の位置情報だけ送ってそこに向かうようにさせる
            # -> そのためにIndex値を固定 その特定座標と近いIndexを求める
            f_x, f_y = get_farthest_xy(target_x)
            index = calculate_nearest_index(f_x, f_y)
            # 送る座標も固定
            x, y = f_x, f_y
            # Swithのためのkeyみたいなboolean変数を一個用意
            # しばらく更新しないことで、ここにroombaが行って時間余ったら止まる気がする
            time.sleep(10)
        else:
            # 普段の時、Interactionは検知しているが、ある程度遠い時
            time.sleep(0.05)

        broadcast_parameter(macmini_osc_client_sender, x, y, z, interaction)
        broadcast_parameter(pd_osc_client_sender, x, y, z, interaction)
        broadcast_parameter(roomba_osc_client_sender, x, y, z, interaction)

        # Interaction の 0/1スイッチのみでの制御 for DEMO
        # if(interaction < 0):
        #     time.sleep(0.01/(-interaction))
        # elif(interaction < 2):
        #     time.sleep(0.01)
        # else:
        #     time.sleep(5)

        index += 1
        if(index >= config.sample_num): index = 0


if __name__ == "__main__":

    # Ctrl+C終了時のイベント検知
    signal.signal(signal.SIGINT, handler)

    # パーリンノイズの生成
    # この時点で動きの経路は確定
    x_list,y_list = generate_perlin_noise()

    # ReceiverのThreadを別Threadで実行
    receive_thread = threading.Thread(target=receiver_thread,name="dual_loop")
    receive_thread.start()

    # BroadCastのloop
    main_thread()
