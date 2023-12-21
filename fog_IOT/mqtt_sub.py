import paho.mqtt.client as mqtt
import json
# from pymongo import MongoClient
import pymysql

# Define MQTT broker information
MQTT_BROKER_HOST = "192.168.1.16"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "IMS/ALLSENSOR"

# MySQL database configuration
MYSQLHOST = "localhost"
MYSQLUSER = "user"
MYSQLPASSWORD = "root"
MYSQLDATABASE = "IMS_sensorData"


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

        # Connect to the MySQL database
        db = pymysql.connect(
            host=MYSQLHOST,
            user=MYSQLUSER,
            password=MYSQLPASSWORD,
            database=MYSQLDATABASE
        )
        # Create a cursor object to interact with the database
        cursor = db.cursor()
        # Store the values in the MySQL database 
        insert_query = "INSERT INTO building_sensor_data (lightlevel, co2, temperatureco2, pm2_5, pm10, temperature, humidity, aqi, fetchtime, lat, lon) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (data['lightlevel'], data['co2'], data['temperatureco2'], data['pm2_5'], data['pm10'], data['temperature'], data['humidity'], data['aqi'], data['fetchtime'], data['lat'], data['lon'])
        cursor.execute(insert_query, values)
        db.commit()
        print("Data stored in MySQL database")
       # Close the cursor and database connection
        cursor.close()
        db.close()
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
