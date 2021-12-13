from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('create_contact/', CreateContact.as_view(), name='create_contact'),
]
