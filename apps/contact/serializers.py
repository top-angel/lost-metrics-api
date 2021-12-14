from rest_framework import serializers

from apps.contact.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        super().validate(attrs)
        Contact(**attrs).clean()
        return attrs

    class Meta:
        model = Contact
        fields = '__all__'
