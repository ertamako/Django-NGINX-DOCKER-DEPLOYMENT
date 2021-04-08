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

function send_met(){
analysis_id = document.getElementById('analysis-id').textContent
$('#ajax-met').show();
     $.ajax({
        url: '/ajax_met/',
        type: 'GET',
        data: {'analysis_id': analysis_id},
        // handle a successful response
        success : function(json) {
            //console.log(json.response)
            $("#met_results").html("")
            $("#met_results").html("<pre>" +json.response_out + "</pre><pre>" +json.response_err + "</pre>");
            $('#ajax-met').hide();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#ajax-met').hide();
            $('#output_err_met').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}
$('#met-form').on('submit', function(event){
    event.preventDefault();
   // console.log("ref!")
    send_met()
});

function send_sex(){
analysis_id = document.getElementById('analysis-id').textContent;
$('#ajax-sex').show();
     $.ajax({
        url: '/ajax_sex_batch/',
        type: 'GET',
        data: {'analysis_id': analysis_id},
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


function send_ref(){
var myForm = document.getElementById('ref-form');
var formData = new FormData(myForm);
var analysis_id = document.getElementById('analysis-id').textContent;
formData.append('analysis_id', analysis_id);
$('#ajax-ref').show();
     $.ajax({
        url: '/ajax_ref/',
        data: formData,
        type: 'POST',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            //console.log(json.response)
            $("#ref_result").html("")
            $("#ref_result").html("<p> Reference " + json.reference_name + " was created!</p>");
            //$("#ref_result").html("<pre>" +json.stdout + "</pre><pre>"+json.stderr+"</pre>");
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
    send_ref()
});
