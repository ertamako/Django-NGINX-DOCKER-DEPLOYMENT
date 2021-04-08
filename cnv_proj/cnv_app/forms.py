from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import BedFile, FastaFile, Reference, BamFile, TargetBed, TargetCoverage, CopyNumberRatio, Analysis, \
    CopyNumberSegment    # CoverageBinner

# user Form
Sex_CHOICES = (
    ('X', 'X'),
    ('Y', 'Y'),
)


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)


class FileFieldForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


# Batch Form
class Bam_Files_Form(forms.Form):
    bam_Files = forms.ModelMultipleChoiceField(queryset=BamFile.objects.all(),
                                                widget=forms.CheckboxSelectMultiple(), required=True,
                                                label="Choose the Files you want to use either for running a CNV "
                                                      "Analysis or for constructing the reference File, "
                                                      "keep in mind the that the chromosomal sex must be the same")


# Upload Bam Files Form from Model Form!
# class BamForm(forms.ModelForm):
#     class Meta:
#         model = BamFile
#         fields = ('bam_document',)


class SexForm(forms.Form):
    chromosomal_sex = forms.ChoiceField(required=False, choices=Sex_CHOICES, label='Chromosomal sex')


class Normal_Files_Form(forms.Form):
    normal_Files = forms.ModelMultipleChoiceField(queryset=BamFile.objects.all(),
                                               widget=forms.CheckboxSelectMultiple(), required=True,
                                               label="Select the normal/control samples")
    description = forms.CharField(required=False, max_length=200, label="Name your Reference File")




class BedForm(forms.Form):
    bed_choice = forms.ModelChoiceField(required=True, queryset=BedFile.objects.all())


class FastaForm(forms.Form):
    fasta_choice = forms.ModelChoiceField(required=True, queryset=FastaFile.objects.all())


class ReferenceForm(forms.Form):
    reference_choice = forms.ModelChoiceField(required=False, queryset=Reference.objects.all())


# Pipeline


SEQ_METHOD = (
    ('H', 'Hybridization Capture'),
    ('A', 'Targeted Amplicon Sequencing'),
    ('W', 'Whole Genome Sequencing'),
)

SEQ_INPUT = (
    ('hybrid', 'Hybridization Capture'),
    ('amplicon', 'Targeted Amplicon Sequencing'),
    ('wgs', 'Whole Genome Sequencing'),
)

SEG_CHOICES = (
    ('cbs', 'circular binary segmentation'),
    ('flasso', 'flasso'),
    ('haar', 'haar'),
    ('hmm', 'hmm'),
    ('hmm-tumor', 'hmm-tumor'),
    ('none', 'none'),
    ('hmm-germline', 'hmm-germline'),
)


class MethodForm(forms.Form):
    seq_method = forms.ChoiceField(choices=SEQ_INPUT, label="Choose the sequencing method")
    seg_choices = forms.ChoiceField(choices=SEG_CHOICES, label="Choose the Segmentation method")


class Autobin(forms.Form):
    method = forms.ChoiceField(choices=SEQ_METHOD)
    bp_per_bin = forms.IntegerField(required=False,
                                    label="Desired average number of sequencing read bases mapped to each bin. Default: 100000.0")


class Coverage(forms.Form):
    use_count = forms.BooleanField(required=False)
    MIN_MAPQ = forms.IntegerField(required=False, label="Minimum mapping quality score (phred scale 0-60) "
                                                        "to count a read for coverage depth. [Default: 0]")


class PooledReference(forms.Form):
    choose_cnn = forms.ModelMultipleChoiceField(queryset=TargetCoverage.objects.all(),
                                                widget=forms.CheckboxSelectMultiple(), required=True,
                                                label="Choose the Files you want to use for the reference File, "
                                                      "keep in mind the that the chromosomal sex must be the same")
    ref_Name = forms.CharField(label='Give your Reference file a name, for ex. FFPE or Fresh-Tissue')
    chromosomal_sex = forms.ChoiceField(required=False, choices=Sex_CHOICES, label='Chromosomal sex')


class Fix(forms.Form):
    reference_choice = forms.ModelChoiceField(required=False, queryset=Reference.objects.all())


class Segment(forms.Form):
    segmentation_method = forms.ChoiceField(choices=SEG_CHOICES)



class Call(forms.Form):
    purity = forms.DecimalField(widget=forms.NumberInput(attrs={'id': 'purity-text'}), label='Purity for ex. 0.8.'
                                                                                             'With the purity option, log2 ratios are rescaled to the value that would '
                                                                                             'be seen a completely pure, uncontaminated sample.')
    # threshold = forms.CharField(required=False, label='Give a list of threshold that map to '
    #                                                   'Integer Copy number 0,1,2,3,4 as in example: -1.1,-0.4,0.3,0.7')
    choose_bam = forms.ModelMultipleChoiceField(required=True, queryset=BamFile.objects.all(),
                                                widget=forms.CheckboxSelectMultiple(),
                                                label="Choose the samples you want to run call for")
    # chromosomal_sex = forms.ChoiceField(required=False, widget=forms.Select(attrs={'id': 'chr-sex'}),
    #                                     choices=Sex_CHOICES,
    #                                     label='Chromosomal sex')


class Metrics(forms.Form):
    copy_ratio_cnr = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    copy_seg_cns = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))  # , label='Copy Segments (.cns Files)'


class Sex(forms.Form):
    reference = forms.FileField(label='Reference file (.cnn)')
    target_cnn_File = forms.FileField(label='.targetcoverage.cnn')
    antitarget_cnn_File = forms.FileField(label='.antitargetcoverage.cnn')


