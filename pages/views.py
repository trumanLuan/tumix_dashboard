import io
import base64

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Employee
from .models import Study
from .models import Marker_Subcluster
from .models import Marker_Celltype
from .models import LRpairs
from .models import SingleCell
from .models import SignalPathway

from django.db.models import Q, Count
from scipy.cluster import hierarchy
import plotly.graph_objects as go
import plotly.express as px

import numpy as np
# import tempfile
import os
import pandas as pd
# import seaborn as sns
# import random
# import string



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
    umi_count_by_sample_svg_path = '/pages/static/assets/img/browse_results/' + get_datasetindex + "_umi_count_by_sample.svg"

    ## brow_by_sample, feature counts of single cells.
    feature_count_by_sample_svg_path = '/pages/static/assets/img/browse_results/' + get_datasetindex + "_feature_count_by_sample.svg"

    ## brow_by_sample,singlecell counts by samples.
    singlecell_count_by_sample_svg_path = '/pages/static/assets/img/browse_results/' + get_datasetindex + "_singlecell_count_by_sample.svg"

    ## brow_by_sample, cell clustering results by sample.
    cell_clust_vis_by_sample = '/pages/static/assets/img/browse_results/' + get_datasetindex + "_vis_tsne_by_sample.svg"


    ## brow_by_celltype, cell stat by cell types.
    singlecell_count_by_celltype_svg = '/pages/static/assets/img/browse_results/' + get_datasetindex + "_singlecell_count_by_celltype.svg"

    ## brow_by_celltype, cell clustering results by cell type.
    cell_clust_vis_by_celltype = '/pages/static/assets/img/browse_results/' + get_datasetindex + "_vis_tsne_by_celltype.svg"

    ## brow_by_ccc, cell_commu_vis.
    cell_commu_vis_svg_path = '/pages/static/assets/img/browse_results/' + get_datasetindex + "_ccc_network_weighted.svg"


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

def analyze_gene_expr_single(request):
    return render(request, 'analyze-gene-expr-single.html')

def analyze_gene_expr_cross(request):
    return render(request, 'analyze-gene-expr-cross.html')


