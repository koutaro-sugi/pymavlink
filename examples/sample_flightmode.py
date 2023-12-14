import sys
import time
# Import mavutil
from pymavlink import mavutil


master: mavutil.mavfile = mavutil.mavlink_connection(
    device="tcp:127.0.0.1:5762",
    source_system=1, source_component=90)

# 変更後モード
mode = 'LOITER'

# モードが有効かをチェック
if mode not in master.mode_mapping():
    print('Unknown mode : {}'.format(mode))
    print('Try:', list(master.mode_mapping().keys()))
    sys.exit(1)

# モードIDを取得
mode_id = master.mode_mapping()[mode]

# モード変更リクエストを送信
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mode_id, 0, 0, 0, 0, 0)
# master.set_mode(mode_id) # モードID指定を使ってもOK
master.set_mode_loiter() # LOITER専用を使ってもOK

# モード変更の確認を行う
while True:
    if master.flightmode == mode:
        break
    master.recv_msg()

print("変更後モード:", master.flightmode)