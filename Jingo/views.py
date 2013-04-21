from django.shortcuts import render, render_to_response
from Jingo.models import *
from Jingo.lib.HttpRequestTasks import HttpRequestResponser

def index(request):
    test = {
            'test': 'This is Jingo Homepage.',
            }
    return render(request, 'index.html', test)

def tasks(request, mode):
    #page = 'index.html'
    http_res = HttpRequestResponser()
    
    if mode == 'login':
        page = 'response.html'
        data = User().login(request)
        
    if mode == 'logout':
        page = 'logout.html'
        data = User().logout(request)
        
    return http_res.response(page, data)
    