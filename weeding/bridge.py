import can
import cantools
import os
import roslibpy
import sys
import time

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.clock import Clock

clock = 0.5
quality = 0
capacity = 0
emergency = False
cameras = True


client = roslibpy.Ros(host="150.140.148.140", port=2233)
while not client.is_connected:
    try:
        client.run()
    except:
        time.sleep(5)
        print("NOT CONNECTED")

if os.name == 'nt':
    bus = can.interface.Bus(channel=3, bustype='vector', app_name=None)
else:
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

dbc = """VERSION ""
BO_ 2365194522 PD_Loader: 8 SEND
  SG_ Quality : 0|32@1+ (1,0) [0|100] "%"  Loader
  SG_ Capacity : 32|32@1+ (1,0) [0|4294967295] "mm2/s"  Loader
BO_ 2566834709 DM1: 8 SEND
  SG_ FlashRedStopLamp : 12|2@1+ (1,0) [0|3] "" Vector__XXX
  SG_ FlashAmberWarningLamp : 10|2@1+ (1,0) [0|3] "" Vector__XXX
BO_ 2365475321 GBSD: 8 Vector__XXX
 SG_ GroundBasedMachineSpeed : 0|16@1+ (0.001,0) [0|64.255] "m/s" Vector__XXX
BO_ 2314732030 GNSSPositionRapidUpdate: 8 Bridge
 SG_ Longitude : 32|32@1- (1E-007,0) [-180|180] "deg" Vector__XXX
 SG_ Latitude : 0|32@1- (1E-007,0) [-90|90] "deg" Vector__XXX
"""

dm1 = cantools.db.load_string(dbc, 'dbc').get_message_by_name("DM1")
pdl = cantools.db.load_string(dbc, 'dbc').get_message_by_name("PD_Loader")
gbsd = cantools.db.load_string(dbc, 'dbc').get_message_by_name("GBSD")
gnss = cantools.db.load_string(dbc, 'dbc').get_message_by_name("GNSSPositionRapidUpdate")

amber_topic = roslibpy.Topic(client, '/lsp1/camera_on_flag', 'std_msgs/Bool')
red_topic = roslibpy.Topic(client, '/lsp1/emergency_stop_flag', 'std_msgs/Bool')
capacity_topic = roslibpy.Topic(client, '/lsp1/capacity', 'std_msgs/Int16')
quality_topic = roslibpy.Topic(client, '/lsp1/quality', 'std_msgs/Int16')
longitude_topic = roslibpy.Topic(client, '/lsp1/longitude', 'std_msgs/Float32')
latitude_topic = roslibpy.Topic(client, '/lsp1/latitude', 'std_msgs/Float32')
speed_topic = roslibpy.Topic(client, '/lsp1/speed', 'std_msgs/Float32')
odometry_topic = roslibpy.Topic(client, '/lsp1/odometry', 'nav_msgs/Odometry')

r4c_topic = roslibpy.Topic(client, '/r4c_lsp1', 'r4c_interfaces/msg/R4C')


def send2can(message):
    try:
        bus.send(message)
        print(message)
    except can.CanError:
        print("Message NOT sent")


def recv4can(db):
    data = None
    try:
        message = bus.recv()
        data = db.decode(message.data)
    except can.CanError:
        print("Message NOT sent")
    return data


def send2topic(topic, message):
    topic.publish(roslibpy.Message(message))
    print(message)


def callback(dt):
    print("CAN:")
    send2can(can.Message(arbitration_id=pdl.frame_id, data=pdl.encode({'Capacity': capacity, 'Quality': quality})))
    send2can(can.Message(arbitration_id=dm1.frame_id, data=dm1.encode({'FlashAmberWarningLamp': int(cameras), 'FlashRedStopLamp': int(emergency)})))

    gnss_message = recv4can(gnss)
    gbsd_message = recv4can(gbsd)

    print("BRIDGE:")
    send2topic(capacity_topic, {'data': capacity})
    send2topic(quality_topic, {'data': quality})
    send2topic(amber_topic, {'data': cameras})
    send2topic(red_topic, {'data': emergency})
    send2topic(speed_topic, {'data': float(gbsd_message["GroundBasedMachineSpeed"])})
    send2topic(longitude_topic, {'data': float(gnss_message["Longitude"])})
    send2topic(latitude_topic, {'data': float(gnss_message["Latitude"])})
    send2topic(odometry_topic, {
        "pose": {
            "pose": {
                "position": {"x": float(gnss_message["Longitude"]), "y": float(gnss_message["Latitude"])}
            }
        },
        "header": {"frame_id": "odom"}
    })
    send2topic(r4c_topic, {"longitude": float(gnss_message["Longitude"]), "latitude": float(gnss_message["Latitude"]), "speed": int(gbsd_message["GroundBasedMachineSpeed"])})
    print("-------\n")


Builder.load_file("control.kv")


class MyLayout(Widget):
    def slide_capacity(self, *args):
        global capacity
        capacity = int(args[1])
        self.capacity_slider_value.text = str(capacity)
        # send2topic(capacity_topic, capacity)
        # send2can(can.Message(arbitration_id=capacity_msg.frame_id, data=capacity_msg.encode({'Capacity':capacity})))

    def slide_quality(self, *args):
        global quality
        quality = int(args[1])
        self.quality_slider_value.text = str(quality)
        # send2topic(quality_topic, quality)
        # send2can(can.Message(arbitration_id=quality_msg.frame_id, data=quality_msg.encode({'Quality':quality})))

    def switch_cameras(self, switchObject, switchValue):
        global cameras
        cameras = bool(switchValue)
        # send2topic(amber_topic, cameras)
        # send2can(can.Message(arbitration_id=amber_msg.frame_id, data=amber_msg.encode({'FlashAmberWarningLamp':int(cameras)})))
 
    def button_emergency(self):
        global emergency
        emergency = not emergency
        # send2topic(red_topic, emergency)
        # send2can(can.Message(arbitration_id=red_msg.frame_id, data=red_msg.encode({'FlashRedStopLamp':int(emergency)})))

class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == "__main__":
    Clock.schedule_interval(callback, clock)
    MyApp().run()
