# coding=utf-8
class Parser(object):

    @staticmethod
    def inserttohistory(current: set, history: list) -> list:
        newcurrent = set()
        newcurrent = current.copy()
        if len(history) >= 10:
            history.pop()
            history.insert(0, newcurrent)
        else:
            history.insert(0, newcurrent)
        return history
