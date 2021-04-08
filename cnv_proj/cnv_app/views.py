import json
import os, stat
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from django.contrib.auth import login

from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import StaticFilesStorage

from django.core.files.storage import FileSystemStorage

from django.http import HttpResponse, QueryDict, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.views.generic import FormView

from .forms import CustomUserCreationForm, Coverage, PooledReference, Segment, Call, \
    Scatter_Res, Diagram_Res, Heatmap_Res, ReferenceForm, BedForm, Bam_Files_Form, FastaForm, \
    Normal_Files_Form, Autobin, Fix, Genemetrics, MethodForm, Breaks, \
    FileFieldForm, SexForm #    SavvyCNVForm,

# VisPipe

# Create your views here.

from .models import BamFile, BedFile, FastaFile, AntiTargetCoverage, TargetCoverage, CopyNumberRatio, CopyNumberSegment, \
    Analysis, Scatter, Diagram, Heatmap, AntiTargetBed, TargetBed, Reference    # , \
    # CoverageBinner, SavvyAnalysis, SavvyCNV, SavvySelectCNV

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def home(request):
    ip = get_client_ip(request)
    print(ip)
    return render(request, "cnv_app/home.html")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
def overview(request):
    return render(request, 'cnv_app/cnvkit_overview.html')

@csrf_protect
def register(request):
    if request.method == "GET":
        return render(request, "registration/register.html",
                      {"form": CustomUserCreationForm})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("home"))
        else:
            error = form.errors
            return render(request, "registration/register.html",
                          {"form": CustomUserCreationForm, "errors": error})


# ----------------------------------------Batch--------------------------------------------------------------

# def upload_file_batch(request):
#     # request.upload_handlers.insert(0, ProgressBarUploadHandler(request))
#     if request.method == 'POST':
#         print(request.POST)
#         form = BamForm(request.POST, request.FILES)
#         if form.is_valid():
#             # save the files
#             bam_file = form.save()
#
#             # add descriptionattributes
#
#             # add user
#
#             bam_form = Bam_Files_Form()
#             data = {'is_valid': True, 'bam_form': bam_form, 'url': bam_file.bam_document.url}
#
#         else:
#             data = {'is_valid': False}
#         return HttpResponse(
#             json.dumps(data),
#             content_type="application/json"
#         )



# ----------------------------------------------- Upload Files in Dropzone ------------------------------------------------------


def handle_bam_upload(request):

    if request.method == "POST":
        form_class = FileFieldForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        if form_class.is_valid():
            for f in files:
                if str(f.name).endswith(".fa"):
                    if FastaFile.objects.filter(description=f.name):
                        continue
                    else:
                        with open(Path(settings.MEDIA_ROOT + "/Data/fasta_files/" + f.name).resolve(), 'wb+') as destination:
                            for chunk in f.chunks():
                                destination.write(chunk)
                        fasta_object = FastaFile.objects.create(description=f.name)
                        fasta_object.fasta_document = "Data/fasta_files/" + f.name
                        fasta_object.save()

                if str(f.name).endswith(".bam"):
                    if BamFile.objects.filter(description=f.name):
                        if BamFile.objects.filter(description=f.name, users=request.user).exists():
                            continue
                        else:
                            bam_object = BamFile.objects.get(description=f.name)
                            bam_object.users.add(request.user)
                            bam_object.save()
                    else:
                        with open(Path(settings.MEDIA_ROOT + "/Data/bam_files/" + f.name).resolve(), 'wb+') as destination:
                            for chunk in f.chunks():
                                destination.write(chunk)
                        bam_object = BamFile.objects.create(description=f.name)
                        bam_object.bam_document = "Data/bam_files/" + f.name
                        bam_object.save()
                        bam_object.users.add(request.user)
                        bam_object.save()
                if str(f.name).endswith(".bed"):
                    if BedFile.objects.filter(description=f.name):
                        continue
                    else:
                        upload_path = Path(settings.MEDIA_ROOT + "/Data/bed_files/" + f.name)
                        with open(upload_path.resolve(), 'wb+') as destination:
                            for chunk in f.chunks():
                                destination.write(chunk)
                        bed_object = BedFile.objects.create(description=f.name)
                        bed_object.bed_document = "Data/bed_files/" + f.name
                        bed_object.save()
                        #os.chmod(str(upload_path), stat.S_IRWXO)
                if str(f.name).startswith("Reference"):
                    if Reference.objects.filter(description=f.name, user=request.user):
                         continue
                    else:
                        upload_path = Path(settings.MEDIA_ROOT + "/CNVKit/Reference_files/" + f.name)
                        with open(upload_path.resolve(), 'wb+') as destination:
                            for chunk in f.chunks():
                                destination.write(chunk)
                        ref_object = Reference.objects.create(description=f.name, chr_sex="N", type="flat")
                        ref_object.reference_document = "CNVKit/Reference_files/" + f.name
                        ref_object.save()
                        ref_object.user = request.user
                        ref_object.save()
                        #os.chmod(str(upload_path), stat.S_IRWXO)

            response_data = {'form': True}
        else:
            response_data = {'form': False}
        return HttpResponse(json.dumps(response_data),
            content_type="application/json")



# def handle_uploaded_bam_file(f):
#     filename, extension = os.path.splitext(f.name)
#     relative_path = "Data/bam_files/%s" % filename
#     full_path = settings.MEDIA_ROOT + "/" + relative_path
#     with open(full_path, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
#         return relative_path

