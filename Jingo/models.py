from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from Jingo.lib.config import *
from Jingo.lib.NoteFilter import *
import urllib, urlparse, datetime
from django.utils import timezone, dateparse
from math import radians, cos, sin, asin, sqrt
from Jingo.lib.SQLExecution import SQLExecuter

class Friend(models.Model, HttpRequestResponser, Formatter):
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
        return Friend.objects.filter(uid=input_uid, is_friendship=2).order_by('invitationid').values()

    def getFriendsList(self, data):
        return list(Friend.objects.filter(uid=data['uid'], is_friendship=1).order_by('invitationid').values('f_uid'))

    def addInvitation(self, data):
        newInvitationid = self.getNewInvitationid()
        friend = Friend()
        friend.uid = data['uid']
        friend.f_uid = data['f_uid']
        friend.is_friendship = 2                 # 0:denied, 1:accepted, 2:pending
        friend.invitationid = newInvitationid
        return Friend.objects.filter(invitationid=newInvitationid)

class Comments(models.Model, HttpRequestResponser, Formatter):
    commentid   = models.IntegerField(primary_key=True)
    noteid      = models.ForeignKey('Note', db_column='noteid')
    c_timestamp = models.DateTimeField()
    uid         = models.ForeignKey('User', db_column='uid')
    c_latitude  = models.DecimalField(max_digits=9, decimal_places=6)
    c_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    comment     = models.CharField(max_length=140)

    class Meta:
        db_table = 'comments'

    def getNewCommentid(self):
        if len(Comments.objects.all().values()) == 0:
            return 1
        else:
            nComments = Comments.objects.all().order_by('commentid').latest('commentid')
            #print tag.tagid
            return nComments.commentid + 1

    def addComment(self, data):
        newCommentid         = self.getNewCommentid()
        nComment             = Comments()
        nComment.commentid   = newCommentid
        nComment.noteid      = Note(noteid=data['noteid'])
        nComment.c_timestamp = timezone.now()
        nComment.uid         = User(uid=data['uid'])
        nComment.c_latitude  = data['c_latitude']
        nComment.c_longitude = data['c_longtitude']
        nComment.comment     = data['comment']
        return newCommentid

