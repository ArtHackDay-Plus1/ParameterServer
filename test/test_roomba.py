
# モジュール変数の定義
import test_config

# OSC受信のため
import argparse
from pythonosc import dispatcher
from pythonosc import osc_server

def print_handler(_data_path, args):
    print("input : {0}".format(args))

# OSCのReceiver初期化
def init_osc_receiver():
    parser = argparse.ArgumentParser()
    parser.add_argument("--roomba_receiver_ip",default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--roomba_receiver_port",type=int, default=test_config.roomba_receiver_port, help="The port the OSC Receiver to listen on")
    args = parser.parse_args()

    _dispatcher = dispatcher.Dispatcher()
    _dispatcher.map("/data", print_handler)

    server = osc_server.ThreadingOSCUDPServer((args.roomba_receiver_ip, args.roomba_receiver_port), _dispatcher)
    print("Serving on {}".format(server.server_address))

    server.serve_forever()

init_osc_receiver()
