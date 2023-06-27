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
    re_path(r"analyze-cell-marker$", views.analyze_gene_expr, name='analyze-cell-marker'),
    re_path(r"analyze-cell-commu$", views.analyze_gene_expr, name='analyze-cell-commu'),
    re_path(r"help$", views.help, name='help')
]