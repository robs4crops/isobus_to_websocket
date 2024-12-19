import can
import cantools
import os
import time

if os.name == 'nt':
    bus = can.interface.Bus(channel=2, bustype='vector', app_name="CANoe")
else:
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')


dbc = """VERSION ""
BO_ 2619670305 TIM21: 8 Vector__XXX
 SG_ Process_Mulfunction : 8|8@1+ (1,0) [0|0] "" Vector__XXX
"""

tim_id = 0x419351061
tim = cantools.db.load_string(dbc, 'dbc').get_message_by_name("TIM21")

def send2can(message):
    print(can.bus.BusState)
    try:
        bus.send(message)
        print(message)
    except can.CanError:
        print("COULD NOT SEND THE MESSAGE")


def recv_can(db, id):
    data = None
    for i in range(20):
        try:
            message = bus.recv()
            if message.arbitration_id == id:
                data = db.decode(message.data)
                print(data)
        except can.CanError:
            print("MESSAGE NOT RECIEVED")
    return data

# tim_message = recv_can(tim, tim_id)
# print(tim_message)

sleeptime = 0.1
while True:
    send2can(can.Message(arbitration_id=tim.frame_id, data=tim.encode({'Process_Mulfunction': 1})))
    time.sleep(sleeptime)