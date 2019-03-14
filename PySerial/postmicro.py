import requests, time
import paho.mqtt.client as mqtt

class Status:
    pir = False
    pirVal = False

    ultra = False
    ultraVal = 1.0

    temp = False
    tempVal = 0

    light = False
    lightVal = 0

url = "iot.jordysamuel.com"
client = mqtt.Client("server")
def on_message(client, userdata, message):
    if message.topic == "pi1/temp":
        Status.temp = True
        tempInt = int(message.payload.decode('utf-8'))
        Status.tempVal = tempInt
        print("tempInt: ", tempInt)
    elif message.topic == "pi1/ultra":
        Status.ultra = True
        ultraFloat = float(message.payload.decode('utf-8'))
        Status.ultraVal = ultraFloat
        print("ultraFloat: ", ultraFloat)
    elif message.topic == "pi1/pir":
        Status.pir = True
        pirInt = int(message.payload.decode('utf-8'))
        if pirInt == 0:
            Status.pirVal = False
        else:
            Status.pirVal = True
        Status.pirVal = pirInt
        print("pirInt: ", pirInt)
    elif message.topic == "pi1/light":
        Status.light = True
        lightInt = int(message.payload.decode('utf-8'))
        Status.lightVal = lightInt
        print('lightInt: ', lightInt)
    
    #print("message received", str(message.payload.decode('utf-8')))
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)

    if Status.light and Status.pir and Status.temp and Status.ultra:
        postURL = "http://iot.jordysamuel.com:8000/api/facility/reading/"
        data = {
            "facility" : 1,
            "pir" : Status.pirVal,
            "temperature" : Status.tempVal,
            "light" : Status.lightVal,
            "ultrasonic" : Status.ultraVal
        }
        print(requests.post(postURL, data).text)
        Status.light = False
        Status.pir = False
        Status.temp = False
        Status.ultra = False
client.on_message = on_message
client.connect(url)
client.subscribe("pi1/temp")
client.subscribe("pi1/light")
client.subscribe("pi1/pir")
client.subscribe("pi1/ultra")
client.loop_forever()




