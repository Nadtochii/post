from django.conf.urls import url
from django.contrib.auth import views as auth_views
from views import user as user_views
from views import post as post_views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', user_views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        user_views.activate, name='activate'),
    url(r'^update_user/$', user_views.update_user),
    url(r'^user_settings/$', user_views.user_settings, name='user_settings'),
    url(r'^$', post_views.home, name='home'),
    url(r'^create_post/$', post_views.create_post),
    url(r'^post/(\d+)/?$', post_views.show_post),
    url(r'^add_comment/$', post_views.add_comment),
]
