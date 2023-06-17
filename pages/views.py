from django.shortcuts import render
from django.shortcuts import get_object_or_404
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
    get_datasetindex = request.GET.get('value')
    print("Parameter value:", get_datasetindex)

    ## dataset meta-information.
    dataset_row = get_object_or_404(Study, dataset=get_datasetindex)

    ## brow_by_sample, UMI counts of single cells.
    umi_count_by_sample_svg_path = 'static/assets/img/browse_results/' + get_datasetindex + "_umi_count_by_sample.svg"

    ## brow_by_sample, feature counts of single cells.
    feature_count_by_sample_svg_path = 'static/assets/img/browse_results/' + get_datasetindex + "_feature_count_by_sample.svg"

    ## brow_by_sample,singlecell counts by samples.
    singlecell_count_by_sample_svg_path = 'static/assets/img/browse_results/' + get_datasetindex + "_singlecell_count_by_sample.svg"

    ## brow_by_sample, cell clustering results by sample.



    ## brow_by_celltype, cell stat by cell types.


    ## brow_by_celltype, cell clustering results by cell type.




    # subset rows from pages_marker_celltype table.
    try:
        row_celltype_marker = Marker_Celltype.objects.filter(dataset=get_datasetindex)
    except Marker_Celltype.DoesNotExist:
        row_celltype_marker = None

    # subset rows from pages_marker_subcluster table.
    try:
        row_subcluster_marker = Marker_Subcluster.objects.filter(dataset=get_datasetindex)
    except Marker_Subcluster.DoesNotExist:
        row_subcluster_marker = None

    # subset rows from pages_lrpairs table.
    try:
        row_LRpairs = LRpairs.objects.filter(dataset=get_datasetindex)
    except LRpairs.DoesNotExist:
        row_LRpairs = None

    # subset rows from pages_signalpathway table.
    try:
        row_signalpathway = SignalPathway.objects.filter(dataset=get_datasetindex)
    except SignalPathway.DoesNotExist:
        row_signalpathway = None

    return render(request, "browse_results.html", {
        'dataset_name': get_datasetindex,
        'dataset_row': dataset_row,
        'row_subcluster_marker': row_subcluster_marker,
        'row_celltype_marker': row_celltype_marker,
        'row_LRpairs': row_LRpairs,
        'row_signalpathway': row_signalpathway,
        'umi_count_by_sample_svg_path': umi_count_by_sample_svg_path,
        'feature_count_by_sample_svg_path': feature_count_by_sample_svg_path,
        'singlecell_count_by_sample_svg_path': singlecell_count_by_sample_svg_path
    })

# views for goto search page from the sidebar.
def search(request):
    return render(request, 'search.html')

# views for goto help page from the sidebar.
def help(request):
    return render(request, 'help.html')