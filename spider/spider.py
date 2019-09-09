# coding=utf-8

import requests
import random

from bs4 import BeautifulSoup

from spider.parser import Parser


class Fetch(object):
    headers = None

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0",
        }

    def gethtml(self, url: str) -> str:
        try:
            res = requests.get(url, headers=self.headers, timeout=(5, 7))
        except Exception as e:
            print("CONNECT Exception:   " + url + " " + str(e))
            return None
        print("CONNECT: " + str(res.status_code) + "   " + url)
        if res.status_code != 200:
            return None
        res.encoding = "utf-8"
        return res.text

    @staticmethod
    def parselink(html: str):
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.select('a')
        rmidx = list()
        for i in range(len(links)):
            try:
                if links[i]['href']:
                    links[i] = links[i]['href']
                else:
                    rmidx.append(i)
                    continue
            except Exception as e:
                print("PARSER ERROR:    " + str(e))
                rmidx.append(i)
                continue
        rmidx.reverse()
        for n in range(len(rmidx)):
            links.pop(n)
        Fetch.formatrawurl(links)
        return links

    @staticmethod
    def geturlfromhtml(html):
        set.add(1)

    @staticmethod
    def verifyurl(strurl: str):
        http = strurl.find("http")
        https = strurl.find("https")

        if http is not 0:
            return False

        if https is 0:
            strurl = strurl[5:]
        else:
            strurl = strurl[4:]

        prefix = strurl.find("://")

        if prefix is not 0:
            return False

        strurl = strurl[3:]

        isend = strurl.endswith("/")
        onlyend = strurl.count("/")

        if not isend and onlyend is not 1:
            return False
        return True

    @staticmethod
    def formatrawurl(links: list):
        rmindex = []
        for i in range(len(links)):
            try:
                http = links[i].find('http')
                if http is None or http < 0:
                    rmindex.append(i)
                    continue
                links[i] = links[i][http:]
                sp = links[i].count('/')
                if sp is None or sp < 2:
                    rmindex.append(i)
                    continue
                else:
                    while sp != 2:
                        ri: int = links[i].rfind('/')
                        links[i] = links[i][0: ri]
                        sp = links[i].count('/')
                if links[i].count('.') is None or links[i].count('.') < 1:
                    rmindex.append(i)
                    continue
                links[i] = links[i]+'/'
            except Exception as e:
                print("FORMAT ERROR:    " + str(e))
                rmindex.append(i)
                continue

        rmindex.reverse()
        for n in rmindex:
            links.pop(n)
        return links

    @staticmethod
    def selectdifferenturl(current_url_set: list, history_url_set: list, url: str):
        new_url = url
        while new_url == url:
            try:
                current_url_set.remove(url)
            except Exception:
                None
            if len(current_url_set) > 0:
                new_url = random.choice(current_url_set)
            else:
                current_url_set = random.choice(history_url_set)
                history_url_set.remove(current_url_set)
        return new_url

    @staticmethod
    def selectdifferenturlandinserthistory(current_url_set: list, history_url_set: list, url: str, size: int):
        new_url = url
        flag = True
        while new_url == url:
            try:
                current_url_set.remove(url)
            except Exception:
                None
            if len(current_url_set) > 0:
                new_url = random.choice(current_url_set)
            else:
                flag = False
                current_url_set = random.choice(history_url_set)
                history_url_set.remove(current_url_set)
        if flag and len(current_url_set) > 0:
            Parser.inserttohistory(current_url_set, history_url_set, size)
        return new_url
