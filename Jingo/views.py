from django.shortcuts import render
from Jingo.models import *

http_res = HttpRequestResponser()


def index(request):
    #dataverify = DataVerifier()
    #dataverify.setRulesBase()
    test = {
        'test': 'This is Jingo Homepage.',
    }
    return render(request, 'index.html', test)

<<<<<<< HEAD

=======
# redirect to specific pages
>>>>>>> modify a little
def pages(request, mode):
    if mode == 'signupform':
        page = 'signup.html'
    elif mode == 'login':
        page = 'login.html'

    return render(request, page, {})

<<<<<<< HEAD

=======
# deal with AJAX request and database access
>>>>>>> modify a little
def tasks(request, mode):
    if mode == 'signup':
        page = 'response.html'
        data = User().signup(request)
<<<<<<< HEAD

    if mode == 'setState':
        page = 'response.html'
        data = User().login(request)

=======
        
>>>>>>> modify a little
    if mode == 'login':
        page = 'response.html'
        data = User().login(request)

    if mode == 'logout':
        page = 'logout.html'
        data = User().logout(request)
<<<<<<< HEAD

=======
    
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
    
>>>>>>> modify a little
    return http_res.response(page, data)
    