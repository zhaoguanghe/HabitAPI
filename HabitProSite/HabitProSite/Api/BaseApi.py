import tornado.web
import json
import math

class BaseApi(tornado.web.RequestHandler):

    da1 = None
    def initialize(self, dacls):
        self.da = da1 = dacls()
        return super().initialize()

    def get(self):
        id = self.get_argument('Id')
        obj = self.da.Get(id)
        self.write(self.da.Obj2Json(obj))

    async def post(self):
        data = json.loads(self.request.body)
        if ('_search' in data):
            self.grid(data)
        elif('oper' in data):
            if(data['oper'] == 'sign'):
                where = "UserId = '%s'"%(data['UserId'])+" AND Date = '%s'"%(data['Date'])
                id = self.da.GetCount(where,{})
                signed = False
                if id>0:
                    signed = True
                total_sign = self.da.GetCount("UserId = '%s'"%(data['UserId']),{})
                self.write({'total':total_sign,'signed':signed})
            elif (data['oper'] == 'add'):
                id = self.da.Add(data)
                if(id>0):
                    self.write('ok')
            elif (data['oper'] == 'edit'):
                self.put()
            elif (data['oper'] == 'del'):
                self.delete()
            elif (data['oper'] == 'fetch'):
                lst = await self.da.GetRows(data['where'], {}, data['from'], data['num'])
                self.write(self.da.List2Json(lst))
        else:
            self.write('0')

    def put(self):
        dict = json.loads(self.request.body)
        del dict['oper']
        self.da.Update(dict)

    def delete(self):
        ids = self.get_argument('id')
        arr = ids.split(',')
        for id in arr:
            self.da.Delete(id)

    def parse(self, filters, dict):
        f = filters.replace('{\"SQL\":\"', '').replace('\"}', '')
        if (len(f.strip()) == 0 or f == '&'):
            return ''

        sql_param = f.split('&')
        where = sql_param[0].replace('@', ':')
        if (len(sql_param) <= 1):
           return where

        param = sql_param[1].strip(';').split(';')
        for s in param:
            items = s.split(':')
            dict.update({items[0].replace('@', ''): items[1]})

        return where

class Oper(object):
    da1 = None
    def initialize(self):
        self.da = dal
        return super().initialize()

    def add(self,data):
         argu= json.loads(data)
         if (argu['oper'] == 'add'):
                id = self.da.Add(argu)
                if(id>0):
                    print('ok')
