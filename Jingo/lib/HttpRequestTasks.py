from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from Jingo.lib.DataVerification import Formatter
import json

class HttpRequestResponser(Formatter):
    def readData(self, request):
        if request.method == 'GET':
            data = request.GET.dict()
        elif request.method == 'POST':
            data = request.POST.dict()
        return data

    def response(self, request, page, data={}, dataType='default'):
        '''
        c = {}
        test = csrf(request)
        print test
        c.update(test)
        '''
        
        if dataType == 'json':
            #resultset['result'] = json.dumps(data)
            resultset = self.jsonEncoder(data)
        if dataType == 'default':
            resultset = data

        return render_to_response(page, resultset, context_instance=RequestContext(request))
        