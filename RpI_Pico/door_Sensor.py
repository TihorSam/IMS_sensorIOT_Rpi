
import utime
from machine import Pin
import machine
import time
from umqttsimple import MQTTClient
import netman
import ujson

country = 'IN'
ssid = 'sai'
password = 'sai38380'
wifi_connection = netman.connectWiFi(ssid,password,country)

# Set up GPIO pins
door_sensor_pin = Pin(28, Pin.IN)
button_pin = Pin(15, Pin.IN, Pin.PULL_UP)
relay_pin = Pin(16, Pin.OUT)

# MQTT configuration
# mqtt_server = '192.168.1.109'
mqtt_server = '65.2.135.170'
client_id = 'pico_client'
user_t = ''
password_t = ''
topic_pub = 'JM/Sensor1'
dp_topic = 'JM/doorpositionsensor'
do_topic = 'JM/doororverride'

# Flag to keep track of door status
# DOOR_STATUS = False

# the following will set the seconds between 2 keep alive messages
keep_alive=60

last_message=time.time()

# Set up MQTT client
# MQTT connect
# def mqtt_connect():
#     client = MQTTClient(client_id, mqtt_server, user=user_t, password=password_t, keepalive=60)
#     client.connect()
#     print('Connected to %s MQTT Broker' % (mqtt_server))
#     return client

# Reconnect & reset
def reconnect():
    print('Failed to connect to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()



def message_callback(topic, msg):
    message = msg.decode('ascii')
    if message != '200': 
        topic, msg = topic.decode('ascii'), ujson.loads(msg.decode())
        door= msg['doorposition']
        if door == 1:
            relay_pin.value(1)
            # DOOR_STATUS = True
            print("=> Remote Command: ", msg)
            print("Door status: open")
            time.sleep(10)
            relay_pin.value(0)
            time.sleep(0.5)
            print("Door status: closed")
            # DOOR_STATUS = False
    else:
        print("Awake")
        

def door_sensor(IR_value):
    # global DOOR_STATUS
    if IR_value == 0:
        print("=> Door sensor")
        # DOOR_STATUS = True
        time.sleep(5)
        # print(dp_output_bytes)
        dp_output_bytes = ujson.dumps(doorPosition)
        client.publish(dp_topic, dp_output_bytes)
    else:
        time.sleep(0.1)

def button_trigger(buttonVal):
    # global DOOR_STATUS
    if buttonVal == 0:
        print("=> Button Triggered")
        relay_pin.value(1)
        # DOOR_STATUS = True
        print("Door status: open")
        time.sleep(5)
        relay_pin.value(0)
        # DOOR_STATUS = False
        print("Door status: closed")
        time.sleep(0.5)
        # print(do_output_bytes)
        do_output_bytes = ujson.dumps(doorOveride)
        client.publish(do_topic, do_output_bytes)
    else:
        time.sleep(0.1)
        
# nodeStatuse = {
#     'Status':'awake',
#     'time':utime.time()
#     }
doorPosition = {
    'accessID':'bafyabxxxx',
    'doorpostionsensor':1,
    'time':utime.time()
    }
# dp_output_bytes = ujson.dumps(doorPosition)
doorOveride = {
    'accessID':'bafyabxxxx',
    'dooroverride':1,
    'time':utime.time()}
# do_output_bytes = ujson.dumps(doorOveride)
# Set up MQTT subscription callback
try:
    client = MQTTClient(client_id, mqtt_server, user=user_t, password=password_t, keepalive=60)
    client.connect()
    print('Connected to %s MQTT Broker' % (mqtt_server))

    client.set_callback(message_callback)
    client.subscribe(topic_pub.encode('utf-8'))

except OSError as e:
    reconnect()


while True: 
    # Check for incoming MQTT messages
    try:
        ir_sensor_value = door_sensor_pin.value()
        button_value = button_pin.value()

        door_sensor(ir_sensor_value)
        button_trigger(button_value)

        client.check_msg()
        time.sleep(0.1)
        if (time.time() - last_message) > keep_alive:
            # node_output_bytes = ujson.dumps(nodeStatuse)
            client.publish(topic_pub, '200')
            last_message = time.time()
    except OSError as e:
        print(e)
        reconnect()
        pass


