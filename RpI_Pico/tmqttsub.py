import paho.mqtt.client as mqtt

# Define MQTT broker information
MQTT_BROKER_HOST = "192.168.1.109"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "iot/picow"

# MQTT callback when the client connects
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    # Subscribe to the MQTT topic
    client.subscribe(MQTT_TOPIC)

# MQTT callback when a message is received
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)

# Start the MQTT client loop
client.loop_forever()
