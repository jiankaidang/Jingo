from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from Jingo.lib.config import *

from Jingo.lib.HttpRequestTasks import *
from Jingo.lib.DataVerification import *
from Jingo.lib.SQLExecution import *

class Comments(models.Model, Formatter):
    commentid = models.IntegerField(primary_key=True)
    noteid = models.ForeignKey('Note', db_column='noteid')
    c_timestamp = models.DateTimeField()
    uid = models.ForeignKey('User', db_column='uid')
    c_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    c_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    comment = models.CharField(max_length=140)

    class Meta:
        db_table = 'comments'

class Filter(models.Model, Formatter):
    stateid      = models.ForeignKey('State', db_column='stateid', primary_key=True)
    tagid        = models.ForeignKey('Tag', db_column='tagid', primary_key=True)
    f_start_time = models.DateTimeField(null=True, blank=True)
    f_stop_time  = models.DateTimeField(null=True, blank=True)
    f_repeat     = models.IntegerField(null=True, blank=True)
    f_visibility = models.IntegerField()
    uid          = models.ForeignKey('State', db_column='uid', primary_key=True)

    class Meta:
        db_table = 'filter'
    
    def categorizeFiltersIntoSystags(self, data, filterset):
        result      = []
        tmp_sysTags = []
        sysTags    = Tag().getUserSysTags(data)
        print "Here ==========>"
        print sysTags
        for sys in sysTags:
            sys['tags']       = []
            sys['is_checked'] = 0
            tmp_sysTags.append(sys)
            
        for sys in tmp_sysTags:
            for row in filterset:
                tagid_id = row['tagid_id']
            
                if sys['tagid'] == tagid_id and (tagid_id >= 0 and tagid_id <= 10):
                    sys['is_checked'] = 1
                
                if tagid_id > 10 and sys['tagid'] == row['sys_tagid']:
                    sys['is_checked'] = 1
                    sys['tags'].append(row)
            print "result row ================"
            print sys
            result.append(sys)
        return result
    
    def extendFilterWithTagInfo(self, data, filterset):
        result = []
        for row in filterset:
            tagid_id          = row['tagid_id']
            tag               = Tag.objects.get(tagid=tagid_id)
            row['tag_name']   = tag.tag_name
            row['sys_tagid']  = tag.sys_tagid
            row['is_checked'] = 1
            print row
            result.append(row)
        return result
    
    def getUserStateFilters(self, data):
        filterset = Filter.objects.filter(uid_id=data['uid_id'], stateid=data['stateid']).values()
        filterset = self.extendFilterWithTagInfo(data, filterset)
        filterset = self.categorizeFiltersIntoSystags(data, filterset)
        if len(filterset) == 0:
            return []
        else:
            filterset = self.simplifyObjToDateString(filterset)  # datetime to iso format
            return filterset
    
    # arguments 'data' need to be a list including values that will be stored into filter 
    def addFilter(self, data):
        db   = SQLExecuter()
        args = dict([('table', 'filter'),('values', data)])
        db.doInsertData(args)
    
    def addDefaultFilter(self, data):
        values = []
        for i in range(0,11):
            values.append(data['stateid'])
            values.append(i)
            values.append(None)
            values.append(None)
            values.append(0)
            values.append(0)
            values.append(data['uid_id'])
            self.addFilter(values)
            values= []
        return i
    
    def deleteFilter(self, data):
        return Filter.objects.filter(uid=data['uid'], stateid=data['stateid'], tagid=data['tagid']).delete()
    
class Friend(models.Model):
    uid = models.ForeignKey('User', db_column='uid')
    f_uid = models.ForeignKey('User', db_column='f_uid')
    is_friendship = models.IntegerField()
    invitationid = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'friend'
    
    def getNewInvitationid(self):
        if len(Friend.objects.all().values()) == 0:
            return 1
        else:
            friend = Friend.objects.all().order_by('invitationid').latest('invitationid')
            print friend.invitationid
            return friend.invitationid + 1
    
    def getFriendsInvitations(self, input_uid):
        return Friend.objects.filter(uid=input_uid, isfriendship=2).order_by('invitationid').values()

    def getFriendsList(self, input_uid):
        return Friend.objects.filter(uid=input_uid, isfriendship=1).order_by('invitationid').values()

    def addInvitation(self, data):
        newInvitationid      = self.getNewInvitationid()
        friend               = Friend()
        friend.uid           = data['uid']
        friend.f_uid         = data['f_uid']
        friend.is_friendship = 2                 # 0:denied, 1:accepted, 2:pending
        friend.invitationid  = newInvitationid
        return Friend.objects.filter(invitationid=newInvitationid)
        
