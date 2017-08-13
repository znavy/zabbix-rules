# -*- coding: utf-8 -*-

import requests
from zabbix_rules.mail_content.site_alarm import site_alarm_content
from zabbix_rules.mail_content.default_alarm import default_alarm_content
from zabbix_rules.utils.sendmail import send_mail

class Actions(object):

    def __init__(self,**kwargs):
        self.status = kwargs["status"]
        self.event_id = kwargs["event_id"]
        self.item_key = kwargs["item_key"]
        self.item_id = kwargs["item_id"]
        self.trigger_id = kwargs["trigger_id"]
        self.trigger_name = kwargs["trigger_name"]
        self.host_name = kwargs["host_name"]
        self.host_id = kwargs["host_id"]
        self.ip = kwargs["ip"]

        # 获取警告级别
        self.level = self.__get_level()

        # 获取报警收件人邮箱
        self.to_user = self.__get_mail()

        self.event_msg = {
            "status":self.status,
            "event_id":self.event_id,
            "item_key":self.item_key,
            "item_id":self.item_id,
            "trigger_id":self.trigger_id,
            "trigger_name":self.trigger_name,
            "host_name":self.host_name,
            "host_id":self.host_id,
            "ip":self.ip,
            "level":self.level,
            "to_user":self.to_user
        }
        self.count = 1

    def __get_level(self):
        '''获取警报级别'''
        url = "http://zabbix_rules_example:8003/get_level/"
        args = {"trigger_name":self.trigger_name,"host_name":self.host_name}
        response = requests.get(url, args).json()
        return response

    def __get_mail(self):
        '''获取收件人邮箱'''
        # 可调用cmdb api接口获取对应机器或业务的接警邮箱
        user_mail = ["opsabnerzhao@gmail.com"]
        return user_mail

    def save_events(self):
        '''保存报警事件'''
        save_status = False
        try:
            check_url = "http://zabbix_rules_example:8003/events_exist/"
            args = {"trigger_name": self.trigger_name, "host_name": self.host_name}
            status = requests.get(check_url, args).json()
            if status:
                print "event is existed no need to save"
                save_status = False
            else:
                url = "http://zabbix_rules_example:8003/save_events/"
                data = self.event_msg
                requests.post(url, data)
                save_status = True
            return save_status
        except Exception as e:
            print e.message
            return save_status

    def run(self):
        '''定制邮件内容'''
        send_mail_flag = 1
        mail_dict = self.event_msg
        host_name = mail_dict["host_name"]
        msg = ''
        if int(self.count) == 1:
            event_status = self.save_events()
            if not event_status and int(self.status) == 1:
                msg = "No need to do anything else!"
            else:
                try:
                    if "xx percent" in mail_dict["trigger_name"]:
                        mail_dict["content"] = site_alarm_content(mail_dict)
                    else:
                        mail_dict["content"] = default_alarm_content(mail_dict)
                except Exception:
                    mail_dict["content"] = "get mail content Exception !"

                if mail_dict["level"] == "ERROR":
                    try:
                        pass
                    except Exception as e:
                        msg = "%s send message error: %s"%(host_name,e.message)
                if send_mail_flag == 1:
                    try:
                        send_mail(mail_dict)
                        msg = "%s send mail success"%host_name
                    except Exception as e:
                        msg = "%s send mail error: %s"%(host_name,e.message)
            self.count += 1
            return msg
        else:
            msg = "no need to do anything"
            return msg