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


def pages(request, mode):
    if mode == 'signupform':
        page = 'signup.html'
    elif mode == 'login':
        page = 'login.html'

    return render(request, page, {})


def tasks(request, mode):
    if mode == 'signup':
        page = 'response.html'
        data = User().signup(request)

    if mode == 'setState':
        page = 'response.html'
        data = User().login(request)

    if mode == 'login':
        page = 'response.html'
        data = User().login(request)

    if mode == 'logout':
        page = 'logout.html'
        data = User().logout(request)

    return http_res.response(page, data)
    