from django.conf.urls import url, include
from rest_framework import routers

from .views import*
from .viewsets import*


router = routers.DefaultRouter()

router.register(r'office', OfficeViewset)

urlpatterns = [
    # url(r'^', Application.as_view(), name='home'),
    url(r'api/',  include(router.urls)),
    # url(r'home', Application.as_view(), name='home'),
    ]
