from Jingo.models import *
import re, types, datetime

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
    
    def simplifyObjToData(self, args):
        
        for k, v in enumerate(args.values()):
            if type(v) is datetime.datetime:
                key = args.keys()[k]
                args[key] = args[key].isoformat()
        
        return args
    
        '''
        if not args:
            pass
       
        # check if everything in args is a Int
        elif all( isinstance(s, types.) for s in args):
            do_some_ather_thing()
       
        # as before with strings
        elif all( isinstance(s, types.StringTypes) for s in args):
            do_totally_different_thing()
        
        elif all( isinstance(s, datetime.datetime) for s in args):
'''