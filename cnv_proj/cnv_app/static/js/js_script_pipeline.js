function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
// Setup ajax connections safetly

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function send_start(){
     $.ajax({
        url: '/ajax_start-pipeline/',
        type: 'GET',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            $("#start_result p").html("");
            $("#start_result p").prepend("The analysis id is the following: <mark id='analysis-id'>" + json.analysis_id + "</mark>");
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#start_result').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
 };

$('#start-pipeline').on('submit', function(event){
    event.preventDefault();
    send_start()
});



function send_autobin(){
var myForm = document.getElementById('autobin-form');
var formData = new FormData(myForm);
var analysis_id = document.getElementById('analysis-id').textContent;
formData.append('analysis_id', analysis_id);

$('#ajax-autobin').show();
     $.ajax({
        url: '/ajax_autobin/',
        data: formData,
        type: 'POST',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            //  console.log(json.output_autobin)
            $("#autobin_result").html("");
            $("#autobin_result").prepend("<br><h6> Recommended bin size for the submitted samples: </h6><pre>" +json.output_autobin + "</pre><pre>" +json.output_err_autobin + "</pre>");
            //$("#output_err_autobin").prepend(json.output_err_autobin);
            $('#ajax-autobin').hide();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#ajax-autobin').hide();
            $('#output_err_autobin').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
 };

$('#autobin-form').on('submit', function(event){
    event.preventDefault();
    //console.log("form submitted!")
    send_autobin()
});

function send_cov(){
var myForm = document.getElementById('cov-form');
var formData = new FormData(myForm);
var analysis_id = document.getElementById('analysis-id').textContent;
formData.append('analysis_id', analysis_id);
$('#ajax-coverage').show();
     $.ajax({
        url: '/ajax_cov/',
        data: formData,
        type: 'POST',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            console.log(json.output_autobin)
            $("#output_err_cov").html("");
            //$("#cov_result").prepend("<br><h6> Coverage antitarget</h6><pre>" +json.output_cov_a + "</pre><hr><br><h6> Coverage target</h6><pre>" +json.output_cov_t + "</pre><hr>");
            $("#output_err_cov").prepend("<br><h6> Coverage antitarget</h6><pre>" +json.parsed_output_err_cov_a + "</pre><hr><br><h6> Coverage target</h6><pre>" +json.parsed_output_err_cov_t + "</pre>");
            $('#ajax-coverage').hide();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
        $('#ajax-coverage').hide();
            $('#output_err_cov').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
 };
$('#cov-form').on('submit', function(event){
    event.preventDefault();
    //console.log("cov!")
    send_cov()
});

function send_sex(){
analysis_id = document.getElementById('analysis-id').textContent;
$('#ajax-sex').show();
     $.ajax({
        url: '/ajax_sex_pipeline/',
        type: 'GET',
        data: { 'analysis_id':analysis_id },
        // handle a successful response
        success : function(json) {
            //console.log(json.response)
            $("#sex_results").html("")
            $("#sex_results").html("<pre>" +json.response_out + "</pre><pre>" +json.response_err + "</pre>");
            $('#ajax-sex').hide();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#ajax-sex').hide();
            $('#output_err_met').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

$('#sex-form').on('submit', function(event){
    event.preventDefault();
    send_sex()
});


function send_ref_pipeline(){
var myForm = document.getElementById('ref-form');
var formData = new FormData(myForm);
var analysis_id = document.getElementById('analysis-id').textContent;
myForm.append('analysis_id', analysis_id);
$('#ajax-ref').show();
     $.ajax({
        url: '/ajax_ref_pipeline/',
        data: formData,
        type: 'POST',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            //console.log(json.response)
            $("#ref_result").html("")
            $("#ref_result").html("<pre>" +json.stdout + "</pre><pre>"+json.stderr+"</pre>");
            $('#ajax-ref').hide();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#ajax-ref').hide();
            $('#output_err_ref').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

$('#ref-form').on('submit', function(event){
    event.preventDefault();
    send_ref_pipeline()
});

function send_fix(){
var myForm = document.getElementById('fix-form');
var formData = new FormData(myForm);
var analysis_id = document.getElementById('analysis-id').textContent;
formData.append('analysis_id', analysis_id);
$('#ajax-fix').show();
     $.ajax({
        url: '/ajax_fix/',
        data: formData,
        type: 'POST',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            //console.log(json.response)
            $('#ajax-fix').hide();
            $("#fix_result").html("")
            $("#fix_result").html("<p>" +json.response + "</p>");
            $("#fix_result").html("<p>" +json.stderr + "</p>");

        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
        $('#ajax-fix').hide();
            $('#output_err_fix').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " +json.stderr +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

$('#fix-form').on('submit', function(event){
    event.preventDefault();
   // console.log("ref!")
    send_fix()
});

function send_segment(){
var myForm = document.getElementById('segment-form');
var formData = new FormData(myForm);
$('#ajax-segment').show();
     $.ajax({
        url: '/ajax_segment/',
        data: formData,
        type: 'POST',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            $('#ajax-segment').hide();
            //console.log(json.response)
            $("#segment_result").html("")
            $("#segment_result").html("<p>" +json.response + "</p>");

        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#ajax-segment').hide();
            $('#output_err_segment').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

$('#segment-form').on('submit', function(event){
    event.preventDefault();
    //console.log("seg!")
    send_segment()
});

function send_call() {
var myForm = document.getElementById('call-form');
var formData = new FormData(myForm);
    $('#ajax-call').show();
     $.ajax({
        url: '/ajax_call/',
        type : "POST", // http method
        data: formData,
        dataType: 'json',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            //$('#purity-text').val(''); // remove the value from the input
            $("#call_results").html("")
            $("#call_results").prepend("<p>"+json.response+"</p>");
            $('#ajax-call').hide();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#ajax-call').hide();
            $('#call_results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

$('#call-form').on('submit', function(event){
    event.preventDefault();
    // sanity check console.log("form submitted!")
    send_call()
});


