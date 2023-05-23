from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee
from .models import Study
from .models import Marker_Subcluster
from .models import Marker_Celltype
from .models import LRpairs
from .models import SingleCell
from .models import SignalPathway


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
    value_dt_selected = request.GET.get('value', '')

    # subset rows from Marker_Subcluster table.
    try:
        row_subcluster_marker = Marker_Subcluster.objects.filter(dataset=value_dt_selected)
    except Marker_Subcluster.DoesNotExist:
        row_subcluster_marker = None
    dataset_title = 'Deficiency of ribosomal proteins reshapes the transcriptional and translational landscape in human cells'
    dataset_organism = "Human"
    dataset_geo = "hahha"
    dataset_design = "To be downloaded"

    return render(request, "browse_results.html", {
        'value': value_dt_selected,
        'dataset_title': dataset_title,
        'dataset_organism': dataset_organism,
        'dataset_geo': dataset_geo,
        'dataset_design': dataset_design,
        'row_subcluster_marker': row_subcluster_marker,
        'major_celltype_marker': Marker_Celltype.objects.all(),
        'LRpairs': LRpairs.objects.all(),
        'signal_pathway': SignalPathway.objects.all()
    } )

# views for goto search page from the sidebar.
def search(request):
    return render(request, 'search.html')

# views for goto help page from the sidebar.
def help(request):
    return render(request, 'help.html')