from Jingo.models import *

http_res = HttpRequestResponser()


def index(request):
    # data = {}
    # data['uid'] = 1
    # data['stateid'] = 0
    # data['tagid'] = 0
    # print Filter().addFilter(data)
    test = {
        'test': 'This is Jingo Homepage',
    }
    return http_res.response(request, 'index.html', test)
    #return render(request, 'index.html', test)

# redirect to specific pages
def pages(request, mode):
    data = {}
    if mode == 'signup':
        page = 'signup.html'

    if mode == 'login':
        page = 'login.html'

    if mode == 'profile':
        page = 'profile.html'
        #if request.session['uid']:
        if request.session.get('uid', False):
            data = User().getUserProfile(request)
        else:
            page = 'login.html'
    return http_res.response(request, page, data)

# deal with AJAX request and database access
def tasks(request, mode):
    if mode == 'signup':
        page = 'profile.html'
        data = User().signup(request)

    if mode == 'login':
        page = 'index.html'
        data = User().login(request)

    if mode == 'logout':
        page = 'login.html'
        data = User().logout(request)
    
    # API for profile settings
    if mode == 'setDefaultState':
        page = 'response.html'
        data = State().setDefaultState(request)
        
    if mode == 'addState':
        page = 'response.html'
        data = State().addState(request)
    
    if mode == 'deleteState':
        page = 'response.html'
        data = State().deleteState(request)
        
    if mode == 'updateState':
        page = 'response.html'
        data = State().updateState(request)
        
    return http_res.response(request, page, data)
    