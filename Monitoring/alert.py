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
        if content['wastage_detected']:
            print("YES")
            bot.send_message(chat_id=chat_id, text="<b>Wastage has been detected</b>" + " at " + now, parse_mode=telegram.ParseMode.HTML)
    except requests.exceptions.RequestException as e:
        bot.send_message(chat_id=chat_id, text="Server is down", parse_mode=telegram.ParseMode.HTML)
    finally:
        time.sleep(600)

