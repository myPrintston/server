#!/bin/bash
sudo stop uwsgi; python manage.py runserver 0.0.0.0:2016; sudo start uwsgi

