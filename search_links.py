__author__ = 'Karl Tiirik'

import sqlite3
import urllib.request as urllib

from bs4 import BeautifulSoup


def get_all_messages():
    db = sqlite3.connect('Database\\main.db')  # TODO: this needs os.path or smth smarter the future
    c = db.cursor()
    c.execute('SELECT from_dispname, body_xml,  DATETIME(timestamp, "unixepoch", "localtime") FROM messages')
    msgs = c.fetchall()
    return msgs


def find_links(msgs):
    msgs_w_links = []
    for m in msgs:
        soup = BeautifulSoup(str(m[1]))
        link = soup.findAll('a')
        if link:
            for i in range(len(link)):
                url = (link[i].get('href'))
                msgs_w_links.append([m[0], url, m[2]])
    return msgs_w_links


def create_report(msgs):
    # TODO: Refactored using some python package
    html = """<!DOCTYPE html>
    <html>
    <head>
    <title>Skype link history</title>
    <meta charset="utf-8">
    </head>
    <body>
    <h1>Skype link history</h1>
    """
    html += """<table align="left" border="0" cellpadding="5" cellspacing="5">
    <thead>
        <tr>
            <th scope="col">Person</th>
            <th scope="col">URL</th>
            <th scope="col">Date</th>
        </tr>
    </thead>
    <tbody>
    """
    for m in msgs:
        html += """<tr>"""
        html += '<td>' + m[0] + '</td>'
        page_title = get_title(m[1])
        html += '<td>' + '<a href="' + m[1] + '">' + page_title + '</a>''</td>'
        html += '<td>' + m[2] + '</td>'
        html += '</tr>'
    html += """</tbody>
    </table>
    </body>
    </html>"""
    with open('report.html', 'w', encoding="utf8") as report:
        report.write(html)


def get_title(url):
    soup = BeautifulSoup(urllib.urlopen(url))
    if soup.title is not None:
        return soup.title.string
    else:
        return url


if __name__ == "__main__":
    msg = get_all_messages()
    msg = find_links(msg)
    create_report(msg)