class Note(models.Model):
    note = models.CharField(max_length=140)
    n_timestamp = models.DateTimeField()
    link = models.TextField(blank=True)
    noteid = models.IntegerField(primary_key=True)
    uid = models.ForeignKey('User', db_column='uid')
    radius = models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)
    n_visibility = models.IntegerField()
    n_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    n_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_comment = models.IntegerField()
    n_like = models.IntegerField()

    class Meta:
        db_table = 'note'

class Note_Tag(models.Model):
    noteid = models.ForeignKey('Note', db_column='noteid', primary_key=True)
    tagid = models.ForeignKey('Tag', db_column='tagid', primary_key=True)

    class Meta:
        db_table = 'note_tag'

class Note_Time(models.Model):
    timeid = models.IntegerField(primary_key=True)
    noteid = models.ForeignKey('Note', db_column='noteid')
    n_start_time = models.DateTimeField()
    n_stop_time = models.DateTimeField(null=True, blank=True)
    n_repeat = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'note_time'

class State(models.Model, HttpRequestResponser, Formatter):
    stateid    = models.IntegerField(primary_key=True)
    state_name = models.CharField(max_length=45)
    uid        = models.ForeignKey('User', db_column='uid', primary_key=True)
    is_current = models.IntegerField()

    class Meta:
        db_table = 'state'

    def getNewStateid(self):
        if len(State.objects.all().values()) == 0:
            return 1
        else:
            ustate = State.objects.all().order_by('uid', 'stateid').latest('stateid')
        return ustate.stateid + 1

    def getUserStatesList(self, data):
        return State.objects.all().filter(uid=data['uid']).order_by('is_current').reverse().values()
    
    def getUserStatesAndFiltersList(self, data):
        filt     = Filter()
        datalist = []
        #print data
        uslist   = self.getUserStatesList(data)  # get user's all states
        print uslist
        for row in uslist:
            filterset      = filt.getUserStateFilters(row)
            row['filters'] = filterset
            datalist.append(row)
        return datalist
    
    def setDefaultState(self, request):
        data = self.readData(request)
        data = State.objects.all().update(is_current=0).filter(stateid=data['stateid'], uid=data['uid']).update(is_current=1)
        return self.createResultSet(data, 'json')
    
    def addState(self, data, mode='user-defined'):
        state            = State()
        state.state_name = data['state_name']
        state.uid        = User(uid=int(data['uid']))
        if mode == 'default':
            state.is_current = 1
            state.stateid    = 0
            state.save();
            data = State.objects.filter(stateid=0, uid=data['uid']).values()
            return data
        else:
            newStateid       = self.getNewStateid()
            state.is_current = 0
            state.stateid    = self.getNewStateid()
            state.save();
            data = State.objects.filter(stateid=newStateid, uid=data['uid']).values()
            return self.createResultSet(data, 'json')

    def deleteState(self, request):
        data               = self.readData(request)
        args               = {}
        args['table']      = 'State'
        args['attributes'] = [{'field':'stateid', 'logic': 'And'}, {'field':'uid', 'logic': 'And'}]
        args['values']     = [data['stateid'], data['uid']]
        SQLExecuter().doDeleteData(args)
        return self.createResultSet(data, 'json')
    
    def updateState(self, request):
        data = self.readData(request)
        data = State.objects.filter(stateid=data['stateid'], uid=data['uid']).update(state_name=data['state_name'])
        return self.createResultSet(data, 'json')
             
