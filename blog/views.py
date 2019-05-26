from django.shortcuts import render


from django.http import HttpResponse #new
from datetime import datetime
# Create your views here.

def index(request):
    return HttpResponse("hello django")

def current_datetime(request):
    html = "<html><body> IT is now %s. </body></html>" % datetime.now()
    return HttpResponse(html)