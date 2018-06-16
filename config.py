# const int sender_osc_port_num = 8016;
# const int receiver_osc_port_num = 8020;
# const std::string osc_sender_ip = "127.0.0.1";

#############################################################

# [Reciver] Kinect
kinect_receiver_ip = "127.0.0.1"
kinect_receiver_port = 8017

# [Sender] PureData
pd_sender_ip = "192.168.2.12"
pd_sender_port = 8012

# [Sender] roomba
roomba_sender_ip = "192.168.2.13"
roomba_sender_port = 8013

#########################[TEST]###############################

# test roomba
test_sender_port = 8020
test_sender_ip="127.0.0.1"

# test roomba / kinect
test_receiver_port = 8016
test_receiver_ip="127.0.0.1"

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

# 磁石動かすサーボモーターの低さの最大値
z_max = 255

# 磁石動かすサーボモーターの通常の速さ (大きくすると早く動く)
z_speed = 10
