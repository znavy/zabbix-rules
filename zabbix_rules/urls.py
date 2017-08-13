from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rules_celery/$', 'zabbix_rules.views.rules_celery'),
    url(r'^events_exist/$', 'zabbix_rules.views.events_exist'),
    url(r'^get_level/$', 'zabbix_rules.views.get_level'),
    url(r'^save_events/$', 'zabbix_rules.views.save_events'),
)
