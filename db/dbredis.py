import redis


class Redis(object):

    conn = None
    pool = None

    def __init__(self, host, port, dbnum, password):
        # self.pool = redis.ConnectionPool(host=host, port=port, password=password, max_connections=1, db=dbnum)
        self.conn = redis.Redis(host=host, port=port, password=password, db=dbnum)

    def putdata(self, url, title):
        # self.conn = redis.Redis(connection_pool=self.pool)
        res = self.conn.hincrby(url, "index", 1)
        if res and int(res) is not 0:
            self.conn.hset(url, "title", title)

    def getdate(self, url, key):
        return self.conn.hget(url, key)
