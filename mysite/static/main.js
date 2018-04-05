$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("3333333333333333333333333333");
    create_post();
});

$('#add-comment').on('submit', function(event){
    event.preventDefault();
    console.log("1111111111111111111");
    add_comment();
});

function create_post() {
    $.ajax({
        url: "create_post/",
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

function add_comment() {
    $.ajax({
        url: "/add_comment/",
        type: "POST",
        data: { comment: $("#comment").val(), post_id: $("#post-id").val() },

        success: function(json) {
            $('#comment').val('');
            console.log(json);
            $('#discussion').prepend("<li><strong>"+json.text+"</strong> - <em>"+json.user+"</em> - <span>"+json.posted+"</span></li>");
            console.log("success");
        },
        error: function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}