@csrf_protect
@login_required
def batch(request):
    if request.method == 'POST':
        # print(request.POST)
        ref_form = ReferenceForm(request.POST)
        bam_form = Bam_Files_Form(request.POST)
        sex_form = SexForm(request.POST)
        normal_form = Normal_Files_Form(request.POST)
        bed_form = BedForm(request.POST)
        fasta_form = FastaForm(request.POST)
        method_form = MethodForm(request.POST)

        if method_form.is_valid() & bam_form.is_valid() & fasta_form.is_valid() & bed_form.is_valid() \
                & sex_form.is_valid():
        #         & normal_form.is_valid() & method_form.is_valid(): ref_form.is_valid() &

            fs = FileSystemStorage()
            # Batch Form Data
            seq_meth = method_form.cleaned_data["seq_method"]
            seg_meth = method_form.cleaned_data["seg_choices"]
            now = datetime.now()
            result_time = str(now.strftime("%Y-%m-%d_%H-%M-%S"))
            batch_object = Analysis(analysis_id=result_time + "_" + request.user.username, sequence_method=seq_meth,
                                        segment_method=seg_meth)
            batch_object.save()
            batch_object.user = request.user
            batch_object.save()

                # Handle Bed File Upload or missing
            batch_object.bed_file = BedFile.objects.get(description=bed_form.cleaned_data["bed_choice"])
            batch_object.save()

                # Handle Fasta File Upload or missing
            batch_object.fasta_file = FastaFile.objects.get(description=fasta_form.cleaned_data["fasta_choice"])
            batch_object.save()

                # adding bam files to bam objects
            bam_files = bam_form.cleaned_data["bam_Files"]
            for file in bam_files:
                bam_single_file = BamFile.objects.get(description=file.description)
                batch_object.bam_files.add(bam_single_file)

                    # adding normal files to bam objects
                    # ---------------------------------------- Normal Files return Result and visualisation------------------------------------------------------------

            arg_bam = ""
            arg_bam_list = list(batch_object.bam_files.all())
            for it in arg_bam_list:
                arg_bam += it.bam_document.path + " "

            arg_norm = ""
            arg_norm_list = list(batch_object.normal_files.all())
            for it in arg_norm_list:
                arg_norm += it.bam_document.path + " "

                # arg_bam = " /".join(arg_bam_list)
                # arg_norm = " /".join(arg_norm_list)

                # create a user batch result folder
            batch_result_folder = batch_object.analysis_id
            process_create_folder = "mkdir " + batch_result_folder
            process_create_file = subprocess.Popen(process_create_folder.split(),
                                                       cwd=fs.path("CNVKit/Batch"), universal_newlines=True)
            process_create_file.wait()
            if sex_form.cleaned_data["chromosomal_sex"] == "Y":
                sex_arg = "-y"
            else:
                sex_arg = ""

                # ------------------------------------------------------- Batch Reference -----------------------------------------------------------------
            if 'reference_submit_button' in request.POST:
                batch_object.analysis_type = "reference"
                batch_object.save()
                command = "cnvkit.py batch -m %s --segment-method %s %s %s -n --drop-low-coverage --targets %s --fasta %s -p 32" \
                              % (batch_object.sequence_method, batch_object.segment_method,
                                 sex_arg, arg_bam, batch_object.bed_file.bed_document.path,
                                 batch_object.fasta_file.fasta_document.path,
                                 )
                # print(command)
                # -------------------------------------Reference is given, return results and visualisation-------------------------------------------------
                # check whether existing ref file is chosen and create command
            elif 'batch_submit_with_reference' in request.POST:
                if ref_form.is_valid():
                    batch_object.analysis_type = "batch"
                    batch_object.save()
                    reference_object = Reference.objects.get(description=ref_form.cleaned_data["reference_choice"])
                    batch_object.reference_file = reference_object
                    batch_object.save()
                    command = "cnvkit.py batch -m %s --segment-method %s %s %s --drop-low-coverage -r %s -p 32" \
                              % (batch_object.sequence_method, batch_object.segment_method, sex_arg, arg_bam,
                                 reference_object.reference_document.path)  # ToDo arg_access
                    # print(command)

                # ------------------------------------------------------- Batch Run with normal files-----------------------------------------------------------------
            elif 'batch_submit_button' in request.POST:
                if normal_form.is_valid():
                    batch_object.analysis_type = "batch"
                    batch_object.save()
                    normal_files = normal_form.cleaned_data["normal_Files"]
                    for normal_f in normal_files:
                        batch_object.normal_files.add(normal_f)
                        batch_object.save()
                    reference_name = normal_form.cleaned_data["description"] + "_" + batch_object.analysis_id + "_reference.cnn"

                    reference_path = settings.MEDIA_ROOT + "/CNVKit/Reference_files/" + reference_name
                    command = "cnvkit.py batch -m %s --segment-method %s %s %s -n %s --drop-low-coverage --targets %s " \
                              "--fasta %s --output-reference %s -p 32" \
                                  % (batch_object.sequence_method, batch_object.segment_method, sex_arg, arg_bam, arg_norm,
                                     batch_object.bed_file.bed_document.path,
                                     batch_object.fasta_file.fasta_document.path,
                                     reference_path)  # ToDo arg_access

        # print(command)
            process_batch = subprocess.Popen(command.split(),
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             cwd=fs.path("CNVKit/Batch/" + batch_result_folder),
                                             universal_newlines=True)

            stdout, stderr = process_batch.communicate()
            process_batch.wait()
            # write batch logfile
            batch_log_name = "log_" + batch_object.analysis_id + ".txt"
            batch_log = open(settings.MEDIA_ROOT + "/CNVKit/Batch/" + batch_result_folder + "/" + batch_log_name, "w+")
            batch_log.write(stdout)
            batch_log.write(stderr)
            batch_log.close()
            batch_log_path = "CNVKit/Batch/" + batch_result_folder + "/" + batch_log_name
            batch_object.log_file = batch_log_path
            batch_object.save()
            # process batch output files

            arg_bam_names = list(batch_object.bam_files.values_list("description", flat=True))
            samples_cnr = ""
            samples_cns = ""
            for bam in arg_bam_names:
                # print("bam in argbam_names: " + bam)
                sample_name = bam[:-4]
                samples_cnr += sample_name + ".cnr "
                samples_cns += sample_name + ".cns "
                scatter_name = sample_name + ".scatter.png"  # sample_name + "_" + batch_object.batch_id +
                #   # sample_name + "_" + batch_object.batch_id +
                command_scatter = "cnvkit.py scatter %s.cnr -s %s.cns -o %s" % (sample_name, sample_name, scatter_name)
                # print("Scatter Command:" + command_scatter)
                process_scatter = subprocess.Popen(command_scatter.split(),
                                                   cwd=fs.path("CNVKit/Batch/" + batch_result_folder))
                process_scatter.communicate()
                process_scatter.wait()

                scatter_object = Scatter(description=scatter_name)
                scatter_object.save()
                scatter_path = "CNVKit/Batch/" + batch_result_folder + "/" + scatter_name
                scatter_object.document = scatter_path
                scatter_object.analysis_run = batch_object
                scatter_object.bam_file = BamFile.objects.get(description=bam)
                scatter_object.save()

                if batch_object.analysis_type == "batch":
                    diagram_name = sample_name + ".diagram.pdf"
                    command_diagram = "cnvkit.py diagram -s %s.cns -o %s" % (
                        sample_name, diagram_name)
                    process_diagram = subprocess.Popen(command_diagram.split(),
                                                       cwd=fs.path("CNVKit/Batch/" + batch_result_folder))
                    process_diagram.communicate()
                    process_diagram.wait()
                    diagram_object = Diagram(description=diagram_name)
                    diagram_object.save()
                    diagram_path = "CNVKit/Batch/" + batch_result_folder + "/" + diagram_name
                    diagram_object.document = diagram_path
                    diagram_object.analysis_run = batch_object
                    diagram_object.bam_file = BamFile.objects.get(description=bam)
                    diagram_object.save()

            if batch_object.analysis_type == "batch":
                command_heatmap_s = "cnvkit.py heatmap %s -o %s" % (samples_cns, "heatmap_s.pdf")
                process_heatmap_s = subprocess.Popen(command_heatmap_s.split(),
                                                     cwd=fs.path("CNVKit/Batch/" + batch_result_folder))
                process_heatmap_s.communicate()
                # command_heatmap_r = "cnvkit.py heatmap %s -d -o %s" % (
                #    samples_cnr, "heatmap_r.png")
                # process_heatmap_r = subprocess.Popen(command_heatmap_r.split(),
                #                                 cwd=fs.path("CNVKit/Batch/" + batch_result_folder))
                # process_heatmap_r.communicate()

            for file_name in os.listdir(fs.path("CNVKit/Batch/" + batch_result_folder)):
                # print(file_name)
                f_path = "CNVKit/Batch/" + batch_result_folder + "/" + file_name
                if file_name.endswith(".antitarget.bed") or file_name.endswith(".antitarget-tmp.bed"):
                    antitarget_bed_object = AntiTargetBed(description=file_name, anti_target_bed_document=f_path)
                    antitarget_bed_object.save()
                    antitarget_bed_object.analysis_run = batch_object
                    antitarget_bed_object.save()
                if file_name.endswith(".target.bed") or file_name.endswith(".target-tmp.bed"):
                    target_bed_object = TargetBed(description=file_name, target_bed_document=f_path)
                    target_bed_object.save()
                    target_bed_object.analysis_run = batch_object
                    target_bed_object.save()
                if file_name.endswith(".antitargetcoverage.cnn"):
                    antitarget_cov_object = AntiTargetCoverage(description=file_name,
                                                               anti_target_coverage_document=f_path)
                    antitarget_cov_object.save()
                    antitarget_cov_object.analysis_run = batch_object
                    antitarget_cov_object.save()
                if file_name.endswith(".targetcoverage.cnn"):
                    target_cov_object = TargetCoverage(description=file_name, target_coverage_document=f_path)
                    target_cov_object.save()
                    target_cov_object.analysis_run = batch_object
                    target_cov_object.save()
                if file_name.endswith(".cnr"):
                    copy_ratio_object = CopyNumberRatio(description=file_name, copy_number_document=f_path)
                    copy_ratio_object.save()
                    copy_ratio_object.analysis_run = batch_object
                    copy_ratio_object.save()
                if file_name.endswith(".cns"):
                    copy_segment_object = CopyNumberSegment.objects.create(description=file_name,
                                                                           copy_segment_document=f_path)
                    copy_segment_object.analysis_run = batch_object
                    copy_segment_object.save()
                # if file_name.endswith(".call.cns"):
                #     copy_segment_object = CopyNumberSegment(description=file_name, copy_segment_document=f_path)
                #     copy_segment_object.save()
                #     copy_segment_object.analysis_run = batch_object
                #     copy_segment_object.save()
                if 'batch_submit_button' in request.POST:
                    if file_name.startswith(normal_form.cleaned_data["description"]):
                        reference_object = Reference.objects.create(description=reference_name,
                                                     chr_sex=sex_arg, type="batch")
                        reference_object.reference_document = "CNVKit/Reference_files/" + file_name
                        reference_object.save()
                        reference_object.user = request.user
                        reference_object.save()
                        for bamFile in batch_object.normal_files.all():
                            reference_object.bam_files.add(bamFile)
                        batch_object.reference_file = reference_object
                        batch_object.save()
                # if file_name.endswith("heatmap_r.png"):
                #     heatmap_object = Heatmap(description=file_name)
                #     heatmap_object.save()
                #     heatmap_object.document = f_path
                #     heatmap_object.analysis_run = batch_object
                #     for bamFile in batch_object.bam_files.all():
                #         heatmap_object.bam_files.add(bamFile)
                #     heatmap_object.save()
                if file_name.endswith("heatmap_s.pdf"):
                    heatmap_object = Heatmap(description=file_name)
                    heatmap_object.save()
                    heatmap_object.document = f_path
                    heatmap_object.analysis_run = batch_object
                    for bamFile in batch_object.bam_files.all():
                        heatmap_object.bam_files.add(bamFile)
                    heatmap_object.save()
            if batch_object.analysis_type == "batch":
                return redirect("batch_result")
            if batch_object.analysis_type == "reference":
                return redirect("reference_view")

    else:
        ref_form = ReferenceForm()
        ref_form.fields["reference_choice"].queryset = Reference.objects.filter(user=request.user)
        fasta_form = FastaForm()
        bam_form = Bam_Files_Form()
        bam_form.fields["bam_Files"].queryset = BamFile.objects.filter(users=request.user)
        bed_form = BedForm()
        sex_form = SexForm()
        normal_form = Normal_Files_Form()
        normal_form.fields["normal_Files"].queryset = BamFile.objects.filter(users=request.user)
        method_form = MethodForm()
        bam_files = BamFile.objects.all()
        context = {"ref_form": ref_form, "fasta_form": fasta_form,
                   "bam_form": bam_form, "bed_form": bed_form,
                   "normal_form": normal_form, "method_form": method_form,
                   "bam_files": bam_files, "sex_form": sex_form}
        return render(request, "cnv_app/batch.html", context)


