from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def apply(request):
    return render(request, 'apply.html')

def logbook(request):
    return render(request, 'logbook.html')

def downloads(request):
    return render(request, 'downloads.html')

def login(request):
    return render(request, 'auth/login.html')