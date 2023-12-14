import sys
import time
# Import mavutil
from pymavlink import mavutil


master: mavutil.mavfile = mavutil.mavlink_connection(
    device="tcp:127.0.0.1:5762",
    source_system=1, source_component=90)


# 目標地点の緯度経度高度のリスト
waypoints = [
    (35.8789167, 140.3393923, 10),
    (35.8787820, 140.3388163, 10),
    (35.8786038, 140.3387386, 10),
    (35.8785212, 140.3388244, 10),
    (35.8786016, 140.3390041, 10),
    (35.8784669, 140.3389558, 10),
    (35.8783756, 140.3390417, 10),
    (35.8784451, 140.3392106, 10),
    (35.8789053, 140.3393957, 10),
]

# SET_POSITION_TARGET_GLOBAL_INTメッセージを送信する関数
def send_position_target(wp_lat, wp_lon, wp_alt):
    master.mav.set_position_target_global_int_send(
        0, master.target_system, master.target_component,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # グローバル座標、相対高度
        0b0000111111111000, # X,Y,Zの位置・速度・加速度は使用、YAWの角度・角速度は未使用
        int(wp_lat * 1e7), int(wp_lon * 1e7), # 緯度・経度は10の7乗倍して整数化
        wp_alt, 0, 0, 0, 0, 0, 0, 0, 0, 0
    )



# GUIDEDモード(4)に設定
master.set_mode(4)
# アーム
master.arducopter_arm()
master.motors_armed_wait()
# 目標高度
target_altitude = 10
# 離陸
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0, 0, 0, 0, 0, 0, 0, target_altitude)

# データストリームレート変更: GLOBAL_POSITION_INT(33)を10Hzで受信
master.mav.command_long_send(master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, 33, 100000, 0, 0, 0, 0, 0)

# 目標高度への到達を確認
while True:
    # GLOBAL_POSITION_INT から相対高度を取得
    recieved_msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    current_altitude = recieved_msg.relative_alt / 1000
    current_lat = recieved_msg.lat
    current_lon = recieved_msg.lon
    print("高度: {}".format(current_altitude))
    # print("緯度: {}".format(current_lat))
    # print("経度: {}".format(current_lon))

    if current_altitude >= target_altitude * 0.95:
        print("離陸・目標高度に到達")
        break

    time.sleep(0.1)
    
# 各目標地点を順番に処理
for waypoint in waypoints:
    wp_lat, wp_lon, wp_alt = waypoint

    # 目標緯度経度高度への到達を確認
    while True:
        # GLOBAL_POSITION_INTから緯度経度高度を取得
        received_msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        current_lat = received_msg.lat / 1e7
        current_lon = received_msg.lon / 1e7
        current_altitude = received_msg.relative_alt / 1000

        print("緯度: {}, 経度: {}, 高度: {}".format(current_lat, current_lon, current_altitude))

        # ウェイポイントに向かって水平移動
        send_position_target(wp_lat, wp_lon, wp_alt)
        # 目標地点に十分に近づいたら次の目標地点へ移動
        if (
            abs(current_lat - wp_lat) < 0.00005 and
            abs(current_lon - wp_lon) < 0.00005 and
            current_altitude >= wp_alt * 0.95
        ):
            print("目標地点に到達")
            break

        # 目標高度まで上昇
        if current_altitude < wp_alt:
            send_position_target(current_lat, current_lon, wp_alt)

        time.sleep(0.1)

    

# 最後の目標地点に到達後、ループを抜ける
print("すべての目標地点に到達しました。")


master.set_mode_rtl()