@login_required
def results(request):
    batch_results = Analysis.objects.filter(user=request.user, analysis_type="batch").order_by("-created_at")
    # pipeline_results = Analysis.objects.filter(user=request.user, analysis_type="pipeline").order_by("-created_at")
    reference_results = Analysis.objects.filter(user=request.user, analysis_type="reference").order_by("-created_at")
    reference_files = Reference.objects.filter(user=request.user)
    context = {"batch_results": batch_results,  # "pipeline_results": pipeline_results,
               "reference_results": reference_results, "reference_files": reference_files}
    return render(request, 'cnv_app/all_results.html', context)


# ----------------------------------Batch_Result------------------------------------------


@login_required
def view_batch_result(request, analysis_id=None):  # ToDo
    if Analysis.objects.filter(user=request.user, analysis_type="batch"):
        if analysis_id:
            analysis_result = Analysis.objects.get(user=request.user, analysis_type="batch", analysis_id=analysis_id)
        else:
            analysis_result = Analysis.objects.filter(user=request.user, analysis_type="batch").latest("created_at")
        scatter_results = Scatter.objects.filter(analysis_run=analysis_result, chromosome__isnull=True, chr_range_from__isnull=True)
        heatmap_results = Heatmap.objects.filter(analysis_run=analysis_result, chromosome__isnull=True, chr_range_from__isnull=True)
        diagram_results = Diagram.objects.filter(analysis_run=analysis_result, threshold__isnull=True)

        scatter_rest_results = Scatter.objects.filter(analysis_run=analysis_result, chromosome__isnull=False)
        heatmap_rest_results = Heatmap.objects.filter(analysis_run=analysis_result, chromosome__isnull=False)
        diagram_rest_results = Diagram.objects.filter(analysis_run=analysis_result, threshold__isnull=False)
        scatter_result_form = Scatter_Res()
        scatter_result_form.fields["choose_bam"].queryset = analysis_result.bam_files.all()
        diagram_result_form = Diagram_Res()
        diagram_result_form.fields["choose_bam"].queryset = analysis_result.bam_files.all()
        heatmap_result_form = Heatmap_Res()
        heatmap_result_form.fields["choose_bam"].queryset = analysis_result.bam_files.all()
        genemetrics_form = Genemetrics()
        genemetrics_form.fields["choose_bam"].queryset = analysis_result.bam_files.all()
        breaks_form = Breaks()
        breaks_form.fields["choose_bam"].queryset = analysis_result.bam_files.all()
        call_form = Call()
        call_form.fields["choose_bam"].queryset = analysis_result.bam_files.all()

        context = {"analysis_result": analysis_result,
                   "scatter_results": scatter_results,
                   "heatmap_results": heatmap_results,
                   "diagram_results": diagram_results,
                   "scatter_rest_results": scatter_rest_results,
                   "heatmap_rest_results": heatmap_rest_results,
                   "diagram_rest_results": diagram_rest_results,
                   "scatter_result_form": scatter_result_form,
                   "diagram_result_form": diagram_result_form,
                   "heatmap_result_form": heatmap_result_form,
                   "genemetrics_form": genemetrics_form,
                   "breaks_form": breaks_form,
                   "call_form": call_form}
        return render(request, "cnv_app/cnvResult_Batch.html", context)
    else:
        return redirect("batch")


def delete_analysis(request):
    if request.method == 'DELETE':
        fs = FileSystemStorage()
        analysis_object = Analysis.objects.get(
            pk=int(QueryDict(request.body).get('analysispk')))
        analysis_object.delete()
        shutil.rmtree(fs.path("CNVKit/Batch/" + analysis_object.analysis_id))
        response_data = {'msg': 'Analysis object was deleted.'}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )



def call(request):
    call_form = Call(request.POST)

    if call_form.is_valid():
        analysis_id = request.POST["analysis_id"]
        analysis_object = Analysis.objects.get(analysis_id=analysis_id, user=request.user)
        purity_arg = call_form.cleaned_data['purity']
        bam_object_list = call_form.cleaned_data["choose_bam"]
        output_call = ""
        output_err_call = ""
        for bam in bam_object_list:
            cns_object = CopyNumberSegment.objects.get(description=bam.description[:-4] + ".cns", analysis_run=analysis_object)
            cns_name = cns_object.description[:-4] + ".call.cns"
            cns_object_call = CopyNumberSegment.objects.get(description=cns_name, analysis_run=analysis_object)
            #cns_object_call.purity = purity_arg
            #cns_object_call.save()
            command = "cnvkit.py call %s -m clonal --purity %s --drop-low-coverage -o %s" % (
                cns_object.description, purity_arg, cns_name)

            process_call = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id,
                                            universal_newlines=True)
            stdout, stderr = process_call.communicate()

            output_call += stdout + '\n'
            output_err_call += stderr + '\n'

        response_data = {'output_call': output_call, 'output_err_call': output_err_call}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


def scatter(request):
    if request.method == 'POST':
        scatter_form = Scatter_Res(request.POST, request.FILES)
        response_data = {}
        if scatter_form.is_valid():
            fs = FileSystemStorage()
            analysis_id = request.POST["analysis_id"]
            chr_arg = scatter_form.cleaned_data["chromosome"]
            if scatter_form.cleaned_data["position_start"]:
                position_start = scatter_form.cleaned_data["position_start"]
            else:
                position_start = ""
            if scatter_form.cleaned_data["position_end"]:
                position_end = scatter_form.cleaned_data["position_end"]
            else:
                position_end = ""

            bam_file = scatter_form.cleaned_data["choose_bam"]
            scatter_name = bam_file.description[:-4] + "_" + chr_arg + "_" + str(position_start) + ":" + str(
                position_end) + ".scatter.png"


            search_pattern = chr_arg + "'\t'"
            chr_part_arg = bam_file.description[:-4] + "_" + chr_arg
            #cnr
            cnr_arg_prev = bam_file.description[:-4] + ".cnr"
            cnr_arg_aft = chr_part_arg + ".cnr"

            #cns
            cns_arg_prev = bam_file.description[:-4] + ".cns"
            cns_arg_aft = chr_part_arg + ".cns"
            if chr_arg == "All":
                pass
            else:
                if fs.exists(settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id + "/" + cns_arg_aft):
                    pass
                else:

                    subprocess.Popen("grep chromosome %s > %s" % (cns_arg_prev, cns_arg_aft),
                                 shell=True, cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id)
                    subprocess.Popen("grep -P %s  %s >> %s" % (search_pattern, cns_arg_prev, cns_arg_aft),
                                 shell=True, cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id)

                if fs.exists(settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id + "/" + cnr_arg_aft):
                    pass
                else:
                    subprocess.Popen("grep chromosome %s > %s" % (cnr_arg_prev, cnr_arg_aft),
                                         shell=True, cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id)
                    subprocess.Popen("grep -P %s  %s >> %s" % (search_pattern, cnr_arg_prev, cnr_arg_aft),
                                         shell=True, cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id)

            if scatter_form.cleaned_data["gene"]:
                gene_arg = scatter_form.cleaned_data["gene"]
                command = "cnvkit.py scatter %s.cnr -s %s.cns -c %s:%s-%s -g %s -o %s --segment-color #56e305" % (
                    chr_part_arg, chr_part_arg, chr_arg, position_start, position_end, gene_arg, scatter_name)
            elif scatter_form.cleaned_data["position_start"]:
                command = "cnvkit.py scatter %s.cnr -s %s.cns -c %s:%s-%s -o %s --segment-color #56e305" % (
                    chr_part_arg, chr_part_arg, chr_arg, position_start, position_end, scatter_name)
            elif scatter_form.cleaned_data["chromosome"] == "All":
                command = "cnvkit.py scatter %s.cnr -s %s.cns -o %s --segment-color #56e305" % (
                    bam_file.description[:-4], bam_file.description[:-4], scatter_name)
                # print(command)
            else:
                command = "cnvkit.py scatter %s.cnr -s %s.cns -c %s -o %s --segment-color #56e305" % (
                    chr_part_arg, chr_part_arg, chr_arg, scatter_name)

            process_scatter = subprocess.Popen(command.split(),
                                               cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id)
            process_scatter.wait()
            f_path = "CNVKit/Batch/" + analysis_id + "/" + scatter_name
            analysis_object = Analysis.objects.get(analysis_id=analysis_id)
            if scatter_form.cleaned_data["position_start"] is not None or scatter_form.cleaned_data["position_end"] is not None:
                if Scatter.objects.filter(description=scatter_name, analysis_run=analysis_object.id):
                    scatter_object = Scatter.objects.get(description=scatter_name, analysis_run=analysis_object.id)
                else:
                    scatter_object = Scatter(description=scatter_name, bam_file=bam_file, document=f_path,
                                             chromosome=chr_arg, chr_range_from=scatter_form.cleaned_data["position_start"],
                                             chr_range_to=scatter_form.cleaned_data["position_end"],
                                             analysis_run=analysis_object)
            else:
                if Scatter.objects.filter(description=scatter_name, analysis_run=analysis_object.id):
                    scatter_object = Scatter.objects.get(description=scatter_name, analysis_run=analysis_object.id)
                else:
                    scatter_object = Scatter(description=scatter_name, bam_file=bam_file, document=f_path,
                                             chromosome=chr_arg,
                                             analysis_run=analysis_object)
            scatter_object.save()
            response_data['url'] = scatter_object.document.url
            return HttpResponse(json.dumps(response_data), content_type="application/json")


