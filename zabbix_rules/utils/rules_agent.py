# -*- coding: utf-8 -*-

import argparse
import sys
import requests
from dbutil import Database

database = Database()

def argumen_parser():
    '''解析参数'''
    parse = argparse.ArgumentParser(description='argparse zabbix program')
    parse.add_argument('--status', type=int, default=1)
    parse.add_argument('--event_id')
    parse.add_argument('--item_key')
    parse.add_argument('--trigger_id')
    parse.add_argument('--trigger_name')
    parse.add_argument('--host_name')
    parse.add_argument('--ip')
    parse.add_argument('--item_id')
    args = parse.parse_args()
    return parse,args

def alert_msg(parse,args):
    '''报警消息'''
    if not (args.event_id and args.item_key and args.trigger_id and args.trigger_name and args.host_name and args.ip):
        parse.print_help()
        sys.exit(0)
    raw_sql = '''select h.hostid from hosts h,interface i where i.ip='%s' and i.hostid=h.hostid'''%args.ip
    res = database.query(raw_sql)
    host_id = res[0]["hostid"]
    message = {
        'status': args.status,
        'event_id': args.event_id,
        'item_key': args.item_key,
        'item_id': args.item_id,
        'trigger_id': args.trigger_id,
        'trigger_name': args.trigger_name,
        'host_name': args.host_name,
        'host_id': host_id,
        'ip': args.ip,
    }
    return message

def events_exist(trigger_name,host_name):
    '''判断报警是否已存在'''
    try:
        url = "http://zabbix_rules_example:8003/events_exist/"
        args = {"trigger_name":trigger_name, "host_name": host_name}
        response = requests.get(url, args).json()
        return response
    except Exception as e:
        print e.message

def send_rmq(message):
    '''发送队列'''
    try:
        url = "http://zabbix_rules_example:8003/rules_celery/"
        response = requests.post(url,message).json()
        if response:
            print "send message to celery success"
        else:
            print "send message to celery fail"
    except Exception as e:
        print e.message

if __name__ == '__main__':
    parse,args = argumen_parser()
    message = alert_msg(parse,args)
    if int(message["status"]) == 1:
        if events_exist(message["trigger_name"],message["host_name"]):
            print "event is existed"
            sys.exit(0)
    send_rmq(message)