# coding=utf-8

import requests
import re

from bs4 import BeautifulSoup


class Fetch(object):
    headers = None

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0",
        }

    def gethtml(self, url: str):
        try:
            res = requests.get("http://"+url, headers=self.headers, timeout=(5, 7))
        except Exception as e:
            # print("CONNECT Exception:   " + url + " " + str(e))
            return None
        # print("CONNECT: " + str(res.status_code) + "   " + url)
        if res.status_code != 200:
            return None
        res.encoding = "utf-8"
        return res.text

    def parselink(self, url: str):
        html = self.gethtml(url)
        if not html:
            return None
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.select('a')
        if not links:
            return None
        rmidx = list()
        for i in range(len(links)):
            try:
                if 'href' in links[i].attrs:
                    links[i] = links[i]['href']
                else:
                    rmidx.append(i)
                    continue
                if type(links[i]) is not str:
                    rmidx.append(i)
                    continue
            except Exception as e:
                print("PARSER ERROR:    " + str(e))
                rmidx.append(i)
                continue
        rmidx.reverse()
        for n in rmidx:
            links.pop(n)
        links = self.formatrawurl(links)
        links = set(links)
        links.remove(url)
        # return list(links)
        return self.gettitle(list(links))

    def gettitle(self, links: list):
        try:
            for i in range(len(links)):
                links[i] = {'link': links[i], 'title': ''}
                html = self.gethtml(links[i]['link'])
                # html = None
                if not html:
                    continue
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.select('title')
                if title:
                    title = title[0].string
                    links[i]['title'] = title
        except Exception as e:
            print("Title : " + str(e))
        return links

    @staticmethod
    def formatrawurl(links: list):
        rmindex = []
        for i in range(len(links)):
            try:
                # prefix = max(links[i].find('http://'), links[i].find('https://'))
                # if prefix is -1:
                #     rmindex.append(i)
                #     continue
                # links[i] = links[i][prefix:]
                h = re.search("http://", links[i])
                hs = re.search("https://", links[i])
                if h:
                    links[i] = links[i][h.span()[1]:]
                elif hs:
                    links[i] = links[i][hs.span()[1]:]
                else:
                    rmindex.append(i)
                    continue

                if links[i].count('.') is None or links[i].count('.') < 1:
                    rmindex.append(i)
                    continue

                index = re.search("[^A-Za-z0-9\.]", links[i])
                if index:
                    links[i] = links[i][0:index.span()[0]]
                # links[i] = links[i]+'/'
            except Exception as e:
                print("FORMAT ERROR:    " + str(e))
                rmindex.append(i)
                continue

        rmindex.reverse()
        for n in rmindex:
            links.pop(n)
        return links


