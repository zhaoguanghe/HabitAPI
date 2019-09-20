import json
import copy
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import sql
from Base import DbSession

class TimeJson(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime):
      return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
      return obj.strftime('%Y-%m-%d')
    else:
      return json.JSONEncoder.default(self, obj)


class BaseDa(object):
    def __init__(self, cls):
        self.cls = cls
    
    def Obj2Json(self, obj):
        d = dict(obj.__dict__)
        del d["_sa_instance_state"]
        return json.dumps(d, cls=TimeJson)

    def List2Json(self, lst):
        ol = []
        for obj in lst:
            d = dict(obj.__dict__)
            del d["_sa_instance_state"]
            ol.append(d)
        return json.dumps(ol, cls=TimeJson)


    def ToObj(self, dic):
        if isinstance(dic, dict):
            obj = self.cls()
            for r in dic.keys():
                obj.__setattr__(r, dic[r])
            return obj
        else:
            return None

    def ToList(self, lst):
        if isinstance(lst, list):
            ol = [] #object list
            for elem in lst:
                obj = self.cls()
                for r in elem.keys():
                    obj.__setattr__(r, elem[r])
                ol.append(obj)
            return ol
        else:
            return None

    def Get(self, id):
        session = DbSession()
        obj = session.query(self.cls).filter(self.cls.Id == id).one()
        session.close()
        return obj

    def Add(self, dict):
        obj = self.ToObj(dict)
        session = DbSession()
        session.add(obj)
        session.commit()
        id = obj.Id
        session.close()
        return id

    def Delete(self, id):
        session = DbSession()
        session.query(self.cls).filter(self.cls.Id == id).delete()
        session.commit()
        session.close()

    def Update(self,where,statu):
        session = DbSession()
        #session.query(self.cls).filter(self.cls.Id == dict['Id']).update(dict)
        rows = session.query(self.cls).filter(sql.text(where)).update({self.cls.Status:statu}, synchronize_session=False)#不对session同步直接delete or update
        session.commit()
        session.close()
        return rows

    def GetCount(self, where, dict):
        session = DbSession()
        #count = session.query(self.cls).from_statement(sql.text(sql))#.params(dict).scalar()
        count = session.query(func.count(self.cls.Id)).filter(sql.text(where)).params(dict).scalar()
        session.commit()
        session.close()
        return count

    def GetRows(self, where, dict, pos, row_num):
        session = DbSession()
        sql_str = "SELECT * FROM " + self.cls().__tablename__
        if len(where.strip()) > 0:
            sql_str += " WHERE " + where
        sql_str += " LIMIT " + str(max(pos - 1,0)) + "," + str(max(0,row_num))
        lst = copy.deepcopy(session.query(self.cls).from_statement(sql.text(sql_str)).params(dict).all())
        session.commit()
        session.close()
        return lst