def delete_scatter(request):
    if request.method == 'DELETE':
        scatter_object = Scatter.objects.get(
            pk=int(QueryDict(request.body).get('imagepk')))
        scatter_object.delete()
        response_data = {'msg': 'Scatter plot was deleted.'}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


# Diagram -------------------------------------------------------------------------------
def diagram(request):
    if request.method == 'POST':
        diagram_form = Diagram_Res(request.POST, request.FILES)
        if diagram_form.is_valid():
            analysis_id = request.POST["analysis_id"]
            analysis_object = Analysis.objects.get(user=request.user, analysis_id=analysis_id)
            threshold_arg = diagram_form.cleaned_data["threshold"]
            bam_file = diagram_form.cleaned_data["choose_bam"]
            #cnr_arg = bam_file.description[:-4] + ".cnr"
            min_prob = diagram_form.cleaned_data["min_probes"]
            diagram_name = bam_file.description[:-4] + "_threshold_" + str(threshold_arg) + "_minprobes_" + str(min_prob) + ".pdf"
            f_path = "CNVKit/Batch/" + analysis_id + "/" + diagram_name

            if Diagram.objects.filter(description=diagram_name, analysis_run=analysis_object):
                diagram_object = Diagram.objects.get(description=diagram_name, analysis_run=analysis_object)
            else:
                cns_arg = bam_file.description[:-4] + ".cns"
                command = "cnvkit.py diagram -s %s -t %s -m %s -o %s" % (cns_arg, threshold_arg, min_prob, diagram_name)
                process_diagram = subprocess.Popen(command.split(),
                                                   cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id)
                process_diagram.wait()
                diagram_object = Diagram.objects.create(description=diagram_name, document=f_path, threshold=threshold_arg,
                                        min_probes=min_prob, analysis_run=analysis_object, bam_file=bam_file)

            response_data = {'url': diagram_object.document.url}
            return HttpResponse(json.dumps(response_data), content_type="application/json")


def delete_diagram(request):
    if request.method == 'DELETE':
        diagram_object = Diagram.objects.get(
            pk=int(QueryDict(request.body).get('diagrampk')))
        diagram_object.delete()
        response_data = {'msg': 'Diagram was deleted.'}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
# -------------------------------------------------------------------------------

def heatmap(request):
    if request.method == 'POST':
        heatmap_form = Heatmap_Res(request.POST, request.FILES)
        if heatmap_form.is_valid():
            fs = FileSystemStorage()
            analysis_id = request.POST["analysis_id"]
            analysis_object = Analysis.objects.get(analysis_id=analysis_id)
            chr_arg = heatmap_form.cleaned_data["chromosome"]

            bam_files = heatmap_form.cleaned_data["choose_bam"]
            cns_args = ""


            for bam_f in bam_files:

                #------------------------------------------------------------------------------------------------------
                search_pattern = chr_arg + "'\t'"
                chr_part_arg = bam_f.description[:-4] + "_" + chr_arg
                # cnr
                cnr_arg_prev = bam_f.description[:-4] + ".cnr"
                cnr_arg_aft = chr_part_arg + ".cnr"

                # cns
                cns_arg_prev = bam_f.description[:-4] + ".cns"
                cns_arg_aft = chr_part_arg + ".cns"
                if chr_arg == "All":
                    pass
                else:
                    if fs.exists(settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id + "/" + cns_arg_aft):
                        pass
                    else:

                        subprocess.Popen("grep chromosome %s > %s" % (cns_arg_prev, cns_arg_aft),
                                         shell=True, cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id)
                        subprocess.Popen("grep -P %s  %s >> %s" % (search_pattern, cns_arg_prev, cns_arg_aft),
                                         shell=True, cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id)

                    if fs.exists(settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id + "/" + cnr_arg_aft):
                        pass
                    else:
                        subprocess.Popen("grep chromosome %s > %s" % (cnr_arg_prev, cnr_arg_aft),
                                         shell=True, cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id)
                        subprocess.Popen("grep -P %s  %s >> %s" % (search_pattern, cnr_arg_prev, cnr_arg_aft),
                                         shell=True, cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id)

                # ------------------------------------------------------------------------------------------------------
                cns_args += " " + cns_arg_aft

            if heatmap_form.cleaned_data["position_start"]:
                position_start = heatmap_form.cleaned_data["position_start"]
                position_end = heatmap_form.cleaned_data["position_end"]
                heatmap_name = analysis_id + "_" + chr_arg + "_" + str(position_start) + ":" + str(
                    position_end) + ".heatmap.pdf"
                command = "cnvkit.py heatmap %s -c %s:%s-%s -o %s" % (
                    cns_args, chr_arg, position_start, position_end, heatmap_name)
            elif chr_arg == "All":
                heatmap_name = analysis_id + "_all_" + ".heatmap.pdf"
                command = "cnvkit.py heatmap %s -o %s" % (
                    cns_args, heatmap_name)
            else:
                heatmap_name = analysis_id + "_" + chr_arg + ".heatmap.pdf"
                command = "cnvkit.py heatmap %s -c %s:%s-%s -o %s" % (
                    cns_args, chr_arg, 1, "", heatmap_name)

            process_heatmap = subprocess.Popen(command.split(),
                                           cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id)
            process_heatmap.wait()
            f_path = "CNVKit/Batch/" + analysis_id + "/" + heatmap_name

            if heatmap_form.cleaned_data["position_start"]:
                if Heatmap.objects.filter(description=heatmap_name, analysis_run=analysis_object):
                    heatmap_object = Heatmap.objects.get(description=heatmap_name, analysis_run=analysis_object)
                else:
                    heatmap_object = Heatmap(description=heatmap_name, document=f_path,
                                         chromosome=chr_arg, chr_range_from=position_start,
                                         chr_range_to=position_end,
                                         analysis_run=analysis_object)
            else:
                if Heatmap.objects.filter(description=heatmap_name, analysis_run=analysis_object):
                    heatmap_object = Heatmap.objects.get(description=heatmap_name, analysis_run=analysis_object)
                else:
                    heatmap_object = Heatmap(description=heatmap_name, document=f_path,
                                         chromosome=chr_arg,
                                         analysis_run=analysis_object)

            heatmap_object.save()
            for bam_f in bam_files:
                heatmap_object.bam_files.add(bam_f)
                heatmap_object.save()
            response_data = {'url': heatmap_object.document.url}
            return HttpResponse(json.dumps(response_data), content_type="application/json")


def delete_heatmap(request):
    if request.method == 'DELETE':
        heatmap_object = Heatmap.objects.get(
            pk=int(QueryDict(request.body).get('heatmappk')))
        heatmap_object.delete()
        response_data = {}
        response_data['msg'] = 'Heatmap was deleted.'
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


def breaks(request):
    if request.method == "POST":
        breaks_form = Breaks(request.POST)
        if breaks_form.is_valid():
            analysis_id = request.POST["analysis_id"]
            analysis_object = Analysis.objects.get(analysis_id=analysis_id)
            output_stdout = ""
            output_stderr = ""
            bam_file_names = []
            for bam_file in breaks_form.cleaned_data["choose_bam"]:
                output_stdout += bam_file.description + "\n"
                name_arg = bam_file.description[:-4]
                command_gene = "cnvkit.py breaks %s.cnr %s.cns" % (name_arg, name_arg)
                if analysis_object.analysis_type == "pipeline":
                    cwd_arg = settings.MEDIA_ROOT + "/CNVKit/cnvkit_pipeline/" + analysis_id
                else:
                    cwd_arg = settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id
                process_gene = subprocess.Popen(command_gene.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                cwd=cwd_arg, universal_newlines=True)

                stdout, stderr = process_gene.communicate()
                output_stdout += stdout
                output_stderr += stderr
                process_gene.wait()

                bam_file_names.append(bam_file.description)
        response_data = {"output_stdout": output_stdout, "output_stderr": output_stderr,
                         "bam_file_names": bam_file_names}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def genemetrics(request):
    if request.method == "POST":
        genemetrics_form = Genemetrics(request.POST)
        if genemetrics_form.is_valid():
            fs = FileSystemStorage()
            threshhold_arg = genemetrics_form.cleaned_data["threshhold"]
            min_probes_arg = genemetrics_form.cleaned_data["min_probes"]
            analysis_id = request.POST["analysis_id"]
            # analysis_object = Analysis.objects.get(analysis_id=analysis_id)
            output_stdout = ""
            output_stderr = ""
            bam_file_names = []
            for bam_file in genemetrics_form.cleaned_data["choose_bam"]:
                cnr_file = bam_file.description[:-4] + ".cnr"
                cns_file = bam_file.description[:-4] + ".cns"
                #output_stdout += bam_file.description + "\n"

                if genemetrics_form.cleaned_data["chromosome"] == "All":
                    command_gene = "cnvkit.py genemetrics %s -s %s -t %s -m %s -o %s" % (
                        cnr_file, cns_file, threshhold_arg, min_probes_arg, bam_file.description[:-4] + ".genemetrics")
                else:
                    chr = str(genemetrics_form.cleaned_data["chromosome"])
                    search_pattern = chr + "'\t'"
                    chr_file_cnr = bam_file.description[:-4] + "_" + chr + ".cnr"
                    chr_file_cns = bam_file.description[:-4] + "_" + chr + ".cns"
                    if fs.exists(settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id + "/" + chr_file_cnr):
                        pass
                    else:
                        subprocess.Popen("grep chromosome %s > %s" % (cnr_file, chr_file_cnr),
                                 shell=True, cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id)
                        subprocess.Popen("grep -P %s  %s >> %s" % (search_pattern, cnr_file, chr_file_cnr),
                                 shell=True, cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id)
                    if fs.exists(settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id + "/" + chr_file_cns):
                        pass
                    else:

                        subprocess.Popen("grep chromosome %s > %s" % (cns_file, chr_file_cns),
                                         shell=True, cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id)
                        subprocess.Popen("grep -P %s  %s >> %s" % (search_pattern, cns_file, chr_file_cns),
                                         shell=True, cwd=settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id)

                    command_gene = "cnvkit.py genemetrics %s -s %s -t %s -m %s" % (
                            chr_file_cnr, chr_file_cns, threshhold_arg, min_probes_arg)
                    print(command_gene)
                cwd_arg = settings.MEDIA_ROOT + "/CNVKit/Batch/" + analysis_id
                process_gene = subprocess.Popen(command_gene.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                cwd=cwd_arg, universal_newlines=True)

                stdout, stderr = process_gene.communicate()
                # output_stdout += chr + "\n"
                output_stdout += stdout
                output_stderr += stderr
                process_gene.wait()
                bam_file_names.append(bam_file.description)
        response_data = {"output_stdout": output_stdout, "output_stderr": output_stderr,
                         "bam_file_names": bam_file_names}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


