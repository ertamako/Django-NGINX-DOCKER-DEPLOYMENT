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

//-------------------------------------------------------Scatter--------------------------------------------------------
function send_scatter(){
var myForm = document.getElementById('scatter-form');
var analysis_id = document.getElementById('analysis-id').textContent;
var formData = new FormData(myForm);
formData.append('analysis_id', analysis_id);

$('#ajax-scatter').show();
     $.ajax({
        url: '/ajax_scatter/',
        data: formData,
        type: 'POST',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            //$("#scatter_results").html("");
            $("#scatter_results").append("<img src="+json.url+">");
            $('#ajax-scatter').hide();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#ajax-scatter').hide();
            $('#output_err_scatter').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
 };

$('#scatter-form').on('submit', function(event){
    event.preventDefault();
    //console.log("form submitted!")
    send_scatter()
});

//---------------------------------------------------Heatmap------------------------------------------------------------

function send_heatmap(){
var myForm = document.getElementById('heatmap-form');
var analysis_id = document.getElementById('analysis-id').textContent;
var formData = new FormData(myForm);
formData.append('analysis_id', analysis_id);

$('#ajax-heatmap').show();
     $.ajax({
        url: '/ajax_heatmap/',
        data: formData,
        type: 'POST',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            //$("#scatter_results").html("");
            $("#heatmap_results").append("<img src="+json.url+">");
            $('#ajax-heatmap').hide();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#ajax-heatmap').hide();
            $('#output_err_scatter').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
 };

$('#heatmap-form').on('submit', function(event){
    event.preventDefault();
    //console.log("hurray")
    send_heatmap()
});

//---------------------------------------------------Diagram------------------------------------------------------------

function send_diagram(){
var myForm = document.getElementById('diagram-form');
var analysis_id = document.getElementById('analysis-id').textContent;
var formData = new FormData(myForm);
formData.append('analysis_id', analysis_id);

$('#ajax-diagram').show();
     $.ajax({
        url: '/ajax_diagram/',
        data: formData,
        type: 'POST',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            //$("#scatter_results").html("");
            $("#diagram_results").append("<embed src="+json.url+" width='1200' height='900' type='application/pdf'>");
            $('#ajax-diagram').hide();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#ajax-diagram').hide();
            $('#output_err_scatter').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
 };

$('#diagram-form').on('submit', function(event){
    event.preventDefault();
    send_diagram()
});


//---------------------------------------------------Genemetrics-------------------------------------------------------------
function send_genemetrics(){
var myForm = document.getElementById('genemetrics-form');
var analysis_id = document.getElementById('analysis-id').textContent;
var formData = new FormData(myForm);
formData.append('analysis_id', analysis_id);

$('#ajax-genemetrics').show();
     $.ajax({
        url: '/ajax_genemetrics/',
        data: formData,
        type: 'POST',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            $('#output_err_genemetrics').html("")
            $("#genemetrics_results").html("");
            $("#genemetrics_results").html("<pre>" + json.output_stdout + "</pre>"); //{% for bam in " json.bam_file_names "%}{% endfor %}
            $('#ajax-genemetrics').hide();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#ajax-genemetrics').hide();
            $('#output_err_genemetrics').html("")
            $('#output_err_genemetrics').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
 };


$('#genemetrics-form').on('submit', function(event){
    event.preventDefault();
    send_genemetrics()
});

//---------------------------------------------------Breaks-------------------------------------------------------------
function send_breaks(){
var myForm = document.getElementById('breaks-form');
var analysis_id = document.getElementById('analysis-id').textContent;
var formData = new FormData(myForm);
formData.append('analysis_id', analysis_id);

$('#ajax-breaks').show();
     $.ajax({
        url: '/ajax_breaks/',
        data: formData,
        type: 'POST',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        // handle a successful response
        success : function(json) {
            $('#output_err_breaks').html("")
            $("#breaks_results").html("");
            $("#breaks_results").html("<pre>" + json.output_stdout + "</pre>"); //{% for bam in " json.bam_file_names "%}{% endfor %}
            $('#ajax-breaks').hide();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#ajax-breaks').hide();
            $('#output_err_breaks').html("")
            $('#output_err_breaks').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
 };


$('#breaks-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")
    send_breaks()
});
//---------------------------------------------------Call-------------------------------------------------------------


function send_call() {
var myForm = document.getElementById('call-form');
var analysis_id = document.getElementById('analysis-id').textContent;
var formData = new FormData(myForm);
formData.append('analysis_id', analysis_id);
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
            $("#call_results").html("<pre>"+json.output_err_call+"</pre>");
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
    send_call()
});

//---------------------------------------------------Delete-------------------------------------------------------------


function delete_image(image_primary_key){
    if (confirm('Are you sure you want to remove this plot?')==true){
        $.ajax({
            url : "/delete_image_ajax/", // the endpoint
            type : "DELETE", // http method
            data : { imagepk : image_primary_key }, // data sent with the delete request
            success : function(json) {
                // hide the post
                console.log(json.msg)
              $('#image-holder'+image_primary_key).hide(); // hide the post on success
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

function delete_heatmap(heatmap_primary_key){
    if (confirm('Are you sure you want to remove this heatmap?')==true){
        $.ajax({
            url : "/delete_heatmap_ajax/", // the endpoint
            type : "DELETE", // http method
            data : { heatmappk : heatmap_primary_key }, // data sent with the delete request
            success : function(json) {
                // hide the post
                console.log(json.msg)
              $('#heatmap-holder'+heatmap_primary_key).hide(); // hide the post on success
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

function delete_diagram(diagram_primary_key){
    if (confirm('Are you sure you want to remove this diagram?')==true){
        $.ajax({
            url : "/delete_diagram_ajax/", // the endpoint
            type : "DELETE", // http method
            data : { diagrampk : diagram_primary_key }, // data sent with the delete request
            success : function(json) {
                // hide the post
                console.log(json.msg)
              $('#diagram-holder'+diagram_primary_key).hide(); // hide the post on success
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