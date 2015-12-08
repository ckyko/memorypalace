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
from test_app import views

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
    url(r'^$', 'coreapp.views.index'),
    url(r'^about/', 'coreapp.views.about'),
    url(r'^contact/', 'coreapp.views.contact'),
    url(r'.*MemoryPalace', 'coreapp.views.MemoryPalace'),
    url(r'.*login/', 'coreapp.views.log_in'),
    url(r'.*register/', 'coreapp.views.register'),
    url(r'.*createPalace/', 'coreapp.views.createPalace'),
    url(r'^palace_library/', 'coreapp.views.palace_library'),
    url(r'^logout/', 'coreapp.views.log_out'),
    url(r'^testing/', 'coreapp.views.testing'),
    url(r'^createRoom/', 'coreapp.views.createRoom'),
    #url(r'^api', include(router.urls)),
    url(r'^snippets/$', 'coreapp.views.snippet_list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', 'coreapp.views.snippet_detail'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^some', include('test_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

