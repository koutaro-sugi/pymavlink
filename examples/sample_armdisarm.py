import time
# Import mavutil
from pymavlink import mavutil


master: mavutil.mavfile = mavutil.mavlink_connection(
    device="tcp:127.0.0.1:5762",
    source_system=1, source_component=90)

# ARM
master.arducopter_arm()
master.motors_armed_wait()
print("ARMED")
time.sleep(10)

# DISARM
master.arducopter_disarm()
master.motors_disarmed_wait()
print("DISARMED")
