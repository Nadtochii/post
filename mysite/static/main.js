$("#test .nav-pills a").on("click", function(){
   $("#test .nav-pills").find("li.active").removeClass("active");
   $(this).parent("li").addClass("active");
});

$('#post-form').on('submit', function(event){
    event.preventDefault();
    create_post();
});

$('#add-comment').on('submit', function(event){
    event.preventDefault();
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
            $("#talk").prepend("<a href=\"post/"+json.id+"\" class=\"list-group-item list-group-item-action flex-column align-items-start\"><div class=\"d-flex w-100 justify-content-between\"><h5 class=\"mb-1\">"+json.title+"</h5><small></small></div><p class=\"mb-1\">"+json.body+"</p><small></small></a>");
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
            $('#discussion').prepend("<li class=\"list-group-item\"><div class=\"card\" style=\"width: 40rem;\"><div class=\"card-body\"><h6 class=\"card-title\">"+json.user+", "+json.posted+"</h6><p class=\"card-text\">"+json.text+"</p></div></div></li>");
            console.log("success");
        },
        error: function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}
