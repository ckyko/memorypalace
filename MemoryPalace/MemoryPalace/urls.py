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
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.conf.urls import url

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'coreapp.views.index', name='index'),
    url(r'^about/', 'coreapp.views.about', name='about'),
    url(r'^contact/', 'coreapp.views.contact', name = 'contact'),
    url(r'.*login/', 'coreapp.views.log_in', name='login'),
    url(r'.*register/', 'coreapp.views.register', name='register'),
    url(r'.*createPalace/', 'coreapp.views.createPalace', name='createPalace'),
    url(r'.*deletePalace/', 'coreapp.views.deletePalace', name='deletePalace'),
    url(r'.*deleteRoom/', 'coreapp.views.deleteRoom', name='deleteRoom'),
    url(r'^palace_library/', 'coreapp.views.palace_library', name='palace_library'),
    url(r'.*createRoom/', 'coreapp.views.createRoom', name='createRoom'),
    url(r'^MemoryPalace/', 'coreapp.views.MemoryPalace', name='MemoryPalace'),
    url(r'^logout/', 'coreapp.views.log_out', name='logout'),
    url(r'^testing/', 'coreapp.views.testing'),
    url(r'^upload_image/', 'coreapp.views.upload_image'),
    #url(r'^api', include(router.urls)),
    url(r'^snippets/$', 'coreapp.views.snippet_list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', 'coreapp.views.snippet_detail'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
