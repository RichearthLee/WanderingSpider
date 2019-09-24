# coding=utf-8

from spider.spider import Fetch
from spider.parser import Parser
from db.controller import Controller

from concurrent.futures import ThreadPoolExecutor
import configparser


def execution(url, historysize):
    current_url_set = list()
    history_url_set = list()
    dbctl = Controller()

    f = Fetch()
    p = Parser()
    # url = "www.baidu.com"
    while True:
        try:
            # html = f.gethtml(url)
            # if not html:
            #     print("Exception:   " + "get no text")
            #     url = p.selectdifferenturl(current_url_set, history_url_set, url)
            #     continue

            resbody = f.parselink(url)
            if not resbody:
                print("Exception:   " + "get nothing")
                url = p.selectdifferenturl(current_url_set, history_url_set, url)
                continue

            for node in resbody:
                dbctl.insert(node['link'], node['title'])

            # 清空current_url_set
            current_url_set.clear()

            for node in resbody:
                current_url_set.append(node['link'])

            url = p.selectdifferenturlandinserthistory(current_url_set, history_url_set, url, historysize)

            print("history_url_set: " + str(len(history_url_set))
                  + "    " + "current_url_set:    " + str(len(current_url_set)))
        except Exception as e:
            print("Exception:   " + str(e))
            url = p.selectdifferenturl(current_url_set, history_url_set, url)
            continue


config = configparser.ConfigParser()
config.read("config")
# start url
starturl = config['main']['startURL']
threads = config["main"]["threads"]
historysize = config['main']['historysize']

threads = int(threads)
historysize = int(historysize)
t = ThreadPoolExecutor(max_workers=threads)

for i in range(threads):
    t.submit(execution, starturl, historysize)

