# coding=utf-8

from spider.spider import Fetch
from spider.parser import Parser
from db.controller import Controller
import configparser

config = configparser.ConfigParser()
current_url_set = list()
history_url_set = list()

dbctl = Controller()

# start url
url = config["main"]["startURL"]

f = Fetch()
p = Parser()
while True:
    try:
        html = f.gethtml(url)
        if not html:
            print("Exception:   " + "get no text")
            url = p.selectdifferenturl(current_url_set, history_url_set, url)

        linklist = Fetch.parselink(html)

        for link in linklist:
            dbctl.insert(link, " ")

        # 清空current_url_set
        current_url_set.clear()

        for link in linklist:
            current_url_set.append(link)

        url = p.selectdifferenturlandinserthistory(current_url_set, history_url_set, url, 20)

        print("history_url_set: " + str(len(history_url_set))
              + "    " + "current_url_set:    " + str(len(current_url_set)))
    except Exception as e:
        print("Exception:   " + str(e))

        url = p.selectdifferenturl(current_url_set, history_url_set, url)
        continue
