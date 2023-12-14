import sys
import time
# Import mavutil
from pymavlink import mavutil


master: mavutil.mavfile = mavutil.mavlink_connection(
    device="tcp:127.0.0.1:5762",
    source_system=1, source_component=90)


master.set_mode(4)

# 目標の緯度・経度、高度を設定
target_lat = 35.8787276
target_lon = 140.3388137
target_alt = 3

# SET_POSITION_TARGET_GLOBAL_INTメッセージを送信
master.mav.set_position_target_global_int_send(
    0, master.target_system, master.target_component,
    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # グローバル座標、相対高度
    0b0000111111111000, # X,Y,Zの位置・速度・加速度は使用、YAWの角度・角速度は未使用
    int(target_lat * 1e7), int(target_lon * 1e7), # 緯度・経度は10の7乗倍して整数化
    target_alt, 0, 0, 0, 0, 0, 0, 0, 0, 0)