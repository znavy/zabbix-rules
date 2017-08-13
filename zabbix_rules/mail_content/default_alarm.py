# -*- coding: utf-8 -*-

import datetime
import os,sys

sys.path.append('/home/prod/deploys/zabbix_rules')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zabbix_rules.settings')
from zabbix_rules.settings import ZABBIX_URL
from zabbix_rules.utils.zabbx_util import ZabbixHandler

zapi = ZabbixHandler()

def default_alarm_content(dict):
    '''
    组织报警邮件,可结合zabbix api获取更多信息

    Args:
        dict:报警信息

    Return:
        html格式邮件内容
    '''
    host_name = dict["host_name"]
    ip = dict["ip"]
    trigger_name = dict["trigger_name"]
    item_id = dict["item_id"]
    level = dict["level"]
    stime = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d%H%M%S")

    content_vars = {
        "host_name": host_name,
        "host_ip": ip,
        "trigger_name": trigger_name,
        "date": datetime.datetime.now().strftime("%Y.%m.%d %X"),
        "item_id": item_id,
        "stime": stime,
        "url": ZABBIX_URL[0]
    }
    if level == "ERROR":
        content_vars["host_color"] = "red"
        content_vars["ip_color"] = "red"
        content_vars["issur_color"] = "red"
        content_vars["date_color"] = "red"
    elif level == "WARNING":
        content_vars["host_color"] = "black"
        content_vars["ip_color"] = "black"
        content_vars["issur_color"] = "black"
        content_vars["date_color"] = "black"

    content = """
        <h3><font color="%(host_color)s">Host: %(host_name)s</font></h3>
        <h3><font color="%(ip_color)s">IP: %(host_ip)s</font></h3>
        <h3><font color="%(issur_color)s">Issue: %(trigger_name)s</font></h3>
        <h3><font color="%(date_color)s">Date: %(date)s</font></h3>
        <a href='%(url)s/history.php?action=showgraph&itemids[]=%(item_id)s'>View zabbix chart details</a><br>
        <img src='%(url)s/chart.php?itemids=%(item_id)s&period=43200&stime=%(stime)s'><br>
    """ % content_vars

    return content