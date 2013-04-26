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

    if mode == 'getSysTags':
        page = 'response.html'
        data = Tag().getSysTags(request)

    if mode == 'getUserTags':
        page = 'response.html'
        data = Tag().getUserTags(request)

    if mode == 'addTag':
        page = 'response.html'
        data = Tag().addTag(request)

    if mode == 'addFilter':
        page = 'response.html'
        data = Filter().addFilter(request)

    if mode == 'getUserFilters':
        page = 'response.html'
        data = Filter().getUserFilters(request)

    if mode == 'addInivitation':
        page = 'response.html'
        data = Friend().addInvitation(data)

    if mode == 'getFriendInivitations':
        page = 'response.html'
        data = Friend().getFriendsInvitations(data)

    if mode == 'getFriendsList':
        page = 'response.html'
        data = Friend().getFriendsList(data)

    return http_res.response(request, page, data)
    