#! /usr/bin/bash
systemctl stop nginx
systemctl stop flaskapp
sleep 2s
systemctl start flaskapp
systemctl start nginx
sleep 2s
systemctl status nginx --no-pager
systemctl status flaskapp --no-pager

