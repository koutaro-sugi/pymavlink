# 1. アーミングできるかチェック
# 2. フライトモードを「GUIDED」に設定
# 3. アーミング実行
# 4. アーミングが完了するまで待つ
# 5. テイクオフ実行
# 6. 目標高度に達するまで待つ


import time
# Import mavutil
from pymavlink import mavutil


master: mavutil.mavfile = mavutil.mavlink_connection(
    device="tcp:127.0.0.1:5762",
    source_system=1, source_component=90)


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
    print("高度: {}".format(current_altitude))

    if current_altitude >= target_altitude * 0.95:
        print("目標高度に到達")
        break

    time.sleep(0.1)