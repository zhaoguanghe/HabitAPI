from tornado.web import RequestHandler
import json
import time

from BaseApi import BaseApi

from DatabaseDa import SignDa,FormDa,HabitDa,TokenDa
from Database import Sign,Form,Habit,Token


class SignApi(BaseApi):
    def initialize(self):
        BaseApi.initialize(self, SignDa)
        self.da = SignDa()

class TokenApi(BaseApi):
    def initialize(self):
        BaseApi.initialize(self, TokenDa)
        self.da = TokenDa()

class FormApi(BaseApi):
    def initialize(self):
        BaseApi.initialize(self, FormDa)
        self.da = FormDa()

class HabitApi(BaseApi):
    def initialize(self):
        BaseApi.initialize(self, HabitDa)
        self.da = HabitDa()

    def post(self):
        data = json.loads(self.request.body)
        if('update' in data):
            row = self.da.Update(data['where'],data['statu'])
            if(row>0):
                self.write('ok')
            else:
                self.write('none')
        else:
            super().post()