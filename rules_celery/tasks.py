# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os,sys
from celery import Celery
from celery import shared_task
from zabbix_rules.utils.rules_actions import Actions
from django.conf import settings

sys.path.append('/home/prod/deploys/zabbix_rules')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','zabbix_rules.settings')

app = Celery('rules_celery')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def zabbix_rules_task(*args,**kwargs):
    '''报警消息处理'''
    try:
        actions = Actions(status=kwargs["status"],event_id=kwargs["event_id"],item_key=kwargs["item_key"],item_id=kwargs["item_id"],trigger_id=kwargs["trigger_id"],
                          trigger_name=kwargs["trigger_name"],host_name=kwargs["host_name"],host_id=kwargs["host_id"],ip=kwargs["ip"])
        return actions.run()
    except Exception as e:
        print e.message

@shared_task
def add(x, y):
    return x + y