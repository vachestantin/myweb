
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout

from blog import views as blog_views


urlpatterns = [
    url(r'^$', blog_views.list_posts, name='list_posts'),

    url(r'^create_post/$', blog_views.create_post, name='create_post'),
    url(r'^post/(?P<pk>[0-9]+)/$', blog_views.view_post, name='view_post'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', blog_views.edit_post, name='edit_post'),
    url(r'^post/(?P<pk>[0-9]+)/delete/$', blog_views.delete_post, name='delete_post'),

    url(r'^comment/(?P<pk>[0-9]+)/delete/$', blog_views.delete_comment, name='delete_comment'),

    url(r'^admin/', admin.site.urls),

    url(r'^{}$'.format(settings.LOGIN_URL[1:]),
        login,
        {'template_name': 'login.html'},
        name='login_url'
    ),
    url(r'^{}$'.format(settings.LOGOUT_URL[1:]),
        logout,
        {'next_page': settings.LOGIN_URL},
        name='logout_url'
    ),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root = settings.MEDIA_ROOT,
)
