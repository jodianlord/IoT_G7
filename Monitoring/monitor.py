import telegram
import datetime as dt
from datetime import datetime
import requests
import time

bot = telegram.Bot(token='709093710:AAFsz53pcCxcTZU2fhche6ihnJoKG9jTjcA')
chat_id = -1001155518486


while True:
    now = dt.datetime.now()
    try:
        content = requests.get("http://localhost:8000/get_latest").json()
        created_at = content['created_at'][0:-6]
        created = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.%f')
        if now - created > dt.timedelta(minutes=10):
            bot.send_message(chat_id=chat_id, text="<b>Data Not collected</b>" + " at " + created_at, parse_mode=telegram.ParseMode.HTML)
    except requests.exceptions.RequestException as e:
        bot.send_message(chat_id=chat_id, text="Server is down", parse_mode=telegram.ParseMode.HTML)
    finally:
        time.sleep(600)

