receiver_port = 8008
interaction = 0
receiver_ip = "127.0.0.1"


# "192.168.2.11"  cannot used

# projector
projector_sender_ip = "192.168.2.14"
projector_sender_port = 8014

# PureData
pd_sender_ip = "192.168.2.12"
pd_sender_port = 8012

# roomba
roomba_sender_ip = "192.168.2.13"
roomba_sender_port = 8013

# 多いほど複雑な動きが生成
pattern_num = 100

# 2x -> 2x slower
sample_num = 20000

# roombaのframeサイズ
x_max = 1200
y_max = 2700

# カニが逃げる半径
prohibited_area_radius = 300
interction_threshold = 100
