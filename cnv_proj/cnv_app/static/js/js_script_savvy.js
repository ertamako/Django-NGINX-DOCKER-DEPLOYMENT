
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


// SavvyCNV

function send_covBin(){
var myForm = document.getElementById("coverageBinner-form");
var analysis_id = document.getElementById('analysis-id').textContent;
var formData = new FormData(myForm);
formData.append('analysis_id', analysis_id);
    $('#ajax-cov').show();
     $.ajax({
        url: '/ajax_covBin/',
        type : "POST", // http method
        data: formData,
        dataType: 'json',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            $("#cov_results").html("")
            $("#cov_results").prepend("<p>"+ json.response +"</p>");
            $('#ajax-cov').hide();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#ajax-cov').hide();
            $('#cov_results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

$('#coverageBinner-form').on('submit', function(event){
    event.preventDefault();
    send_covBin()
});

function send_savvy(){
var myForm = document.getElementById("savvy-form");
var analysis_id = document.getElementById('analysis-id').textContent;
var formData = new FormData(myForm);
formData.append('analysis_id', analysis_id);
    $('#ajax-savvy').show();
     $.ajax({
        url: '/ajax_savvy/',
        type : "POST", // http method
        data: formData,
        dataType: 'json',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            $("#savvy_results").html("")
            $("#savvy_results").prepend("<p>"+ json.response +"</p>");
            $('#ajax-savvy').hide();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#ajax-savvy').hide();
            $('#cov_results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

$('#savvy-form').on('submit', function(event){
    event.preventDefault();
    send_savvy()
});

function send_select_savvy(){
var myForm = document.getElementById("savvy-select-form");
var analysis_id = document.getElementById('analysis-id').textContent;
var formData = new FormData(myForm);
formData.append('analysis_id', analysis_id);
    $('#ajax-savvy-select').show();
     $.ajax({
        url: '/ajax_savvy_select/',
        type : "POST", // http method
        data: formData,
        dataType: 'json',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            $("#savvy_select_results").html("")
            $("#savvy_select_results").prepend("<p>"+ json.response +"</p>");
            $('#ajax-savvy-select').hide();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#ajax-savvy-select').hide();
            $('#cov_results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

$('#savvy-select-form').on('submit', function(event){
    event.preventDefault();
    send_select_savvy()
});