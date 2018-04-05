$('#post-form').on('submit', function(event){
    event.preventDefault();
    create_post();
});

function create_post() {
    $.ajax({
        url : "create_post/",
        type : "POST",
        data : { post_title: $("#post-title").val(), post_text: $('#post-text').val() },

        // handle a successful response
        success : function(json) {
            $('#post-text').val('');
            $('#post-title').val('');
            console.log(json); // log the returned json to the console
            $("#talk").prepend("<li><strong>"+json.title+"</strong> - <em> "+json.user+"</em> - <span> "+json.created+"</span><br>"+json.body+"</li>");
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
