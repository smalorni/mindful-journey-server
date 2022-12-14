"""mindfuljourney URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from multiprocessing import Event
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import include
from rest_framework import routers
from django.conf import settings
from mindfuljourneyapi.views import PostView, register_user, login_user, EventView, PostCategoryView, PostCommentView

router = routers.DefaultRouter(trailing_slash=False)
# route for post
router.register(r'posts', PostView, 'post')
router.register(r'events', EventView, 'event')
router.register(r'categories', PostCategoryView, 'category')
router.register(r'postComments', PostCommentView, 'postComment')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    # Requests to http://localhost:8000/login will be routed to the login_user function
    path('login', login_user),
    path('', include(router.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