# if analysis_object.analysis_type == "pipeline":
#     cwd_arg = settings.MEDIA_ROOT + "/CNVKit/cnvkit_pipeline/" + analysis_id
#     else:
# --------------------------------------Reference----------------------------------------------------------

# ToDo create a log_file for Reference

@login_required
def metrics(request):
    fs = FileSystemStorage()
    analysis_id = request.GET["analysis_id"]
    analysis_results = Analysis.objects.get(user=request.user, analysis_id=analysis_id)
    cnr_arg = ""
    cns_arg = ""

    for bam_files in analysis_results.bam_files.all():
        cnr_object = CopyNumberRatio.objects.get(description=str(bam_files.description)[:-4] + ".cnr",
                                                 analysis_run=analysis_results.id)
        cns_object = CopyNumberSegment.objects.get(description=str(bam_files.description)[:-4] + ".cns",
                                                   analysis_run=analysis_results.id)
        cnr_arg += cnr_object.description + " "
        cns_arg += cns_object.description + " "

    command_met = 'cnvkit.py metrics %s -s %s' % (cnr_arg, cns_arg)
    print(command_met)
    process = subprocess.Popen(command_met.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               cwd=fs.path("CNVKit/Batch/" + analysis_results.analysis_id),
                               universal_newlines=True)  # , text=True
    stdout_met, stderr_met = process.communicate()
    process.wait()
    response_data = {'response_out': stdout_met, 'response_err': stderr_met}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def sex_batch(request):
    fs = FileSystemStorage()
    analysis_id = request.GET["analysis_id"]
    analysis_results = Analysis.objects.get(user=request.user, analysis_id=analysis_id)
    tar_arg = ""
    anti_arg = ""
    for bam_files in analysis_results.bam_files.all():
        tar_cov_object = TargetCoverage.objects.get(description=str(bam_files.description)[:-4] + ".targetcoverage.cnn",
                                                    analysis_run__analysis_id=analysis_results.analysis_id)
        antitar_cov_object = AntiTargetCoverage.objects.get(
            description=str(bam_files.description)[:-4] + ".antitargetcoverage.cnn",
            analysis_run__analysis_id=analysis_results.analysis_id)
        tar_arg += tar_cov_object.description + " "
        anti_arg += antitar_cov_object.description + " "

    command_sex = "cnvkit.py sex %s %s" % (tar_arg, anti_arg)
    process = subprocess.Popen(command_sex.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               cwd=fs.path("CNVKit/Batch/" + analysis_results.analysis_id), universal_newlines=True)

    stdout_sex, stderr_sex = process.communicate()
    process.wait()

    response_data = {'response_out': stdout_sex, 'response_err': stderr_sex}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def pooled_reference(request):
    if request.method == "POST":
        fs = FileSystemStorage()
        analysis_id = request.POST["analysis_id"]
        analysis_object = Analysis.objects.get(user=request.user, analysis_id=analysis_id)
        ref_form = PooledReference(request.POST, request.FILES)
        fasta_form = FastaForm(request.POST, request.FILES)
        if ref_form.is_valid() & fasta_form.is_valid():
            ref_name = ref_form.cleaned_data['ref_Name']
            now = datetime.now()
            result_time = str(now.strftime("%Y-%m-%d_%H-%M-%S"))
            reference_description = ref_name + "_" + result_time + ".cnn"
            chr_sex = ref_form.cleaned_data['chromosomal_sex']
            if chr_sex == "X":
                sex_arg = '--gender x'
            elif chr_sex == "Y":
                sex_arg = '--gender y'

            fasta_file = FastaFile.objects.get(description=fasta_form.cleaned_data["fasta_choice"])

            # print(request.POST)
            cnn_list = ref_form.cleaned_data["choose_cnn"]
            target_coverage_arg = ""
            antitarget_coverage_arg = ""
            ref_out_arg = settings.MEDIA_ROOT + "/CNVKit/Reference_files/" + reference_description

            reference_object = Reference(description=reference_description, user=request.user, chr_sex=chr_sex,
                                         type="batch")
            reference_object.save()
            reference_object.reference_document = "CNVKit/Reference_files/" + reference_description
            reference_object.save()

            for t_object in cnn_list:
                target_coverage_arg += t_object.description + " "
                # a_object = AntiTargetCoverage.objects.get(description=)
                antitarget_coverage_arg += t_object.description[:-18] + "antitargetcoverage.cnn" + " "
                bam_object = BamFile.objects.get(description=t_object.description[:-18] + "bam")
                reference_object.bam_files.add(bam_object)
                # reference_object.save()
            command_reference = "cnvkit.py reference %s %s -f %s %s -o %s" % (target_coverage_arg,
                                                                           antitarget_coverage_arg,
                                                                           fasta_file.fasta_document.path, sex_arg,
                                                                           ref_out_arg)
            print(command_reference)
            process_ref = subprocess.Popen(command_reference.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           cwd=fs.path("CNVKit/Batch/" + analysis_object.analysis_id),
                                           universal_newlines=True)

            stdout, stderr = process_ref.communicate()
            process_ref.wait()

            reference_object.reference_document = "CNVKit/Reference_files/" + reference_description
            reference_object.save()

            response_data = {"stdout": stdout, "stderr": stderr, "reference_name": reference_description}
            return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def reference_view(request, analysis_id=None):
    if Analysis.objects.filter(user=request.user, analysis_type="reference"):
        if analysis_id:
            analysis_result = Analysis.objects.get(user=request.user, analysis_id=analysis_id)
        else:
            analysis_result = Analysis.objects.filter(user=request.user, analysis_type="reference").latest("created_at")
        # for result in analysis_results:
        scatter_results = Scatter.objects.filter(analysis_run__analysis_id=analysis_result.analysis_id)

        context = {"analysis_results": analysis_result,
                   "scatter_results": scatter_results}
        ref_form = PooledReference()
        ref_form.fields["choose_cnn"].queryset = TargetCoverage.objects.filter(
            analysis_run__analysis_id=analysis_result.analysis_id)
        fasta_form = FastaForm()
        context["ref_form"] = ref_form
        context["fasta_form"] = fasta_form
        return render(request, "cnv_app/reference.html", context)
    else:
        return redirect("batch")


def delete_reference_file(request):
    if request.method == 'DELETE':
        fs = FileSystemStorage()
        reference_object = Reference.objects.get(
            pk=int(QueryDict(request.body).get('referencepk')))
        # print(analysis_object.description)
        reference_object.delete()
        response_data = {}
        response_data['msg'] = 'Reference object was deleted.'
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )



# --------------------------------SavvyCNV------------------------------------


