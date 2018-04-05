$('#post-form').on('submit', function(event){
    event.preventDefault();
    create_post();
});

function create_post() {
    $.ajax({
        url : "create_post/",
        type : "POST",
        data : { the_post : $('#post-text').val() },

        // handle a successful response
        success : function(json) {
            $('#post-text').val('');
            console.log(json); // log the returned json to the console
            $("#talk").prepend("<li><strong>"+json.body+"</strong> - <em> "+json.user+"</em> - <span> "+json.created+"</span></li>");
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