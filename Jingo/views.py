from django.shortcuts import redirect
from Jingo.models import *

http_res = HttpRequestResponser()

def init(request):
    # for post notes
    data              = {}
    data['uid']       = request.session['uid']
    data['tagslist']  = Tag().getUserCategoryTagsList(data)
    #data              = dict([('tagslist', data)])
    #print data
    data['n_request'] = len(Friend.objects.filter(f_uid=data['uid'], is_friendship=2).values())
    return Formatter().createResultSet(data)

def index(request):
    page = 'login.html'
    if request.session.get('uid', False):
        page = 'index.html'
        data = init(request)
        return http_res.response(request, page, data)
    return http_res.response(request, page)

def admin(request):
    if isRedirect(request):
        page = 'admin.html'
        data = AdminArea().init()
        
    return http_res.response(request, page, data)

def isRedirect(request, target='index'):
    if request.session.get('uid', False):
        return redirect(target)
    return False

# redirect to specific pages
def pages(request, mode):
    if mode == 'signup':
        return http_res.response(request, 'signup.html')

    if mode == 'login':
        if request.session.get('uid', False):
            return redirect('index')
        else:
            return http_res.response(request, 'login.html')

    if mode == 'profile':
        if request.session.get('uid', False):
            usr = request.session['usrdata']
            return http_res.response(request, 'profile.html', dict([('stateslist', State().getUserStatesAndFiltersList(usr))]))
        else: 
            return redirect('/pages/login/')
            
    if mode == 'friends':
        if request.session.get('uid', False):
            return http_res.response(request, 'friends.html', User().initFriendArea(request))
        else: 
            return redirect('/pages/login/')

# deal with AJAX request and database access
def tasks(request, mode):
    # API for user behaviors
    if mode == 'logout':
        data = User().logout(request)
        return redirect('/pages/login/')

    if mode == 'signup':
        page = 'profile.html'
        data = User().signup(request)
        if data['result']:
            return redirect('/pages/profile/')
        else:
            return http_res.response(request, 'signup.html', data)

    if mode == 'login':
        data = User().login(request)
        if data['result']:
            return redirect('index')
        else:
            return http_res.response(request, 'login.html', data)

    # API for profile settings
    if mode == 'setDefaultState':
        data = State().setDefaultState(request)
        return http_res.responseJSON(request, data)

    if mode == 'addState':
        page = 'state.html'
        data = State().addState(request)
        return http_res.response(request, page, data)

    if mode == 'deleteState':
        data = State().deleteState(request)
        return http_res.responseJSON(request, data)

    if mode == 'updateState':
        data = State().updateState(request)
        return http_res.responseJSON(request, data)

    # API for filter settings
    if mode == 'activateFilter':
        data = Filter().activateFilter(request)
        return http_res.responseJSON(request, data)

    if mode == 'addFilter':
        data = Filter().addFilterAndTag(request)
        return http_res.responseJSON(request, data)

    if mode == 'deleteFilter':
        data = Filter().deleteFilter(request)
        return http_res.responseJSON(request, data)

    if mode == 'updateFilter':
        data = Filter().updateFilter(request)
        return http_res.responseJSON(request, data)

    if mode == 'retrieveFilter':
        page = 'filter.html'
        data = Filter().retrieveFilter(request)
        return http_res.response(request, page, data)

    # API for note settings
    if mode == 'postNote':
        data = User().postNote(request)
        return http_res.responseJSON(request, data)

    if mode == 'searchNotes':
        data = User().searchNotes(request)
        return http_res.responseJSON(request, data)

    if mode == 'postComment':
        data = User().postComment(request)
        return http_res.responseJSON(request, data)
        
    if mode == 'deleteNoteTag':
        data = User().deleteNoteTag(request)
        return http_res.responseJSON(request, data)

    if mode == 'addExtraNoteTag':
        data = User().addExtraNoteTag(request)
        return http_res.responseJSON(request, data)

    if mode == 'clickLike':
        data = User().clickLike(request)
        return http_res.responseJSON(request, data)

    if mode == 'receiveNotes':
        data = User().receiveNotes(request)
        return http_res.responseJSON(request, data)
    
    if mode == 'readNote':
        page = 'note.html'
        data = User().readNote(request)
        return http_res.response(request, page, data)

    # API for Friendship settings
    if mode == 'sendInvitation':
        data = User().sendInvitation(request)
        return http_res.responseJSON(request, data)
    
    if mode == 'replyInvitation':
        data = User().replyInvitation(request)
        return http_res.responseJSON(request, data)
    
    if mode == 'unfollow':
        data = User().unfollow(request)
        return http_res.responseJSON(request, data)
    