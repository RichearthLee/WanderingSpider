import configparser
from db import dbhbase
from db import dbredis

config = configparser.ConfigParser()
config.read("config")


class Controller(object):

    conn = None

    def __init__(self):
        self.dbtype = config["main"]["dbtype"]
        if self.dbtype == "hbase":
            host = config["hbase"]["host"]
            port = config["hbase"]["port"]
            table = config["hbase"]["table"]
            print("connecting hbase:",host, port, table)
            self.conn = dbhbase.HBase(host=host, port=port, table=table)
            if self.conn:
                print("hbase connect success")
            else:
                print("hbase connect failed")
                raise
        elif self.dbtype == "redis":
            host = config["redis"]["host"]
            port = config["redis"]["port"]
            password = config["redis"]["password"]
            dbnum = config["redis"]["dbnum"]
            print("connecting redis:", host, port, password, dbnum)
            self.conn = dbredis.Redis(host=host, port=port, password=password, dbnum=dbnum)
            if self.conn:
                print("redis connect success")
            else:
                print("redis connect failed")
                raise
        elif self.dbtype == "mysql":
            host = config["mysql"]["host"]
            port = config["mysql"]["port"]
            password = config["mysql"]["password"]

    def insert(self, url, title):
        if self.dbtype == "hbase":
            self.conn.putdata(url, title)
        elif self.dbtype == "redis":
            self.conn.putdata(url, title)
        elif self.dbtype == "mysql":
            None
        return None

    def query(self, key):
        if self.dbtype == "hbase":
            self.conn.qurydatabyrowkey(key)
        elif self.dbtype == "redis":
            self.conn.getdate(key, "index")
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


