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


function delete_analysis(analysis_primary_key){
    if (confirm('Are you sure you want to remove this batch result?')==true){
        $.ajax({
            url : "/delete_analysis_ajax/", // the endpoint
            type : "DELETE", // http method
            data : { analysispk : analysis_primary_key }, // data sent with the delete request
            success : function(json) {
                // hide the post
                console.log(json.msg)
              $('#analysis-holder'+analysis_primary_key).hide(); // hide the post on success
            },

            error : function(xhr,errmsg,err) {
                // Show an error
                $('#results').html("<div class='alert-box alert radius' data-alert>"+
                "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    } else {
        return false;
    }
};

function delete_reference(analysis_primary_key){
    if (confirm('Are you sure you want to remove this batch result?')==true){
        $.ajax({
            url : "/delete_analysis_ajax/", // the endpoint
            type : "DELETE", // http method
            data : { analysispk : analysis_primary_key }, // data sent with the delete request
            success : function(json) {
                // hide the post
                console.log(json.msg)
              $('#reference-holder'+analysis_primary_key).hide(); // hide the post on success
            },

            error : function(xhr,errmsg,err) {
                // Show an error
                $('#results').html("<div class='alert-box alert radius' data-alert>"+
                "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    } else {
        return false;
    }
};

function delete_reference_file(reference_primary_key){
    if (confirm('Are you sure you want to remove this reference file?')==true){
        $.ajax({
            url : "/delete_reference_file_ajax/", // the endpoint
            type : "DELETE", // http method
            data : { referencepk : reference_primary_key }, // data sent with the delete request
            success : function(json) {
                // hide the post
                console.log(json.msg)
              $('#reference-file-holder'+reference_primary_key).hide(); // hide the post on success
            },

            error : function(xhr,errmsg,err) {
                // Show an error
                $('#results').html("<div class='alert-box alert radius' data-alert>"+
                "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    } else {
        return false;
    }
};