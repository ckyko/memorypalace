"""MemoryPalace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'coreapp.views.index', name='index'),
    url(r'^about/', 'coreapp.views.about', name='about'),
    url(r'^contact/', 'coreapp.views.contact', name = 'contact'),
    url(r'.*MemoryPalace', 'coreapp.views.MemoryPalace', name='MemoryPalace'),
    url(r'.*login/', 'coreapp.views.log_in', name='login'),
    url(r'.*register/', 'coreapp.views.register', name='register'),
    url(r'.*createPalace/', 'coreapp.views.createPalace', name='createPalace'),
    url(r'^palace_library/', 'coreapp.views.palace_library', name='palace_library'),
    url(r'^logout/', 'coreapp.views.log_out', name='logout'),
    url(r'^testing/', 'coreapp.views.testing'),
    url(r'^createRoom/', 'coreapp.views.createRoom', name='createRoom'),
    url(r'^upload_image/', 'coreapp.views.upload_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

