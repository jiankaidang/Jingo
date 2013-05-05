from django.shortcuts import redirect
from Jingo.models import *

http_res = HttpRequestResponser()

def init(request):
    data        = {}
    data['uid'] = request.session['uid']
    data        = Tag().getUserCategoryTagsList(data)
    data        = dict([('tagslist', data)])
    print "show tagslist"
    print data
    return Formatter().createResultSet(data)

def index(request):
    #print User().searchNotes([])
    #data={}
    #data['uid'] = 4
    #print Tag().getUserCategoryTagsList(data)
    #request.session.clear()
    page = 'login.html'
    if request.session.get('uid', False):
        page = 'index.html'
        data = init(request)
        return http_res.response(request, page, data)
    return http_res.response(request, page)

def admin(request):
    page = 'admin.html'
    return http_res.response(request, page)

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
        page = 'response.html'
        data = State().setDefaultState(request)
        return http_res.response(request, page, data, 'json')

    if mode == 'addState':
        page = 'state.html'
        data = State().addState(request)
        return http_res.response(request, page, data)

    if mode == 'deleteState':
        page = 'response.html'
        data = State().deleteState(request)
        return http_res.response(request, page, data, 'json')

    if mode == 'updateState':
        page = 'response.html'
        data = State().updateState(request)
        return http_res.response(request, page, data, 'json')

    # API for filter settings
    if mode == 'activateFilter':
        page = 'response.html'
        data = Filter().activateFilter(request)
        return http_res.response(request, page, data, 'json')

    if mode == 'addFilter':
        page = 'response.html'
        data = Filter().addFilterAndTag(request)
        return http_res.response(request, page, data, 'json')

    if mode == 'deleteFilter':
        page = 'response.html'
        data = Filter().deleteFilter(request)
        return http_res.response(request, page, data, 'json')

    if mode == 'updateFilter':
        page = 'response.html'
        data = Filter().updateFilter(request)
        return http_res.response(request, page, data, 'json')

    if mode == 'retrieveFilter':
        page = 'filter.html'
        data = Filter().retrieveFilter(request)
        return http_res.response(request, page, data)

    # API for note settings
    if mode == 'postNote':
        page = 'response.html'
        data = User().postNote(request)
        return http_res.response(request, page, data, 'json')

    if mode == 'searchNotes':
        page = 'response.html'
        data = User().searchNotes(request)
        return http_res.response(request, page, data, 'json')

    if mode == 'postComment':
        page = 'response.html'
        data = User().postComment(request)
        return http_res.response(request, page, data, 'json')
        
    if mode == 'deleteNoteTag':
        page = 'response.html'
        data = User().deleteNoteTag(request)
        return http_res.response(request, page, data, 'json')

    if mode == 'addExtraNoteTag':
        page = 'response.html'
        data = User().addExtraNoteTag(request)
        return http_res.response(request, page, data, 'json')

    if mode == 'clickLike':
        page = 'response.html'
        data = User().clickLike(request)
        return http_res.response(request, page, data, 'json')

    if mode == 'receiveNotes':
        page = 'response.html'
        data = User().receiveNotes(request)
        return http_res.response(request, page, data, 'json')
    
    if mode == 'readNote':
        page = 'note.html'
        data = User().readNote(request)
        return http_res.response(request, page, data)

    # API for Friendship settings
    if mode == 'sendInvitation':
        data = User().sendInvitation(request)
        return http_res.response(request, page, data, 'json')
    
    if mode == 'replyInvitation':
        data = User().replyInvitation(request)
        return http_res.response(request, page, data, 'json')
    