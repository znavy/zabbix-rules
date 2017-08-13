# -*- coding: utf-8 -*-

import time
import datetime
from pyzabbix import ZabbixAPI
from zabbix_rules.settings import ZABBIX_API

class ZabbixHandler(object):

    def __init__(self):
        server = ZABBIX_API["url"]
        user = ZABBIX_API["user"]
        password = ZABBIX_API["pass"]
        zapi = ZabbixAPI(server=server)
        zapi.login(user=user,password=password)
        self.zapi = zapi

    def get_item_value(self,hostname,item_key):
        '''获取key对应的值'''
        try:
            items = self.zapi.item.get(
                        filter={"host": hostname,
                                "key_": item_key},
                                selectInterfaces=["interfaceid"],
                                selectGroups=["extend"])
            return items[0]["lastvalue"]
        except Exception as e:
            print e.message

    def get_item_history(self,hostname,item_key,interval):
        '''获取特定时间间隔的历史数据'''
        try:
            item_value_list = []
            interval = int(interval)
            hosts = self.zapi.host.get(filter={"host": hostname}, selectInterfaces=["interfaceid"], selectGroups=["extend"])
            hostid = hosts[0]["hostid"]
            items = self.zapi.item.get(filter={"host": hostname, "key_": item_key},
                                  selectInterfaces=["interfaceid"], selectGroups=["extend"])
            itemid = items[0]["itemid"]
            time_till = time.mktime(datetime.now().timetuple())
            time_from = time_till - 60 * interval  # interval minutes
            history = self.zapi.history.get(hostids=[hostid], itemids=[itemid], time_from=time_from,
                                       time_till=time_till, output='extend', limit='1000')
            if not len(history):
                history = self.zapi.history.get(hostids=[hostid], itemids=[itemid], time_from=time_from,
                                           time_till=time_till, output='extend', limit='1000', history=0)
            for point in history:
                item_value_dict = {}
                item_value_dict["clock"] = datetime.fromtimestamp(int(point["clock"])).strftime("%H:%M")
                item_value_dict["value"] = point["value"]
                item_value_list.append(item_value_dict)
            return item_value_list
        except Exception as e:
            print e.message