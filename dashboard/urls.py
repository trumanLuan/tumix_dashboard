"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.urls import re_path
from django import urls

from pages import views
from pages import urls as pages_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    re_path(r'index$', views.index, name='index'),
    re_path(r"browse$", views.browse, name='browse'),
    re_path(r"browse_results$", views.browse_results, name='browse_results'),
    re_path(r"search$", views.process_search_forms, name='search'),
    re_path(r"analyze-gene-expr$", views.analyze_gene_expr, name='analyze-gene-expr'),
    # re_path(r"analyze-cell-marker$", views.analyze_cell_marker, name='analyze-cell-marker'),
    re_path(r"analyze-cell-marker-single$", views.analyze_cell_marker_single, name='analyze-cell-marker-single'),
    re_path(r"analyze-cell-marker-cross$", views.analyze_cell_marker_cross, name='analyze-cell-marker-cross'),
    re_path(r"analyze-cell-commu-single$", views.analyze_cell_commu_singledataset, name='analyze-cell-commu-single'),
    re_path(r"analyze-cell-commu-cross$", views.analyze_cell_commu_crossdataset, name='analyze-cell-commu-cross'),
    re_path(r"help$", views.help, name='help')
]
