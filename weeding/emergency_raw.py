import can
import os
import time

class Rosbridge():
    def __init__(self):
        self.sleeper = 1
        self.bridge = roslibpy.Ros(host="10.147.17.52", port=2233)
        self.trigger = roslibpy.Topic(self.bridge, "/lspn/trigger_flag", 'std_msgs/Bool')

    def send_topic(self, topic, message):
        topic.publish(roslibpy.Message(message))
        print(message)

    def sleep(self):
        time.sleep(self.sleeper)


def main(args=None):
    trig = Trigger()


if os.name == 'nt':
    bus = can.interface.Bus(channel=2, bustype='vector', app_name="CANoe", )
else:
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

tim_id = 0x1C24FF21
msg0 = can.Message(
    arbitration_id=tim_id,
    data=[0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    is_extended_id=True
)

def send_can(message):
    print(can.bus.BusState)
    try:
        bus.send(message)
        print(message)
    except can.CanError:
        print("COULD NOT SEND THE MESSAGE")

def recv_can(id):
    data = None
    try:
        message = bus.recv(timeout=2)
        if message is not None and message.arbitration_id == id:
            data = message.data
            return data
    except can.CanError:
        print("MESSAGE NOT RECIEVED")

# tim_message = recv_can(tim_id)
# print(tim_message)

sleeptime = 0.1
while True:
    send_can(msg0)
    time.sleep(sleeptime)