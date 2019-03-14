import serial
import paho.mqtt.client as mqtt

port = "COM6"
baud = 115200

s = serial.Serial(port)
s.baudrate = baud

#url = "http://iot.jordysamuel.com:8000/api/facility/reading/"
url = "iot.jordysamuel.com"

client = mqtt.Client("pi1")
client.connect(url)

while True:
    data = s.readline()
    converted = data.decode('utf-8')
    print(converted)
    if 'light' in converted:
        lightVal = converted[6:]
        lightInt = int(lightVal)
        client.publish("pi1/light", lightInt)
    elif 'temp' in converted:
        tempVal = converted[5:]
        tempInt = int(tempVal)
        client.publish("pi1/temp", tempInt)
    elif 'ultra' in converted:
        ultraVal = converted[6:]
        ultraFloat = float(ultraVal)
        client.publish("pi1/ultra", ultraFloat)
    elif 'pir' in converted:
        pirVal = converted[4:]
        pirInt = int(pirVal)
        client.publish("pi1/pir", pirInt)