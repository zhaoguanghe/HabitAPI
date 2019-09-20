from tornado.web import RequestHandler
import json
import datetime
import time as now
import requests
from sqlalchemy import sql
from DatabaseDa import TokenDa
from Base import DbSession
from Database import Token,Habit,Form
from BaseApi import Oper

class GetOpenid(RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        if(data['code'] != ''):
            appid = 'appid'
            secret = 'passwd'
            requestString = 'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={JSCODE}&grant_type=authorization_code'.format(APPID=appid,SECRET=secret,JSCODE=data['code'])
            r = requests.get(requestString)
            r = r.json()
            self.write(r['openid'])
        else:
            self.write(u'请求编码错误')

class SentMsg(RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        appid = 'appid'
        secret = 'passwd'
        requestString = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}'.format(APPID=appid,SECRET=secret)
        r = requests.get(requestString)
        r = r.json()
        if('access_token' in r):
            token = r['access_token']
            if(token != ''):
                s = json.dumps({"touser": "openid","template_id": "template_id",
                     "page": "pages/sign/sign",
                     "form_id": "form_id",
                     "data": {
                         "keyword1": {
                             "value": "习惯养成方案"
                         },
                         "keyword2": {
                             "value": "未签到"
                         }
                     },
                     "emphasis_keyword": "keyword1.DATA"
                     })
                requestString = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token={ACCESS_TOKEN}'.format(ACCESS_TOKEN=token)
                r = requests.post(url=requestString,data=s)
                r = r.json()
                if(r['errcode'] == 0):
                    self.write(u'发送成功')
                else:
                    self.write(u'发送失败')
        else:
            self.write(u'token出错')

class TokenOper:
    def Add(str,curtime):
        token = Token()
        token.Access_token=str
        token.Time=curtime
        session = DbSession()
        session.add(token)
        session.commit()
        session.close()
        if(1):
            print('token insert ok')

    def find():
        session = DbSession()
        obj = session.query(Token.Access_token).first()
        session.close()
        return obj

    def update(str,curtime):
        session = DbSession()
        rows = 0
        try:
            rows = session.query(Token).update({Token.Access_token:str,Token.Time:curtime},synchronize_session=False)
            session.commit()
        except:
            session.rollback()
        session.close()
        return rows

class Sent:
    def valuetime(where):
        session = DbSession()
        obj = session.query(Habit.Hrange,Habit.Date).filter(sql.text(where)).first()
        session.close()
        if(obj):
            print(int(obj[0]),obj[1])
            struct_time = now.strptime(obj[1])
            res = (struct_time+datetime.timedelta(days=int(obj[0]))).strftime("%Y-%m-%d %H:%M:%S")
            return res
        else:
            return 'null'

    def getime():
        time = (datetime.datetime.now()-datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")#减7天，获得有效formid
        return time

    def getuid(where):
        session = DbSession()
        obj = session.query(Habit.UserId).filter(sql.text(where)).all()
        session.close()
        return obj

    def getformid(where):
        session = DbSession()
        obj = session.query(Form.FormId).filter(sql.text(where)).first()
        session.close()
        return obj

    def delformid(where):
        session = DbSession()
        session.query(Form).filter(sql.text(where)).delete(synchronize_session=False)
        session.commit()
        session.close()

    def sent(access_token,uid,formid):
        if(access_token!=''):
            token = access_token
            if(token != ''):
                s = json.dumps({"touser": str(uid),"template_id": "template_id",
                     "page": "pages/sign/sign",#签到页面
                     "form_id": str(formid),
                     "data": {
                         "keyword1": {
                             "value": "习惯养成方案"
                         },
                         "keyword2": {
                             "value": "未签到"
                         }
                     },
                     "emphasis_keyword": "keyword1.DATA"
                     })
                requestString = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token={ACCESS_TOKEN}'.format(ACCESS_TOKEN=token)
                r = requests.post(url=requestString,data=s)
                r = r.json()
                if(r['errcode'] == 0):
                    return 'ok'
                else:
                    return 'unsend'
        else:
            return 'token wrong'

