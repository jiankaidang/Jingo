from Jingo.models import User

class Users:
    def doLogin(self, request, data):
        if request.session.get('uid', False):
            print 'you already logged in!'
            return dict([('result', 'fail'), ('data', 'test!')])
        else:
            usr = User.objects.filter(email=data['email'], password=data['password']).values()
            if len(usr) == 0:
                return dict([('result', 'fail'), ('data', 0)])
            else:
                request.session["uid"] = usr[0]['uid']
                usr[0]['u_timestamp'] = usr[0]['u_timestamp'].isoformat()
                return dict([('result', 'success'), ('data', usr[0])])
        
    