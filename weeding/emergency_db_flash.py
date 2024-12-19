import can
import cantools
import os
import time

if os.name == 'nt':
    bus = can.interface.Bus(channel=2, bustype='vector', app_name="CANoe")
else:
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')


dbc = """VERSION ""
BO_ 2566834709 DM1: 8 SEND
 SG_ FlashAmberWarningLamp : 10|2@1+ (1,0) [0|3] "" Vector__XXX
 SG_ FlashRedStopLamp : 12|2@1+ (1,0) [0|3] "" Vector__XXX
"""

dm1 = cantools.db.load_string(dbc, 'dbc').get_message_by_name("DM1")

def send2can(message):
    print(can.bus.BusState)
    try:
        bus.send(message)
        print(message)
    except can.CanError:
        print("COULD NOT SEND THE MESSAGE")

sleeptime = 0.1
while True:
    send2can(can.Message(arbitration_id=dm1.frame_id, data=dm1.encode({'FlashAmberWarningLamp': 1, 'FlashRedStopLamp': 1})))
    time.sleep(sleeptime)