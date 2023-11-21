import paho.mqtt.client as mqtt
import json

MQTT_BROKER_HOST = '192.168.1.109'
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "iot/picow"
data = "hello PicoW"

client = mqtt.Client()
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
client.publish(MQTT_TOPIC, data)
client.disconnect()


  
