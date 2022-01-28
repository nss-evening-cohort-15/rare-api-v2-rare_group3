"""rare_v2 URL Configuration

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
from rest_framework import routers

from rare_v2api.views import (
    register_user,
    login_user,
    RareUserView,
)

from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from django.conf.urls import include 
from rare_v2api.views import ReactionView
from rare_v2api.views import PostReactionView
from rare_v2api.views import TagView



router = routers.DefaultRouter(trailing_slash=False)
router.register(r'reactions', ReactionView, 'reaction')
router.register(r'postreactions', PostReactionView, 'postreactions') 
router.register(r'rareusers', RareUserView, 'rareusers')
router.register(r'tags', TagView, 'tags')


router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
