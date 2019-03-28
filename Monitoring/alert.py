import telegram
import datetime as dt
from datetime import datetime
import requests
import time

bot = telegram.Bot(token='')
chat_id = -1001246134353


while True:
    now = dt.datetime.now()
    try:
        content = requests.get("http://localhost:8000/alert").json()
        print(content)
        message = "<b>Wastage has been detected</b>" + " at " + str(datetime.now()) 
        if content['wastage_detected']:
            #if content['lights_on']:
            #    message += "Lights are turned on <br>"
            #if content['aircon_on']:
            #    message += "Air conditioning is turned on <br>"
            message += ". No one is present in the room. Please proceed to the Energise room to switch the utilities off."
            print(message)
            bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)
    except requests.exceptions.RequestException as e:
        bot.send_message(chat_id=chat_id, text="Server is down", parse_mode=telegram.ParseMode.HTML)
    finally:
        time.sleep(600)

