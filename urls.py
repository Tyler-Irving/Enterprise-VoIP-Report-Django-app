"""bsw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from .views import cms_im_audit_report, ServiceLocationViewSet, Home, FilterData, BuildNumberStatusViewSet

# ROUTERS
serv_local_router = routers.DefaultRouter()
serv_local_router.register(r'update_service_locations', ServiceLocationViewSet)

num_stat_router = routers.DefaultRouter()
num_stat_router.register(r'update_num_stat', BuildNumberStatusViewSet)
#########

urlpatterns = [
    path('', Home.as_view(), name='home'),
    url('filter_data', FilterData.as_view(), name='filter_data'),
    url('download/', cms_im_audit_report, name='download'),
    url(r'^api/', include(serv_local_router.urls)),
    url(r'^api/', include(num_stat_router.urls))
]