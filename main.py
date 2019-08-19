# coding=utf-8
import random
from db import hdfs
from spider.spider import Fetch
from spider.parser import Parser


current_url_set = set()
history_url_set = list()

dbconn = hdfs.HBase("9.111.141.58", "webspider:webindex")

# start url
url = "http://www.163.com/"

f = Fetch()
while True:
    try:
        html = f.gethtml(url)
        if not html:
            print("Exception:   " + "state code is not 200")
            if len(current_url_set) > 0:
                url = current_url_set.pop()
            else:
                current_url_set = random.choice(history_url_set)
                history_url_set.remove(current_url_set)
                url = current_url_set.pop()
            continue

        linklist = Fetch.parselink(html)

        for link in linklist:
            if Fetch.verifyurl(link):
                dbconn.putdata(link, "")

        # 清空current_url_set
        current_url_set.clear()

        for link in linklist:
            current_url_set.add(link)

        if len(current_url_set) > 0:
            url = current_url_set.pop()
            history_url_set = Parser.inserttohistory(current_url_set, history_url_set)
        else:
            current_url_set = random.choice(history_url_set)
            history_url_set.remove(current_url_set)
            url = current_url_set.pop()

        print("history_url_set: " + str(len(history_url_set))
              + "    " + "current_url_set:    " + str(len(current_url_set)))
    except Exception as e:
        print("Exception:   " + str(e))
        if len(current_url_set) > 0:
            url = current_url_set.pop()
        else:
            current_url_set = random.choice(history_url_set)
            history_url_set.remove(current_url_set)
            url = current_url_set.pop()
        continue
