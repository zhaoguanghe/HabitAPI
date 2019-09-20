# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
import time
import json
import asyncio
import requests as req
from apscheduler.schedulers.tornado import TornadoScheduler

settings = {
    'template_path': 'Views',        # html文件
    'static_path': 'Statics',        # 静态文件（css,js,img）
    'static_url_prefix': '/Statics/',# 静态文件前缀
    #'cookie_secret': 'suoning',      # cookie自定义字符串加盐
    # 'xsrf_cookies': True,          # 防止跨站伪造
    # 'ui_methods': mt,              # 自定义UIMethod函数
    # 'ui_modules': md,              # 自定义UIModule类
}

import sys
sys.path.append(r'./Api')
sys.path.append(r'./App/Dal')
sys.path.append(r'./App/Model')

from WechatApi import GetOpenid,SentMsg,Sent,TokenOper
from DatabaseApi import SignApi,FormApi,HabitApi,TokenApi

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('HabitAPI运行中...')

class Async(tornado.web.RequestHandler):
    async def get(self):
        await asyncio.sleep(10)                     #阻塞10s
        self.write('end blocking')

api_router = [
    (r"/", MainHandler),
    (r"/Api/GetOpenid", GetOpenid),
    #(r"/Api/SentMsg", SentMsg),
    #(r"/Api/Sign", SignApi),
    #(r'/Api/Formid',FormApi),
    (r'/Api/Habit',HabitApi),
    (r'/async',Async)
    ]

router = api_router

application = tornado.web.Application(
    router,
    **settings,
    debug=True,
    autoreload=True
    )


def token():#2小时获取一次token存入数据库
    appid = 'appid'
    secret = 'secret'
    #requestString = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}'.format(APPID=appid,SECRET=secret)
    #r = req.get(requestString)
    #r = r.json()
    r = ''
    if('access_token' in r):
        token = r['access_token']
        curtime = str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        row = TokenOper.update(token,curtime)
        if(row>0):
            print('token updated')
    else:
        errmsg = r['errmsg']
        print(errmsg)

def send(Htime):
    #获取Status=1 and Htime=7:00/20:00 and today<Date+Hrange的UserId,获取UserId的一个FormId(距离当日不超过7天)使用后删除
    appid = 'appid'
    secret = 'secret'
    requestString = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}'.format(APPID=appid,SECRET=secret)
    r = req.get(requestString)
    r = r.json()
    now = str(time.strftime("%Y-%m-%d",time.localtime()))
    if('access_token' in r):
        token = r['access_token']
        openid = Sent.getuid("Htime = '%s' && Status = 1 && Date < '%s'"%(Htime,now))
        if(openid):
            enabletime = Sent.getime()
            for uid in openid:#enumerate()函数可带index索引，循环发送给UserId
                print(uid[0])
                formid = Sent.getformid("UserId = '%s' && Date > '%s'"%(uid[0],enabletime))
                if(formid):
                    print(formid[0])
                    Sent.delformid("UserId = '%s' && FormId = '%s'"%(uid[0],formid[0]))
                    res = Sent.sent(token,uid[0],formid[0])
                    if(res=='ok'):
                        print(u"'%s':发送成功"%uid[0])
                        pass
                    else:
                        print(res)
        else:
            print('no find')

def moring():
    send('7:00')

def night():
    send('20:00')

def myjob():
    scheduler = TornadoScheduler()
    scheduler.add_job(night,'cron',hour=20, minute=0,second=0)#自动发送day_of_week='mon,tue,wed,thu,fri,sat,sun',单多选周几可连续mon-wed,调用的函数无参
    scheduler.add_job(moring,'cron',hour=7, minute=0,second=0)#hour=5, minute=30, end_date='2016-12-31'截止日期
    scheduler.start()

if __name__ == '__main__':
    server = tornado.httpserver.HTTPServer(application)
    server.listen(9999)
    myjob() #定时任务放在tornado前面
    tornado.ioloop.IOLoop.instance().start()
