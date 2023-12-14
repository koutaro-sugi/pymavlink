"""
Example of how to connect pymavlink to an autopilot via an TCP connection
"""

import time
# Import mavutil
from pymavlink import mavutil


master: mavutil.mavfile = mavutil.mavlink_connection(
    device="tcp:127.0.0.1:5762",
    source_system=1, source_component=90)

# 全てを10Hzで受信
master.mav.request_data_stream_send(
    master.target_system,
    master.target_component,
    0, 10, 1)

# GLOBAL_POSITION_INT(33)を 10Hzで受信
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
    0, 33, 100000, 0, 0, 0, 0, 0)


# メッセージを取得
while True:
    print(master.recv_match().to_dict())
    time.sleep(1.0)


