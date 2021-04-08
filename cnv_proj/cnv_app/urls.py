from django.urls import path, include
from django.conf import settings  # This is only for Debug Mode
from django.conf.urls.static import static  # This is only for Debug Mode too!

from . import views

urlpatterns = [

    path("accounts/", include("django.contrib.auth.urls")),

    path("home/", views.home, name="home"),
    path("register/", views.register, name="register"),
    # Dropzone
    path('fileupload/', views.handle_bam_upload, name="fileupload"),

    # path("bam_upload/", views.upload_file_batch, name="bam_upload"),

    path("batch/upload/", views.batch, name="batch"),
    path("batch/result/<str:analysis_id>/", views.view_batch_result, name="batch_result_id"),
    path("batch/result/", views.view_batch_result, name="batch_result"),


    path("cnvkit/", views.overview, name="cnvkit"),

    path("batch/reference/<str:analysis_id>/", views.reference_view, name="reference_view_id"),
    path("batch/reference/", views.reference_view, name="reference_view"),

    path("cnvPipeline/<str:analysis_id>/", views.pipeline_view, name="cnvkit_pipeline_id"),
    path("cnvPipeline/", views.pipeline_view, name="cnvkit_pipeline"),

    path("results/", views.results, name="results"),

    # Ajax
    # CNVKit
    path("ajax_start-pipeline/", views.start, name="ajax_start-pipeline"),
    path("ajax_autobin/", views.autobin, name="ajax_autobin"),
    path("ajax_cov/", views.coverage, name="ajax_cov"),
    path("ajax_call/", views.call, name="ajax_call"),
    path("ajax_genemetrics/", views.genemetrics, name="ajax_genemetrics"),
    path("ajax_breaks/", views.breaks, name="ajax_breaks"),

    path("ajax_met/", views.metrics, name="ajax_met"),
    path("ajax_sex_pipeline/", views.sex_pipeline, name="ajax_sex_pipeline"),
    path("ajax_sex_batch/", views.sex_batch, name="ajax_sex_batch"),
    path("ajax_ref_pipeline/", views.reference_pipeline, name="ajax_ref"),
    path("ajax_ref/", views.pooled_reference, name="ajax_ref"),

    path("ajax_fix/", views.fix, name="ajax_fix"),
    path("ajax_segment/", views.segment, name="ajax_segment"),

    path("ajax_scatter/", views.scatter, name="ajax_scatter"),
    path("ajax_diagram/", views.diagram, name="ajax_diagram"),
    path("ajax_heatmap/", views.heatmap, name="ajax_heatmap"),

    path("delete_image_ajax/", views.delete_scatter, name="delete_image_ajax"),
    path("delete_heatmap_ajax/", views.delete_heatmap, name="delete_heatmap"),
    path("delete_diagram_ajax/", views.delete_diagram, name="delete_diagram"),


    path("delete_analysis_ajax/", views.delete_analysis, name="delete_analysis_ajax"),
    path("delete_reference_file_ajax/", views.delete_reference_file, name="delete_reference_file_ajax"),

    # SavvyCNV
    # path("ajax_covBin/", views.coverageBinner, name="ajax_covBin"),
    # path("ajax_savvy/", views.savvyAnalysis, name="ajax_savvy"),
    # path("ajax_savvy_select/", views.savvyControlAnalysis, name="ajax_savvy_select"),
    #
    # path("savvycnv/", views.savvycnv_view, name="savvycnv"),
    # path("savvycnv/<str:analysis_id>/", views.savvycnv_view, name="savvycnv"),
    # path("savvy_overview/", views.savvy_overview, name="savvy_overview"),
    # path("savvy_results/", views.savvy_results, name="savvy_results"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