# savvy_tool_dir = settings.STATIC_ROOT + "/savvyCNV/SavvySuite-master/"
# htsjdk_dir = settings.STATIC_ROOT + "/savvyCNV/htsjdk-2.21.2-8-gbd1b739-SNAPSHOT.jar"
# jama_dir = settings.STATIC_ROOT + "/savvyCNV/Jama-1.0.3.jar"
#
#
# @login_required
# def coverageBinner(request):
#     if request.method == 'POST':
#         analysis_id = request.POST["analysis_id"]
#         analysis_object = SavvyAnalysis.objects.get(analysis_id=analysis_id, user=request.user)
#         bam_form = Bam_Files_Form(request.POST, request.FILES)
#         if bam_form.is_valid():
#             bam_files = request.FILES.getlist("bam_Files")
#             for file in bam_files:
#                 if BamFile.objects.filter(description=file.name):
#                     bam_single_file = BamFile.objects.get(description=file.name)
#                 else:
#                     bam_single_file = BamFile()
#                     bam_single_file.description = file.name
#                     bam_single_file.bam_document = file
#                     bam_single_file.save()
#                 arg_bam = settings.MEDIA_ROOT + "/" + bam_single_file.bam_document.name
#                 cov_name = bam_single_file.description + ".coverageBinner"
#                 cov_arg = settings.MEDIA_ROOT + "/savvyCNV/" + analysis_id + "/" + cov_name
#                 command ="java -cp %s:%s:%s -Xmx1g CoverageBinner %s > %s" % (htsjdk_dir, savvy_tool_dir, jama_dir, arg_bam, cov_arg)
#                 # print(command)
#                 process_cov_bin = subprocess.Popen(command, cwd=savvy_tool_dir, universal_newlines=True, shell=True)
#                 process_cov_bin.wait()
#                 # create the coverageBinner objects
#                 if CoverageBinner.objects.filter(description=cov_name, analysis_run=analysis_object):
#                     pass
#                 else:
#                     covBinner_object = CoverageBinner(description=cov_name)
#                     covBinner_object.save()
#                     covBinner_object.bam_file_savvy = bam_single_file
#                     covBinner_object.save()
#                     covBinner_object.analysis_run = analysis_object
#                     covBinner_object.save()
#                     covBinner_object.document = "savvyCNV/" + analysis_id + "/" + cov_name
#                     covBinner_object.save()
#                 analysis_object.bam_files_savvy.add(bam_single_file)
#         response_data = {"response": "Coverage summary file successfully created" }
#         return HttpResponse(json.dumps(response_data), content_type="application/json")
#
#
# @login_required
# def savvyAnalysis(request):
#     if request.method == 'POST':
#         savvy_form = SavvyCNVForm(request.POST, request.FILES)
#         if savvy_form.is_valid():
#             analysis_id = request.POST["analysis_id"]
#             analysis_object = SavvyAnalysis.objects.get(analysis_id=analysis_id, user=request.user)
#             cov_bin_list = savvy_form.cleaned_data["coverage_binner"]
#             size = savvy_form.cleaned_data['size']
#             cov_bin_arg = ""
#             savvy_object_name = "cnv_list_" + analysis_id + ".csv"
#             cnv_list_arg = settings.MEDIA_ROOT + "/savvyCNV/" + analysis_id +"/" +savvy_object_name
#             cnv_log_arg = settings.MEDIA_ROOT + "/savvyCNV/" + analysis_id +"/" + "log_messages.txt"
#             for cov_bin in cov_bin_list:
#                 cov_bin_arg += cov_bin.document.path + " "
#             command = "java -cp %s:%s:%s -Xmx30g SavvyCNV -data -sv 1 -d %s %s >%s 2>%s" % (htsjdk_dir, savvy_tool_dir, jama_dir,
#                                                 size, cov_bin_arg, cnv_list_arg, cnv_log_arg)
#             process_savvy = subprocess.Popen(command, cwd=savvy_tool_dir, universal_newlines=True, shell=True)
#             process_savvy.wait()
#             savvy_object = SavvyCNV(description=savvy_object_name, d_size=size)
#             savvy_object.save()
#             savvy_object.analysis_run = analysis_object
#             savvy_object.save()
#             for cov_bin in cov_bin_list:
#                 savvy_object.coverage_files.add(cov_bin)
#             savvy_object.save()
#             savvy_object.document = "savvyCNV/" + analysis_id +"/cnv_list.csv"
#             savvy_object.save()
#         response_data = {"response": "Coverage summary file successfully created"}
#         return HttpResponse(json.dumps(response_data), content_type="application/json")
#
#
# @login_required
# def savvyControlAnalysis(request):
#     if request.method == 'POST':
#         savvy_form = SavvyCNVForm(request.POST)
#         if savvy_form.is_valid():
#
#             analysis_id = request.POST["analysis_id"]
#             analysis_object = SavvyAnalysis.objects.get(analysis_id=analysis_id, user=request.user)
#             cov_bin_list = savvy_form.cleaned_data["coverage_binner"]
#             size = savvy_form.cleaned_data['size']
#             cov_bin_arg = ""
#             savvy_object_name = "cnv_list_" + analysis_id + "_summary_file"
#             cnv_list_arg = settings.MEDIA_ROOT + "/savvyCNV/" + analysis_id + "/" +savvy_object_name
#             for cov_bin in cov_bin_list:
#                 cov_bin_arg += cov_bin.document.path + " "
#             command = "java -cp %s:%s:%s -Xmx30g SelectControlSamples -d %s %s >%s" % (htsjdk_dir, savvy_tool_dir, jama_dir,
#                                                 size, cov_bin_arg, cnv_list_arg)
#             # print(command)
#             process_savvy = subprocess.Popen(command, cwd=savvy_tool_dir, universal_newlines=True, shell=True)
#             process_savvy.wait()
#             savvy_object = SavvySelectCNV(description=savvy_object_name, d_size=size)
#             savvy_object.save()
#             savvy_object.analysis_run = analysis_object
#             for cov_bin in cov_bin_list:
#                 savvy_object.coverage_files.add(cov_bin)
#             savvy_object.document = "savvyCNV/" + analysis_id +"/cnv_list.csv"
#             savvy_object.save()
#             response_data = {"response": "Summaryfile successfully created"}
#             return HttpResponse(json.dumps(response_data), content_type="application/json")
#
# @login_required
# def savvy_results(request):
#     savvy_results = SavvyAnalysis.objects.filter(user=request.user).order_by("-created_at")
#     context = {"savvy_results": savvy_results}
#     return render(request, "cnv_app/savvy_results.html", context)
#
#
# def delete_savvy_analysis(request):
#     if request.method == 'DELETE':
#         fs = FileSystemStorage()
#         analysis_object = SavvyAnalysis.objects.get(
#             pk=int(QueryDict(request.body).get('analysispk')))
#         analysis_object.delete()
#         shutil.rmtree(fs.path("savvyCNV/" + analysis_object.analysis_id))
#         response_data = {'msg': 'Analysis object was deleted.'}
#         return HttpResponse(
#             json.dumps(response_data),
#             content_type="application/json"
#         )
#
# @login_required
# def savvy_overview(request):
#     return render(request, "cnv_app/savvy_overview.html",)
#
# @login_required
# def savvycnv_view(request, analysis_id=None):
#     if SavvyAnalysis.objects.filter(user=request.user):
#         if analysis_id:
#             analysis_object = SavvyAnalysis.objects.get(user=request.user, analysis_id=analysis_id)
#         else:
#             analysis_object = SavvyAnalysis.objects.filter(user=request.user).latest("created_at")
#     else:
#         now = datetime.now()
#         analysis_time = str(now.strftime("%Y-%m-%d_%H-%M-%S"))
#         analysis_id = analysis_time + "_" + request.user.username
#         process_create_folder = "mkdir " + analysis_id
#         process_create_file = subprocess.Popen(process_create_folder.split(),
#                                                cwd=settings.MEDIA_ROOT + "/savvyCNV", universal_newlines=True)
#         process_create_file.wait()
#         analysis_object = SavvyAnalysis(analysis_id=analysis_id, user=request.user)
#         analysis_object.save()
#
#     bam_form = Bam_Files_Form()
#     savvy_form = SavvyCNVForm()
#     savvy_form.fields["coverage_binner"].queryset = CoverageBinner.objects.filter(analysis_run=analysis_object)
#     return render(request, "cnv_app/savvycnv.html", {
#         "bam_form": bam_form,
#         "savvy_form": savvy_form,
#         "analysis_object": analysis_object
#     })


# -------------------------------------- Pipeline ----------------------------------------


@login_required  # view
def pipeline_view(request, analysis_id=None):
    if Analysis.objects.filter(user=request.user, analysis_type="pipeline"):
        if analysis_id:
            analysis_object = Analysis.objects.get(analysis_id=analysis_id, user=request.user)
        else:
            analysis_object = Analysis.objects.filter(analysis_type="pipeline", user=request.user).order_by(
                '-created_at').first()
        bed_form = BedForm()  # Autobin,
        bam_form = Bam_Files_Form()  # Autobin, Reference
        fasta_form = FastaForm()  # Reference
        rest_Autobin = Autobin()
        rest_Reference = PooledReference()  # Reference
        # rest_Reference.fields["choose_cnn"].queryset = TargetCoverage.objects.filter(
        #    analysis_run__analysis_id=analysis_object.analysis_id)
        # analysis_object = Analysis.objects.filter(user=request.user).order_by(
        #    "created_at").first()
        coverage_form = Coverage()
        # coverage_form.fields['choose_bamFile'].queryset = analysis_object.bam_files.all()
        fix_form = Fix()
        fix_form.fields["reference_choice"].queryset = Reference.objects.filter(user=request.user)
        seg_form = Segment()
        call_form = Call()
        context = {'bed_form': bed_form, 'bam_form': bam_form,
                   'fasta_form': fasta_form, 'rest_Reference': rest_Reference,
                   'rest_Autobin': rest_Autobin, 'coverage_form': coverage_form,
                   'fix_form': fix_form, 'seg_form': seg_form, 'call_form': call_form,
                   'analysis_object': analysis_object}
        # return render(request, 'cnv_app/cnvkit_pipeline.html', context)
    else:
        bed_form = BedForm()  # Autobin,
        bam_form = Bam_Files_Form()  # Autobin, Reference
        fasta_form = FastaForm()  # Reference
        rest_Autobin = Autobin()
        rest_Reference = PooledReference()  # Reference
        coverage_form = Coverage()
        fix_form = Fix()
        fix_form.fields["reference_choice"].queryset = Reference.objects.filter(user=request.user)
        seg_form = Segment()
        call_form = Call()
        context = {'bed_form': bed_form, 'bam_form': bam_form,
                   'fasta_form': fasta_form, 'rest_Reference': rest_Reference,
                   'rest_Autobin': rest_Autobin, 'coverage_form': coverage_form,
                   'fix_form': fix_form, 'seg_form': seg_form, 'call_form': call_form,
                   }  # 'analysis_object': analysis_object
    return render(request, 'cnv_app/cnvkit_pipeline.html', context)


