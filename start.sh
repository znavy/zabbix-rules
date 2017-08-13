#!/bin/bash
nohup python manage.py runserver 0.0.0.0:8003 > tmp/console.log &
