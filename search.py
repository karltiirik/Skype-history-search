__author__ = 'Karl Tiirik'

import sqlite3
import argparse
import datetime
import os
import html


def parse_args():
    parser = argparse.ArgumentParser(description='Search Skype messages by username and date')
    parser.add_argument('date', type=str, help='a valid date in format YYYY-MM-DD')
    parser.add_argument('name', type=str, help='Skype user display name')
    arguments = parser.parse_args()
    return arguments


def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        print('Incorrect data format, should be YYYY-MM-DD')
        return False


def get_messages(date, person):
    with sqlite3.connect(os.path.join('Database', 'main.db')) as db:
        c = db.cursor()
        start_date = date + ' 00:00:00'
        end_date = date + ' 23:59:99'
        msgs = c.execute('SELECT m.body_xml FROM messages m WHERE DATETIME(m.timestamp, "unixepoch", "localtime") '
                         'BETWEEN ? AND ? AND m.from_dispname = ?', (start_date, end_date, person,))
    return msgs


if __name__ == "__main__":
    args = parse_args()
    if validate_date(args.date):
        messages = get_messages(args.date, args.name)
        for msg in messages:
            try:
                print(html.unescape(msg[0]))
            except TypeError:
                pass
