import paho.mqtt.client as mqtt
import json
import time

# MQTT configurations
fog_node_ip = "fog-node-ip"  # Replace with the actual IP of the fog node
fog_node_port = 1883
data_topic = "edge/data"
ack_topic = "fog/ack"

# Create a MQTT client instance
client = mqtt.Client()

# Callback function for connection to MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Failed to connect to MQTT broker with code {rc}")

# Callback function for receiving acknowledgment from fog node
def on_message(client, userdata, message):
    if message.topic == ack_topic:
        print("Acknowledgment received from fog node")

# Connect MQTT client to the broker
client.on_connect = on_connect
client.on_message = on_message
client.connect(fog_node_ip, fog_node_port)

# Subscribe to acknowledgment topic
client.subscribe(ack_topic)

# Function to send data to fog node
def send_data():
    data = {"sensor": "temperature", "value": 25}
    client.publish(data_topic, json.dumps(data))
    print("Data sent to fog node")

# Main loop
while True:
    send_data()  # Send data to fog node
    client.loop_start()  # Start MQTT loop to listen for acknowledgment
    time.sleep(5)  # Wait for acknowledgment
    client.loop_stop()  # Stop MQTT loop temporarily
    time.sleep(5)  # Wait before sending next data