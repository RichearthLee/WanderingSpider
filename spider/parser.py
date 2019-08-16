
class Parser(object):

    @staticmethod
    def inserttohistory(current: set, history: list) -> list:
        if len(history) >= 10:
            history.pop()
            history.insert(0, current)
        else:
            history.insert(0, current)
        return history
