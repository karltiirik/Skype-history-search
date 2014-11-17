__author__ = 'Karl Tiirik'

import sqlite3
from bs4 import BeautifulSoup
import urllib.request as urllib


def get_all_messages():
    db = sqlite3.connect('Database\\main.db')  #TODO: this needs os.path or smth smarter the future
    c = db.cursor()
    c.execute('SELECT from_dispname, body_xml,  DATETIME(timestamp, "unixepoch", "localtime") FROM messages')
    msgs = c.fetchall()
    return msgs


def find_links(msgs):
    msgs_w_links = []
    for m in msgs:
        soup = BeautifulSoup(str(m[1]))
        link = soup.findAll('a')
        if link != []:
            for i in range(len(link)):
                url = (link[i].get('href'))
                msgs_w_links.append([m[0], url, m[2]])
    return msgs_w_links

def create_report(msgs):
    # TODO: Implement HTML report creation
    pass

def get_title(url):
    soup = BeautifulSoup(urllib.urlopen(url))
    return soup.title.string

if __name__ == "__main__":
    msg = get_all_messages()
    msg = find_links(msg)