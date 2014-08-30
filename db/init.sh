#!/bin/bash

uwsgi --http :2016 --wsgi-file fdjlserver.py --master --processes 4 --threads 2 --stats 127.0.0.1:9191 --die-on-term & #--logto logs.txt &
