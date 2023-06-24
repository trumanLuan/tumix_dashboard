from django import forms
from .models import Marker_Celltype
from .models import Marker_Subcluster

class testForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class CelltypeGeneMarkerForm(forms.Form):
    class Meta:
        model = Marker_Celltype
        fields = ['dataset', 'cluster', 'avg_log2FC', 'gene', 'pct1', 'pct2', 'padj']
        # fields = '__all__'
    # 表单1的字段

class CellsubclusterGeneMarkerForm(forms.Form):
    class Meta:
        model = Marker_Subcluster
        fields = ['dataset', 'cluster', 'avg_log2FC', 'gene', 'pct1', 'pct2', 'padj']
        # fields = '__all__'
    # 表单2的字段

# 创建其他表单类...

