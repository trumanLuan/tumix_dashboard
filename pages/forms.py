from django import forms
from .models import Marker_Celltype
from .models import Marker_Subcluster

class CelltypeGeneMarkerForm(forms.Form):
    class Meta:
        model = Marker_Celltype
        fields = []
        # fields = '__all__'
    # 表单1的字段

class CellsubclusterGeneMarkerForm(forms.Form):
    class Meta:
        model = Marker_Subcluster
        fields = '__all__'
    # 表单2的字段

# 创建其他表单类...

