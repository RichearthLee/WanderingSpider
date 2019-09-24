# coding=utf-8
import happybase


class HBase(object):

    conn = None
    table = None

    def __init__(self, url, port, tablename):
        self.conn = happybase.Connection(url, 9090)
        self.table = self.conn.table(tablename)

    def getalltables(self):
        return self.conn.tables()

    def tableisexit(self):
        return self.table is not None

    def putdata(self, url, title):
        res = self.table.row(url, ('index:num',))
        res = res.get(b'index:num')
        if not res:
            self.table.put(url, {"index:num": "1"})
            self.table.put(url, {"info:title": title})
            # print("DB INSERT:  " + url)
            return
        res = int(res)
        res = res + 1
        self.table.put(url, {"index:num": str(res)})
        # print("DB UPDATE:  " + url)

    def qurydatabyrowkey(self, ky):
        return self.table.row(ky, ('index:num',))

    def querydataoftable(self):
        return self.table.scan()
