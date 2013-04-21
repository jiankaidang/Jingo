class HttpRequestParser:
    def readData(self, request):
        #data = {}
        if request.method == 'GET':
            data = request.GET.dict()
        elif request.method == 'POST':
            data = request.POST.dict()
        return data
        