__author__ = 'Karl Tiirik'

import sqlite3
import argparse
import datetime


def parse_args():
    parser = argparse.ArgumentParser(description='Search Skype messages by username and date')
    parser.add_argument('date', type=str, help='a valid date in format DD.MM.YYYY')
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
    db = sqlite3.connect('Database\\main.db')  # this needs os.path or smth smarter the future
    c = db.cursor()
    start_date = date + ' 00:00:00'
    end_date = date + ' 24:59:99'
    msgs = c.execute('SELECT m.body_xml FROM messages m WHERE DATETIME(m.timestamp, "unixepoch", "localtime") '
                     'BETWEEN ? AND ? AND m.from_dispname = ?', (start_date, end_date, person,))
    return msgs


if __name__ == "__main__":  # Needs output formatting
    args = parse_args()
    if validate_date(args.date):
        messages = get_messages(args.date, args.name)
        for msg in messages:
            print(msg)
