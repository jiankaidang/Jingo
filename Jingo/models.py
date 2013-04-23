# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.utils import timezone
from django.db import models

from Jingo.lib.HttpRequestTasks import HttpRequestResponser
from Jingo.lib.DataVerification import Formatter, DataVerifier


class Comments(models.Model):
    commentid = models.IntegerField(primary_key=True)
    noteid = models.ForeignKey('Note', db_column='noteid')
    c_timestamp = models.DateTimeField()
    uid = models.ForeignKey('User', db_column='uid')
    c_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    c_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    comment = models.CharField(max_length=140)

    class Meta:
        db_table = 'comments'


class Filter(models.Model):
    stateid = models.ForeignKey('State', db_column='stateid', primary_key=True)
    tagid = models.ForeignKey('Tag', db_column='tagid', primary_key=True)
    f_start_time = models.DateTimeField(null=True, blank=True)
    f_stop_time = models.DateTimeField(null=True, blank=True)
    f_repeat = models.IntegerField(null=True, blank=True)
    f_visibility = models.IntegerField()
    uid = models.ForeignKey('State', db_column='uid', primary_key=True)

    class Meta:
        db_table = 'filter'
    
    def getUserFilters(self, input_id):
        return Filter.objects.filter(uid=input_id).order_by('uid', 'stateid', 'tagid').values()
    
    def addFilter(self, data):
        filters = Filter()
        filters.stateid      = State(stateid=data['stateid'])
        filters.tagid        = Tag(tagid=data['tagid'])
        filters.f_start_time = data['f_start_time']
        filters.f_stop_time  = data['f_stop_time']
        filters.f_repeat     = data['f_repeat']
        filters.f_visibility = data['f_visibility']
        filters.uid          = User(uid=data['uid'])
        filters.save()
        return data


class Friend(models.Model):
    uid = models.ForeignKey('User', db_column='uid')
    f_uid = models.ForeignKey('User', db_column='f_uid')
    is_friendship = models.IntegerField()
    invitationid = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'friend'
    
    def getNewInvitationid(self):
        friend = Friend.objects.all().order_by('invitationid').latest('invitationid')
        print friend.invitationid
        return friend.invitationid + 1
    
    def getFriendsInvitations(self, input_uid):
        return Friend.objects.filter(uid=input_uid, isfriendship=2).order_by('invitationid').values()

    def getFriendsList(self, input_uid):
        return Friend.objects.filter(uid=input_uid, isfriendship=1).order_by('invitationid').values()

<<<<<<< HEAD

=======
    def addInvitation(self, data):
        newInvitationid      = self.getNewInvitationid()
        friend               = Friend()
        friend.uid           = data['uid']
        friend.f_uid         = data['f_uid']
        friend.is_friendship = 2                 # 0:denied, 1:accepted, 2:pending
        friend.invitationid  = newInvitationid
        return Friend.objects.filter(invitationid=newInvitationid)
        
>>>>>>> model
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


class State(models.Model):
    stateid = models.IntegerField(primary_key=True)
    state_name = models.CharField(max_length=45)
    uid = models.ForeignKey('User', db_column='uid', primary_key=True)
    is_current = models.IntegerField()

    class Meta:
        db_table = 'state'

    def getNewStateid(self):
        ustate = State.objects.all().order_by('uid, stateid').latest('stateid')
        return ustate.stateid + 1

    def addState(self, data):
        state = State()
        state.stateid = 0
        state.state_name = data['state_name']
        state.uid = User(uid=int(data['uid']))
        state.is_current = 1
        state.save();
        return State.objects.filter(stateid=0, uid=data['uid']).values()[0]


class Tag(models.Model):
    tagid = models.IntegerField(primary_key=True)
    tag_name = models.CharField(max_length=45)
    uid = models.ForeignKey('User', null=True, db_column='uid', blank=True)
    sys_tagid = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'tag'
<<<<<<< HEAD

    def getSysTags(self):
        return Tag.objects.order_by('tagid').filter(tagid__gte=0, tagid__lte=10)


=======
    
    def getNewTagid(self):
        tag = Tag.objects.all().order_by('tagid').latest('tagid')
        print tag.tagid
        return tag.tagid + 1
    
    def getSysTags(self):
        return Tag.objects.order_by('tagid').filter(tagid__gte=0, tagid__lte=10)
    
    def addTag(self, data):
        newTagid      = self.getNewTagid()
        tag           = Tag()
        tag.tagid     = newTagid
        tag.tag_name  = data['tag_name']
        tag.uid       = User(uid=int(data['uid']))
        tag.sys_tagid = data['sys_tagid']
        tag.save()
        return Tag.objects.filter(tagid=newTagid, uid=int(data['uid'])).values()
    
>>>>>>> model
class User(models.Model, HttpRequestResponser):
    uid = models.IntegerField(primary_key=True)
    u_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    u_timestamp = models.DateTimeField()
    password = models.CharField(max_length=15)

    class Meta:
        db_table = 'user'

    def getNewUid(self):
<<<<<<< HEAD
        if len(User.objects.all().values()) == 0:
            return 1
        else:
            usr = User.objects.all().order_by('uid').latest('uid')
            print usr.uid
            return usr.uid + 1

=======
        usr = User.objects.all().order_by('uid').latest('uid')
        #print usr.uid
        return usr.uid + 1
    
>>>>>>> model
    def addUser(self, data):
        usr = User()
        usr.uid = self.getNewUid()
        usr.u_name = data['u_name']
        usr.email = data['email']
        usr.password = data['password']
        usr.u_timestamp = timezone.now()
        usr.save()
        return User.objects.filter(email=data['email']).values()[0]

    def signup(self, request):
        result = 'success'
        message = []
        verifier = DataVerifier()
        formatter = Formatter()
        data = self.readData(request)

        if not verifier.isValidFormat(data['email'], 'email'):
            message.append('The email address is invalid.')
            result = 'fail'

        if not verifier.isEmailUnique(User.objects, data['email']):
            message.append('The email address is already taken.')
            result = 'fail'

        usr = formatter.simplifyObjToData(self.addUser(data))
        usr['state_name'] = 'myState'
        state = State().addState(usr)
        data = dict([('usr', usr), ('state', state), ])

        #print data
        return dict([('result', result), ('data', data), ('message', message), ])

    def login(self, request):
        if request.method != 'POST':
            pass
            # raise Http404('Only POSTs are allowed')
        print request.session.get('uid', False)
        if request.session.get('uid', False):
            print 'you already logged in!'
            return dict([('result', 'fail'), ('data', '')])
        else:
            try:
                data = self.readData(request)
                print data
                usr = User.objects.get(email=data['email']).__dict__

                if usr['password'] == data['password']:
                    del usr['_state']
                    request.session['uid'] = usr['uid']
                    usr['u_timestamp'] = usr['u_timestamp'].isoformat()
                    #print usr
                    return dict([('result', 'success'), ('data', usr)])

            except User.DoesNotExist:
                return dict([('result', 'fail'), ('data', 0)])

    def logout(self, request):
        try:
            del request.session['uid']
            request.session.clear()
        except KeyError:
            pass
        return dict([('result', 'success'), ('message', 'You\'re logged out.')])
