# coding: utf-8
import os
from fabric.api import run, env, cd, roles, lcd, local, sudo, prompt
from fabric.operations import get
# Списком можно перечислить несколько серверов, которые у вас считаются "продакшеном"

env.roledefs['whitemandarin'] = ['root@91.121.71.107']



def whitemandarin_env():
    env.user = 'root'  # На сервере будем работать из под пользователя "git"
    env.password = "vl9s4fGC_GWAsipqd"


@roles('whitemandarin')
def d():
    whitemandarin_env()
    with cd('/home/www/whitemandarin/www'):
        sudo('find /home/www/whitemandarin/www -name "*.pyc" -exec rm -rf {} \;')
        sudo('git pull origin master')
        # sudo('kill `cat /tmp/tovarok.pid`')
        sudo('find /home/www/whitemandarin/www -name "*.pyc" -exec rm -rf {} \;')
        sudo('supervisorctl restart whitemandarin')


def g():
    lcd('/home/hottabov/whitemandarin/whitemandarin')
    local('sudo git add .')
    local("sudo git commit -a")
    local("sudo git push origin master")
