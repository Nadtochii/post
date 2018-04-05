from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from post.models import Blog, Profile
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def home(request):
    posts = Blog.objects.all().order_by('-posted')
    user = Profile.objects.get(user_id=request.user.id)
    return render(request, 'home.html', {'posts': posts, 'location': user.location})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account')
    else:
        return HttpResponse('Activation link is invalid!')

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

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@csrf_exempt
def update_user(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        # response_data = {}
        print("11111111111111111")
        print(request.user.id)
        user = Profile.objects.get(user_id=request.user.id)
        user.location = location
        user.save()

        return redirect('/')
