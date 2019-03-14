import requests, time
import paho.mqtt.client as mqtt

url = "iot.jordysamuel.com"
client = mqtt.Client("server")
def on_message(client, userdata, message):
    print("message received", str(message.payload.decode('utf-8')))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
client.on_message = on_message
client.connect(url)
client.subscribe("pi1/temp")
client.subscribe("pi1/light")
client.subscribe("pi1/pir")
client.subscribe("pi1/ultra")
client.loop_forever()




