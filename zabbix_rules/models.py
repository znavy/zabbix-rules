from django.db import models

class Events(models.Model):
    eventid = models.CharField(max_length=30)
    triggerid = models.CharField(max_length=30)
    triggername = models.CharField(max_length=255)
    hostname = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=255, default="WARNING")
    status = models.SmallIntegerField(default=0)
    item_key = models.CharField(max_length=255, null=True)
    user = models.CharField(max_length=50, null=True, blank=True,db_column="username")
    closetype = models.SmallIntegerField(blank=True, default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s %s" % (self.hostname, self.triggername)

    class Meta:
        db_table = 'alarm_events'

class EventHistory(models.Model):
    eventid = models.CharField(max_length=30)
    triggerid = models.CharField(max_length=30)
    triggername = models.CharField(max_length=255)
    hostname = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=255, default="WARNING")
    status = models.SmallIntegerField(default=0)
    item_key = models.CharField(max_length=255, null=True)
    user = models.CharField(max_length=50, null=True, blank=True, db_column="username")
    closetype = models.SmallIntegerField(blank=True, default=0)
    handleTime = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'alarm_events_history'

class AlarmLevel(models.Model):
    LEVEL_CHOICES = (
        (0, "ERROR"),
        (1, "WARNING")
    )
    triggername = models.CharField(max_length=255,default="*")
    hostname = models.CharField(max_length=100,default="*")
    level = models.IntegerField(choices=LEVEL_CHOICES,default=0)
    user = models.CharField(max_length=50,null=True,blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "alarm_level"