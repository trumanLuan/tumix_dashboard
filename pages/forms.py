from django import forms
from .models import Marker_Celltype
from .models import Marker_Subcluster

class sampleForm(forms.Form):
    dataset = forms.CharField(label='Dataset', max_length=100, required=False)
    celltype = forms.CharField(label='Select cell type', max_length=100, required=False)
    gene = forms.CharField(label='Official gene name', max_length=100, required=False)
    pct1 = forms.CharField(label='Percent / input cell type', max_length=100, required=False)
    pct2 = forms.CharField(label='Percent/Other cell type', max_length=100, required=False)
    padj = forms.CharField(label='Adjusted P (cutoff)', max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        active_fields = kwargs.pop('active_fields', None)
        super(sampleForm, self).__init__(*args, **kwargs)

        # 根据用户选择设置字段的可见性和可编辑性
        if active_fields:
            for field_name in self.fields.keys():
                if field_name not in active_fields:
                    self.fields[field_name].widget = forms.HiddenInput()


class geneMarkerForm(forms.Form):
    # CELLCLUSTER_CHOICES = [
    #     ('Y', 'Yes, cell sub-type is defined by major cell type and sub-cluster'),
    #     ('N', 'No, by major cell type'),
    # ]
    # dataset = forms.CharField(label='Dataset', max_length=500, required=False, initial='GSE107747_human_LIHC_tissue.Blood')
    # bycluster = forms.ChoiceField(label="Is By Cell Sub-type", choices=CELLCLUSTER_CHOICES, widget=forms.RadioSelect, initial='N')
    # celltype = forms.CharField(label='Select cell type', required=False, max_length=100, initial="Monocytes")
    # gene = forms.CharField(label='Official gene name', required=False, max_length=100, initial="EGR1")
    # pct1 = forms.CharField(label='Percent / input cell type', required=False, max_length=100, initial=0.5)
    # pct2 = forms.CharField(label='Percent/Other cell type', required=False, max_length=100, initial=0.5)
    # padj = forms.CharField(label='Adjusted P (cutoff)', required=False, max_length=100, initial=0.05)

    active_fields = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=(
            ('field1', '字段1'),
            ('field2', '字段2'),
            ('field3', '字段3'),
            # 添加更多的字段选择
        )
    )
    field1 = forms.CharField(required=False)
    field2 = forms.IntegerField(required=False)
    field3 = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        active_fields = cleaned_data.get('active_fields', [])

        for field_name in active_fields:
            field_value = cleaned_data.get(field_name)

            if field_name == 'field1':
                # 处理 field1 的筛选条件
                if field_value:
                    # 设置包含部分字符的筛选条件
                    self.fields[field_name].widget.attrs['contains'] = field_value
            elif field_name == 'field2':
                # 处理 field2 的筛选条件
                if field_value:
                    # 设置大于、小于、等于等条件
                    filter_condition = cleaned_data.get(f'{field_name}_filter_condition')
                    if filter_condition == 'greater':
                        self.fields[field_name].widget.attrs['gt'] = field_value
                    elif filter_condition == 'less':
                        self.fields[field_name].widget.attrs['lt'] = field_value
                    elif filter_condition == 'equal':
                        self.fields[field_name].widget.attrs['exact'] = field_value

            elif field_name == 'field3':
                # 处理 field3 的筛选条件
                if field_value:
                    # 设置包含部分字符的筛选条件
                    self.fields[field_name].widget.attrs['contains'] = field_value

            return cleaned_data

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
