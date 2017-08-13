# -*- coding: utf-8 -*-

import re
import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from zabbix_rules.models import AlarmLevel,Events
from rules_celery.tasks import zabbix_rules_task


def events_exist(request):
    '''报警事件是否已存在'''
    status = False
    if "trigger_name" in request.GET and "host_name" in request.GET:
        trigger_name = request.GET["trigger_name"]
        host_name = request.GET["host_name"]
        try:
            events = Events.objects.get(triggername=trigger_name,hostname=host_name)
        except Events.DoesNotExist:
            status = False
        except Events.MultipleObjectsReturned:
            stauts = True
        else:
            status = True
    status = simplejson.dumps(status)
    return HttpResponse(status)

@csrf_exempt
def rules_celery(request):
    '''执行celery task'''
    status = False
    if request.method == "POST":
        status = request.POST["status"]
        event_id = request.POST["event_id"]
        item_key = request.POST["item_key"]
        item_id = request.POST["item_id"]
        trigger_id = request.POST["trigger_id"]
        trigger_name = request.POST["trigger_name"]
        host_name = request.POST["host_name"]
        host_id = request.POST["host_id"]
        ip = request.POST["ip"]
        zabbix_rules_task.delay(status=status,event_id=event_id,item_key=item_key,item_id=item_id,trigger_id=trigger_id,
                               trigger_name=trigger_name,host_name=host_name,host_id=host_id,ip=ip)
        status = True
        status = simplejson.dumps(status)
        return HttpResponse(status)
    else:
        status = simplejson.dumps(status)
        return HttpResponse(status)

def get_level(request):
    '''根据机器名和触发器名获取报警级别'''
    severity = "WARNING"
    level = 1
    if "trigger_name" in request.GET and "host_name" in request.GET:
        trigger_name = request.GET["trigger_name"]
        host_name = request.GET["host_name"]
        level_table = AlarmLevel.objects.all()
        item_list = []
        for item in level_table:
            item_dict = {}
            if item.triggername == "*":
                trigger_rule = r".*"
            else:
                trigger_rule = r".*" + item.triggername.strip()
            if item.hostname == "*":
                host_rule = r".*"
            else:
                host_rule = r".*" + item.hostname.strip()
            item_dict["triggername"] = trigger_rule
            item_dict["hostname"] = host_rule
            item_dict["level"] = item.level
            item_list.append(item_dict)
        for i in item_list:
            if re.match(i["triggername"],trigger_name,flags=re.I) and re.match(i["hostname"],host_name,flags=re.I):
                level = i["level"]
    if int(level) == 0:
        severity = "ERROR"
    elif int(level) == "1":
        severity = "WARNING"
    severity = simplejson.dumps(severity)
    return HttpResponse(severity)

@csrf_exempt
def save_events(request):
    '''保存报警事件'''
    status = False
    if request.method == "POST":
        trigger_name = request.POST["trigger_name"]
        host_name = request.POST["host_name"]
        event_id = request.POST["event_id"]
        item_key = request.POST["item_key"]
        trigger_id = request.POST["trigger_id"]
        level = request.POST["level"]
        status = request.POST["status"]
        username = "abnerzhao" #机器负责人或运维负责人 调用cmdb api
        closetype = 0 #关闭类型
        content = '' #描述备注
        try:
            event = Events.objects.get(triggername=trigger_name,hostname=host_name)
            if event:
                status = False
        except Events.DoesNotExist:
            Events.objects.create(
                eventid=event_id,
                triggerid=trigger_id,
                triggername=trigger_name,
                hostname=host_name,
                content=content,
                severity=level,
                status=status,
                item_key=item_key,
                user=username,
                closetype=closetype
            )
            status = True
        except Exception as e:
            print e.message
        status = simplejson.dumps(status)
        return HttpResponse(status)