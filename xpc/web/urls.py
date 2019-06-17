"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from web.views.composer import *
from web.views.post import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^list/(?P<page>\d+)/$', index),
    url(r'user/oneuser/userid-(?P<cid>\d+)$', oneuser),
    url(r'a(?P<pid>\d+)$', detail),
    url(r'u(?P<cid>\d+)$', homepage),
    url(r'comments$', comments),
    url(r'index.php', index_php),
    url(r'article/filmplay/ts-viewed',ts_view),
    url(r'^api/user-center/captcha/send$', send_signup_captcha),
    url(r'^signup/$', signup),
    url(r'^api/codes/phone$', phone_codes),
    url(r'^api/user-center/user/register$', register),
    url(r'^login', login),



]
