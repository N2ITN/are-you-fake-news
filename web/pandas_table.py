import hashlib
import random

import pandas

from mongo_ip import DB
pandas.set_option('display.expand_frame_repr', False)


def make_table():
    df = pandas.DataFrame(list(DB['ip_logs'].find()))
    df['2time'] = pandas.to_datetime(df['time'])
    df = df.sort_values('2time', ascending=False)
    table = df[['time', 'city', 'region_name', 'ip', 'request']].head(250)
    table['ip_NaCl'] = df['ip'].apply(
        lambda row: hashlib.md5(bytes(row.encode('utf-8'))).hexdigest()[7:12])
    table = table.drop('ip', axis=1)
    return table


if __name__ == '__main__':
    print(make_table())


def run():
    with open('templates/data.html', 'w') as t:
        t.write(
            '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/milligram/1.1.0/milligram.min.css">'
        )
        t.write(make_table().to_html(index=False, justify='center'))


run()
