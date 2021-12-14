# Create your views here.
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView

from apps.contact.models import Contact
from apps.contact.serializers import ContactSerializer


@method_decorator(name='post',
                  decorator=swagger_auto_schema(
                      tags=['Contact'],
                      operation_summary='Create Contact',
                      operation_description="Use this API to create contact. Either uid or email is required"
                  ))
class CreateContact(CreateAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
