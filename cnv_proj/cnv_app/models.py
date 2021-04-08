from django.core.files.storage import FileSystemStorage
from django.db import models
# Create your models here.
from django.db.models import ForeignKey
from django.contrib.auth.models import User

fs_reference = FileSystemStorage(location="CNVKit/Reference_files")


# input files
class BamFile(models.Model):
    description = models.CharField(max_length=200)
    bam_document = models.FileField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User)
    PROTOCOL_CHOICES = (
        ('H', 'Hybridization Capture'),
        ('A', 'Targeted Amplicon Sequencing'),
        ('W', 'Whole Genome Sequencing'),
    )
    seq_protocol = models.CharField(max_length=1, choices=PROTOCOL_CHOICES, default="H", null=True)

    def __str__(self):
        return self.description


class BedFile(models.Model):
    description = models.CharField(max_length=200, blank=True)
    bed_document = models.FileField(max_length=500, upload_to='Data/bed_files', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.description


class FastaFile(models.Model):
    description = models.CharField(max_length=200, blank=True)
    fasta_document = models.FileField(max_length=500, upload_to='Data/fasta_files', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.description


# Savvy Models

# class SavvyAnalysis(models.Model):
#     analysis_id = models.CharField(max_length=200)  # , help_text='Enter batch run name'
#     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     bam_files_savvy = models.ManyToManyField(BamFile, related_name='bam_savvy_sample')
#     log_file = models.FileField(max_length=500, null=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#
#     def __str__(self):
#         return self.analysis_id
#

# class CoverageBinner(models.Model):
#     description = models.CharField(max_length=200)
#     bam_file_savvy = models.OneToOneField(BamFile, on_delete=models.SET_NULL, null=True)
#     document = models.FileField(max_length=500, upload_to='savvyCNV/')
#     created_at = models.DateTimeField(auto_now_add=True)
#     analysis_run = models.ForeignKey(SavvyAnalysis, on_delete=models.CASCADE, null=True)
#
#     def __str__(self):
#         return self.description
#

# class SavvyCNV(models.Model):
#     description = models.CharField(max_length=200)
#     coverage_files = models.ManyToManyField(CoverageBinner)
#     document = models.FileField(max_length=500)
#     d_size = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     analysis_run = models.ForeignKey(SavvyAnalysis, on_delete=models.CASCADE, null=True)
#
#     def __str__(self):
#         return self.description
#
#
# class SavvySelectCNV(models.Model):
#     description = models.CharField(max_length=200)
#     coverage_files = models.ManyToManyField(CoverageBinner)
#     document = models.FileField(max_length=500)
#     d_size = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     analysis_run = models.ForeignKey(SavvyAnalysis, on_delete=models.CASCADE, null=True)
#
#     def __str__(self):
#         return self.description


# CNVKit Models

class Reference(models.Model):
    description = models.CharField(max_length=200, blank=True)
    reference_document = models.FileField(max_length=500, upload_to=fs_reference)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, null=True)
    chr_sex = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    bam_files = models.ManyToManyField(BamFile)
    type = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.description


class Analysis(models.Model):
    analysis_id = models.CharField(max_length=200)  # , help_text='Enter batch run name'
    # TYPE_CHOICES = (('batch', 'batch'), ('pipeline', 'pipeline'))
    analysis_type = models.CharField(max_length=200, null=True)
    sequence_method = models.CharField(max_length=200, null=True)
    segment_method = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    normal_files = models.ManyToManyField(BamFile, related_name='normal_sample', blank=True)
    bam_files = models.ManyToManyField(BamFile, related_name='bam_sample')

    # Batch run can have only one Reference, but a Reference can be used for many batch runs
    reference_file = models.ForeignKey(Reference, on_delete=models.SET_NULL, blank=True, null=True)

    bed_file = models.ForeignKey(BedFile, on_delete=models.SET_NULL, null=True)
    fasta_file = models.ForeignKey(FastaFile, on_delete=models.SET_NULL, null=True)
    log_file = models.FileField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    # scatter_results = models.ManyToManyField(Scatter, blank=True, null=True)
    # diagram_results = models.ManyToManyField(Diagram, blank=True, null=True)
    # heatmap_results = models.ManyToManyField(Heatmap, blank=True, null=True)

    def __str__(self):
        return self.analysis_id


# Visualisation
CHR_CHOICES = (
    ('chr1', 'chr1'), ('chr2', 'chr2'), ('chr3', 'chr3'),
    ('chr4', 'chr4'), ('chr5', 'chr5'), ('chr6', 'chr6'),
    ('chr7', 'chr7'), ('chr8', 'chr8'), ('chr9', 'chr9'),
    ('chr10', 'chr10'), ('chr11', 'chr11'), ('chr12', 'chr12'),
    ('chr13', 'chr13'), ('chr14', 'chr14'), ('chr15', 'chr15'),
    ('chr16', 'chr16'), ('chr17', 'chr17'), ('chr18', 'chr18'),
    ('chr19', 'chr19'), ('chr20', 'chr20'), ('chr21', 'chr21'),
    ('chr22', 'chr22'), ('chrX', 'chrX'), ('chrY', 'chrY')
)


class Diagram(models.Model):
    description = models.CharField(max_length=200)
    bam_file = models.ForeignKey(BamFile, on_delete=models.SET_NULL, null=True)
    document = models.ImageField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    analysis_run = models.ForeignKey(Analysis, on_delete=models.CASCADE, null=True)
    threshold = models.DecimalField(decimal_places=3, max_digits=10, blank=True, null=True)
    min_probes = models.IntegerField(default=3, blank=True, null=True)


class Scatter(models.Model):
    description = models.CharField(max_length=200)
    bam_file = models.ForeignKey(BamFile, on_delete=models.SET_NULL, null=True)
    document = models.ImageField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    analysis_run: ForeignKey = models.ForeignKey(Analysis, on_delete=models.CASCADE, null=True)
    chromosome = models.CharField(max_length=10, choices=CHR_CHOICES, null=True)  # 'chr1:2333000-2444000'
    chr_range_from = models.IntegerField(blank=True, null=True)
    chr_range_to = models.IntegerField(blank=True, null=True)
    genes = models.CharField(max_length=1000, null=True)


class Heatmap(models.Model):
    bam_files = models.ManyToManyField(BamFile, blank=True)
    description = models.CharField(max_length=200)
    document = models.ImageField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    analysis_run: ForeignKey = models.ForeignKey(Analysis, on_delete=models.CASCADE, null=True)
    chromosome = models.CharField(max_length=10, choices=CHR_CHOICES, null=True)
    chr_range_from = models.IntegerField(blank=True, null=True)
    chr_range_to = models.IntegerField(blank=True, null=True)


# output files
class TargetBed(models.Model):
    description = models.CharField(max_length=200)
    target_bed_document = models.FileField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    analysis_run = models.ForeignKey(Analysis, on_delete=models.CASCADE, null=True)
    r_b_m_b = models.IntegerField(default=100000, null=True)  # number of sequencing read bases mapped to each bin

    #
    def __str__(self):
        return self.description


class AntiTargetBed(models.Model):
    description = models.CharField(max_length=200)
    anti_target_bed_document = models.FileField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    analysis_run = models.ForeignKey(Analysis, on_delete=models.CASCADE, null=True)
    r_b_m_b = models.IntegerField(default=100000, null=True)

    def __str__(self):
        return self.description


class TargetCoverage(models.Model):
    description = models.CharField(max_length=200)
    target_coverage_document = models.FileField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    analysis_run = models.ForeignKey(Analysis, on_delete=models.CASCADE, null=True)
    count = models.BooleanField(default=False, null=True)
    min_mapq = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.description


class AntiTargetCoverage(models.Model):
    description = models.CharField(max_length=200)
    anti_target_coverage_document = models.FileField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    analysis_run = models.ForeignKey(Analysis, on_delete=models.CASCADE, null=True)
    count = models.BooleanField(default=False, null=True)
    min_mapq = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.description


class CopyNumberRatio(models.Model):
    description = models.CharField(max_length=200)
    copy_number_document = models.FileField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    analysis_run = models.ForeignKey(Analysis, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.description


class CopyNumberSegment(models.Model):
    description = models.CharField(max_length=200)
    copy_segment_document = models.FileField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    analysis_run = models.ForeignKey(Analysis, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.description


#
# METHOD_CHOICES = (
#     ('H', 'Hybridization Capture'),
#     ('A', 'Targeted Amplicon Sequencing'),
#     ('W', 'Whole Genome Sequencing'),
# )
#
# SEGMENT_CHOICES = (
#     ('cbs', 'circular binary segmentation'),
#     ('flasso', 'flasso'),
#     ('haar', 'haar'),
#     ('hmm', 'hmm'),
#     ('hmm-tumor', 'hmm-tumor'),
#     ('none', 'none'),
#     ('hmm-germline', 'hmm-germline'),
# )

