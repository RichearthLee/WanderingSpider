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
