import time
# Import mavutil
from pymavlink import mavutil

master: mavutil.mavfile = mavutil.mavlink_connection(
    device="tcp:127.0.0.1:5762",
    source_system=1, source_component=90)



def add_waypoint(mission, lat, lon, alt):
    # 新しいウェイポイントを追加
    if mission:
        new_waypoint = mavutil.mavlink.MAVLink_mission_item_int_message(
            mission[0].target_system,
            mission[0].target_component,
            len(mission),
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0, 0, 0, 0, 0, 0,
            int(lat * 1e7),
            int(lon * 1e7),
            int(alt)
        )
        mission.append(new_waypoint)
    else:
        print("ミッションが空です。他のウェイポイントを追加する前に、初期のウェイポイントを追加してください。")

mission = []
add_waypoint(mission, 37.7749, -122.4194, 20)
