from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.template import RequestContext
from Jingo.lib.DataVerification import Formatter
import json

class HttpRequestResponser(Formatter):
    
    def convertToDict(self, request):
        data = {}
        if request.method == 'POST':
            args = dict(request.POST.iterlists())
        else:
            args = dict(request.GET.iterlists())
        for key in args:
            if len(args[key]) > 1:
                data[key] = args[key]
            else:
                data[key] = args[key][0]
        return data
    
    def jsonEncoder(self, resultset):
        return json.JSONEncoder().encode(resultset)
    
    def readData(self, request):
        data = self.convertToDict(request)
        print "POST/GET data"
        print data
        return data
    
    def responseJSON(self, request, data):
        return self.response(request, '', data, 'json')
        
    def response(self, request, page, data={}, dataType='default'):
        if dataType == 'json':
            resultset = self.jsonEncoder(data)
            print "final json data"
            print resultset
            return HttpResponse(resultset, mimetype="application/json")
        if dataType == 'default':
            resultset = data
            print "final data"
            print resultset
            return render_to_response(page, resultset, context_instance=RequestContext(request))
        