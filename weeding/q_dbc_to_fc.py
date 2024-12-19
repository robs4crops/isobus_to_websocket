import roslibpy
import time
import can
import struct
import cantools

class Com():
    def __init__(self):
        self.canbus = None
        self.iters = 50
        self.sleeper = 1
        self.bridge = roslibpy.Ros(host="10.147.17.52", port=2233)

        self.dbc = """VERSION ""
        BO_ 2365194536 PD_Loader: 8 SIM
            SG_ Capacity : 32|32@1+ (1,0) [0|4294967295] "mm2/s"  Loader
            SG_ Quality : 0|32@1+ (1,0) [0|100] "%"  Loader
        """

        self.id = 0xCFA011A
        self.db = cantools.db.load_string(self.dbc, 'dbc').get_message_by_name("PD_Loader")
        self.quality_topic = roslibpy.Topic(self.bridge, '/lspn/quality', 'std_msgs/Int16')
        self.capacity_topic = roslibpy.Topic(self.bridge, '/lspn/capacity', 'std_msgs/Int16')

    def send_topic(self, topic, message):
        topic.publish(roslibpy.Message(message))

    def sleep(self):
        time.sleep(self.sleeper)
    
    def recv_can(self, db, id):
        data = None
        try:
            i = 0
            while(i < self.iters):
                i = i + 1
                message = self.canbus.recv()
                if message.arbitration_id == id:
                    data = db.decode(message.data)
                    break
        except can.CanError:
            print("MESSAGE NOT RECIEVED")
        return data
 
    def send_topic(self, topic, message):
        topic.publish(roslibpy.Message(message))
        print(message)


def main(args=None):
    com = Com()
    while not com.bridge.is_connected:
        try:
            print("BRIDGE CONNECTED")
            com.bridge.run()
        except:
            print("BRIDGE NOT CONNECTED")
            time.sleep(5)

    while com.canbus is None:
        try:
            com.canbus = can.interface.Bus(channel=2, bustype='vector', app_name="CANoe", fd=True)
            print("CAN CONNECTED")
        except:
            print("CAN NOT CONNECTED")
            time.sleep(5)

    while True:
        message = com.recv_can(com.db, com.id)
        if message is None:
            print("MESSAGE NOT RECIEVED, LOOKING AGAIN...")
            continue
        quality = message['Quality']
        capacity = message['Capacity']

        print(f"Quality: {quality}")
        com.send_topic(com.quality_topic, {'data': quality})
        print(f"Capacity: {capacity}")
        com.send_topic(com.capacity_topic, {'data': capacity})


if __name__ == '__main__':
    main()
