# coding=utf-8
import random


class Parser(object):

    @staticmethod
    def inserttohistory(current: list, history: list, size: int) -> list:
        newcurrent = current.copy()
        if len(history) >= size:
            history.pop()
            history.insert(random.randint(0, size), newcurrent)
        else:
            history.insert(random.randint(0, len(history)), newcurrent)
        return history

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
