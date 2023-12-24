#! /usr/bin/bash
systemctl stop nginx
systemctl stop flaskapp
systemctl start flaskapp
systemctl start nginx
systemctl status nginx
systemctl status flaskapp

