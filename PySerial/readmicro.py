import serial, requests

port = "COM3"
baud = 115200

s = serial.Serial(port)
s.baudrate = baud

light = 0
temp = 0
ultrasonic = 0
pir = False

url = "http://127.0.0.1:8000/api/facility/reading/"

while True:
    data = s.readline()
    converted = data.decode('utf-8')
    if 'light' in converted:
        lightVal = converted[6:]
        lightInt = int(lightVal)
        light = lightInt
        print('light value: ')
        print(lightInt)
    elif 'temp' in converted:
        tempVal = converted[5:]
        tempInt = int(tempVal)
        temp = tempInt
        print("temp value: ")
        print(tempInt)
    elif 'ultrasonic' in converted:
        ultraVal = converted[11:]
        ultraInt = int(float(ultraVal))
        ultrasonic = ultraInt
        print("ulta value: ")
        print(ultraInt)
    elif 'pir' in converted:
        pirVal = converted[4:]
        pirInt = int(pirVal)
        if pirInt == 1:
            pir = True
        else:
            pir = False

        payload = {
            'facility' : 1,
            'pir': pir,
            'temperature': temp,
            'light': light,
            'ultrasonic': ultrasonic
        }

        response = requests.post(url, data=payload)

        print("pir value: ")
        print(pirInt)

        print(response.content)
    #print(converted)