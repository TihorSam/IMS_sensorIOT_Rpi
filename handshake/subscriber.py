import paho.mqtt.client as mqtt

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

# Callback function for receiving data from edge node
def on_message(client, userdata, message):
    if message.topic == data_topic:
        print("Data received from edge node:", message.payload.decode())
        client.publish(ack_topic, "OK")  # Send acknowledgment back to edge node

# Connect MQTT client to the broker
client.on_connect = on_connect
client.on_message = on_message
client.connect(fog_node_ip, fog_node_port)

# Subscribe to data topic
client.subscribe(data_topic)

# Start MQTT loop to listen for messages
client.loop_forever()
