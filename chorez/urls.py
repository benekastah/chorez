"""chorez URL Configuration

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
from django.views.generic import RedirectView

from chorez.scheduler import views

urlpatterns = [
    url(r'^$', views.ScheduleView.as_view(), name='home'),
    url(r'^chores$', views.ChoreList.as_view(), name='chores'),
    url(r'^chores/new$', views.ChoreCreate.as_view(), name='create_chore'),
    url(r'^chores/(?P<pk>\d+)$', views.ChoreEdit.as_view(), name='chore'),
    url(r'^chores/(?P<pk>\d+)/delete$', views.ChoreDelete.as_view(), name='chore_delete'),

    url(r'^admin/', admin.site.urls),
]