class Filter(models.Model, HttpRequestResponser, Formatter):
    stateid      = models.ForeignKey('State', db_column='stateid', primary_key=True)
    tagid        = models.ForeignKey('Tag', db_column='tagid', primary_key=True)
    f_start_time = models.DateTimeField(null=True, blank=True)
    f_stop_time  = models.DateTimeField(null=True, blank=True)
    f_repeat     = models.IntegerField(null=True, blank=True)
    f_visibility = models.IntegerField()
    uid          = models.ForeignKey('State', db_column='uid', primary_key=True)
    is_checked   = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'filter'

    def categorizeFiltersIntoSystags(self, data, filterset):
        result      = []
        tmp_sysTags = []
        #sysTags    = Tag().getUserSysTags(data)
        sysTags = Tag().getSysTags()
        #print "Here ==========>"
        #print sysTags
        for sys in sysTags:
            sys['tags']       = []
            sys['is_checked'] = 0
            tmp_sysTags.append(sys)

        for sys in tmp_sysTags:
            for row in filterset:
                tagid_id = row['tagid_id']

                if sys['tagid'] == tagid_id and (tagid_id >= 0 and tagid_id <= 10):
                    sys['is_checked'] = row['is_checked']

                if tagid_id > 10 and sys['tagid'] == row['sys_tagid']:
                    sys['is_checked'] = 1
                    sys['tags'].append(row)
                #print "result row ================"
            #print sys
            result.append(sys)
        return result

    def extendFilterWithTagInfo(self, data, filterset):
        result = []
        for row in filterset:
            tagid_id         = row['tagid_id']
            tag              = Tag.objects.get(tagid=tagid_id)
            row['tag_name']  = tag.tag_name
            row['sys_tagid'] = tag.sys_tagid
            #print row
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

    def getDefaultFilterDataArray(self, data):
        return [int(data['stateid']), data['tagid'], None, None, 0, 0, int(data['uid']), IS_CHECKED_DEFAULT]
    
    def addFilterAndTag(self, request):
        data          = self.readData(request)
        data['tagid'] = Tag().addTag(data)
        if 'f_start_time' in data:
            values = [int(data['stateid']), data['tagid'], data['f_start_time'], data['f_stop_time'], data['f_repeat'], data['f_visibility'], int(data['uid']), IS_CHECKED_DEFAULT]
        else:
            values = [int(data['stateid']), data['tagid'], None, None, 0, 0, int(data['uid']), IS_CHECKED_DEFAULT]
        self.addFilter(values)
        return self.createResultSet({'tagid': data['tagid']}, 'json')
    
    # arguments 'data' need to be a list including values that will be stored into filter 
    def addFilter(self, data):
        args = dict([('table', 'filter'), ('values', data)])
        SQLExecuter().doInsertData(args)

    def addDefaultFilter(self, data):
        for i in range(0, N_SYSTEM_TAGS):
            data['tagid'] = i
            values        = self.getDefaultFilterDataArray(data)
            self.addFilter(values)
        return i

    def deleteFilter(self, request):
        data = self.readData(request)
        args = {}
        args['table'] = 'Filter'
        args['attributes'] = [{'field': 'tagid', 'logic': 'And'}, {'field': 'uid', 'logic': 'And'},
                              {'field': 'stateid', 'logic': 'And'}]
        args['values'] = [data['tagid'], data['uid'], data['stateid']]
        SQLExecuter().doDeleteData(args)
        return self.createResultSet(data, 'json')
    
    def updateFilter(self, request):
        #request = 'stateid=0&tagid=1&f_start_time=2013-04-14 04:49:44&f_stop_time=2013-04-14 04:49:44&f_repeat=1&f_visibility=1&uid'
        #data = urlparse.parse_qsl(request)
        data = self.readData(request)
        if data['f_repeat'] == 'on':
            data['f_repeat'] = 1
        else:
            data['f_repeat'] = 0
        Filter.objects.filter(stateid=data['stateid'],uid=data['uid'],tagid=data['tagid']).update(f_start_time=data['f_start_time'],f_stop_time=data['f_stop_time'],f_repeat=data['f_repeat'],f_visibility=data['f_visibility'])
        return self.createResultSet(data, 'json')
    
    def activateFilter(self, request):
        data = self.readData(request)
        objFilter = Filter.objects.filter(tagid=data['tagid'], stateid=data['stateid'], uid=data['uid'])
        if objFilter.count() == 0 and int(data['tagid']) < N_SYSTEM_TAGS:
            values = self.getDefaultFilterDataArray(data)
            self.addFilter(values)
        else:
            objFilter.update(is_checked=data['is_checked'])
        return self.createResultSet(data, 'json')

    def retrieveFilter(self, request):
        data                  = self.readData(request)
        objFilter             = Filter.objects.filter(tagid=data['tagid'], stateid=data['stateid'], uid=data['uid']).values()[0]
        objFilter['tag_name'] = Tag.objects.get(tagid=data['tagid']).tag_name
        print objFilter
        return self.createResultSet(objFilter)

