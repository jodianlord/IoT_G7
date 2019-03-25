import requests, time
import paho.mqtt.client as mqtt

url = "iot.jordysamuel.com"
client = mqtt.Client("server")
def on_message(client, userdata, message):
    print("message came in")
    if message.topic == "pi1/temp":
        tempInt = int(message.payload.decode('utf-8'))
        print("tempInt: ", tempInt)

        postURL = "http://127.0.0.1:8000/api/facility/reading/"
        data = {
            "facility" : 1,
            "reading_type" : "temp",
            "value" : float(tempInt)
        }
        print(requests.post(postURL, data).text)        
    elif message.topic == "pi1/ultra":
        ultraFloat = float(message.payload.decode('utf-8'))
        print("ultraFloat: ", ultraFloat)

        postURL = "http://127.0.0.1:8000/api/facility/reading/"
        data = {
            "facility" : 1,
            "reading_type" : "ultra",
            "value" : ultraFloat
        }
        print(requests.post(postURL, data).text)
    elif message.topic == "pi1/pir":
        pirInt = int(message.payload.decode('utf-8'))
        print("pirInt: ", pirInt)

        postURL = "http://127.0.0.1:8000/api/facility/reading/"
        data = {
            "facility" : 1,
            "reading_type" : "pir",
            "value" : float(pirInt)
        }
        print(requests.post(postURL, data).text)
    elif message.topic == "pi1/light":
        lightInt = int(message.payload.decode('utf-8'))
        print('lightInt: ', lightInt)

        postURL = "http://127.0.0.1:8000/api/facility/reading/"
        data = {
            "facility" : 1,
            "reading_type" : "light",
            "value" : float(lightInt)
        }
        print(requests.post(postURL, data).text)

client.on_message = on_message
client.connect(url)
client.subscribe("pi1/temp")
client.subscribe("pi1/light")
client.subscribe("pi1/pir")
client.subscribe("pi1/ultra")
client.loop_forever()