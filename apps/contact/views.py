# Create your views here.
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from apps.contact.models import Contact, Interest
from apps.contact.serializers import ContactSerializer, InterestSerializer


@method_decorator(name='post',
                  decorator=swagger_auto_schema(
                      tags=['Contact'],
                      operation_summary='Create Contact',
                      operation_description="Use this API to create contact. Either uid or email is required"
                  ))
class CreateContact(CreateAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


@method_decorator(name='list', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="List all the contacts",
    operation_description="""List all API users. 
    """
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="Get contact object",
    operation_description="""Show full information for contact."""
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="Update a contact list",
    operation_description="""Update contact object."""
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="Partial Update a contact list",
    operation_description="""Partial Update contact object."""
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="Create Contact",
    operation_description="""Create a new contact"""
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="Delete Contact"
))
class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


@method_decorator(name='post',
                  decorator=swagger_auto_schema(
                      tags=['Contact'],
                      operation_summary='Create Interest for a contact',
                      operation_description="Use this API to create Interest for a contact."
                  ))
class CreateInterest(CreateAPIView):
    serializer_class = InterestSerializer
    queryset = Interest.objects.all()


@method_decorator(name='list', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="List all the interests",
    operation_description="""List all API users. 
    """
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="Get interest object",
    operation_description="""Show full information for interest."""
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="Update a interest list",
    operation_description="""Update interest object."""
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="Partial Update a Interest object",
    operation_description="""Partial Update interest object."""
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="Create Interest object",
    operation_description="""Create a new interest"""
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="Delete Interest"
))
class InterestViewSet(ModelViewSet):
    serializer_class = InterestSerializer
    queryset = Interest.objects.all()
    filterset_fields = {
        'category': ['exact'],
        'contact': ['exact',]
    }
    search_fields = ['url', 'category', 'value']

@method_decorator(name='list', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="List all the contact interest",
    operation_description="""List all API users. 
    """
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="Get contact interest object",
    operation_description="""Show full information for interest."""
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="Update a contact interest object",
    operation_description="""Update interest object."""
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="Partial Update a interest list",
    operation_description="""Partial Update interest object."""
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    tags=['Contact'],
    operation_summary="Delete a contact interest"
))
class FilteredInterestViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = InterestSerializer
    queryset = Interest.objects.all()
    filterset_fields = {
        'category': ['exact'],
        'contact': ['exact',]
    }
    search_fields = ['url', 'category', 'value']

    def get_queryset(self):
        if 'contact_pk' in self.kwargs:
            return super().get_queryset().filter(contact_id=self.kwargs.get('contact_pk'))
        return super().get_queryset()