class Note(models.Model, HttpRequestResponser, Formatter):
    note         = models.CharField(max_length=140)
    n_timestamp  = models.DateTimeField()
    link         = models.TextField(blank=True)
    noteid       = models.IntegerField(primary_key=True)
    uid          = models.ForeignKey('User', db_column='uid')
    radius       = models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)
    n_visibility = models.IntegerField()
    n_latitude   = models.DecimalField(max_digits=9, decimal_places=6)
    n_longitude  = models.DecimalField(max_digits=9, decimal_places=6)
    is_comment   = models.IntegerField()
    n_like       = models.IntegerField()

    class Meta:
        db_table = 'note'

    def getNewNoteid(self):
        if len(Note.objects.all().values()) == 0:
            return 1
        else:
            notetuple = Note.objects.all().order_by('noteid').latest('noteid')
            #print tag.tagid
            return notetuple.noteid + 1

    def addNote(self, data):
        newNoteid          = self.getNewNoteid()
        notetime              = Note()
        notetime.note         = data['note']
        notetime.n_timestamp  = datetime.datetime.now()
        notetime.link         = ''
        notetime.noteid       = newNoteid
        notetime.uid          = User(uid=data['uid'])
        
        if 'radius' in data:
            notetime.radius       = data['radius']
            notetime.n_visibility = data['n_visibility']
            if 'is_comment' in data:
                notetime.is_comment = data['is_comment']
            else:
                notetime.is_comment = 0
        else:
            notetime.radius       = 200                  # default 200 yards
            notetime.n_visibility = 0                    # default 0: public
            notetime.is_comment   = 1
        
        notetime.n_latitude   = data['n_latitude']
        notetime.n_longitude  = data['n_longitude']
        notetime.n_like       = 0
        notetime.save()
        data['noteid']        = newNoteid
        return data

    def plusLike(self, data):
        data['n_like'] = int(Note.objects.get(noteid=data['noteid']).n_like) + 1
        Note.objects.filter(noteid=data['noteid']).update(n_like=data['n_like'])
        return data

    def filterNotes(self, data):
        nowtime = timezone.now()
        # retrieve user filter
        uCTags = self.getUserCategoryTagsList(data)
        
        # retrieve notesets
        nlist1 = Note_Time.objects.filter(n_repeat=0, n_start_time__lte=nowtime, n_stop_time__gte=nowtime).values('noteid')
        nlist2 = Note_Time.objects.raw("Select noteid From Note_Time Where n_repeat=1 And Time(Now()) Between Time(n_start_time) And Time(n_stop_time)").values('noteid')
        nlist  = nlist1 + nlist2
        notesets = Note.objects.filter(n_visibility__in=[0,1], noteid__in=nlist)
        return data
    
class Note_Tag(models.Model, HttpRequestResponser, Formatter):
    noteid = models.ForeignKey('Note', db_column='noteid', primary_key=True)
    tagid  = models.ForeignKey('Tag', db_column='tagid', primary_key=True)

    class Meta:
        db_table = 'note_tag'
    
    def getSysTagid(self, data):
        for tagid in data['tagids']:
            if tagid >= 0 and tagid <= 10:
                return tagid
    
    def addNoteTag(self, data):
        notetag        = Note_Tag()
        notetag.noteid = Note(noteid=data['noteid'])
        notetag.tagid  = Tag(tagid=data['tagid'])
        notetag.save()
        return data

    def addMultipleNoteTags(self, data):
        if 'tagids' in data and type(data['tagids']) == list and len(data['tagids']) > 1:
            tags = data['tagids']
            for index in tags:
                data['tagid'] = tags[index]
                Note_Tag().addNoteTag(data)
        elif 'tagids' in data:
            Note_Tag().addNoteTag(data)
        
        # add tags from tag_names
        self.addNoteTagFromTagName(data)
        
        # add a default tag (all)
        data['tagid'] = 0
        Note_Tag().addNoteTag(data)
        return data
    
    def addNoteTagFromTagName(self, data):
        sys_tagid = self.getSysTagid(data)
        if 'tag_names' in data and len(data['tag_names']) > 1:
            for tag_name in data['tag_names']:
                data['tag_name']  = tag_name
                data['sys_tagid'] = sys_tagid
                tagid             = Tag().addTag(data)
                
    def deleteNoteTag(self, request):
        data = self.readData(request)
        Note_Tag.objects.filter(tagid=data['tagid'], noteid=data['noteid']).delete()
        return 0
    
