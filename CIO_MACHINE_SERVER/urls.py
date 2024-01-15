"""
URL configuration for CIO_MACHINE_SERVER project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from users.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', getUsers,name="getUsers"),
    path('week-data',week_data,name= "week_data"),
    path('month-data',month_data,name="month_data"),
    path('year-data',year_data,name="year_data"),
    path('add-user',add_user,name="add_user"),
    path("<str:username>",getSpecficUser,name="getSpecficUser"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)