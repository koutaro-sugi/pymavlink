import sys
import time
# Import mavutil
from pymavlink import mavutil

master: mavutil.mavfile = mavutil.mavlink_connection(
    device="tcp:127.0.0.1:5762",
    source_system=1, source_component=90)



master.mav.param_request_list_send(master.target_system, master.target_component)
while True:
    time.sleep(0.01)
    try:
        message = master.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
        print('name: %s¥tvalue: %d' % (message['param_id'], message['param_value']))

    except Exception as error:
        print(error)
        sys.exit(0)
