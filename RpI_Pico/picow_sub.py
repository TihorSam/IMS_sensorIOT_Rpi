import netman
import time
from umqttsimple import MQTTClient

country = 'IN'
ssid = 'sai'
password = 'sai38380'
wifi_connection = netman.connectWiFi(ssid,password,country)

#mqtt config
mqtt_server = '192.168.1.109'
client_id = ''
user_t = ''
password_t = ''
topic_pub = 'iot/picow'

last_message = 0
message_interval = 5
counter = 0

# the following will set the seconds between 2 keep alive messages
keep_alive=30

#MQTT connect
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, user=user_t, password=password_t, keepalive=60)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

#reconnect & reset
def reconnect():
    print('Failed to connected to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

# This code is executed once a new message is published
def new_message_callback(topic, msg):
    topic , msg=topic.decode('ascii') , msg.decode('ascii')
    print("Topic: "+topic+" | Message: "+msg)

try:
    client = mqtt_connect()
    client.set_callback(new_message_callback)
    client.subscribe(topic_pub.encode('utf-8'))

except OSError as e:
    reconnect()

last_message=time.time()

# Main loop
while True:
    try:
        client.check_msg()
        time.sleep(0.001)
        if (time.time() - last_message) > keep_alive:
              client.publish(topic_pub, "Keep alive message")
              last_message = time.time()

    except OSError as e:
        print(e)
        reconnect()
        pass

client.disconnect()
