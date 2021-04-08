
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');


    Dropzone.autoDiscover = false;

    $('#MultiFileUpload').dropzone({
        url: "/fileupload/",
        crossDomain: false,
        paramName: "file",
        parallelUploads: 5,
        autoProcessQueue: true,
        timeout: 0,
        filesizeBase: 1024,
        maxFilesize: 10000,
        dictRemoveFileConfirmation: null,
        init: function () {
            this.on("uploadprogress", function (file, progress, bytesSent) {
                progress = bytesSent / file.size * 100;
                console.log(filesizecalculation(bytesSent))
            });
            this.on("maxfilesexceeded", function (data) {
                var res = eval('(' + data.xhr.responseText + ')');
            });
            this.on("addedfile", function (file) {
                var removeButton = Dropzone.createElement("<button data-dz-remove " +
                    "class='del_thumbnail btn btn-default'><span class='glyphicon glyphicon-trash'></span> Cancel </button>");
                var _this = this;
                removeButton.addEventListener("click", function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    _this.removeFile(file);
                });
                file.previewElement.appendChild(removeButton);
            });
            this.on("error", function (file, message) {

                console.log(message);
                this.removeFile(file);
            });
            this.on('sending', function (file, xhr, formData) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            });
        }
    });

    Dropzone.prototype.filesize = function (size) {
       filesizecalculation(size)
    };

    function filesizecalculation(size) {
        if (size < 1024 * 1024) {
            return "<strong>" + (Math.round(Math.round(size / 1024) * 10) / 10) + " KB</strong>";
        } else if (size < 1024 * 1024 * 1024) {
            return "<strong>" + (Math.round((size / 1024 / 1024) * 10) / 10) + " MB</strong>";
        } else if (size < 1024 * 1024 * 1024 * 1024) {
            return "<strong>" + (Math.round((size / 1024 / 1024 / 1024) * 10) / 10) + " GB</strong>";
        }
    }