# Savvy
# class SavvyCNVForm(forms.Form):
#     coverage_binner = forms.ModelMultipleChoiceField(required=True, queryset=CoverageBinner.objects.all(),
#                                                 widget=forms.CheckboxSelectMultiple(),
#                                                 label="Choose the samples you want to visualize")
#     size = forms.IntegerField(required=True, max_value=1000000000, min_value=1,
#                                         label='Choose bin size')


Scatter_CHOICES = (
    # ('CNN', 'CNN'),
    ('CNR', 'CNR'),
    ('CNVS', 'CNVS'),
)


class Scatter_Ref(forms.Form):
    bam_File = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    level = forms.ChoiceField(choices=Scatter_CHOICES)


CHR_CHOICES = (
    ('chr1', 'chr1'), ('chr2', 'chr2'), ('chr3', 'chr3'), ('chr4', 'chr4'),
    ('chr5', 'chr5'), ('chr6', 'chr6'), ('chr7', 'chr7'), ('chr8', 'chr8'),
    ('chr9', 'chr9'), ('chr10', 'chr10'), ('chr11', 'chr11'), ('chr12', 'chr12'),
    ('chr13', 'chr13'), ('chr14', 'chr14'), ('chr15', 'chr15'), ('chr16', 'chr16'),
    ('chr17', 'chr17'), ('chr18', 'chr18'), ('chr19', 'chr19'), ('chr20', 'chr20'),
    ('chr21', 'chr21'), ('chr22', 'chr22'), ('chrX', 'chrX'), ('chrY', 'chrY')
)

CHR_CHOICES_ALL = (
        ('chr1', 'chr1'), ('chr2', 'chr2'), ('chr3', 'chr3'),
        ('chr4', 'chr4'), ('chr5', 'chr5'), ('chr6', 'chr6'),
        ('chr7', 'chr7'), ('chr8', 'chr8'), ('chr9', 'chr9'),
        ('chr10', 'chr10'), ('chr11', 'chr11'), ('chr12', 'chr12'),
        ('chr13', 'chr13'), ('chr14', 'chr14'), ('chr15', 'chr15'),
        ('chr16', 'chr16'), ('chr17', 'chr17'), ('chr18', 'chr18'),
        ('chr19', 'chr19'), ('chr20', 'chr20'), ('chr21', 'chr21'),
        ('chr22', 'chr22'), ('chrX', 'chrX'), ('chrY', 'chrY'), ('All', 'All')
)


class Scatter_Res(forms.Form):
    chromosome = forms.ChoiceField(required=True, choices=CHR_CHOICES_ALL, label='Choose a specific chromosome to scatter plot')
    position_start = forms.IntegerField(required=False, max_value=1000000000, min_value=1,
                                        label='Choose a starting position in chosen chr., for ex. "1"')
    position_end = forms.IntegerField(required=False, max_value=1000000000, min_value=1,
                                      label='Choose an end position in chosen chr. for ex. "50000000"')
    choose_bam = forms.ModelChoiceField(required=True, queryset=BamFile.objects.all(),
                                                 label="Choose the sample you want to visualize")
    gene = forms.CharField(required=False, label='Choose genes for the required chr., for ex. in chr12 "CDK4,MDM2"')

class Diagram_Res(forms.Form):
    # Sample = forms.FilePathField(required=True, path=settings.STATIC_ROOT + "/cnv_app/b_result/", match=".*.cnr") ToDo
    threshold = forms.DecimalField(label='Determine a log2 threshold of the alterations to be displayed, for ex. "0.5"')
    min_probes = forms.IntegerField(label="Minimum number of covered probes to report a gain/loss, you could start with 3 min probes.")
    choose_bam = forms.ModelChoiceField(required=True, queryset=BamFile.objects.all(),
                                                 label="Choose the sample you want to visualize")

class Heatmap_Res(forms.Form):
    # Sample = forms.FilePathField(required=True, path=settings.STATIC_ROOT + "/cnv_app/b_result/", match=".*.cnr") ToDo
    chromosome = forms.ChoiceField(required=True, choices=CHR_CHOICES_ALL, label='Choose a specific chromosome for the heatmap plot')
    #    gene = forms.CharField(required=False, label='Choose genes for the required chr., for ex. "CDK4,MDM2"')
    position_start = forms.IntegerField(required=False, max_value=1000000000, min_value=1,
                                        label='Choose a starting position in chosen chr., for ex. "1"')
    position_end = forms.IntegerField(required=False, max_value=1000000000, min_value=1,
                                      label='Choose an end position in chosen chr. for ex. "50000000"')
    choose_bam = forms.ModelMultipleChoiceField(required=True, queryset=BamFile.objects.all(),
                                                widget=forms.CheckboxSelectMultiple(),
                                                label="Choose the samples you want to visualize")



class Breaks(forms.Form):
    choose_bam = forms.ModelMultipleChoiceField(required=True, queryset=BamFile.objects.all(),
                                                widget=forms.CheckboxSelectMultiple(),
                                                label="Choose the samples you want to run genemetrics for")

class Genemetrics(forms.Form):
    choose_bam = forms.ModelMultipleChoiceField(required=True, queryset=BamFile.objects.all(),
                                                widget=forms.CheckboxSelectMultiple(),
                                                label="Choose the samples you want to run genemetrics for")
    threshhold = forms.DecimalField(decimal_places=4, label="Copy number change threshold to report a gene gain/loss, you could start with 0.2")
    min_probes = forms.IntegerField(label="Minimum number of covered probes to report a gain/loss, you could start with 3 min probes.")
    chromosome = forms.ChoiceField(required=False, choices=CHR_CHOICES_ALL, label="Choose a specific chromosome to find out the cnv's or all chromosomes.")