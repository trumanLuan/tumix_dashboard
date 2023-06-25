from django import forms
from .models import Marker_Celltype
from .models import Marker_Subcluster

class sampleForm(forms.Form):
    dataset = forms.CharField(label='Dataset', max_length=100)
    celltype = forms.CharField(label='Select cell type', max_length=100)
    gene = forms.CharField(label='Official gene name', max_length=100)
    pct1 = forms.CharField(label='Percent / input cell type', max_length=100)
    pct2 = forms.CharField(label='Percent/Other cell type', max_length=100)
    padj = forms.CharField(label='Adjusted P (cutoff)', max_length=100)
    # your_name = forms.CharField(label='Your name', max_length=100)

class geneMarkerForm(forms.Form):
    CELLCLUSTER_CHOICES = [
        ('Y', 'Yes, cell sub-type is defined by major cell type and sub-cluster'),
        ('N', 'No, by major cell type'),
    ]
    dataset = forms.CharField(label='Dataset', max_length=100)
    bycluster = forms.ChoiceField(label="Is By Cell Sub-type", choices=CELLCLUSTER_CHOICES, widget=forms.RadioSelect)
    celltype = forms.CharField(label='Select cell type', max_length=100)
    gene = forms.CharField(label='Official gene name', max_length=100)
    pct1 = forms.CharField(label='Percent / input cell type', max_length=100)
    pct2 = forms.CharField(label='Percent/Other cell type', max_length=100)
    padj = forms.CharField(label='Adjusted P (cutoff)', max_length=100)

    # 表单1的字段

class geneExprForm(forms.Form):
    class Meta:
        model = Marker_Subcluster
        fields = ['dataset', 'cluster', 'avg_log2FC', 'gene', 'pct1', 'pct2', 'padj']
        # fields = '__all__'
    # 表单2的字段

# 创建其他表单类...

class cellCommuForm(forms.Form):
    class Meta:
        model = Marker_Subcluster
        fields = ['dataset', 'cluster', 'avg_log2FC', 'gene', 'pct1', 'pct2', 'padj']
