from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup

start_date = date(2017, 1, 1)
end_date = datetime.utcnow().date()
delta = end_date - start_date

for chat_date in (start_date + timedelta(n) for n in range(delta.days)):
    page = 1
    while True:
        response = requests.get('https://botbot.me/freenode/django/{}/?page={}'.format(chat_date.strftime('%Y-%m-%d'), page), headers={
            'X-Requested-With': 'XMLHttpRequest',
        })
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        actor = None
        for msg in soup.select('.privmsg'):
            actors = msg.select('.actor')
            if actors:
                actor = actors[0].get_text()
            message = msg.select('.message')[0].get_text()
            timestamp = msg.find('time').attrs['datetime']

            print('{}: {}: {}'.format(timestamp, actor, message))

        page += page
