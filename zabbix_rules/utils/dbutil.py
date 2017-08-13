# -*- coding: utf-8 -*-

import os
import sys
import MySQLdb
os.environ['DJANGO_SETTINGS_MODULE'] = 'zabbix_rules.settings'
sys.path.append('/home/prod/deploys/zabbix_rules')
from zabbix_rules.settings import ZABBIX_DB

class Database(object):

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.host = ZABBIX_DB["server"]
        self.port = ZABBIX_DB["port"]
        self.user = ZABBIX_DB["user"]
        self.passwd = ZABBIX_DB["pass"]
        self.db = ZABBIX_DB["db"]
        self.conn = MySQLdb.connect(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    passwd=self.passwd,
                                    db=self.db)
        self.cursor = self.conn.cursor()

    def insert(self,query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except:
            self.conn.rollback()

    def query(self, query):
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()