import telegram
import datetime as dt
from datetime import datetime, timezone
import requests
import time
import pytz
import json

bot = telegram.Bot(token='')
chat_id = -1001246134353


while True:
    now = dt.datetime.now()
    try:
        content = requests.get("http://localhost:8000/sensor_health").json()
        print(content)
        time_now = pytz.utc.localize(datetime.now(), is_dst=None).astimezone(pytz.timezone("Asia/Singapore"))
        date_now = time_now.date()
        print(time_now)
        message = "<b>Wastage has been detected</b>" + " at " + str(date_now)[8:10] + "-" + str(date_now)[5:7] + "-" + str(date_now)[0:4] + ", " + str(time_now.time())[0:5]
        if content['ultra']['value'] > 510:
            waste = False
            if content['light']['value'] > 18:
                waste = True
                message += "; the lights are turned on"
            if content['temp']['value'] < 26:
                waste = True
                message += "; the air conditioning is turned on"
            if waste:
                message += ", please proceed to turn them off. No one is present in the room."
                print(message)
                bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)
    except requests.exceptions.RequestException as e:
        bot.send_message(chat_id=chat_id, text="Server is down", parse_mode=telegram.ParseMode.HTML)
    except ValueError:
        print("error")
    finally:
        time.sleep(30)