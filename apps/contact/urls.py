from django.urls import path, include
from rest_framework_nested import routers


from .views import *

router = routers.SimpleRouter()
router.register('contact', ContactViewSet, basename='contact')
router.register('interest', InterestViewSet, basename='interest')
interest_contact_router = routers.NestedSimpleRouter(router, 'contact', lookup='contact')
interest_contact_router.register('interest', FilteredInterestViewSet, basename='contact_interest')

# router.register('<str:contact_id>/interest', FilteredInterestViewSet, basename='contact_interest')
urlpatterns = [
    path('', include(router.urls)),
    path('', include(interest_contact_router.urls)),
    # path('create_contact/', CreateContact.as_view(), name='create_contact'),
    # path('create_interest/', CreateInterest.as_view(), name='create_interest'),
]
