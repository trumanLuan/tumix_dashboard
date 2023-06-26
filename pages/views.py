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
from .forms import sampleForm, geneMarkerForm, geneExprForm, cellCommuForm


# Create your views here.
def index(request):
    return render(request, "index.html", {"employees": Employee.objects.all()})

def home(request):
    return render(request, 'index.html')

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
    cell_clust_vis_by_sample = 'static/assets/img/browse_results/' + get_datasetindex + "_vis_tsne_by_sample.svg"


    ## brow_by_celltype, cell stat by cell types.
    singlecell_count_by_celltype_svg = 'static/assets/img/browse_results/' + get_datasetindex + "_singlecell_count_by_celltype.svg"

    ## brow_by_celltype, cell clustering results by cell type.
    cell_clust_vis_by_celltype = 'static/assets/img/browse_results/' + get_datasetindex + "_vis_tsne_by_celltype.svg"

    ## brow_by_ccc, cell_commu_vis.
    cell_commu_vis_svg_path = 'static/assets/img/browse_results/' + get_datasetindex + "_ccc_network_weighted.svg"


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
        'singlecell_count_by_sample_svg_path': singlecell_count_by_sample_svg_path,
        'cell_commu_vis_svg_path': cell_commu_vis_svg_path,
        'cell_clust_vis_by_sample': cell_clust_vis_by_sample,
        'cell_clust_vis_by_celltype': cell_clust_vis_by_celltype,
        'singlecell_count_by_celltype_svg': singlecell_count_by_celltype_svg
    })

def process_search_forms(request):
    if request.method == 'POST':
        field1_checkbox = request.POST.get('field1_checkbox')
        field1_condition = request.POST.get('field1_condition')
        field1_value = request.POST.get('field1_value')

        field2_checkbox = request.POST.get('field2_checkbox')
        field2_condition = request.POST.get('field2_condition')
        field2_value = request.POST.get('field2_value')

        # 构建查询条件
        filters = {}
        if field1_checkbox:
            field1_filter = f'dataset__{field1_condition}'
            filters[field1_filter] = field1_value

        if field2_checkbox:
            field2_filter = f'cluster__{field2_condition}'
            filters[field2_filter] = field2_value

        # 执行数据库查询
        results = Marker_Celltype.objects.filter(**filters)

        # 将查询条件传递给模板进行渲染
        context = {
            'results': results,
            'filters': filters,
        }

        return render(request, 'search.html', context)

    return render(request, 'search.html')


# views for goto help page from the sidebar.
def help(request):
    return render(request, 'help.html')