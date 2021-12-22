from rest_framework import serializers

from apps.contact.models import Contact, Interest


class ContactSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        super().validate(attrs)
        Contact(**attrs).clean()
        return attrs

    class Meta:
        model = Contact
        fields = '__all__'


class InterestSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        return attrs

    class Meta:
        model = Interest
        fields = '__all__'

