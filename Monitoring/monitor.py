import telegram
import datetime as dt
from datetime import datetime
import requests
import time

bot = telegram.Bot(token='709093710:AAFsz53pcCxcTZU2fhche6ihnJoKG9jTjcA')
chat_id = -1001155518486


while True:
    now = dt.datetime.now()
    content = requests.get("http://iot.jordysamuel.com:8000/api/facility/reading/").json()
    created_at = content['data']['items'][0]['created_at'][0:-6]
    created = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.%f')
    if now - created > dt.timedelta(minutes=10):
        bot.send_message(chat_id=chat_id, text="<b>Data Not collected</b>" + " at " + created_at, parse_mode=telegram.ParseMode.HTML)
    time.sleep(600)