def start(request):
    if request.method == "GET":
        fs = FileSystemStorage()
        now = datetime.now()
        result_time = str(now.strftime("%Y-%m-%d_%H-%M-%S"))
        pipeline_name = result_time + "_" + request.user.username
        # if fs.path("CNVKit/cnvkit_pipeline/" + pipeline_name):
        #     command_del = "rm -r " + pipeline_name
        #     process_del = subprocess.Popen(command_del.split(), cwd=fs.path("CNVKit/cnvkit_pipeline/"))
        #     process_del.wait()
        command_mkdir = "mkdir " + pipeline_name
        process_mkdir = subprocess.Popen(command_mkdir.split(), cwd=fs.path("CNVKit/cnvkit_pipeline"))
        process_mkdir.wait()
        analysis_object = Analysis(analysis_id=pipeline_name, analysis_type="pipeline")
        analysis_object.user = request.user
        analysis_object.save()
        response_data = {'analysis_id': analysis_object.analysis_id}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def autobin(request):
    analysis_id = request.POST["analysis_id"]
    fs = FileSystemStorage()
    pipeline_object = Analysis.objects.get(user=request.user, analysis_id=analysis_id)
    # user=request.user, analysis_type="pipeline"
    pipeline_folder = pipeline_object.analysis_id
    # print(pipeline_folder)
    rest_autobin = Autobin(request.POST, request.FILES)
    bam_form = Bam_Files_Form(request.POST, request.FILES)
    bed_form = BedForm(request.POST, request.FILES)
    if rest_autobin.is_valid() & bam_form.is_valid() & bed_form.is_valid():
        # adding bam files to bam objects
        bam_files = request.FILES.getlist("bam_Files")
        arg_bam = ""
        for file in bam_files:
            if BamFile.objects.filter(description=file.name):
                bam_single_file = BamFile.objects.get(description=file.name)
                arg_bam += bam_single_file.bam_document.path + " "
                bam_single_file.seq_protocol = rest_autobin.cleaned_data["method"]
                bam_single_file.save()
                pipeline_object.bam_files.add(bam_single_file)
            else:
                bam_single_file = BamFile()
                bam_single_file.description = file.name
                bam_single_file.bam_document = file
                bam_single_file.save()
                arg_bam += bam_single_file.bam_document.path + " "
                bam_single_file.seq_protocol = rest_autobin.cleaned_data["method"]
                bam_single_file.save()
                pipeline_object.bam_files.add(bam_single_file)

        # Handle Bed File Upload or missing
        # bed_file = bed_form.save(commit=False)
        if request.FILES.getlist("bed_document"):
            if BedFile.objects.filter(description=str(request.FILES["bed_document"].name)):
                bed_file = BedFile.objects.get(description=request.FILES["bed_document"].name)
            else:
                bed_file = bed_form.save(commit=False)
                bed_file.description = request.FILES["bed_document"].name
                bed_file.save()
        else:
            bed_file = BedFile.objects.get(description="TST500C_manifest.bed")
        pipeline_object.bed_file = bed_file
        pipeline_object.save()
        # access_arg = sfs.path('cnv_app/access_file/access-5k-mappable.hg19.bed')
        if rest_autobin.cleaned_data['bp_per_bin']:
            bp_per_bin = rest_autobin.cleaned_data['bp_per_bin']
            command = "cnvkit.py autobin %s -t %s -b %s" % (
                arg_bam, bed_file.bed_document.path, bp_per_bin)  # ToDo -g %s
        else:
            command = "cnvkit.py autobin %s -t %s " % (arg_bam, bed_file.bed_document.path)  # ToDo -g %s
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd=fs.path("CNVKit/cnvkit_pipeline/" + pipeline_folder),
                                   universal_newlines=True)
        process.wait()
        output_autobin, output_err_autobin = process.communicate()
        # write log file for Target&Antitarget Bed File
        log_file_name = pipeline_object.analysis_id + ".txt"
        log_path = "CNVKit/cnvkit_pipeline/" + pipeline_folder + "/" + log_file_name
        autobin_log = open(settings.MEDIA_ROOT + "/" + log_path, "w+")
        autobin_log.write(output_autobin)
        autobin_log.write(output_err_autobin)
        autobin_log.close()
        pipeline_object.log_file = log_path
        pipeline_object.save()
        for file_name in os.listdir(fs.path("CNVKit/cnvkit_pipeline/" + pipeline_folder)):
            f_path = "CNVKit/cnvkit_pipeline/" + pipeline_folder + "/" + file_name
            if file_name.endswith(".antitarget.bed"):
                if AntiTargetBed.objects.filter(analysis_run=pipeline_object).exists():
                    pass
                else:
                    antitarget_bed_object = AntiTargetBed(description=file_name)
                    antitarget_bed_object.save()
                    if rest_autobin.cleaned_data["bp_per_bin"]:
                        antitarget_bed_object.r_b_m_b = rest_autobin.cleaned_data["bp_per_bin"]
                    else:
                        antitarget_bed_object.r_b_m_b = 100000
                    antitarget_bed_object.anti_target_bed_document = f_path
                    antitarget_bed_object.analysis_run = pipeline_object
                    antitarget_bed_object.save()
                # f.close()
                # fs.delete(file_name)
            if file_name.endswith(".target.bed"):
                if TargetBed.objects.filter(analysis_run=pipeline_object).exists():
                    pass
                else:
                    target_bed_object = TargetBed(description=file_name)
                    target_bed_object.save()
                    if rest_autobin.cleaned_data["bp_per_bin"]:
                        target_bed_object.r_b_m_b = rest_autobin.cleaned_data["bp_per_bin"]
                    else:
                        target_bed_object.r_b_m_b = 100000
                    target_bed_object.target_bed_document = f_path
                    target_bed_object.analysis_run = pipeline_object
                    target_bed_object.save()

        response_data = {'output_autobin': output_autobin, 'output_err_autobin': output_err_autobin, }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
        #


def coverage(request):
    analysis_id = request.POST["analysis_id"]
    fs = FileSystemStorage()
    pipeline_object = Analysis.objects.get(user=request.user,
                                           analysis_id=analysis_id)  # user=request.user, analysis_type="pipeline"
    pipeline_folder = pipeline_object.analysis_id
    coverage_form = Coverage(request.POST, request.FILES)
    target_object = TargetBed.objects.get(analysis_run=pipeline_object)
    antitarget_object = AntiTargetBed.objects.get(analysis_run=pipeline_object)
    target_arg = target_object.target_bed_document.path
    antitarget_arg = antitarget_object.anti_target_bed_document.path
    if coverage_form.is_valid():
        if coverage_form.cleaned_data["use_count"]:
            use_count_arg = "-c"
        else:
            use_count_arg = ""
        all_out_a = ""
        all_out_t = ""
        for bam_object in pipeline_object.bam_files.all():
            if coverage_form.cleaned_data["MIN_MAPQ"]:
                command_t = "cnvkit.py coverage %s -q %s %s %s" % (use_count_arg,
                                                                   coverage_form.cleaned_data["MIN_MAPQ"],
                                                                   bam_object.bam_document.path,
                                                                   target_arg)
                command_a = "cnvkit.py coverage %s -q %s %s %s" % (use_count_arg,
                                                                   coverage_form.cleaned_data["MIN_MAPQ"],
                                                                   bam_object.bam_document.path,
                                                                   antitarget_arg)
            else:
                command_t = "cnvkit.py coverage %s %s %s" % (use_count_arg,
                                                             bam_object.bam_document.path, target_arg)
                command_a = "cnvkit.py coverage %s %s %s" % (use_count_arg,
                                                             bam_object.bam_document.path, antitarget_arg)
            process_t = subprocess.Popen(command_t.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         cwd=fs.path("CNVKit/cnvkit_pipeline/" + pipeline_folder),
                                         universal_newlines=True)
            process_a = subprocess.Popen(command_a.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         cwd=fs.path("CNVKit/cnvkit_pipeline/" + pipeline_folder),
                                         universal_newlines=True)
            process_t.wait()
            process_a.wait()
            output_cov_t, output_err_cov_t = process_t.communicate()
            output_cov_a, output_err_cov_a = process_a.communicate()
            all_out_t += output_cov_t
            all_out_a += output_cov_a
            coverage_log = open(pipeline_object.log_file.path, "a")
            coverage_log.write("\n# COVERAGE Target\n")
            coverage_log.write(output_err_cov_t + "\n")
            coverage_log.write("# COVERAGE Antitarget\n")
            coverage_log.write(output_err_cov_a)
            coverage_log.close()

        for file_name in os.listdir(fs.path("CNVKit/cnvkit_pipeline/" + pipeline_folder)):
            f_path = "CNVKit/cnvkit_pipeline/" + pipeline_folder + "/" + file_name
            if file_name.endswith(".antitargetcoverage.cnn"):
                if AntiTargetCoverage.objects.filter(analysis_run=pipeline_object,
                                                     anti_target_coverage_document=f_path).exists():
                    pass
                else:
                    antitarget_cov_object = AntiTargetCoverage(description=file_name,
                                                               anti_target_coverage_document=f_path)
                    antitarget_cov_object.save()
                    antitarget_cov_object.min_mapq = coverage_form.cleaned_data["MIN_MAPQ"]
                    antitarget_cov_object.count = coverage_form.cleaned_data["use_count"]
                    antitarget_cov_object.save()
                    antitarget_cov_object.analysis_run = pipeline_object
                    antitarget_cov_object.save()
                    # f.close()
                    # fs.delete(file_name)
            if file_name.endswith(".targetcoverage.cnn"):
                if TargetCoverage.objects.filter(analysis_run=pipeline_object,
                                                 target_coverage_document=f_path).exists():
                    pass
                else:
                    target_cov_object = TargetCoverage(description=file_name, target_coverage_document=f_path)
                    target_cov_object.save()
                    target_cov_object.min_mapq = coverage_form.cleaned_data["MIN_MAPQ"]
                    target_cov_object.count = coverage_form.cleaned_data["use_count"]
                    target_cov_object.save()
                    target_cov_object.analysis_run = pipeline_object
                    target_cov_object.save()

        response_data = {'output_cov_a': all_out_a, 'parsed_output_err_cov_a': output_err_cov_a,
                         'output_cov_t': all_out_t, 'parsed_output_err_cov_t': output_err_cov_t}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


