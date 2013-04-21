from django.shortcuts import render, render_to_response
import json

class HttpRequestResponser:
    def readData(self, request):
        if request.method == 'GET':
            data = request.GET.dict()
        elif request.method == 'POST':
            data = request.POST.dict()
        return data
    
    def response(self, page, data, dataType='json'):
        if dataType == 'json':
            result = {'result' : json.dumps(data),}
        
        return render_to_response(page, result)
        