class Note_Time(models.Model, HttpRequestResponser, Formatter):
    timeid       = models.IntegerField(primary_key=True)
    noteid       = models.ForeignKey('Note', db_column='noteid')
    n_start_time = models.DateTimeField()
    n_stop_time  = models.DateTimeField(null=True, blank=True)
    n_repeat     = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'note_time'

    def getNewNoteTimeid(self):
        if len(Note_Time.objects.all().values()) == 0:
            return 1
        else:
            notetime = Note_Time.objects.all().order_by('timeid',).latest('timeid')
            #print tag.tagid
            return notetime.timeid + 1

    def addNoteTime(self, data):
        newNoteTimeid         = self.getNewNoteTimeid()
        notetime              = Note_Time()
        notetime.timeid       = newNoteTimeid
        notetime.noteid       = Note(noteid=data['noteid'])
        notetime.n_start_time = data['n_start_time']
        notetime.n_stop_time  = data['n_stop_time']
        notetime.n_repeat     = data['n_repeat']
        notetime.save()
        return data
    
    def addNoteTimeRange(self, data):
        '''
        if 'n_start_time' in data and type(data['n_start_time']) == list and len(data['n_start_time']) > 1:
            start_time = data['n_start_time']
            stop_time  = data['n_stop_time']
            repeat     = data['n_repeat']
            for index in start_time:
                data['n_start_time'] = start_time[index]
                data['n_stop_time']  = stop_time[index]
                data['n_repeat']     = repeat[index]
                Note_Time().addNoteTime(data)
        '''
        
        if 'n_start_time' in data:
            if 'n_repeat' not in data:
                data['n_repeat'] = 0
            Note_Time().addNoteTime(data)
        else:
            data['n_start_time'] = datetime.datetime.now()
            data['n_stop_time']  = datetime.datetime.now() + datetime.timedelta(days=1)
            data['n_repeat']     = 0
            Note_Time().addNoteTime(data)
    
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
        filt = Filter()
        datalist = []
        #print data
        uslist = self.getUserStatesList(data)  # get user's all states
        #print uslist
        for row in uslist:
            filterset = filt.getUserStateFilters(row)
            row['filters'] = filterset
            datalist.append(row)
        return datalist

    def setDefaultState(self, request):
        data = self.readData(request)
        State.objects.all().update(is_current=0)
        State.objects.filter(stateid=data['stateid'], uid=data['uid']).update(is_current=1)
        return self.createResultSet(data, 'json')

    def insertState(self, uid, is_current, stateid):
        data = [stateid, STATE_NAME_DEFAULT, uid, is_current]
        args = dict([('table', 'State'), ('values', data)])
        SQLExecuter().doInsertData(args)
        '''
        state            = State()
        state.state_name = STATE_NAME_DEFAULT
        state.uid        = User(uid=input_uid)
        state.is_current = is_current
        state.stateid    = stateid
        state.save();
        '''

    def addState(self, request, mode='user-defined'):

        if mode == 'default':
            self.insertState(request['uid'], 1, 0)
            data = State.objects.filter(stateid=0, uid=request['uid']).values()
            return data
        else:
            request = self.readData(request)
            newStateid = self.getNewStateid()
            self.insertState(request['uid'], 0, newStateid)
            newState = State.objects.filter(stateid=newStateid).values()[0]
            #newState['filters'] = Filter().getUserStateFilters(newState)
            newState['filters'] = Tag().getSysTags()
            data = dict([('state', newState)])
            print data
            return self.createResultSet(data)

    def deleteState(self, request):
        data = self.readData(request)
        args = {}
        args['table'] = 'State'
        args['attributes'] = [{'field': 'stateid', 'logic': 'And'}, {'field': 'uid', 'logic': 'And'}]
        args['values'] = [data['stateid'], data['uid']]
        SQLExecuter().doDeleteData(args)
        return self.createResultSet(data, 'json')

    def updateState(self, request):
        data = self.readData(request)
        State.objects.filter(stateid=data['stateid'], uid=data['uid']).update(state_name=data['state_name'])
        return self.createResultSet(data, 'json')

