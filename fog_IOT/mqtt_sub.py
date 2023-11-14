import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient

# Define MQTT broker information
MQTT_BROKER_HOST = "65.2.135.170"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "JM/ALLSENSOR"

# Define MongoDB connection information
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "jm"
MONGO_COLLECTION = "IoTSensorData"

# MQTT callback when the client connects
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    # Subscribe to the MQTT topic
    client.subscribe(MQTT_TOPIC)

# MQTT callback when a message is received on the MQTT topic
def on_message(client, userdata, msg):
    try:
        # Decode the received JSON message
        data = json.loads(msg.payload.decode())
        
        # Connect to MongoDB
        mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
        db = mongo_client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        
        # Insert the JSON data into MongoDB
        collection.insert_one(data)
        
        print("Data inserted into MongoDB:")
        print(data)
        
        # Disconnect from MongoDB
        mongo_client.close()
    except Exception as e:
        print(f"Error: {str(e)}")

# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)

# Start the MQTT client loop
client.loop_forever()
