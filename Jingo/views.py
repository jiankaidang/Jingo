from django.shortcuts import redirect
from Jingo.models import *

http_res = HttpRequestResponser()


def index(request):
    page = 'login.html'
    if request.session.get('uid', False):
        page = 'index.html'
    return http_res.response(request, page)
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
        #page = 'response.html'
        if request.session.get('uid', False):
            data = User().getUserProfile(request)
        else:
            page = 'login.html'
    return http_res.response(request, page, data)

# deal with AJAX request and database access
def tasks(request, mode):
    # API for user behaviors
    if mode == 'logout':
        data = User().logout(request)
        return redirect('http://localhost:8000')

    if mode == 'signup':
        page = 'profile.html'
        data = User().signup(request)
        return redirect('/pages/profile/')

    if mode == 'login':
        page = 'index.html'
        data = User().login(request)

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

    # API for tag settings
    if mode == 'getUserTags':
        page = 'response.html'
        data = Tag().getUserTags(request)
        return http_res.response(request, page, data, 'json')

    if mode == 'addTag':
        page = 'response.html'
        data = Tag().addTag(request)

    if mode == 'deleteTag':
        page = 'response.html'
        data = Tag().deleteTag(request)

    if mode == 'updateTag':
        page = 'response.html'
        data = Tag().updateTag(request)

    # API for filter settings
    if mode == 'activateFilter':
        page = 'response.html'
        data = Filter().addFilter(request)
        return http_res.response(request, page, data, 'json')

    if mode == 'deactivateFilter':
        page = 'response.html'
        data = Filter().addFilter(request)
        return http_res.response(request, page, data, 'json')

    if mode == 'addFilter':
        page = 'response.html'
        data = Filter().addFilter(request)

    if mode == 'deleteFilter':
        page = 'response.html'
        data = Filter().deleteFilter(request)

    if mode == 'updateFilter':
        page = 'response.html'
        data = Filter().updateFilter(request)

    return http_res.response(request, page, data)
    