class Tag(models.Model, HttpRequestResponser, Formatter):
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

    def getUserTagsList(self, request, returnType='html'):
        data        = self.readData(request)
        data['uid'] = '1'
        taglist     = list(Tag.objects.filter(uid=data['uid']).order_by('tagid').values())
        defaultlist = list(Tag.objects.filter(uid=None).order_by('tagid').values())
        data        = dict([('tagslist', taglist + defaultlist)])
        return self.createResultSet(data, returnType)

    def getUserCategoryTagsList(self, data):
        tmp         = []
        result      = []
        taglist     = list(Tag.objects.filter(uid=data['uid']).order_by('tagid').values())
        defaultlist = list(Tag.objects.filter(uid=None).order_by('tagid').values())
        print taglist
        
        for dtag in defaultlist[1:]:
            dtag['tags'] = []
            tmp.append(dtag)
        
        for row in tmp:
            for tag in taglist:
                if tag['sys_tagid'] == row['sys_tagid']:
                    row['tags'].append(tag)
            result.append(row)
                
        return result
    
    def addTag(self, data):
        newTagid      = self.getNewTagid()
        tag           = Tag()
        tag.tagid     = newTagid
        tag.tag_name  = data['tag_name']
        tag.uid       = User(uid=int(data['uid']))
        tag.sys_tagid = data['sys_tagid']
        tag.save()
        return newTagid

    def deleteTag(self, request):
        data = self.readData(request)
        args = {}
        args['table'] = 'Tag'
        args['attributes'] = [{'field': 'stateid', 'logic': 'And'}, {'field': 'uid', 'logic': 'And'}]
        args['values'] = [data['tagid'], data['uid']]
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
        request.session['uid'] = usr['uid']
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
        result = RESULT_SUCCESS
        message = []
        verifier = DataVerifier()
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
        state['uid']      = state['uid_id']
        ufilter = Filter().addDefaultFilter(state)

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
            return self.createResultSet({}, 'html', RESULT_FAIL, message)
        message = LOGOUT_SUCCESS
        return self.createResultSet({}, 'html', RESULT_SUCCESS, message)

    def getUserProfile(self, request):
        uid = request.session['uid']
        usr = self.getUserData(uid)
        data = dict([('user', usr), ('stateslist', State().getUserStatesAndFiltersList(usr))])
        #print data
        return self.createResultSet(data)
    
    def postNote(self, request):
        data       = self.readData(request)
        data       = Note().addNote(data)
        
        Note_Time().addNoteTimeRange(data)
        Note_Tag().addMultipleNoteTags(data)
            
        return self.createResultSet(data)

    def addExtraNoteTag(self, request):
        data = self.readData(request)
        Note_Tag().addNoteTags(data)
        return self.createResultSet(data)
    
    def clickLike(self, request):
        data = self.readData(request)
        data = Note().plusLike(data)
        return self.createResultSet(data)
    
    def postComment(self, request):
        data              = self.readData(request)
        data['commentid'] = Comments().addComment(data)
        return self.createResultSet(data)

    def searchNotes(self, request):
        data              = self.readData(request)
        '''
        data = {}
        data['uid']         = 2
        data['u_longitude'] = 39.557878
        data['u_latitude']  = 30.110333
        data['keyword']     = 'test'
        data['noteslist'] = NoteFilter().searchNotes(data)
        '''
        return self.createResultSet(data)
    
    def receiveNotes(self, request):
        data       = self.readData(request)
        '''
        data = {}
        data['uid']         = 2
        data['u_longitude'] = 39.557878
        data['u_latitude']  = 30.110333
        data['noteslist']   = NoteFilter().filterNotes(data)
        '''
        return self.createResultSet(data)
    
