import time
# Import mavutil
from pymavlink import mavutil

master: mavutil.mavfile = mavutil.mavlink_connection(
    device="tcp:127.0.0.1:5762",
    source_system=1, source_component=90)

# シミュレーションでの動作がよくわからなかった
msg = master.mav.command_long_encode(
    0, 1, # ターゲットシステム、コンポーネント
    mavutil.mavlink.MAV_CMD_CONDITION_YAW, # コマンド
    0,
    180, # 角度指定（degrees）
    0, # スピード指定（deg/s）
    1, # 方向 -1:反時計周り, 1:時計回り
    1, # オフセット 1:相対, 0:絶対
    0, 0, 0)

# MAVLinkメッセージ送信
master.mav.send(msg)