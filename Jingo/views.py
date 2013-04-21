from django.shortcuts import render, render_to_response
from Jingo.lib.HttpRequestTasks import HttpRequestParser
from Jingo.lib.Users import Users
import json

hrt = HttpRequestParser()

def index(request):
    request.session.clear()
    test = {
            'test': 'This is Jingo Homepage.',
            }
    return render(request, 'index.html', test)

def tasks(request, mode):
    data = hrt.readData(request)
    #page = 'index.html'
    page = 'response.html'
    if mode == 'login':
        usr = Users()
        result = {'result' : json.dumps(usr.doLogin(request, data)),}
        #print result
    return render_to_response(page, result)