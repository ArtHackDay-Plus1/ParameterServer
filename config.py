#############################################################

receiver_port = 8015
receiver_ip = "127.0.0.1"

# "192.168.2.11"  cannot used

# Parameter Server
# macmini_sender_ip = "192.168.2.15"
macmini_sender_ip = "127.0.0.1" # for dummy
macmini_sender_port = 8015

# projector + Kinect
macmini_sender_ip = "127.0.0.1"
# macmini_sender_ip = "192.168.2.17"
macmini_sender_port = 8017

# PureData
pd_sender_ip = "192.168.2.12"
pd_sender_port = 8012

# roomba
roomba_sender_ip = "192.168.2.13"
roomba_sender_port = 8013

#########################[TEST]###############################

# test kinect
kinect_sender_port = 8015
kinect_sender_ip="127.0.0.1"

# test roomba
roomba_receiver_port = 8014
roomba_receiver_ip="127.0.0.1"

#############################################################

# 多いほど複雑な動きが生成
pattern_num = 25

# 2x -> 2x slower
sample_num = 20000

# roombaのframeサイズ
frame_x_max = 1200
frame_y_max = 2700

frame_margin = 300

x_max_scale = frame_x_max - frame_margin*2
y_max_scale = frame_y_max - frame_margin*2

# カニが逃げる半径
prohibited_area_radius = 1000
interaction_threshold = 1

# 磁石動かすサーボモーターの高さの最大値
z_max = 250
