from bs4 import BeautifulSoup
import csv
from datetime import datetime
import urllib.request

def get_messages(url):
    page_msgs = []

    fp = urllib.request.urlopen(url)
    bytes = fp.read()

    page_s = bytes.decode('UTF-8').replace(u'\xa0', ' ').replace('&nbsp;', ' ')
    fp.close()

    soup = BeautifulSoup(page_s,
                         features='lxml')

    msgs = soup.find_all('tr', {'class': 'message'})

    for msg in msgs[1:]:
        username = msg.find_all('b', {'class': 's2'})[0].get_text()
        if len(username) > 11:
            username = username[:10] + username[11:]
        username = username.strip()

        date_s = msg.find_all('div', {'class': 'left'})[0].get_text().strip()

        if username != 'Publicité':
            _, _, day_s, _, hour_s = date_s.split(' ')

            day, month, year = day_s.split('-')
            hour, minute, second = hour_s.split(':')

            dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

            page_msgs.append((dt, username))

    return page_msgs


messages = []
for i in range(28000, 29559):
    print(i)
    url = 'https://forum.hardware.fr/hfr/Discussions/politique/lrem-sebastopol-vite-sujet_113751_%d.htm' % i
    
    messages += get_messages(url)

with open('lrem8.csv', 'w') as f:
    wtr = csv.writer(f)

    wtr.writerow(['date', 'username'])
    for dt, username in messages:
        wtr.writerow([dt, username])
