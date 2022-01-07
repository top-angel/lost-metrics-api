from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register('contact', ContactViewSet, basename='contact')
router.register('interest', InterestViewSet, basename='interest')
urlpatterns = [
    path('', include(router.urls)),
    # path('create_contact/', CreateContact.as_view(), name='create_contact'),
    # path('create_interest/', CreateInterest.as_view(), name='create_interest'),
]