class NoteFilter(HttpRequestResponser, Formatter):
    
    def __init__(self):
        self.sql = SQLExecuter()
    
    def getValuesBasedonKey(self, valueset, key):
        result = []
        for row in valueset:
            result.append(row[key])
        return result
    
    def getNoteInfoListByKewords(self, data, currenttime):
        data['keyword'] = '%' + data['keyword'] + '%'
        strSQL          = "Select a.*, b.tagid, c.sys_tagid, c.tag_name, d.n_start_time, d.n_stop_time, n_repeat From note as a, note_tag as b, tag as c, (Select * From note_time Where %s between n_start_time And n_stop_time And n_repeat=0) as d Where a.noteid=b.noteid And b.tagid=c.tagid And a.noteid=d.noteid And (a.note like %s Or c.tag_name like %s) Union Select a.*, b.tagid, c.sys_tagid, c.tag_name, d.n_start_time, d.n_stop_time, n_repeat From note as a, note_tag as b, tag as c, (Select * From note_time Where %s between n_start_time And n_stop_time And n_repeat=1) as d Where a.noteid=b.noteid And b.tagid=c.tagid And a.noteid=d.noteid And (a.note like %s Or c.tag_name like %s)"
        noteslist       = self.sql.doRawSQL(strSQL, [currenttime, data['keyword'], data['keyword'], currenttime, data['keyword'], data['keyword']])
        return noteslist
    
    def getNoteInfoList(self, currenttime):
        # retrieve every detail of notes
        strSQL    = 'Select a.*, b.tagid, c.sys_tagid, d.n_start_time, d.n_stop_time, n_repeat From note as a, note_tag as b, tag as c, (Select * From note_time Where %s between n_start_time And n_stop_time And n_repeat=0) as d Where a.noteid=b.noteid And b.tagid=c.tagid And a.noteid=d.noteid Union Select a.*, b.tagid, c.sys_tagid, d.n_start_time, d.n_stop_time, n_repeat From note as a, note_tag as b, tag as c, (Select * From note_time Where %s between n_start_time And n_stop_time And n_repeat=1) as d Where a.noteid=b.noteid And b.tagid=c.tagid And a.noteid=d.noteid'
        noteslist = self.sql.doRawSQL(strSQL, [currenttime, currenttime])
        return noteslist
    
    def getUserCategoryTagsList(self, data):
        args               = {}
        args['columns']    = ['b.*, c.sys_tagid']
        args['tables']     = ['state as a', 'filter as b', 'tag as c']
        args['joins']      = ['a.stateid=b.stateid And a.uid=b.uid And b.tagid=c.tagid And a.is_current=1 And is_checked=1']
        args['conditions'] = [{'criteria': 'b.uid=', 'logic': 'And'}]
        args['values']     = [data['uid']]
        uCTags             = self.sql.doSelectData(args)
        return uCTags
    
    def computeDistance(self, data, n_longitude, n_latitude):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [n_longitude, n_latitude, data['u_longitude'], data['u_latitude']])
        
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a    = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c    = 2 * asin(sqrt(a)) 
        dist = (6367 * c) * 1093.61 # km to yard
        return dist
    
    def filterByTags(self, uProfile, noteslist):
        result  = []
        passset = self.getValuesBasedonKey(uProfile, 'sys_tagid')
        for note in noteslist:
            if note['sys_tagid'] in passset:
                result.append(note)
        return result
    
    def filterByTime(self, uProfile, noteslist, currenttime):
        result      = []
        sys_tagset  = []
        for filter in uProfile:
            if filter.f_repeat:
                current = dateparse.parse_time(currenttime)
                start   = dateparse.parse_time(filter.f_start_time)
                end     = dateparse.parse_time(filter.f_stop_time)
            else:
                current = currenttime
                start   = filter.f_start_time
                end     = filter.f_stop_time
                
            if current >= start and current <= end:
                sys_tagset.append(filter.sys_tagid)
         
        for note in noteslist:
            if note['sys_tagid'] in sys_tagset:
                result.append(note)
        return result
    
    def filterByVisibility(self, data, uProfile, noteslist):
        friendslist = Friend().getFriendsList(data)
        # generalize visibility of user tags based on sys_tags
        sys_visset = {}
        result     = []
        for ufilter in uProfile:
            sys_tag    = ufilter.systagid
            visibility = ufilter.f_visibility
            if (sys_tag in sys_visset and sys_visset[sys_tag] < visibility) or (sys_tag not in sys_visset):
                sys_visset[sys_tag] = visibility
        
        for note in noteslist:
            if note['sys_tagid'] in sys_visset and sys_visset[note.sys_tagid] == note['n_visibility']:
                if (note['n_visibility'] == 1 and note['uid'] in friendslist) or note['n_visibility'] == 0:
                    result.append(note)
    
        return result
    
    def filterByLocation(self, data, noteslist):
        result = []
        for note in noteslist:
            dist = self.computeDistance(data, note['n_longitude'], note['n_latitude'])
            if dist <= note['radius']:
                result.append(note)
        return result
    
    def filterNotes(self, data, mode='normal'):
        currenttime = timezone.now()
        if mode == 'normal':
            noteslist = self.getNoteInfoList(currenttime)
        else:
            noteslist = self.getNoteInfoListByKewords(data, currenttime)
        uProfile    = self.getUserCategoryTagsList(data)
        
        # filter by user's tags
        noteslist = self.filterByTags(uProfile, noteslist)
        
        # filter by user's time range
        noteslist = self.filterByTime(uProfile, noteslist, currenttime)
        
        # filter by visibility and friendship
        noteslist = self.filterByVisibility(data, uProfile, noteslist)
        
        # filter by location
        noteslist = self.filterByLocation(data, noteslist)
        print noteslist
        return noteslist

    def searchNotes(self, data):
        noteslist = self.filterNotes(data, 'keyword')
        
        
        