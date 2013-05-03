from django.shortcuts import redirect
from Jingo.models import *

http_res = HttpRequestResponser()

def index(request):
    #print User().searchNotes([])
    #data={}
    #data['uid'] = 4
    #print Tag().getUserCategoryTagsList(data)

    page = 'login.html'
    if request.session.get('uid', False):
        page = 'index.html'
    return http_res.response(request, page)


def admin(request):
    page = 'admin.html'
    return http_res.response(request, page)

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
<<<<<<< HEAD
        return redirect("/pages/login/")
=======
        return redirect('/pages/login/')
>>>>>>> commit

    if mode == 'signup':
        page = 'profile.html'
        data = User().signup(request)
        return redirect('/pages/profile/')

    if mode == 'login':
        page = 'index.html'
        data = User().login(request)
        return http_res.response(request, page, data)

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

    if mode == 'searchNote':
        page = 'response.html'
        data = User().searchNote(request)
        return http_res.response(request, page, data, 'json')

    if mode == 'postComment':
        page = 'response.html'
        data = User().postComment(request)
<<<<<<< HEAD
        return http_res.response(request, page, data, 'json')

=======
        return redirect('http://localhost:8000')
        #return http_res.response(request, page, data, 'json')
    
>>>>>>> commit
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

    if mode == 'getTagsList':
        page = 'response.html'
        data = User().clickLike(request)
        return http_res.response(request, page, data, 'json')

    # API for Tag settings
    if mode == 'getUserTagsList':
        page = 'response.html'
        data = Tag().getUserTagsList(request)
        return http_res.response(request, page, data, 'json')