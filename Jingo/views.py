from django.shortcuts import render

def index(request):
    test = {'test': 'This is Jingo Homepage.'}
    return render(request, 'index.html', test)