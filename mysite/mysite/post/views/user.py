from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

from post.models import Profile
from post.forms import SignupForm, ProfileForm
from post.tokens import account_activation_token


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
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
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


def update_user(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            location = request.POST.get('location')
            bdate = request.POST.get('birth_day')
            user = Profile.objects.get(user_id=request.user.id)

            user.location = location if location else user.location
            user.birth_date = bdate if bdate else user.birth_date
            user.save()

            return redirect('/user_settings')


@login_required
def user_settings(request):
    user_active = Profile.objects.get(user_id=request.user.id)
    return render(request, 'user_settings.html', {'user_active': user_active})