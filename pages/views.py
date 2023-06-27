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
        ## 初始化 variables for render.

        ## STEP 1. get form values input by users.
        ## form values of filter-smaple.
        form_sample_field_dataset_checkbox = request.POST.get('form_sample_field_dataset_checkbox')
        form_sample_field_dataset_condition = request.POST.get('form_sample_field_dataset_condition')
        form_sample_field_dataset_value = request.POST.get('form_sample_field_dataset_value')

        form_sample_field_species_checkbox = request.POST.get('form_sample_field_species_checkbox')
        form_sample_field_species_condition = request.POST.get('form_sample_field_species_condition')
        form_sample_field_species_value = request.POST.get('form_sample_field_species_value')

        form_sample_field_sampleSource_checkbox = request.POST.get('form_sample_field_sampleSource_checkbox')
        form_sample_field_sampleSource_condition = request.POST.get('form_sample_field_sampleSource_condition')
        form_sample_field_sampleSource_value = request.POST.get('form_sample_field_sampleSource_value')

        form_sample_field_treatment_checkbox = request.POST.get('form_sample_field_treatment_checkbox')
        form_sample_field_treatment_condition = request.POST.get('form_sample_field_treatment_condition')
        form_sample_field_treatment_value = request.POST.get('form_sample_field_treatment_value')


        ## form values of filter-gene-marker.
        form_gene_marker_field_dataset_checkbox = request.POST.get('form_gene_marker_field_dataset_checkbox')
        form_gene_marker_field_dataset_condition = request.POST.get('form_gene_marker_field_dataset_condition')
        form_gene_marker_field_dataset_value = request.POST.get('form_gene_marker_field_dataset_value')

        form_gene_marker_field_cluster_checkbox = request.POST.get('form_gene_marker_field_cluster_checkbox')
        form_gene_marker_field_cluster_condition = request.POST.get('form_gene_marker_field_cluster_condition')
        form_gene_marker_field_cluster_value = request.POST.get('form_gene_marker_field_cluster_value')

        form_gene_marker_field_gene_checkbox = request.POST.get('form_gene_marker_field_gene_checkbox')
        form_gene_marker_field_gene_condition = request.POST.get('form_gene_marker_field_gene_condition')
        form_gene_marker_field_gene_value = request.POST.get('form_gene_marker_field_gene_value')

        form_gene_marker_field_log2fc_checkbox = request.POST.get('form_gene_marker_field_log2fc_checkbox')
        form_gene_marker_field_log2fc_condition = request.POST.get('form_gene_marker_field_log2fc_condition')
        form_gene_marker_field_log2fc_value = request.POST.get('form_gene_marker_field_log2fc_value')

        form_gene_marker_field_pct1_checkbox = request.POST.get('form_gene_marker_field_pct1_checkbox')
        form_gene_marker_field_pct1_condition = request.POST.get('form_gene_marker_field_pct1_condition')
        form_gene_marker_field_pct1_value = request.POST.get('form_gene_marker_field_pct1_value')

        form_gene_marker_field_pct2_checkbox = request.POST.get('form_gene_marker_field_pct2_checkbox')
        form_gene_marker_field_pct2_condition = request.POST.get('form_gene_marker_field_pct2_condition')
        form_gene_marker_field_pct2_value = request.POST.get('form_gene_marker_field_pct2_value')

        form_gene_marker_field_padj_checkbox = request.POST.get('form_gene_marker_field_padj_checkbox')
        form_gene_marker_field_padj_condition = request.POST.get('form_gene_marker_field_padj_condition')
        form_gene_marker_field_padj_value = request.POST.get('form_gene_marker_field_padj_value')

        ## form values of filter-gene-corr.
        form_gene_corr_field_dataset_checkbox = request.POST.get('form_gene_corr_field_dataset_checkbox')
        form_gene_corr_field_dataset_condition = request.POST.get('form_gene_corr_field_dataset_condition')
        form_gene_corr_field_dataset_value = request.POST.get('form_gene_corr_field_dataset_value')

        form_gene_corr_field_gene1_checkbox = request.POST.get('form_gene_corr_field_gene1_checkbox')
        form_gene_corr_field_gene1_condition = request.POST.get('form_gene_corr_field_gene1_condition')
        form_gene_corr_field_gene1_value = request.POST.get('form_gene_corr_field_gene1_value')

        form_gene_corr_field_gene2_checkbox = request.POST.get('form_gene_corr_field_gene2_checkbox')
        form_gene_corr_field_gene2_condition = request.POST.get('form_gene_corr_field_gene2_condition')
        form_gene_corr_field_gene2_value = request.POST.get('form_gene_corr_field_gene2_value')

        form_gene_corr_field_corr_checkbox = request.POST.get('form_gene_corr_field_corr_checkbox')
        form_gene_corr_field_corr_condition = request.POST.get('form_gene_corr_field_corr_condition')
        form_gene_corr_field_corr_value = request.POST.get('form_gene_corr_field_corr_value')

        form_gene_corr_field_padj_checkbox = request.POST.get('form_gene_corr_field_padj_checkbox')
        form_gene_corr_field_padj_condition = request.POST.get('form_gene_corr_field_padj_condition')
        form_gene_corr_field_padj_value = request.POST.get('form_gene_corr_field_padj_value')


        ## form values of filter-cell-commu (corresponding to ligand-receptor table).
        form_cell_commu_field_dataset_checkbox = request.POST.get('form_cell_commu_field_dataset_checkbox')
        form_cell_commu_field_dataset_condition = request.POST.get('form_cell_commu_field_dataset_condition')
        form_cell_commu_field_dataset_value = request.POST.get('form_cell_commu_field_dataset_value')

        form_cell_commu_field_source_checkbox = request.POST.get('form_cell_commu_field_source_checkbox')
        form_cell_commu_field_source_condition = request.POST.get('form_cell_commu_field_source_condition')
        form_cell_commu_field_source_value = request.POST.get('form_cell_commu_field_source_value')

        form_cell_commu_field_target_checkbox = request.POST.get('form_cell_commu_field_target_checkbox')
        form_cell_commu_field_target_condition = request.POST.get('form_cell_commu_field_target_condition')
        form_cell_commu_field_target_value = request.POST.get('form_cell_commu_field_target_value')

        form_cell_commu_field_pathway_checkbox = request.POST.get('form_cell_commu_field_pathway_checkbox')
        form_cell_commu_field_pathway_condition = request.POST.get('form_cell_commu_field_pathway_condition')
        form_cell_commu_field_pathway_value = request.POST.get('form_cell_commu_field_pathway_value')

        form_cell_commu_field_ligand_checkbox = request.POST.get('form_cell_commu_field_ligand_checkbox')
        form_cell_commu_field_ligand_condition = request.POST.get('form_cell_commu_field_ligand_condition')
        form_cell_commu_field_ligand_value = request.POST.get('form_cell_commu_field_ligand_value')

        form_cell_commu_field_receptor_checkbox = request.POST.get('form_cell_commu_field_receptor_checkbox')
        form_cell_commu_field_receptor_condition = request.POST.get('form_cell_commu_field_receptor_condition')
        form_cell_commu_field_receptor_value = request.POST.get('form_cell_commu_field_receptor_value')

        form_cell_commu_field_pval_checkbox = request.POST.get('form_cell_commu_field_pval_checkbox')
        form_cell_commu_field_pval_condition = request.POST.get('form_cell_commu_field_pval_condition')
        form_cell_commu_field_pval_value = request.POST.get('form_cell_commu_field_pval_value')

        # STEP 2. 构建查询条件
        ## for form_sample.
        if form_sample_field_dataset_checkbox or form_sample_field_species_checkbox or form_sample_field_sampleSource_checkbox or form_sample_field_treatment_checkbox:
            form_sample_filters = {}
            if form_sample_field_dataset_checkbox:
                form_sample_field_dataset_filter = f'dataset__{form_sample_field_dataset_condition}'
                form_sample_filters[form_sample_field_dataset_filter] = form_sample_field_dataset_value

            if form_sample_field_species_checkbox:
                form_sample_field_species_filter = f'species__{form_sample_field_species_condition}'
                form_sample_filters[form_sample_field_species_filter] = form_sample_field_species_value

            if form_sample_field_sampleSource_checkbox:
                form_sample_field_sampleSource_filter = f'biosample_source__{form_sample_field_sampleSource_condition}'
                form_sample_filters[form_sample_field_sampleSource_filter] = form_sample_field_sampleSource_value

            if form_sample_field_treatment_checkbox:
                form_sample_field_treatment_filter = f'treatment__{form_sample_field_treatment_condition}'
                form_sample_filters[form_sample_field_treatment_filter] = form_sample_field_treatment_value

            # 执行数据库查询
            form_sample_results = Sample.objects.filter(**form_sample_filters)

            # 将查询条件传递给模板进行渲染
            form_sample_context = { 'form_sample_results': form_sample_results, 'form_sample_filters': form_sample_filters }
            return render(request, 'search.html', form_sample_context)

        ## for form_sample.
        elif form_gene_marker_field_dataset_checkbox or form_gene_marker_field_cluster_checkbox or form_gene_marker_field_gene_checkbox or form_gene_marker_field_log2fc_checkbox or \
                form_gene_marker_field_pct1_checkbox or form_gene_marker_field_pct2_checkbox or form_gene_marker_field_padj_checkbox:
            form_gene_marker_filters = {}
            if form_gene_marker_field_dataset_checkbox:
                form_gene_marker_field_dataset_filter = f'dataset__{form_gene_marker_field_dataset_condition}'
                form_gene_marker_filters[form_gene_marker_field_dataset_filter] = form_gene_marker_field_dataset_value

            if form_gene_marker_field_cluster_checkbox:
                form_gene_marker_field_cluster_filter = f'cluster__{form_gene_marker_field_cluster_condition}'
                form_gene_marker_filters[form_gene_marker_field_cluster_filter] = form_gene_marker_field_cluster_value

            if form_gene_marker_field_gene_checkbox:
                form_gene_marker_field_gene_filter = f'gene__{form_gene_marker_field_gene_condition}'
                form_gene_marker_filters[form_gene_marker_field_gene_filter] = form_gene_marker_field_gene_value

            if form_gene_marker_field_log2fc_checkbox:
                form_gene_marker_field_log2fc_filter = f'avg_log2FC__{form_gene_marker_field_log2fc_condition}'
                form_gene_marker_filters[form_gene_marker_field_log2fc_filter] = form_gene_marker_field_log2fc_value

            if form_gene_marker_field_pct1_checkbox:
                form_gene_marker_field_pct1_filter = f'pct1__{form_gene_marker_field_pct1_condition}'
                form_gene_marker_filters[form_gene_marker_field_pct1_filter] = form_gene_marker_field_pct1_value

            if form_gene_marker_field_pct2_checkbox:
                form_gene_marker_field_pct2_filter = f'pct2__{form_gene_marker_field_pct2_condition}'
                form_gene_marker_filters[form_gene_marker_field_pct2_filter] = form_gene_marker_field_pct2_value

            if form_gene_marker_field_padj_checkbox:
                form_gene_marker_field_padj_filter = f'padj__{form_gene_marker_field_padj_condition}'
                form_gene_marker_filters[form_gene_marker_field_padj_filter] = form_gene_marker_field_padj_value

            # 执行数据库查询 and render.
            form_gene_marker_results = Marker_Celltype.objects.filter(**form_gene_marker_filters)
            form_gene_marker_context = {'form_gene_marker_results': form_gene_marker_results, 'form_gene_marker_filters': form_gene_marker_filters}
            return render(request, 'search.html', form_gene_marker_context)

        ## for form_gene_corr.
        elif form_gene_corr_field_dataset_checkbox or form_gene_corr_field_gene1_checkbox or form_gene_corr_field_gene2_checkbox or \
            form_gene_corr_field_corr_checkbox or form_gene_corr_field_padj_checkbox:
            form_gene_corr_filters = {}
            if form_gene_marker_field_dataset_checkbox:
                form_gene_corr_field_dataset_filter = f'dataset__{form_gene_corr_field_dataset_condition}'
                form_gene_corr_filters[form_gene_corr_field_dataset_filter] = form_gene_corr_field_dataset_value

            if form_gene_corr_field_gene1_checkbox:
                form_gene_corr_field_gene1_filter = f'gene1__{form_gene_corr_field_gene1_condition}'
                form_gene_corr_filters[form_gene_corr_field_gene1_filter] = form_gene_corr_field_gene1_value

            if form_gene_corr_field_gene2_checkbox:
                form_gene_corr_field_gene2_filter = f'gene2__{form_gene_corr_field_gene2_condition}'
                form_gene_corr_filters[form_gene_corr_field_gene2_filter] = form_gene_corr_field_gene2_value

            if form_gene_corr_field_corr_checkbox:
                form_gene_corr_field_corr_filter = f'corr__{form_gene_corr_field_corr_condition}'
                form_gene_corr_filters[form_gene_corr_field_corr_filter] = form_gene_corr_field_corr_value

            if form_gene_corr_field_padj_checkbox:
                form_gene_corr_field_padj_filter = f'padj__{form_gene_corr_field_padj_condition}'
                form_gene_corr_filters[form_gene_corr_field_padj_filter] = form_gene_corr_field_padj_value

            # 执行数据库查询 and render.
            form_gene_corr_results = GeneExprCorr.objects.filter(**form_gene_corr_filters)
            form_gene_corr_context = {'form_gene_corr_results': form_gene_corr_results,
                                        'form_gene_corr_filters': form_gene_corr_filters}
            return render(request, 'search.html', form_gene_corr_context)

        ## for form_cell_Commu.
        elif form_cell_commu_field_dataset_checkbox or form_cell_commu_field_source_checkbox or form_cell_commu_field_target_checkbox or \
                form_cell_commu_field_pathway_checkbox or form_cell_commu_field_ligand_checkbox or form_cell_commu_field_receptor_checkbox or \
                form_cell_commu_field_pval_checkbox:
            form_cell_commu_filters = {}
            if form_cell_commu_field_dataset_checkbox:
                form_cell_commu_field_dataset_filter = f'dataset__{form_cell_commu_field_dataset_condition}'
                form_cell_commu_filters[form_cell_commu_field_dataset_filter] = form_cell_commu_field_dataset_value

            if form_cell_commu_field_source_checkbox:
                form_cell_commu_field_source_filter = f'source__{form_cell_commu_field_source_condition}'
                form_cell_commu_filters[form_cell_commu_field_source_filter] = form_cell_commu_field_source_value

            if form_cell_commu_field_target_checkbox:
                form_cell_commu_field_target_filter = f'target__{form_cell_commu_field_target_condition}'
                form_cell_commu_filters[form_cell_commu_field_target_filter] = form_cell_commu_field_target_value

            if form_cell_commu_field_pathway_checkbox:
                form_cell_commu_field_pathway_filter = f'pathway__{form_cell_commu_field_pathway_condition}'
                form_cell_commu_filters[form_cell_commu_field_pathway_filter] = form_cell_commu_field_pathway_value

            if form_cell_commu_field_ligand_checkbox:
                form_cell_commu_field_ligand_filter = f'ligand__{form_cell_commu_field_ligand_condition}'
                form_cell_commu_filters[form_cell_commu_field_ligand_filter] = form_cell_commu_field_ligand_value

            if form_cell_commu_field_receptor_checkbox:
                form_cell_commu_field_receptor_filter = f'receptor__{form_cell_commu_field_receptor_condition}'
                form_cell_commu_filters[form_cell_commu_field_receptor_filter] = form_cell_commu_field_receptor_value

            if form_cell_commu_field_pval_checkbox:
                form_cell_commu_field_pval_filter = f'pval__{form_cell_commu_field_pval_condition}'
                form_cell_commu_filters[form_cell_commu_field_pval_filter] = form_cell_commu_field_pval_value

            # 执行数据库查询 and render.
            form_cell_commu_results = LRpairs.objects.filter(**form_cell_commu_filters)
            form_cell_commu_context = {'form_cell_commu_results': form_cell_commu_results,
                                      'form_cell_commu_filters': form_cell_commu_filters}
            return render(request, 'search.html', form_cell_commu_context)

        else:
            form_sample_filters = None
            form_sample_results = None
            form_gene_marker_filters = None
            form_gene_marker_results = None
            form_gene_corr_filters = None
            form_gene_corr_results = None
            form_cell_commu_filters = None
            form_cell_commu_results = None
            return render(request, 'search.html', {
                'form_sample_filters': form_sample_filters,
                'form_sample_results': form_sample_results,
                'form_gene_marker_filters': form_gene_marker_filters,
                'form_gene_marker_results': form_gene_marker_results,
                'form_gene_corr_filters': form_gene_corr_filters,
                'form_gene_corr_results':form_gene_corr_results,
                'form_cell_commu_filters': form_cell_commu_filters,
                'form_cell_commu_results': form_cell_commu_results
            })
    return render(request, 'search.html')

def analyze_gene_expr(request):
    return render(request, 'analyze-gene-expr.html')

def analyze_cell_marker(request):
    return render(request, 'analyze-cell-marker.html')

def analyze_cell_commu(request):
    return render(request, 'analyze-cell-commu.html')

# views for goto help page from the sidebar.
def help(request):
    return render(request, 'help.html')