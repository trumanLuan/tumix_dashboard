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
    value = request.GET.get('value', '')
    dataset_title = 'Deficiency of ribosomal proteins reshapes the transcriptional and translational landscape in human cells'
    dataset_organism = "Human"
    dataset_geo = "hahha"
    dataset_design = "To be downloaded"

    return render(request, "browse_results.html", {
        'value': value,
        'dataset_title': dataset_title,
        'dataset_organism': dataset_organism,
        'dataset_geo': dataset_geo,
        'dataset_design': dataset_design,
        'studies': Study.objects.all()
    } )

# views for goto search page from the sidebar.
def search(request):
    return render(request, 'search.html')

# views for goto help page from the sidebar.
def help(request):
    return render(request, 'help.html')