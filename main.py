# coding=utf-8
import random
from db import hdfs
from spider.spider import Fetch
from spider.parser import Parser


current_url_set = list()
history_url_set = list()

dbconn = hdfs.HBase("9.111.141.58", "webspider:webindex")

# start url
url = "http://www.baidu.com/"

f = Fetch()
while True:
    try:
        html = f.gethtml(url)
        if not html:
            print("Exception:   " + "get no text")
            url = f.selectdifferenturl(current_url_set, history_url_set, url)

        linklist = Fetch.parselink(html)

        for link in linklist:
            if Fetch.verifyurl(link):
                dbconn.putdata(link, "")

        # 清空current_url_set
        current_url_set.clear()

        for link in linklist:
            current_url_set.append(link)

        # if len(current_url_set) > 0:
        #     url = random.choice(current_url_set)
        #     current_url_set.remove(url)
        #     history_url_set = Parser.inserttohistory(current_url_set, history_url_set)
        # else:
        #     current_url_set = random.choice(history_url_set)
        #     # history_url_set.remove(current_url_set)
        #     url = random.choice(current_url_set)
        #     current_url_set.remove(url)
        url = f.selectdifferenturlandinserthistory(current_url_set, history_url_set, url, 20)

        print("history_url_set: " + str(len(history_url_set))
              + "    " + "current_url_set:    " + str(len(current_url_set)))
    except Exception as e:
        print("Exception:   " + str(e))
        # if len(current_url_set) > 0:
        #     url = random.choice(current_url_set)
        #     current_url_set.remove(url)
        # else:
        #     current_url_set = random.choice(history_url_set)
        #     # history_url_set.remove(current_url_set)
        #     url = random.choice(current_url_set)
        #     current_url_set.remove(url)
        url = f.selectdifferenturl(current_url_set, history_url_set, url)
        continue
