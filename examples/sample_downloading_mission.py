import time
# Import mavutil
from pymavlink import mavutil

master: mavutil.mavfile = mavutil.mavlink_connection(
    device="tcp:127.0.0.1:5762",
    source_system=1, source_component=90)



# 動作未確認
def download_mission(master):
    mission = []
    # ミッションアイテムの数を取得
    master.mav.mission_request_list_send(master.target_system, master.target_component)
    mission_count = master.recv_match(type='MISSION_COUNT', blocking=True).count

    # ミッションアイテムをダウンロード
    for i in range(mission_count):
        master.mav.mission_request_int_send(master.target_system, master.target_component, i)
        item = master.recv_match(type='MISSION_ITEM_INT', blocking=True)
        new_waypoint = mavutil.mavlink.MAVLink_mission_item_int_message(
            master.target_system,
            master.target_component,
            item.seq,
            item.frame, item.command, item.current, item.autocontinue,
            item.param1, item.param2, item.param3, item.param4,
            item.x, item.y, item.z,
        )
        mission.append(new_waypoint)

    return mission


download_mission(master)