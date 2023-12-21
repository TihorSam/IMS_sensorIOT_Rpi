import adafruit_dht
import paho.mqtt.client as mqtt
import json, geocoder
import time
from lightsensorRead import readLight
import mh_z19
import board, geocoder
import sds011
from mqttPub import publish
from getaqi import calculate_overall_aqi

#Connect and wakeup PM Sensor
sensor = sds011.SDS011("/dev/ttyUSB0", use_query_mode=True)
sensor.sleep(sleep=0)

#get lat and long
location = geocoder.ip('me')
if location.ok:
    latitude = location.latlng[0]
    longitude = location.latlng[1]
else:
    latitude = 0.0
    longitude = 0.0


#read light sensor
try:
  lightlevel = round(readLight(),2)
except:
  lightlevel = -1.0
#light sensor value is -1 if there is sensor error

#read CO2 level
try:
    co2Sensor = mh_z19.read_all()
    co2Sensor = mh_z19.read_all()
    co2 = co2Sensor['co2']
    temperatureco2 = co2Sensor['temperature']
except:
  co2 = -1
  temperatureco2 = -1

#Read DHT11
try:
  dhtDevice = adafruit_dht.DHT11(board.D17)
  humidity = dhtDevice.humidity
  temperature = dhtDevice.temperature
except:
  humidity = -1
  temperature = -1

#Read PM2.5 and PM10    
try:
# AQIsensor = SDS011Reader()
# PM = AQIsensor.readValue()
    PM = sensor.query()
    sensor.sleep()
except:
    PM = [-1, -1]

#get AQI values
try:
    aqi = calculate_overall_aqi(PM[0], PM[1], co2)
except:
    aqi = -1

data = {
  'lightlevel':lightlevel,
  'co2':co2,
  'temperatureco2':temperatureco2,
  'pm2_5':PM[0],
  'pm10':PM[1],
  'temperature': temperature,
  'humidity': humidity,
  'aqi': aqi,
  'fetchtime': int(time.time()),
  'lat':latitude,
  'lon':longitude
}
print(data)
publish("192.168.1.16","IMS/ALLSENSOR",data)
