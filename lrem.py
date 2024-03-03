import csv
from datetime import datetime

from tabulate import tabulate

def compute_stats(msgs, n_top,
                  first_day=None):

    today = msgs[-1][0]
    n_msgs = len(msgs)
    msg_d = {}
    for msg in msgs:
        if msg[1] != 'Profil supprimé':
            msg_d.setdefault(msg[1], [])
            msg_d[msg[1]].append(msg[0])

    first = {}
    for user in msg_d:
        first[user] = min(msg_d[user])

    def _key(_k):
        return len(msg_d[_k])

    sorted_users = sorted(msg_d,
                          key=_key,
                          reverse=True)

    cols = ['#', 'pseudo', 'posts', '%']
    if first_day is None:
        cols.append('posts/jour depuis 1er post')
        cols.append('actif depuis')
    else:
        cols.append('posts/jour')

    vals = []

    i = 1
    for user in sorted_users[:n_top]:
        n_user = len(msg_d[user])
        share = len(msg_d[user]) / n_msgs
        if first_day is None:
            msg_per_day = len(msg_d[user]) / (today - first[user]).days
            active_since = first[user].strftime('%d-%m-%Y')
        else:
            msg_per_day = len(msg_d[user]) / (today - first_day).days
        user_vals = [f'{i}', user, f'{n_user}', f'{share:.2%}', f'{msg_per_day:.1f}']
        if first_day is None:
            user_vals.append(active_since)
        vals.append(user_vals)
        i += 1

    print(tabulate(vals, cols, tablefmt='grid'))

all_msgs = []
with open('lrem.csv', 'r') as f:
    rdr = csv.DictReader(f)
    for row in rdr:
        all_msgs.append((datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S'), row['username']))

compute_stats(all_msgs, 20)

for yr in range(2016, 2025):
    print()
    print(yr)
    yr_msgs = [_m for _m in all_msgs if _m[0].year == yr]
    compute_stats(yr_msgs, 3,
                  first_day=datetime(yr, 1, 1))