# if parsed output is desired ToDo
def sex_pipeline(request):
    fs = FileSystemStorage()
    # analysis_results = Analysis.objects.filter(user=request.user, analysis_type="reference").latest("created_at")
    analysis_id = request.GET["analysis_id"]
    analysis_results = Analysis.objects.get(user=request.user, analysis_id=analysis_id)
    tar_arg = ""
    anti_arg = ""
    for bam_files in analysis_results.bam_files.all():
        tar_cov_object = TargetCoverage.objects.get(description=str(bam_files.description)[:-4] + ".targetcoverage.cnn",
                                                    analysis_run__analysis_id=analysis_results.analysis_id)
        antitar_cov_object = AntiTargetCoverage.objects.get(
            description=str(bam_files.description)[:-4] + ".antitargetcoverage.cnn",
            analysis_run__analysis_id=analysis_results.analysis_id)
        tar_arg += tar_cov_object.description + " "
        anti_arg += antitar_cov_object.description + " "

    command_sex = "cnvkit.py sex %s %s" % (tar_arg, anti_arg)
    process = subprocess.Popen(command_sex.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               cwd=fs.path("CNVKit/cnvkit_pipeline/" + analysis_results.analysis_id),
                               universal_newlines=True)

    stdout_sex, stderr_sex = process.communicate()
    process.wait()

    response_data = {'response_out': stdout_sex, 'response_err': stderr_sex}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def reference_pipeline(request):
    # print(request.POST)
    analysis_id = request.POST["analysis_id"]
    analysis_object = Analysis.objects.get(user=request.user, analysis_id=analysis_id)
    if request.method == "POST":
        fs = FileSystemStorage()
        ref_form = PooledReference(request.POST, request.FILES)
        fasta_form = FastaForm(request.POST, request.FILES)
        # cnn_arg =
        if ref_form.is_valid() & fasta_form.is_valid():
            # print("is_valid")
            ref_name = ref_form.cleaned_data['ref_Name']
            now = datetime.now()
            result_time = str(now.strftime("%Y-%m-%d_%H-%M-%S"))
            reference_description = ref_name + "_" + result_time + ".cnn"
            chr_sex = ref_form.cleaned_data['chromosomal_sex']
            if chr_sex == "X":
                sex_arg = '--gender x'
            else:
                sex_arg = '--gender y'
            if 'fasta_File' in request.FILES.keys():
                if FastaFile.objects.filter(description=str(request.FILES["fasta_document"].name)):
                    fasta_file = FastaFile.objects.get(description=request.FILES["fasta_document"].name)
                else:
                    fasta_file = fasta_form.save(commit=False)
                    fasta_file.description = request.FILES["fasta_document"].name  # + "_" + batch_object.batch_id
                    fasta_file.save()
            else:
                fasta_file = FastaFile.objects.get(description="hg19.fa")
            # print(request.POST)
            cnn_list = ref_form.cleaned_data["choose_cnn"]
            target_coverage_arg = ""
            antitarget_coverage_arg = ""
            ref_out_arg = settings.MEDIA_ROOT + "/CNVKit/Reference_files/" + reference_description

            reference_object = Reference(description=reference_description, user=request.user, chr_sex=chr_sex)
            reference_object.save()

            for t_object in cnn_list:
                target_coverage_arg += t_object.description + " "
                # a_object = AntiTargetCoverage.objects.get(description=)
                antitarget_coverage_arg += t_object.description[:-18] + "antitargetcoverage.cnn" + " "
                bam_object = BamFile.objects.get(description=t_object.description[:-18] + "bam")
                reference_object.bam_files.add(bam_object)
                # reference_object.save()
            command_reference = "cnvkit.py reference %s %s -f %s %s -o %s" % (target_coverage_arg,
                                                                              antitarget_coverage_arg,
                                                                              fasta_file.fasta_document.path, sex_arg,
                                                                              ref_out_arg)
            process_ref = subprocess.Popen(command_reference.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           cwd=fs.path("CNVKit/cnvkit_pipeline/" + analysis_object.analysis_id),
                                           universal_newlines=True)

            stdout, stderr = process_ref.communicate()
            process_ref.wait()

            reference_object.reference_document = "CNVKit/Reference_files/" + reference_description
            reference_object.save()

            response_data = {"stdout": stdout, "stderr": stderr}
            return HttpResponse(json.dumps(response_data), content_type="application/json")


def fix(request):
    analysis_id = request.POST["analysis_id"]
    pipeline_object = Analysis.objects.get(user=request.user, analysis_id=analysis_id)
    fix_form = Fix(request.POST, request.FILES)
    if fix_form.is_valid():
        ref_arg = fix_form.cleaned_data['reference_choice']
        working_dir = settings.MEDIA_ROOT + "/CNVKit/cnvkit_pipeline/" + pipeline_object.analysis_id
        standard_out = ""
        standard_err = ""
        for bam_file in pipeline_object.bam_files.all():
            target_name = bam_file.description[:-4] + ".targetcoverage.cnn"
            antitarget_name = bam_file.description[:-4] + ".antitargetcoverage.cnn"
            # print(pipeline_object)
            target_arg = TargetCoverage.objects.get(analysis_run=pipeline_object, description=target_name)
            antitarget_arg = AntiTargetCoverage.objects.get(analysis_run=pipeline_object, description=antitarget_name)
            output_name = bam_file.description[:-4] + ".cnr"
            command = "cnvkit.py fix %s %s %s -o %s" % (
                target_arg.description, antitarget_arg.description, ref_arg.reference_document.path, output_name)
            process_fix = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           cwd=settings.MEDIA_ROOT + "/CNVKit/cnvkit_pipeline/" + pipeline_object.analysis_id,
                                           universal_newlines=True)
            # print(command)
            # print(working_dir)
            process_fix.wait()
            stdout, stderr = process_fix.communicate()
            standard_out += stdout
            standard_err += stderr
            copy_ratio_object = CopyNumberRatio(description=output_name,
                                                copy_number_document="CNVKit/cnvkit_pipeline/" + pipeline_object.analysis_id + "/" + output_name)
            copy_ratio_object.save()
            copy_ratio_object.analysis_run = pipeline_object
            copy_ratio_object.save()
        # response = "Fix on "
        # for f in bam_files:
        #     response += f + ", "
        # response += "is finished!"
        response_data = {'response': standard_out, 'stderr': standard_err}
        return HttpResponse(json.dumps(response_data), content_type="application/json")



def segment(request):
    seg_form = Segment(request.POST)
    if seg_form.is_valid():
        method_arg = seg_form.cleaned_data['segmentation_method']
        cwd_val = "cnv_app/segment_CNS/" + method_arg
        sfs = StaticFilesStorage()
        cnr_path = sfs.path('cnv_app/fix_CNR')
        cnr_files = os.listdir(cnr_path)
        for cnr in cnr_files:
            cnr_file = sfs.path('cnv_app/fix_CNR/' + cnr)
            command = "cnvkit.py segment -m %s %s " % (method_arg, cnr_file)
            proces_seg = subprocess.Popen(command.split(), cwd=sfs.path(cwd_val), universal_newlines=True)
            proces_seg.communicate()
        response = "Segmentation with " + method_arg + " is finished!"
        response_data = {'response': response}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


