from Base import DbSession
from BaseDa import BaseDa
from Database import Sign,Form,Habit,Token
from sqlalchemy import func

class SignDa(BaseDa):
    def __init__(self):
        BaseDa.__init__(self, Sign)

class FormDa(BaseDa):
    def __init__(self):
        BaseDa.__init__(self, Form)

class HabitDa(BaseDa):
    def __init__(self):
        BaseDa.__init__(self, Habit)

class TokenDa(BaseDa):
    def __init__(self):
        BaseDa.__init__(self, Token)
