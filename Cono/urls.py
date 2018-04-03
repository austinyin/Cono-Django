"""Cono URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter(trailing_slash=False)
from apps.urls import registAll

registAll()


urlpatterns = [
    path('manage/admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/user/', include('apps.user.urls')),
    path('api/account/', include('apps.account.urls')),
    path('api/upload/', include('apps.medium.urls')),
    path('api/relation/', include('apps.relation.urls')),
    path('api/tweet/', include('apps.tweet.urls')),
    url(r'^api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
