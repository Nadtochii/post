from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from post.models import Blog, Comments


@login_required
def home(request):
    posts = Blog.objects.all().order_by('-posted')
    return render(request, 'home.html', {'posts': posts})


@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        post_title = request.POST.get('post_title')
        post_text = request.POST.get('post_text')
        response_data = {}

        post = Blog(title=post_title, body=post_text, user=request.user)
        post.save()

        response_data['result'] = 'Create post successful!'
        response_data['title'] = post.title
        response_data['body'] = post.body
        response_data['created'] = post.posted.strftime('%B %d, %Y %I:%M %p')
        response_data['user'] = post.user.username
        response_data['post_id'] = post.id

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required
def show_post(request, post_id):
    post = Blog.objects.get(id=post_id)
    comment_list = Comments.objects.filter(post_id=post_id).order_by('-posted')
    page = request.GET.get('page', 1)

    paginator = Paginator(comment_list, 5)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    return render(request, 'post.html', {'post': post, 'comments': comments})


@csrf_exempt
def add_comment(request):
    if request.method == "POST":
        comment_text = request.POST.get('comment')
        post_id = request.POST.get('post_id')
        response_data = {}
        comment = Comments(text=comment_text, user=request.user, post_id=post_id)
        comment.save()

        response_data['result'] = "Success!"
        response_data['text'] = comment.text
        response_data['posted'] = comment.posted.strftime('%B %d, %Y %I:%M %p')
        response_data['user'] = comment.user.username

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"ERROR"}),
            content_type="application/json"
        )
