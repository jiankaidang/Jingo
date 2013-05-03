from Jingo.lib.config import *
from django.core import serializers
from Jingo.models import *
import re, types, datetime, json
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder

class DataVerifier:
    
    def __init__(self):
        self.re = {}
        self.setRulesBase()
        
    def setRulesBase(self):
        self.re['email']    = re.compile("[a-zA-Z0-9.!#$%&'*+-/=?\^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*")
        self.re['password'] = re.compile("^[a-zA-Z0-9*]+$")
        
    def isValidFormat(self, data, dataType):
        if self.re[dataType].match(data):
            return True
        return False
        
    def isEmailUnique(self, tarlist, input_email):
        if tarlist.filter(email=input_email).count() == 0:
            return True
        return False


class Formatter:
    
    def __init__(self):
        self.re = {}
        self.setRulesBase()
    
    def setRulesBase(self):
        self.re['int'] = re.compile("[.]+id$")
        
    def simplifyLongToInt(self, data):
        if self.re['int'].search(data) is None:
            return data
        else:
            return int(data)
    
    # deal with datetime object like datetime.datetime(2013, 4, 13, 9, 0)
    # we need to transfer it in the form of "2013-04-13T21:38:01"
    def simplifyObjToDateString(self, data):
        result = []
        for row in data:
            for k, v in enumerate(row.values()):
                if type(v) is datetime.datetime:
                    key      = row.keys()[k]
                    row[key] = row[key].isoformat()
            result.append(row)
        return result # list with several valuequerysets
    
    def jsonEncoder(self, resultset):
        return json.JSONEncoder().encode(resultset)
    
    def createResultSet(self, data={}, outputType='html', result=RESULT_SUCCESS, message={}):
        resultset = dict([('result', result), ('message', message), ])
        
        for k, v in enumerate(data.values()):
            key            = data.keys()[k]
            resultset[key] = v
            
        if outputType == 'json':
            return self.jsonEncoder(resultset)
        else:
            return resultset
