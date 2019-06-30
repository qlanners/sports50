"""sports50 URL Configuration

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

from sports50web import views

#All URL patterns are stored in the master sports50 folder. These could also be moved to a URL file in the sports50web folder,
#but for now they work here just as well.

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^teams/(\d+)/', views.team_info, name='team_info'),
    url(r'^field_breakdown/(\d+)/', views.field_breakdown, name='field_breakdown'),
    url(r'^stadium_map/(\d+)/', views.stadium_map, name='stadium_map'),
    url(r'^passing_zones/(\d+)/', views.passing_zones, name='passing_zones'),
    url(r'^fp_bkdwn/(\d+)/', views.fp_bkdwn, name='fp_bkdwn'),
    url(r'^field_breakdown_passing/(\d+)/', views.field_breakdown_passing, name='field_breakdown_passing'),
    url(r'^field_breakdown_rushing/(\d+)/', views.field_breakdown_rushing, name='field_breakdown_rushing'),
    url(r'^stadium_map_passing/(\d+)/', views.stadium_map_passing, name='stadium_map_passing'),
    url(r'^stadium_map_rushing/(\d+)/', views.stadium_map_rushing, name='stadium_map_rushing'),
    url(r'^fp_bkdwn_passing/(\d+)/', views.fp_bkdwn_passing, name='fp_bkdwn_passing')
    
]
