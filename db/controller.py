import configparser
from db import dbhbase

config = configparser.ConfigParser()
config.read("config")


class Controller(object):

    conn = None

    def __init__(self):
        self.dbtype = config["main"]["dbtype"]

        if self.dbtype == "hbase":
            host = config["hbase"]["host"]
            port = config["hbase"]["port"]
            password = config["hbase"]["password"]
            table = config["hbase"]["table"]
            self.conn = dbhbase.HBase(host, port, "webspider:webindex")
        elif self.dbtype == "redis":
            host = config["redis"]["host"]
            port = config["redis"]["port"]
            password = config["redis"]["password"]
        elif self.dbtype == "mysql":
            host = config["mysql"]["host"]
            port = config["mysql"]["port"]
            password = config["mysql"]["password"]

    def insert(self, url, title):
        if self.dbtype == "hbase":
            self.conn.putdata(url, title)
        elif self.dbtype == "redis":
            None
        elif self.dbtype == "mysql":
            None
        return None

    def query(self, key):
        if self.dbtype == "hbase":
            self.conn.qurydatabyrowkey(key)
        elif self.dbtype == "redis":
            None
        elif self.dbtype == "mysql":
            None
        return None

    def delete(self, key):
        if self.dbtype == "hbase":
            self.conn.qurydatabyrowkey(key)
        elif self.dbtype == "redis":
            None
        elif self.dbtype == "mysql":
            None
        return None


