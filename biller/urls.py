from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url,include
from django.contrib.auth import views
from django.contrib.auth import views as auth_views
from invoice.forms import LoginForm
from invoice.views import signup

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^invoice/', include('invoice.urls')),
    url(r'^signup/$', signup, name='signup'),
    url(r'^$', views.login, {'template_name': 'login.html', 
    	'authentication_form': LoginForm,
    	'redirect_authenticated_user': True},name='login'),
    url(r'^logout', auth_views.logout, {'next_page': 'login'}),
    url('^change-password/$', auth_views.PasswordChangeView.as_view()),
    url('^password_change_done/$', auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
]
