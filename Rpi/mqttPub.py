import paho.mqtt.client as mqtt
import json


# MQTT_TOPIC = "JM/ALLSENSOR"

client = mqtt.Client()

def publish(broker, MQTT_TOPIC, data):
  MQTT_BROKER_HOST = broker
  MQTT_BROKER_PORT = 1883
  
  client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
  client.publish(MQTT_TOPIC, json.dumps(data))
  client.disconnect()
