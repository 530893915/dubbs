#coding: utf8
from exts import db
from datetime import datetime
import json

class BaseModel(object):
    def to_dict(self):
        columns = self.__table__.columns
        model_dict = {}
        for column in columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            model_dict[column.name] = value
        return model_dict

    def to_json(self):
        model_dict = self.to_dict()
        model_json = json.dumps(model_dict)
        # loads：将json转换成dict
        # dumps：讲dict转换成json
        return model_json