def analyze_cell_marker_single(request):
    if request.method == 'POST':
        ## STEP 1. get form values input by users.
        ## form values of tab1.
        tab1_field_queryTable_checkbox = request.POST.get('tab1_field_queryTable_checkbox')
        tab1_field_queryTable_condition = request.POST.get('tab1_field_queryTable_condition')

        tab1_field_dataset_checkbox = request.POST.get('tab1_field_dataset_checkbox')
        tab1_field_dataset_condition = request.POST.get('tab1_field_dataset_condition')
        tab1_field_dataset_value = request.POST.get('tab1_field_dataset_value')

        tab1_field_log2fc_checkbox = request.POST.get('tab1_field_log2fc_checkbox')
        tab1_field_log2fc_condition = request.POST.get('tab1_field_log2fc_condition')
        tab1_field_log2fc_value = request.POST.get('tab1_field_log2fc_value')

        tab1_field_pct1_checkbox = request.POST.get('tab1_field_pct1_checkbox')
        tab1_field_pct1_condition = request.POST.get('tab1_field_pct1_condition')
        tab1_field_pct1_value = request.POST.get('tab1_field_pct1_value')

        tab1_field_pct2_checkbox = request.POST.get('tab1_field_pct2_checkbox')
        tab1_field_pct2_condition = request.POST.get('tab1_field_pct2_condition')
        tab1_field_pct2_value = request.POST.get('tab1_field_pct2_value')

        tab1_field_padj_checkbox = request.POST.get('tab1_field_padj_checkbox')
        tab1_field_padj_condition = request.POST.get('tab1_field_padj_condition')
        tab1_field_padj_value = request.POST.get('tab1_field_padj_value')

       # STEP 2. 构建查询条件
        ## for form in tab1.
        if tab1_field_queryTable_checkbox != 'on':
            error_message = 'One or more required fields are missing. Please fill the Query Form.'
            return render(request, 'analyze-cell-marker-cross.html', {'error_message': error_message})

        elif tab1_field_dataset_checkbox != 'on' or tab1_field_dataset_value == '':
            error_message = 'One or more required fields are missing. Please fill the Query Form.'
            return render(request, 'analyze-cell-marker-cross.html', {'error_message': error_message})

        elif tab1_field_padj_checkbox != 'on' or tab1_field_padj_value == '':
            error_message = 'One or more required fields are missing.Please fill the Query Form.'
            return render(request, 'analyze-cell-marker-cross.html', {'error_message': error_message})

        elif tab1_field_queryTable_checkbox and tab1_field_dataset_checkbox and tab1_field_padj_checkbox and \
                tab1_field_dataset_value is not None and tab1_field_padj_value is not None:
            # if tab1_field_dataset_value and tab1_field_padj_value:
            tab1_filters = {}
            if tab1_field_dataset_checkbox:
                tab1_field_dataset_filter = f'dataset__{tab1_field_dataset_condition}'
                tab1_filters[tab1_field_dataset_filter] = tab1_field_dataset_value

            if tab1_field_log2fc_checkbox:
                tab1_field_log2fc_filter = f'avg_log2FC__{tab1_field_log2fc_condition}'
                tab1_filters[tab1_field_log2fc_filter] = tab1_field_log2fc_value

            if tab1_field_pct1_checkbox:
                tab1_field_pct1_filter = f'pct1__{tab1_field_pct1_condition}'
                tab1_filters[tab1_field_pct1_filter] = tab1_field_pct1_value

            if tab1_field_pct2_checkbox:
                tab1_field_pct2_filter = f'pct2__{tab1_field_pct2_condition}'
                tab1_filters[tab1_field_pct2_filter] = tab1_field_pct2_value

            if tab1_field_padj_checkbox:
                tab1_field_padj_filter = f'padj__{tab1_field_padj_condition}'
                tab1_filters[tab1_field_padj_filter] = tab1_field_padj_value

            # 数据库查询 and render.
            if tab1_field_queryTable_condition == 'major':
                tab1_filter_results = Marker_Celltype.objects.filter(**tab1_filters)
            elif tab1_field_queryTable_condition == 'minor':
                tab1_filter_results = Marker_Subcluster.objects.filter(**tab1_filters)

            # 数据库查询结果数据集的统计分析。
            total_records = tab1_filter_results.count()
            dataset_distinct_values = tab1_filter_results.values_list('dataset', flat=True).distinct()
            num_distinct_values_of_dataset = len(dataset_distinct_values)

            if num_distinct_values_of_dataset > 1:
                error_message = 'This analysis only allows for 1 dataset. You are attempting to extract multiple sets of data.'
                return render(request, 'analyze-cell-marker-cross.html', {'error_message': error_message})

            cluster_distinct_values = tab1_filter_results.values_list('cluster', flat=True).distinct()
            num_distinct_values_of_cluster = len(cluster_distinct_values)

            gene_distinct_values = tab1_filter_results.values_list('gene', flat=True).distinct()
            num_distinct_values_of_gene = len(gene_distinct_values)

            pct1_data = tab1_filter_results.values_list('pct1', flat=True)
            pct1_data_array = np.array(list(pct1_data))
            pct1_summary_stats = f"pct1 range:\n"
            pct1_summary_stats += f"-- mean: {round(np.mean(pct1_data_array),2)}\n"
            pct1_summary_stats += f"-- median: {round(np.median(pct1_data_array),2)}\n"
            pct1_summary_stats += f"-- min: {round(np.min(pct1_data_array),2)}\n"
            pct1_summary_stats += f"-- max: {round(np.max(pct1_data_array),2)}"

            pct2_data = tab1_filter_results.values_list('pct2', flat=True)
            pct2_data_array = np.array(list(pct2_data))
            pct2_summary_stats = f"pct2 range:\n"
            pct2_summary_stats += f"-- mean: {round(np.mean(pct2_data_array), 2)}\n"
            pct2_summary_stats += f"-- median: {round(np.median(pct2_data_array),2)}\n"
            pct2_summary_stats += f"-- min: {round(np.min(pct2_data_array),2)}\n"
            pct2_summary_stats += f"-- max: {round(np.max(pct2_data_array),2)}"

            ## 构造数据
            df_data = list(tab1_filter_results.values('cluster', 'gene', 'avg_log2FC') )
            df = pd.DataFrame(df_data)
            # Aggregate duplicate values by taking the mean
            df_agg = df.groupby(['gene', 'cluster'])['avg_log2FC'].mean().reset_index()
            df_wide = df_agg.pivot(index='gene', columns='cluster', values='avg_log2FC').fillna(0)
            df_wide = df_wide.astype(float)

            ## two-way clustering.
            row_clusters = hierarchy.linkage(df_wide.values, method='average', metric='euclidean')
            column_clusters = hierarchy.linkage(df_wide.values.T, method='average', metric='euclidean')
            # 获取行和列的排序索引
            row_order = hierarchy.leaves_list(row_clusters)
            column_order = hierarchy.leaves_list(column_clusters)

            # 根据排序索引重新排列数据框
            df_reordered = df_wide.iloc[row_order, column_order]

            # 构造热图数据
            heat_data = df_reordered.values.tolist()
            x_labels = df_reordered.columns.tolist()
            y_labels = df_reordered.index.tolist()

            # 绘制交互式热图
            fig = go.Figure(data=go.Heatmap(
                z=heat_data,
                x=x_labels,
                y=y_labels
            ))

            # 设置图表布局
            fig.update_layout(
                title={
                    'text': 'Interactive Heatmap',
                    'x': 0.5,  # 设置标题居中
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                xaxis_title='Cell Clusters',
                yaxis_title='Gene Markers',
                width=1000,  # 设置宽度为 800 像素
                height=1000  # 设置高度为 600 像素
            )

            # 将图表渲染到网页
            plot_div = fig.to_html(full_html=False)

            result_data = {
                'num_distinct_values_of_dataset': num_distinct_values_of_dataset,
                'dataset_distinct_values': dataset_distinct_values,
                'total_records': total_records,
                'num_distinct_values_of_cluster': num_distinct_values_of_cluster,
                'num_distinct_values_of_gene': num_distinct_values_of_gene,
                'pct1_summary_stats': pct1_summary_stats,
                'pct2_summary_stats': pct2_summary_stats,
                'filter_results': tab1_filter_results,
                'filters': tab1_filters,
                'plot_url': plot_div
            }
            return render(request, 'analyze-cell-marker-single.html', result_data)

        else:
            error_message = 'Please fill the Query Form.'
            print(error_message)
            return render(request, 'analyze-cell-marker-single.html', {'error_message': error_message})

    return render(request, 'analyze-cell-marker-single.html')

def analyze_cell_marker_cross(request):
    if request.method == 'POST':
        tab2_field_querytable_checkbox = request.POST.get('tab2_field_querytable_checkbox')
        tab2_field_querytable_condition = request.POST.get('tab2_field_querytable_condition')

        tab2_field_dataset_checkbox = request.POST.get('tab2_field_dataset_checkbox')
        tab2_field_dataset_condition = request.POST.get('tab2_field_dataset_condition')
        tab2_field_dataset_value = request.POST.get('tab2_field_dataset_value')

        tab2_field_cluster_checkbox = request.POST.get('tab2_field_cluster_checkbox')
        tab2_field_cluster_condition = request.POST.get('tab2_field_cluster_condition')
        tab2_field_cluster_value = request.POST.get('tab2_field_cluster_value')

        tab2_field_gene_checkbox = request.POST.get('tab2_field_gene_checkbox')
        tab2_field_gene_condition = request.POST.get('tab2_field_gene_condition')
        tab2_field_gene_value = request.POST.get('tab2_field_gene_value')

        tab2_field_log2fc_checkbox = request.POST.get('tab2_field_log2fc_checkbox')
        tab2_field_log2fc_condition = request.POST.get('tab2_field_log2fc_condition')
        tab2_field_log2fc_value = request.POST.get('tab2_field_log2fc_value')

        tab2_field_pct1_checkbox = request.POST.get('tab2_field_pct1_checkbox')
        tab2_field_pct1_condition = request.POST.get('tab2_field_pct1_condition')
        tab2_field_pct1_value = request.POST.get('tab2_field_pct1_value')

        tab2_field_pct2_checkbox = request.POST.get('tab2_field_pct2_checkbox')
        tab2_field_pct2_condition = request.POST.get('tab2_field_pct2_condition')
        tab2_field_pct2_value = request.POST.get('tab2_field_pct2_value')

        tab2_field_padj_checkbox = request.POST.get('tab2_field_padj_checkbox')
        tab2_field_padj_condition = request.POST.get('tab2_field_padj_condition')
        tab2_field_padj_value = request.POST.get('tab2_field_padj_value')

        # STEP 2. 构建查询条件,使用字符串插值法构建，格式为 f'dataset__{tab2_field_dataset_condition}'
        if tab2_field_querytable_checkbox != 'on':
            error_message = 'One or more required fields are missing. Please fill the Query Form.'
            return render(request, 'analyze-cell-marker-cross.html', {'error_message': error_message})

        elif tab2_field_dataset_checkbox != 'on' or tab2_field_dataset_value == '':
            error_message = 'One or more required fields are missing. Please fill the Query Form.'
            return render(request, 'analyze-cell-marker-cross.html', {'error_message': error_message})

        elif tab2_field_padj_checkbox != 'on' or tab2_field_padj_value == '':
            error_message = 'One or more required fields are missing. Please fill the Query Form.'
            return render(request, 'analyze-cell-marker-cross.html', {'error_message': error_message})

        elif tab2_field_querytable_checkbox and tab2_field_dataset_checkbox and tab2_field_padj_checkbox and \
                tab2_field_dataset_value is not None and tab2_field_padj_value is not None:

            filter_dataset = {} # if multiple datasets input.
            filter_cluster = {} # if multiple cell type input.
            filter_gene = {} # if multiple genes input.
            filter_others = {}
            filter_dataset_combined = Q()
            filter_cluster_combined = Q()
            filter_gene_combined = Q()
            filter_others_combined = Q()

            if tab2_field_dataset_checkbox:
                split_words = tab2_field_dataset_value.split(';') # split the words into single word;
                for single_word in split_words:
                    single_word_ok = single_word.strip() # Remove spaces at both ends of the valid characters
                    filter_now = f'dataset__{tab2_field_dataset_condition}'
                    filter_dataset[filter_now] = single_word_ok
                    filter_dataset_combined |= Q(**{filter_now: single_word_ok})

            if tab2_field_cluster_checkbox:
                split_words = tab2_field_cluster_value.split(';') # split the words into single word;
                for single_word in split_words:
                    single_word_ok = single_word.strip() # Remove spaces at both ends of the valid characters
                    filter_now = f'cluster__{tab2_field_cluster_condition}'
                    filter_cluster[filter_now] = single_word_ok
                    filter_cluster_combined |= Q(**{filter_now: single_word_ok})
                # tab2_field_cluster_filter = f'cluster__{tab2_field_cluster_condition}'
                # tab2_filters[tab2_field_cluster_filter] = tab2_field_cluster_value

            if tab2_field_gene_checkbox:
                split_words = tab2_field_gene_value.split(';')  # split the words into single word;
                for single_word in split_words:
                    single_word_ok = single_word.strip()  # Remove spaces at both ends of the valid characters
                    filter_now = f'gene__{tab2_field_cluster_condition}'
                    filter_gene[filter_now] = single_word_ok
                    filter_gene_combined |= Q(**{filter_now: single_word_ok})
                # tab2_field_gene_filter = f'gene__{tab2_field_gene_condition}'
                # tab2_filters[tab2_field_gene_filter] = tab2_field_gene_value


            if tab2_field_log2fc_checkbox:
                tab2_field_log2fc_filter = f'avg_log2FC__{tab2_field_log2fc_condition}'
                filter_others[tab2_field_log2fc_filter] = tab2_field_log2fc_value

            if tab2_field_pct1_checkbox:
                tab2_field_pct1_filter = f'pct1__{tab2_field_pct1_condition}'
                filter_others[tab2_field_pct1_filter] = tab2_field_pct1_value

            if tab2_field_pct2_checkbox:
                tab2_field_pct2_filter = f'pct2__{tab2_field_pct2_condition}'
                filter_others[tab2_field_pct2_filter] = tab2_field_pct2_value

            if tab2_field_padj_checkbox:
                tab2_field_padj_filter = f'padj__{tab2_field_padj_condition}'
                filter_others[tab2_field_padj_filter] = tab2_field_padj_value

            if filter_others:
                for key, value in filter_others.items():
                    filter_others_combined &= Q(**{key: value})

            combined_filters = filter_dataset_combined & filter_cluster_combined & filter_gene_combined & filter_others_combined

            # 数据库查询 and render.
            if tab2_field_querytable_condition == 'major':
                # tab2_filter_results = Marker_Celltype.objects.filter(**tab2_filters)
                tab2_filter_results = Marker_Celltype.objects.filter(combined_filters)
            elif tab2_field_querytable_condition == 'minor':
                # tab2_filter_results = Marker_Subcluster.objects.filter(**tab2_filters)
                tab2_filter_results = Marker_Subcluster.objects.filter(combined_filters)

            # 数据库查询结果数据集的统计分析。
            tab2_total_records = tab2_filter_results.count()
            tab2_dataset_distinct_values = tab2_filter_results.values_list('dataset', flat=True).distinct()
            tab2_num_distinct_values_of_dataset = len(tab2_dataset_distinct_values)

            tab2_cluster_distinct_values = tab2_filter_results.values_list('cluster', flat=True).distinct()
            tab2_num_distinct_values_of_cluster = len(tab2_cluster_distinct_values)

            tab2_gene_distinct_values = tab2_filter_results.values_list('gene', flat=True).distinct()
            tab2_num_distinct_values_of_gene = len(tab2_gene_distinct_values)

            tab2_pct1_data = tab2_filter_results.values_list('pct1', flat=True)
            tab2_pct1_data_array = np.array(list(tab2_pct1_data))
            tab2_pct1_summary_stats = f"pct1 range:\n"
            tab2_pct1_summary_stats += f"-- mean: {round(np.mean(tab2_pct1_data_array), 2)}\n"
            tab2_pct1_summary_stats += f"-- median: {round(np.median(tab2_pct1_data_array), 2)}\n"
            tab2_pct1_summary_stats += f"-- min: {round(np.min(tab2_pct1_data_array), 2)}\n"
            tab2_pct1_summary_stats += f"-- max: {round(np.max(tab2_pct1_data_array), 2)}"

            tab2_pct2_data = tab2_filter_results.values_list('pct2', flat=True)
            tab2_pct2_data_array = np.array(list(tab2_pct2_data))
            tab2_pct2_summary_stats = f"pct2 range:\n"
            tab2_pct2_summary_stats += f"-- mean: {round(np.mean(tab2_pct2_data_array), 2)}\n"
            tab2_pct2_summary_stats += f"-- median: {round(np.median(tab2_pct2_data_array), 2)}\n"
            tab2_pct2_summary_stats += f"-- min: {round(np.min(tab2_pct2_data_array), 2)}\n"
            tab2_pct2_summary_stats += f"-- max: {round(np.max(tab2_pct2_data_array), 2)}"


            ## plots - global map between gene markers and cell types
            ## 构造数据
            if tab2_num_distinct_values_of_cluster > 1:
                df_data = list(tab2_filter_results.values('cluster', 'gene', 'avg_log2FC'))
                df = pd.DataFrame(df_data)
                # Aggregate duplicate values by taking the mean
                df_agg = df.groupby(['gene', 'cluster'])['avg_log2FC'].mean().reset_index()
                df_wide = df_agg.pivot(index='gene', columns='cluster', values='avg_log2FC').fillna(0) # convert long-format table to wide-format table.
                df_wide = df_wide.astype(float)

                ## two-way clustering.
                row_clusters = hierarchy.linkage(df_wide.values, method='average', metric='euclidean')
                column_clusters = hierarchy.linkage(df_wide.values.T, method='average', metric='euclidean')
                # 获取行和列的排序索引
                row_order = hierarchy.leaves_list(row_clusters)
                column_order = hierarchy.leaves_list(column_clusters)

                # 根据排序索引重新排列数据框
                df_reordered = df_wide.iloc[row_order, column_order]

                # 构造热图数据
                heat_data = df_reordered.values.tolist()
                x_labels = df_reordered.columns.tolist()
                y_labels = df_reordered.index.tolist()

                # 绘制交互式热图
                fig = go.Figure(data=go.Heatmap(
                    z=heat_data,
                    x=x_labels,
                    y=y_labels
                ))

                # 设置图表布局
                fig.update_layout(
                    title={
                        'text': 'Interactive Heatmap',
                        'x': 0.5,  # 设置标题居中
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    xaxis_title='Cell Clusters',
                    yaxis_title='Gene Markers',
                    width=1000,  # 设置宽度为 800 像素
                    height=1000  # 设置高度为 600 像素
                )

                # 将图表渲染到网页
                global_plot_div = fig.to_html(full_html=False)

            else:
                global_plot_div = ""

            ## plots - comparing gene markers of selected cell type between datasets.
            ## 构建数据
            if tab2_num_distinct_values_of_cluster == 1: # This analysis is only applicable to a single cell type.
                df_data = list(tab2_filter_results.values('gene', 'dataset', 'avg_log2FC'))
                df = pd.DataFrame(df_data)
                # Aggregate duplicate values by taking the mean
                df_agg = df.groupby(['gene', 'dataset'])['avg_log2FC'].mean().reset_index()
                df_wide = df_agg.pivot(index='gene', columns='dataset', values='avg_log2FC').fillna(0)  # convert long-format table to wide-format table.
                df_wide = df_wide.astype(float)

                ## two-way clustering.
                row_clusters = hierarchy.linkage(df_wide.values, method='average', metric='euclidean')
                column_clusters = hierarchy.linkage(df_wide.values.T, method='average', metric='euclidean')
                # 获取行和列的排序索引
                row_order = hierarchy.leaves_list(row_clusters)
                column_order = hierarchy.leaves_list(column_clusters)

                # 根据排序索引重新排列数据框
                df_reordered = df_wide.iloc[row_order, column_order]

                # 构造热图数据
                heat_data = df_reordered.values.tolist()
                x_labels = df_reordered.columns.tolist()
                y_labels = df_reordered.index.tolist()

                # 绘制交互式热图
                fig = go.Figure(data=go.Heatmap(
                    z=heat_data,
                    x=x_labels,
                    y=y_labels
                ))

                # 设置图表布局
                fig.update_layout(
                    title={
                        'text': 'Interactive Heatmap',
                        'x': 0.5,  # 设置标题居中
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    xaxis_title='Dataset',
                    yaxis_title='Gene Markers',
                    width=1000,  # 设置宽度为 800 像素
                    height=1000  # 设置高度为 600 像素
                )

                compr_plot_div = fig.to_html(full_html=False)

                ## for ploting ranked genes according to frequency
                gene_count_df = tab2_filter_results.values('gene').annotate(count=Count('gene')).order_by('-count')
                genes = [item['gene'] for item in gene_count_df]
                gene_freq = [item['count'] / tab2_num_distinct_values_of_dataset for item in gene_count_df]

                    # 创建ranked dot plot
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=genes, y=gene_freq, mode='markers', marker=dict(size=8)))
                    # 自定义图形的布局和样式
                fig.update_layout(title={
                                        'text': 'Ranked Dot Plot',
                                        'x': 0.5,  # 设置标题居中
                                        'xanchor': 'center',
                                        'yanchor': 'top'
                                    },
                                  xaxis_title="Ranked genes",
                                  yaxis_title='Normalized Frequency <br> Gene Counts / dataset counts')
                gene_rank_plot_div = fig.to_html(full_html=False)

            else:
                compr_plot_div = ""
                gene_rank_plot_div = ""

            tab2_context = {
                'tab2_num_distinct_values_of_dataset': tab2_num_distinct_values_of_dataset,
                'tab2_dataset_distinct_values': tab2_dataset_distinct_values,
                'tab2_total_records': tab2_total_records,
                'tab2_num_distinct_values_of_cluster': tab2_num_distinct_values_of_cluster,
                'tab2_num_distinct_values_of_gene': tab2_num_distinct_values_of_gene,
                'tab2_pct1_summary_stats': tab2_pct1_summary_stats,
                'tab2_pct2_summary_stats': tab2_pct2_summary_stats,

                # for print form_data in html.
                'tab2_filter_results': tab2_filter_results, # data tables extracted from database
                'tab2_filters': combined_filters, # for print current inputs
                'filter_dataset_checkbox': tab2_field_dataset_checkbox,
                # 'filter_dataset_condition': tab2_field_dataset_condition,
                'filter_dataset_value': tab2_field_dataset_value,

                'filter_querytable_checkbox': tab2_field_querytable_checkbox,
                'filter_querytable_condition': tab2_field_querytable_condition,

                'filter_cluster_checkbox': tab2_field_cluster_checkbox,
                # 'filter_cluster_condition': tab2_field_cluster_condition,
                'filter_cluster_value': tab2_field_cluster_value,

                'filter_gene_checkbox': tab2_field_gene_checkbox,
                # 'filter_gene_condition': tab2_field_gene_condition,
                'filter_gene_value': tab2_field_gene_value,

                'filter_fc_checkbox': tab2_field_log2fc_checkbox,
                'filter_fc_condition': tab2_field_log2fc_condition,
                'filter_fc_value': tab2_field_log2fc_value,

                'filter_pct1_checkbox': tab2_field_pct1_checkbox,
                'filter_pct1_condition': tab2_field_pct1_condition,
                'filter_pct1_value': tab2_field_pct1_value,

                'filter_pct2_checkbox': tab2_field_pct2_checkbox,
                'filter_pct2_condition': tab2_field_pct2_condition,
                'filter_pct2_value': tab2_field_pct2_value,

                'filter_padj_checkbox': tab2_field_padj_checkbox,
                'filter_padj_condition': tab2_field_padj_condition,
                'filter_padj_value': tab2_field_padj_value,

                # for plots region in html.
                'global_plot_url': global_plot_div, # for global map between genes and cell types
                'compr_plot_url': compr_plot_div, # for compar gene markers of selected cell type between datasets.
                'gene_rank_plot_div': gene_rank_plot_div
            }

            # print('num_distinct_values_of_dataset', tab2_num_distinct_values_of_dataset)
            return render(request, 'analyze-cell-marker-cross.html', tab2_context)

    return render(request, 'analyze-cell-marker-cross.html')

def analyze_cell_commu_singledataset(request):
    if request.method == 'POST':
        # 处理表单提交：判断当前提交的是哪个表单
        option = request.POST.get('option', None)
        if option == 'option1':
            # f_dataset_check = request.POST.get('f_dataset_checkbox', None)
            f_dataset_value = request.POST.get('f_dataset_value', None)
            # f_pathway_check = request.POST.get('f_pathway_checkbox', None)
            f_pathway_value = request.POST.get('f_pathway_value', None)
            # f_source_check = request.POST.get('f_source_checkbox', None)
            f_source_value = request.POST.get('f_source_value', None)
            # f_target_check = request.POST.get('f_target_checkbox', None)
            f_target_value = request.POST.get('f_target_value', None)
            # f_ligand_check = request.POST.get('f_ligand_checkbox', None)
            f_ligand_value = request.POST.get('f_ligand_value', None)
            # f_receptor_check = request.POST.get('f_receptor_checkbox', None)
            f_receptor_value = request.POST.get('f_receptor_value', None)
            # f_pval_check = request.POST.get('f_pval_checkbox', None)
            f_pval_value = request.POST.get('f_pval_value', None)

            if f_dataset_value == '' and f_pathway_value == '' and f_source_value == '' and f_target_value == ''\
                and f_ligand_value == '' and f_receptor_value == '' and f_pval_value == '':
                error_message = "The form is empty. Please fill out the form."
                result = {'error_message': error_message}
                return render(request, 'analyze-cell-commu-single.html', result)
            # //

            filters = {}
            if f_dataset_value == '':
                error_message = "The form is empty. Please fill out the form."
                result = {'error_message': error_message}
                return render(request, 'analyze-cell-commu-single.html', result)

            elif f_dataset_value:
                f_dataset_filter = f'dataset__contains'
                filters[f_dataset_filter] = f_dataset_value

                if f_pathway_value:
                    f_pathway_filter = f'pathway__contains'
                    filters[f_pathway_filter] = f_pathway_value

                if f_source_value:
                    f_source_filter = f'source__contains'
                    filters[f_source_filter] = f_source_value

                if f_target_value:
                    f_target_filter = f'target__contains'
                    filters[f_target_filter] = f_target_value

                if f_ligand_value:
                    f_ligand_filter = f'ligand__contains'
                    filters[f_ligand_filter] = f_ligand_value

                if f_receptor_value:
                    f_receptor_filter = f'receptor__contains'
                    filters[f_receptor_filter] = f_receptor_value

                if f_pval_value:
                    f_pval_filter = f'pval__lt'
                    filters[f_pval_filter] = f_pval_value
                else:
                    f_pval_filter = f'pval__lt'
                    filters[f_pval_filter] = 0.05

                filter_results = LRpairs.objects.filter(**filters)

                # ---------------------------------
                ## 数据库查询结果数据集的统计分析。
                row_count = filter_results.count() # total counts of rows.
                dataset_uniq_value = filter_results.values_list('dataset', flat=True).distinct()
                n_dataset = len(dataset_uniq_value)

                if n_dataset > 1:
                    error_message = 'This analysis only allows for 1 dataset. You are attempting to extract multiple sets of data.'
                    return render(request, 'analyze-cell-commu-single.html', {'error_message': error_message})

                # how many cell types in source and target cells.
                ## number of minor cell types.
                source_minor_uniq_value = filter_results.values_list('source', flat=True).distinct()
                target_minor_uniq_value = filter_results.values_list('target', flat=True).distinct()
                n_minor_source = len(source_minor_uniq_value)
                n_minor_target = len(target_minor_uniq_value)

                ## number of major cell types.
                source_split_values = [i.split('_')[1] for i in source_minor_uniq_value]
                source_split_uniq = list(set(source_split_values))
                n_major_source = len(source_split_uniq)

                target_split_values = [i.split('_')[1] for i in target_minor_uniq_value]
                target_split_uniq = list(set(target_split_values))
                n_major_target = len(target_split_uniq)

                # how many signal pathways.
                pathway_uniq_value = filter_results.values_list('pathway', flat=True).distinct()
                n_pathway = len(pathway_uniq_value)

                # how many ligand-receptor paires.
                n_uniq_LR = filter_results.values('ligand', 'receptor').distinct().count()

                # how many source-target paires.
                n_uniq_source_target = filter_results.values('source', 'target').distinct().count()


                # ---------------------------------
                # plots
                ## cell-cell interaction measured by probability of LR pairs.
                ## construct data objects for plotting.
                df_data = list(filter_results.values('source', 'target', 'ligand', 'receptor', 'prob'))
                df = pd.DataFrame(df_data)

                df['cell_pair'] = df['source'] + '=>' + df['target']
                df['LR_pair'] = df['ligand'] + ':' + df['receptor']
                df_plt = pd.pivot_table(df, values='prob', index='LR_pair', columns='cell_pair').fillna(0)

                ## two-way clustering in heatmap
                row_clusters = hierarchy.linkage(df_plt.values, method='average', metric='euclidean')
                column_clusters = hierarchy.linkage(df_plt.values.T, method='average', metric='euclidean')
                # 获取行和列的排序索引
                row_order = hierarchy.leaves_list(row_clusters)
                column_order = hierarchy.leaves_list(column_clusters)

                # 根据排序索引重新排列数据框
                df_reordered = df_plt.iloc[row_order, column_order]

                # 构造热图数据
                heat_data = df_reordered.values.tolist()
                x_labels = df_reordered.columns.tolist()
                y_labels = df_reordered.index.tolist()

                # 绘制交互式热图
                fig = go.Figure(data=go.Heatmap(
                    z=heat_data,
                    x=x_labels,
                    y=y_labels
                ))

                # 设置图表布局
                fig.update_layout(
                    title={
                        'text': 'Interactive Heatmap',
                        'x': 0.5,  # 设置标题居中
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    xaxis_title='Source=>Target cell interaction',
                    yaxis_title='Ligand-receptor pairs',
                    width=1000,  # 设置宽度为 800 像素
                    height=1000  # 设置高度为 600 像素
                )

                # 将图表渲染到网页
                ccc_prob_plot_div = fig.to_html(full_html=False)

                # 构建render字典
                result = {
                    'total_records': row_count,
                    'n_dataset': n_dataset,
                    'n_minor_source': n_minor_source,
                    'n_minor_target': n_minor_target,
                    'n_major_source': n_major_source,
                    'n_major_target': n_major_target,
                    'n_uniq_source_target': n_uniq_source_target,
                    "n_pathway": n_pathway,
                    'n_uniq_LR': n_uniq_LR,
                    'filters':filters,
                    'filter_results': filter_results,
                    'plot_url1': ccc_prob_plot_div
                }
                return render(request, 'analyze-cell-commu-single.html', result)

        elif option == 'option2':
            # f_dataset_check = request.POST.get('f2_dataset_checkbox', None)
            f_dataset_value = request.POST.get('f2_dataset_value', None)
            # f_pathway_check = request.POST.get('f2_pathway_checkbox', None)
            f_pathway_value = request.POST.get('f2_pathway_value', None)
            # f_source_check = request.POST.get('f2_source_checkbox', None)
            f_source_value = request.POST.get('f2_source_value', None)
            # f_target_check = request.POST.get('f2_target_checkbox', None)
            f_target_value = request.POST.get('f2_target_value', None)
            # f_pval_check = request.POST.get('f2_pval_checkbox', None)
            f_pval_value = request.POST.get('f2_pval_value', None)

            if f_dataset_value == '' and f_pathway_value == "" and f_source_value == ''\
                and f_target_value == '' and f_pval_value == '':
                error_message = "The form is empty. Please fill out the form."
                result = {'error_message': error_message}
                return render(request, 'analyze-cell-commu-single.html', result)

            elif f_dataset_value == '':
                error_message = "Dataset field in the form is required. Please fill out the form."
                result = {'error_message': error_message}
                return render(request, 'analyze-cell-commu-single.html', result)

            elif f_dataset_value:
                filters = {} # construct filters.

                f_dataset_filter = f'dataset__contains'
                filters[f_dataset_filter] = f_dataset_value

                if f_pathway_value:
                    f_pathway_filter = f'pathway__contains'
                    filters[f_pathway_filter] = f_pathway_value

                if f_source_value:
                    f_source_filter = f'source__contains'
                    filters[f_source_filter] = f_source_value

                if f_target_value:
                    f_target_filter = f'target__contains'
                    filters[f_target_filter] = f_target_value

                if f_pval_value:
                    f_pval_filter = f'pval__lt'
                    filters[f_pval_filter] = f_pval_value
                else:
                    f_pval_filter = f'pval__lt'
                    filters[f_pval_filter] = 0.05

                filter_results = SignalPathway.objects.filter(**filters)

                # ---------------------------------
                ## 数据库查询结果数据集的统计分析。
                row_count = filter_results.count()  # total counts of rows.
                dataset_uniq_value = filter_results.values_list('dataset', flat=True).distinct()
                n_dataset = len(dataset_uniq_value)

                if n_dataset > 1:
                    error_message = 'This analysis only allows for 1 dataset. You are attempting to extract multiple sets of data.'
                    return render(request, 'analyze-cell-commu-single.html', {'error_message': error_message})

                # how many cell types in source and target cells.
                ## number of minor cell types.
                source_minor_uniq_value = filter_results.values_list('source', flat=True).distinct()
                target_minor_uniq_value = filter_results.values_list('target', flat=True).distinct()
                n_minor_source = len(source_minor_uniq_value)
                n_minor_target = len(target_minor_uniq_value)

                ## number of major cell types.
                source_split_values = [i.split('_')[1] for i in source_minor_uniq_value]
                source_split_uniq = list(set(source_split_values))
                n_major_source = len(source_split_uniq)

                target_split_values = [i.split('_')[1] for i in target_minor_uniq_value]
                target_split_uniq = list(set(target_split_values))
                n_major_target = len(target_split_uniq)

                # how many signal pathways.
                pathway_uniq_value = filter_results.values_list('pathway', flat=True).distinct()
                n_pathway = len(pathway_uniq_value)
                #
                # # how many ligand-receptor paires.
                # n_uniq_LR = filter_results.values('ligand', 'receptor').distinct().count()

                # how many source-target paires.
                n_uniq_source_target = filter_results.values('source', 'target').distinct().count()

                # ---------------------------------
                # plots
                ## cell-cell interaction measured by probability of LR pairs.
                ## construct data objects for plotting.
                df_data = list(filter_results.values('source', 'target', 'pathway', 'prob'))
                df = pd.DataFrame(df_data)

                df['cell_pair'] = df['source'] + '=>' + df['target']
                df_plt = pd.pivot_table(df, values='prob', index='pathway', columns='cell_pair').fillna(0)

                ## two-way clustering in heatmap
                row_clusters = hierarchy.linkage(df_plt.values, method='average', metric='euclidean')
                column_clusters = hierarchy.linkage(df_plt.values.T, method='average', metric='euclidean')
                # 获取行和列的排序索引
                row_order = hierarchy.leaves_list(row_clusters)
                column_order = hierarchy.leaves_list(column_clusters)

                # 根据排序索引重新排列数据框
                df_reordered = df_plt.iloc[row_order, column_order]

                # 构造热图数据
                heat_data = df_reordered.values.tolist()
                x_labels = df_reordered.columns.tolist()
                y_labels = df_reordered.index.tolist()

                # 绘制交互式热图
                fig = go.Figure(data=go.Heatmap(
                    z=heat_data,
                    x=x_labels,
                    y=y_labels
                ))

                # 设置图表布局
                fig.update_layout(
                    title={
                        'text': 'Interactive Heatmap',
                        'x': 0.5,  # 设置标题居中
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    xaxis_title='Source=>Target cell interaction',
                    yaxis_title='Signal pathway',
                    width=1000,  # 设置宽度为 800 像素
                    height=1000  # 设置高度为 600 像素
                )

                # 将图表渲染到网页
                prob_plot_div = fig.to_html(full_html=False)

                # ---------------------------------
                # plots 2
                ## number of ligand-receptor pairs in query pathway.
                filter_results_lrpair = LRpairs.objects.filter(**filters)
                df_data = list(filter_results_lrpair.values('source', 'target', 'ligand', 'target', 'pathway'))
                df = pd.DataFrame(df_data)

                df['cell_pair'] = df['source'] + '=>' + df['target']
                df_new = df.groupby(['cell_pair', 'pathway']).size().reset_index(name="count")
                df_plt = pd.pivot_table(df_new, values='count', index='pathway', columns='cell_pair').fillna(0)

                ## two-way clustering in heatmap
                row_clusters = hierarchy.linkage(df_plt.values, method='average', metric='euclidean')
                column_clusters = hierarchy.linkage(df_plt.values.T, method='average', metric='euclidean')
                # 获取行和列的排序索引
                row_order = hierarchy.leaves_list(row_clusters)
                column_order = hierarchy.leaves_list(column_clusters)

                # 根据排序索引重新排列数据框
                df_reordered = df_plt.iloc[row_order, column_order]

                # 构造热图数据
                heat_data = df_reordered.values.tolist()
                x_labels = df_reordered.columns.tolist()
                y_labels = df_reordered.index.tolist()

                # 绘制交互式热图
                fig = go.Figure(data=go.Heatmap(
                    z=heat_data,
                    x=x_labels,
                    y=y_labels
                ))

                # 设置图表布局
                fig.update_layout(
                    title={
                        'text': 'Counting Ligand-receptor pairs in Selected Pathways',
                        'x': 0.5,  # 设置标题居中
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    xaxis_title='Source=>Target cell interaction',
                    yaxis_title='Signal pathway',
                    width=1000,  # 设置宽度为 800 像素
                    height=1000  # 设置高度为 600 像素
                )

                # 将图表渲染到网页
                number_plot_div = fig.to_html(full_html=False)

                # 构建render字典
                result = {
                    'total_records': row_count,
                    'n_dataset': n_dataset,
                    'n_minor_source': n_minor_source,
                    'n_minor_target': n_minor_target,
                    'n_major_source': n_major_source,
                    'n_major_target': n_major_target,
                    'n_uniq_source_target': n_uniq_source_target,
                    "n_pathway": n_pathway,
                    'filters': filters,
                    'filter_results': filter_results,
                    'plot_url2': prob_plot_div,
                    'plot_url3': number_plot_div
                }
                return render(request, 'analyze-cell-commu-single.html', result)

        else:
            filters = None
            filter_results = None
            plot_url1 = None
            plot_url2 = None
            plot_url3 = None

            results = {
                'filters': filters,
                'filter_results': filter_results,
                'plot_url1': plot_url1,
                'plot_url2': plot_url2,
                'plot_url3': plot_url3
            }

            return render(request, 'analyze-cell-commu-single.html', results)

    return render(request, 'analyze-cell-commu-single.html')

def analyze_cell_commu_crossdataset(request):
    if request.method == 'POST':
        # 处理表单提交：判断当前提交的是哪个表单
        # if option == 'option1':
        # f_dataset_check = request.POST.get('f_dataset_checkbox', None)
        f_dataset_value = request.POST.get('f_dataset_value', None)
        # f_pathway_check = request.POST.get('f_pathway_checkbox', None)
        f_pathway_value = request.POST.get('f_pathway_value', None)
        # f_source_check = request.POST.get('f_source_checkbox', None)
        f_source_value = request.POST.get('f_source_value', None)
        # f_target_check = request.POST.get('f_target_checkbox', None)
        f_target_value = request.POST.get('f_target_value', None)
        # f_ligand_check = request.POST.get('f_ligand_checkbox', None)
        f_ligand_value = request.POST.get('f_ligand_value', None)
        # f_receptor_check = request.POST.get('f_receptor_checkbox', None)
        f_receptor_value = request.POST.get('f_receptor_value', None)
        # f_pval_check = request.POST.get('f_pval_checkbox', None)
        f_pval_value = request.POST.get('f_pval_value', None)

        if f_dataset_value == '' and f_pathway_value == '' and f_source_value == '' and f_target_value == ''\
            and f_ligand_value == '' and f_receptor_value == '' and f_pval_value == '':
            error_message = "The form is empty. Please fill out the form."
            result = {'error_message': error_message}
            return render(request, 'analyze-cell-commu-cross.html', result)
        # //

        elif f_dataset_value == '':
            error_message = "The form is empty. Please fill out the form."
            result = {'error_message': error_message}
            return render(request, 'analyze-cell-commu-cross.html', result)

        elif f_dataset_value:
            filters = {}
            f_dataset_filter = f'dataset__contains'
            filters[f_dataset_filter] = f_dataset_value

            if f_pathway_value:
                f_pathway_filter = f'pathway__contains'
                filters[f_pathway_filter] = f_pathway_value

            if f_source_value:
                f_source_filter = f'source__contains'
                filters[f_source_filter] = f_source_value

            if f_target_value:
                f_target_filter = f'target__contains'
                filters[f_target_filter] = f_target_value

            if f_ligand_value:
                f_ligand_filter = f'ligand__contains'
                filters[f_ligand_filter] = f_ligand_value

            if f_receptor_value:
                f_receptor_filter = f'receptor__contains'
                filters[f_receptor_filter] = f_receptor_value

            if f_pval_value:
                f_pval_filter = f'pval__lt'
                filters[f_pval_filter] = f_pval_value
            else:
                f_pval_filter = f'pval__lt'
                filters[f_pval_filter] = 0.05

            filter_results = LRpairs.objects.filter(**filters)

            # ---------------------------------
            ## 数据库查询结果数据集的统计分析。
            row_count = filter_results.count() # total counts of rows.
            dataset_uniq_value = filter_results.values_list('dataset', flat=True).distinct()
            n_dataset = len(dataset_uniq_value)

            # how many cell types in source and target cells.
            ## number of minor cell types.
            source_minor_uniq_value = filter_results.values_list('source', flat=True).distinct()
            target_minor_uniq_value = filter_results.values_list('target', flat=True).distinct()
            n_minor_source = len(source_minor_uniq_value)
            n_minor_target = len(target_minor_uniq_value)

            ## number of major cell types.
            source_split_values = [i.split('_')[1] for i in source_minor_uniq_value]
            source_split_uniq = list(set(source_split_values))
            n_major_source = len(source_split_uniq)

            target_split_values = [i.split('_')[1] for i in target_minor_uniq_value]
            target_split_uniq = list(set(target_split_values))
            n_major_target = len(target_split_uniq)

            # how many signal pathways.
            pathway_uniq_value = filter_results.values_list('pathway', flat=True).distinct()
            n_pathway = len(pathway_uniq_value)

            # how many ligand-receptor paires.
            n_uniq_LR = filter_results.values('ligand', 'receptor').distinct().count()

            # how many source-target paires.
            n_uniq_source_target = filter_results.values('source', 'target').distinct().count()

            # ---------------------------------
            # plots 1
            ## cell-cell interaction measured by probability of LR pairs.
            ## construct data objects for plotting.
            df_data = list(filter_results.values('source', 'target', 'ligand', 'receptor', 'prob'))
            df = pd.DataFrame(df_data)

            df['cell_pair'] = df['source'] + '=>' + df['target']
            df['LR_pair'] = df['ligand'] + ':' + df['receptor']
            df_agg = df.groupby(['cell_pair', 'LR_pair'])['prob'].mean().reset_index()
            df_plt = pd.pivot_table(df_agg, values='prob', index='LR_pair', columns='cell_pair').fillna(0)

            ## two-way clustering in heatmap
            row_clusters = hierarchy.linkage(df_plt.values, method='average', metric='euclidean')
            column_clusters = hierarchy.linkage(df_plt.values.T, method='average', metric='euclidean')
            # 获取行和列的排序索引
            row_order = hierarchy.leaves_list(row_clusters)
            column_order = hierarchy.leaves_list(column_clusters)

            # 根据排序索引重新排列数据框
            df_reordered = df_plt.iloc[row_order, column_order]

            # 构造热图数据
            heat_data = df_reordered.values.tolist()
            x_labels = df_reordered.columns.tolist()
            y_labels = df_reordered.index.tolist()

            # 绘制交互式热图
            fig = go.Figure(data=go.Heatmap(
                z=heat_data,
                x=x_labels,
                y=y_labels
            ))

            # 设置图表布局
            fig.update_layout(
                title={
                    'text': 'Overview of source and target cell interaction <br> Probability of Ligand-receptor pairs between cell clusters',
                    'x': 0.5,  # 设置标题居中
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                xaxis_title='Source=>Target cell interaction',
                yaxis_title='Ligand-receptor pairs',
                width=1000,  # 设置宽度为 800 像素
                height=1000  # 设置高度为 600 像素
            )

            # 将图表渲染到网页
            ccc_prob_plot_div = fig.to_html(full_html=False)

            # ---------------------------------
            # plots 2
            ## meta-plot
            ## count of LRpair:source:target pairs in different datasets.
            ## construct data objects for plotting.
            df_data = list(filter_results.values('dataset', 'source', 'target', 'ligand', 'receptor'))
            df = pd.DataFrame(df_data)

            df['source_new'] = [i.split("_")[1] for i in df['source']]
            df['target_new'] = [i.split("_")[1] for i in df['target']]

            df['cell_pair'] = df['source_new'] + ':' + df['target_new']
            df['LR_pair'] = df['ligand'] + ':' + df['receptor']
            df['combine_index'] = df['cell_pair'] + '__' + df['LR_pair']
            uniq_rows = df.drop_duplicates(subset=['combine_index', 'dataset'])
            count_df = uniq_rows['combine_index'].value_counts()

            # 创建ranked dot plot
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=count_df.index, y=count_df.values, mode='markers', marker=dict(size=8)))
            # 自定义图形的布局和样式
            fig.update_layout(title={
                'text': 'Ranked Dot Plot',
                'x': 0.5,  # 设置标题居中
                'xanchor': 'center',
                'yanchor': 'top'
            },
                xaxis_title="Ranked LR pairs + source-target cell pairs",
                yaxis_title='Counts')
            LRpair_cellpair_plot_div = fig.to_html(full_html=False)

            # ---------------------------------
            # plots 3
            ## meta-plot
            ## count of LRpair:source:target pairs in different datasets.
            ## construct data objects for plotting.
            df_data = list(filter_results.values('source', 'target', 'pathway',  'dataset'))
            df = pd.DataFrame(df_data)

            df['source_new'] = [i.split("_")[1] for i in df['source']]
            df['target_new'] = [i.split("_")[1] for i in df['target']]

            df['cell_pair'] = df['source_new'] + ':' + df['target_new']
            df['combine_index'] = df['cell_pair'] + '__' + df['pathway']

            uniq_rows = df.drop_duplicates(subset=['combine_index', 'dataset'])
            count_df = uniq_rows['combine_index'].value_counts()

            # 创建ranked dot plot
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=count_df.index, y=count_df.values, mode='markers', marker=dict(size=8)))
            # 自定义图形的布局和样式
            fig.update_layout(title={
                'text': 'Ranked Dot Plot',
                'x': 0.5,  # 设置标题居中
                'xanchor': 'center',
                'yanchor': 'top'
            },
                xaxis_title="Ranked Pathway + source-target cell pairs",
                yaxis_title='Counts')
            pathway_cellpair_plot_div = fig.to_html(full_html=False)

            # 构建render字典
            result = {
                'total_records': row_count,
                'n_dataset': n_dataset,
                'n_minor_source': n_minor_source,
                'n_minor_target': n_minor_target,
                'n_major_source': n_major_source,
                'n_major_target': n_major_target,
                'n_uniq_source_target': n_uniq_source_target,
                "n_pathway": n_pathway,
                'n_uniq_LR': n_uniq_LR,
                'filters':filters,
                'filter_results': filter_results,
                'plot_url1': ccc_prob_plot_div,
                'plot_url2': LRpair_cellpair_plot_div,
                'plot_url3': pathway_cellpair_plot_div
            }
            return render(request, 'analyze-cell-commu-cross.html', result)

        else:
            filters = None
            filter_results = None
            plot_url1 = None
            plot_url2 = None
            plot_url3 = None

            results = {
                'filters': filters,
                'filter_results': filter_results,
                'plot_url1': plot_url1,
                'plot_url2': plot_url2,
                'plot_url3': plot_url3
            }

            return render(request, 'analyze-cell-commu-cross.html', results)

    return render(request, 'analyze-cell-commu-cross.html')

# views for goto help page from the sidebar.
def help(request):
    return render(request, 'help.html')

