from django.contrib import admin
from django.urls import path, re_path
from django import urls
from . import views

urlpatterns = [
    re_path(r"index$", views.home, name='index'),
    re_path(r"browse$", views.browse, name='browse'),
    re_path(r"browse_results$", views.browse_results, name='browse_results'),
    re_path(r"search$", views.process_search_forms, name='search'),
    re_path(r"analyze-gene-expr$", views.analyze_gene_expr, name='analyze-gene-expr'),
    re_path(r"analyze-cell-marker-single$", views.analyze_cell_marker_single, name='analyze-cell-marker-single'),
    re_path(r"analyze-cell-marker-cross$", views.analyze_cell_marker_cross, name='analyze-cell-marker-cross'),
    re_path(r"analyze-cell-commu-single$", views.analyze_cell_commu_singledataset, name='analyze-cell-commu-single'),
    re_path(r"analyze-cell-commu-cross$", views.analyze_cell_commu_crossdataset, name='analyze-cell-commu-cross'),
    re_path(r"help$", views.help, name='help')
]