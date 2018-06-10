[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# ParameterServer
This is a server program that performs allreduce and scatter of data with other servers via OSC.

```
├── __pycache__
│   ├── config.cpython-34.pyc
│   └── received_data.cpython-34.pyc
├── config.py
├── demo
│   ├── __pycache__
│   │   └── config.cpython-34.pyc
│   ├── config.py
│   └── kinect_dummy.py
├── parameter_server.py
├── received_data.py
├── sandbox
│   ├── __pycache__
│   │   └── config.cpython-34.pyc
│   ├── config.py
│   ├── osc_sequential_sender.py
│   ├── parameter_server.py
│   ├── receiver_sample.py
│   └── sender_sample.py
└── time_series_data_generator
    ├── csv_to_df_generator.py
    ├── data
    │   ├── perlin.csv
    │   └── sample.csv
    ├── log_plotter.py
    └── perlin_noise_generator.py
```

## requirement
#### Python Version
- Python 3.4.3 (using pyenv is recommend)

#### Python Libraries
- noise 1.2.2
- numpy 1.14.1
- python-osc 1.6.4

you can install following command.

```bash
pip install --require requirements.txt
```

#### Python Libraries(unconfirmed)
- portend 2.2
- python-dateutil 2.6.1

## Tutorial 

#### Configuration
configuration file is `ParameterServer/config.py`

```py
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
```

you have to fix ip address and set port num
- Projector + Kinect Machine
- Roomba Controller Machine
- PureData Controller Machine
- Parameter Server (for receiving interaction from Kinect)

#### Launch Server

```bash
$ cd workspace
$ git clone https://github.com/ArtHackDay-Plus1/ParameterServer
$ cd ParameterServer
$ pip install --require requirements.txt
$ python parameter_server.py
[Sender] sender_ip:127.0.0.1, sender_port:8017, address:/data
[Sender] sender_ip:192.168.2.12, sender_port:8012, address:/data
[Sender] sender_ip:192.168.2.13, sender_port:8013, address:/data
send message: x[600.0],y[1350.0],z[218],interaction[0]
send message: x[600.0],y[1350.0],z[218],interaction[0]
[Receiver] Receiving on ('127.0.0.1', 8015)
send message: x[600.0],y[1350.0],z[218],interaction[0]
send message: x[601.1999976821244],y[1350.525008153636],z[173],interaction[0]

======================= ========================

^CExit with Ctrl+C / sys.exit(0) 
^CExit with Ctrl+C / sys.exit(0) 
Exception ignored in: <module 'threading' from '/Users/hirokinaganuma/.pyenv/versions/3.4.3/Python.framework/Versions/3.4/lib/python3.4/threading.py'>
Traceback (most recent call last):
  File "/Users/hirokinaganuma/.pyenv/versions/3.4.3/Python.framework/Versions/3.4/lib/python3.4/threading.py", line 1294, in _shutdown
    t.join()
  File "/Users/hirokinaganuma/.pyenv/versions/3.4.3/Python.framework/Versions/3.4/lib/python3.4/threading.py", line 1060, in join
    self._wait_for_tstate_lock()
  File "/Users/hirokinaganuma/.pyenv/versions/3.4.3/Python.framework/Versions/3.4/lib/python3.4/threading.py", line 1076, in _wait_for_tstate_lock
    elif lock.acquire(block, timeout):
  File "parameter_server.py", line 36, in handler
    sys.exit(0)
SystemExit: 0
```


## LISENSE

Copyright 2018 Hiroki11x(Hiroki Naganuma)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
