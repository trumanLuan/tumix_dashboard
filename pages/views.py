from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee
from .models import Study

# Create your views here.
def index(request):
    return render(request, "index.html", {"employees": Employee.objects.all()})

def home(request):
    return render(request, 'index.html')

# views for search function in the homepage.


# views for goto browse page from the sidebar.
def browse(request):
    return render(request, 'browse.html', {"studies": Study.objects.all()}) # need to define Study class in models.py.

def browse_results(request):
    dataset = Study.objects.all()
    return render(request, "browse_results.html", {'dataset': dataset} )

# views for goto search page from the sidebar.
def search(request):
    return render(request, 'search.html')

# views for goto help page from the sidebar.
def help(request):
    return render(request, 'help.html')