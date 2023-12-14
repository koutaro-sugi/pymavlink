import sys
import time
# Import mavutil
from pymavlink import mavutil

master: mavutil.mavfile = mavutil.mavlink_connection(
    device="tcp:127.0.0.1:5762",
    source_system=1, source_component=90)


while True:
    # HOME_POSITIONメッセージを受信, アームのタイミングで受信できる
    msg = master.recv_match(type='HOME_POSITION', blocking=True)
    if msg is not None:
    # ホームロケーション情報を設定
    home_latitude = msg.latitude / 1.0e7
    home_longitude = msg.longitude / 1.0e7
    home_altitude = msg.altitude / 1000.0 # メートル単位に変換
    print(f"ホームロケーション:lat={home_latitude},lon={home_longitude},alt={home_altitude}")
        break # ホームロケーションを取得したら終了
