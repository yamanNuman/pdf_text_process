"""pdfProcess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from user import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('',views.index, name="index"),
    path('dashBoard',views.dashBoard, name="dashBoard"),
    path('addPdf',views.addPDF, name="addPdf"),
    path('search', views.searchData, name = "search"),
    path('details/<int:id>', views.details, name = "details"),
    path('delete/<int:id>', views.deletePdf, name = "delete"),
    path('loginUser', views.loginUser, name = "loginUser"),
    path('logOut', views.logOut, name = "logOut"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
