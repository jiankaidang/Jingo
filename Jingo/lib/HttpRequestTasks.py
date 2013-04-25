from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from Jingo.lib.DataVerification import Formatter
import json

class HttpRequestResponser:
    def readData(self, request):
        if request.method == 'GET':
            data = request.GET.dict()
        elif request.method == 'POST':
            data = request.POST.dict()
        return data

    def response(self, page, data={}, dataType='default'):
        fmr      = Formatter()
        if dataType == 'json':
            #result = {'result' : json.dumps(data),}
            result = {'result' : fmr.jsonEncoder(data),}
        if dataType == 'default':
            result = {'result' : data,}
        return render_to_response(page, result)
        