from machine import Pin
import time
import _thread
from umqttsimple import MQTTClient
import netman

# Set up GPIO pins
door_sensor_pin = Pin(28, Pin.IN)
button_pin = Pin(15, Pin.IN, Pin.PULL_UP)
relay_pin = Pin(16, Pin.OUT)

# MQTT configuration
mqtt_server = '192.168.1.109'
client_id = ''
user_t = ''
password_t = ''
topic_pub = 'iot/picow'
topic_remote = 'iot/remote'

# GPIO pins
door_sensor_pin = Pin(14, Pin.IN, Pin.PULL_UP)
button_pin = Pin(15, Pin.IN, Pin.PULL_UP)
relay_pin = Pin(16, Pin.OUT)

# MQTT connect
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, user=user_t, password=password_t, keepalive=60)
    client.connect()
    print('Connected to %s MQTT Broker' % (mqtt_server))
    return client

# Reconnect & reset
def reconnect():
    print('Failed to connect to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

DOOR_STATUS = False

# Core 0: MQTT message processing
def mqtt_thread():
    last_message = time.time()
    keep_alive = 30
    global DOOR_STATUS

    def message_callback(topic, msg):
        nonlocal last_message  # Use nonlocal to access the outer variable
        topic, msg = topic.decode('ascii'), msg.decode('ascii')

        if msg == "open":
            relay_pin.value(1)
            DOOR_STATUS = True
            print("Remote Command:", msg)
            print("Door status: open")
            time.sleep(60)
            relay_pin.value(0)
            print("Door status: closed")
            DOOR_STATUS = False
        elif msg != '200':
            print("Topic: " + topic + " | Message: " + msg)
        else:
            print("Awake")

    # Subscribe to topic and listen for
    try:
        client = mqtt_connect()
        client.set_callback(message_callback)
        client.subscribe(topic_pub.encode('utf-8'))

    except OSError as e:
        reconnect()

    while True:
        try:
            client.check_msg()
            time.sleep(0.1)
            if (time.time() - last_message) > keep_alive:
                client.publish(topic_pub, '200')
                last_message = time.time()

        except OSError as e:
            print(e)
            reconnect()
            pass
    client.disconnect()

# Core 1: GPIO input handling
def gpio_thread():
    
    def button_trigger():
        global DOOR_STATUS
        while True:
            if button_pin.value() == 0 and not DOOR_STATUS:
                relay_pin.value(1)
                DOOR_STATUS = True
                print("Button Triggered")
                print("Open")
                time.sleep(60)
                relay_pin.value(0)
                DOOR_STATUS = False
                print("Button Door status: closed")
                print("Closed")
                time.sleep(0.5)
                client.publish(topic_remote, 'Button Triggered')
            else:
                time.sleep(0.5)

    def door_sensor():
        global DOOR_STATUS
        while True:
            if door_sensor_pin.value() == 1 and not DOOR_STATUS:
                relay_pin.value(1)
                DOOR_STATUS = True
                print("Door sensor")
                print("Open")
                time.sleep(60)
                relay_pin.value(0)
                DOOR_STATUS = False
                print("Closed")
                time.sleep(0.5)
                client.publish(topic_remote, 'Door Triggered')
            else:
                time.sleep(0.5)

    while True:
        try:
            door_sensor()
            time.sleep(0.1)
            button_trigger()
            time.sleep(0.1)
        except OSError as e:
            print(e)
            reconnect()
            pass
    client.disconnect()

# Start the two threads on separate cores
_thread.start_new_thread(mqtt_thread, ())
gpio_thread()

# # Main loop (empty)
# while True:
#     time.sleep(1)
