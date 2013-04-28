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
        if dataType == 'json':
            #resultset['result'] = json.dumps(data)
            #resultset = dict([('result', self.jsonEncoder(data))])
            resultset = dict([('result', data)])
            print resultset
        if dataType == 'default':
            resultset = data

        return render_to_response(page, resultset, context_instance=RequestContext(request))
        