class Tag(models.Model):
    tagid     = models.IntegerField(primary_key=True)
    tag_name  = models.CharField(max_length=45)
    uid       = models.ForeignKey('User', null=True, db_column='uid', blank=True)
    sys_tagid = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'tag'

    def getSysTags(self):
        return Tag.objects.order_by('tagid').filter(tagid__gte=0, tagid__lte=10).values()
    
    def getNewTagid(self):
        if len(Tag.objects.all().values()) == 0:
            return 1
        else:
            tag = Tag.objects.all().order_by('tagid').latest('tagid')
            #print tag.tagid
            return tag.tagid + 1
        
    def getUserSysTags(self, data):
        print data
        result             = []
        args               = {}
        args['columns']    = ['b.*, a.tag_name, a.sys_tagid']
        args['tables']     = ['tag as a', 'filter as b']
        args['joins']      = ['a.tagid = b.tagid', 'a.tagid>=%s And a.tagid<=%s']
        args['conditions'] = [{'criteria': 'b.uid=', 'logic': 'And'}, {'criteria': 'b.stateid=', 'logic': 'And'}]
        args['values']     = [0, 10, data['uid_id'], data['stateid']]
        slist              = SQLExecuter().doSelectData(args)
        for sys in slist:
            sys['is_checked'] = 0
            result.append(sys)
        return result
    
    def getUserTags(self, input_uid):
        return Tag.objects.filter(uid=User(uid=input_uid)).order_by('tagid').values()
    
    def addTag(self, data):
        newTagid      = self.getNewTagid()
        tag           = Tag()
        tag.tagid     = newTagid
        tag.tag_name  = data['tag_name']
        tag.uid       = User(uid=int(data['uid']))
        tag.sys_tagid = data['sys_tagid']
        tag.save()
        return Tag.objects.filter(tagid=newTagid, uid=int(data['uid'])).values()
    
    def deleteTag(self, request):
        data               = self.readData(request)
        args               = {}
        args['table']      = 'Tag'
        args['attributes'] = [{'field':'stateid', 'logic': 'And'}, {'field':'uid', 'logic': 'And'}]
        args['values']     = [data['tagid'], data['uid']]
        SQLExecuter().doDeleteData(args)
        return self.createResultSet(data, 'json')
    
    def updateTag(self, request):
        data = self.readData(request)
        data = Tag.objects.filter(tagid=data['tagid'], uid=data['uid']).update(state_name=data['tag_name'])
        return self.createResultSet(data, 'json')
    
class User(models.Model, HttpRequestResponser, Formatter):
    uid         = models.IntegerField(primary_key=True)
    u_name      = models.CharField(max_length=45)
    email       = models.CharField(max_length=45)
    u_timestamp = models.DateTimeField()
    password    = models.CharField(max_length=15)

    class Meta:
        db_table = 'user'

    def setUserSession(self, request, usr):
        request.session['uid']     = usr['uid']
        request.session['usrdata'] = usr
    
    def getNewUid(self):
        if len(User.objects.all().values()) == 0:
            return 1
        else:
            usr = User.objects.all().order_by('uid').latest('uid')
            #print usr.uid
            return usr.uid + 1

        usr = User.objects.all().order_by('uid').latest('uid')
        #print usr.uid
        return usr.uid + 1
    
    def getUserData(self, input_uid):
        print "usr_id=" + str(input_uid)
        return User.objects.filter(uid=input_uid).values()[0]
    
    def addUser(self, data):
        usr             = User()
        usr.uid         = self.getNewUid()
        usr.u_name      = data['u_name']
        usr.email       = data['email']
        usr.password    = data['password']
        usr.u_timestamp = timezone.now()
        usr.save()
        return User.objects.filter(email=data['email']).values()

    def signup(self, request):
        result    = RESULT_SUCCESS
        message   = []
        verifier  = DataVerifier()
        data = self.readData(request)

        if not verifier.isValidFormat(data['email'], 'email'):
            message.append('The email address is invalid.')
            result = 'fail'

        if not verifier.isEmailUnique(User.objects, data['email']):
            message.append('The email address is already taken.')
            result = 'fail'
        
        usr               = self.simplifyObjToDateString(self.addUser(data))[0]
        usr['state_name'] = STATE_NAME_DEFAULT
        state             = State().addState(usr, 'default')[0]
        ufilter           = Filter().addDefaultFilter(state)
        
        self.setUserSession(request, usr)
      
    def login(self, request):
        if request.method != 'POST':
            pass
            # raise Http404('Only POSTs are allowed')
        #print request.session.get('uid', False)
        if request.session.get('uid', False):
            print 'you already logged in!'
            return dict([('result', 'fail'), ('data', '')])
        else:
            data = self.readData(request)
            check = User.objects.filter(email=data['email']).values()
            if len(check) == 0:
                message = MESSAGE_EMAIL_ERROR
                return self.createResultSet(data, 'html', RESULT_FAIL, message) 
            else:
                usr = self.simplifyObjToDateString(check)[0]
                if usr['password'] == data['password']:
                    self.setUserSession(request, usr)
                    self.createResultSet(usr)
                else:
                    message = MESSAGE_PASSWORD_ERROR
                    return self.createResultSet(data, 'html', RESULT_FAIL, message) 

    def logout(self, request):
        try:
            del request.session['uid']
            request.session.clear()
        except KeyError:
            message = LOGOUT_FAIL
            return self.createResultSet([], 'html', RESULT_FAIL, message)
        message = LOGOUT_SUCCESS
        return self.createResultSet([], 'html', RESULT_SUCCESS, message)

    def getUserProfile(self, request):
        uid    = request.session['uid']
        usr    = self.getUserData(uid)
        data   = dict([('user', usr), ('stateslist', State().getUserStatesAndFiltersList(usr))])
        #print data
        return self.createResultSet(data)
    
    
