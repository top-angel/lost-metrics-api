from django.db.models import Q
from rest_framework import serializers

from apps.contact.models import Contact, Interest
from apps.utils.serializer_utils import ModifiedEnhancedToRepSerializer


class ContactSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        super().validate(attrs)
        Contact(**attrs).clean()
        return attrs

    def create(self, validated_data):
        uid = validated_data.get('uid', None)
        email = validated_data.get('email', None)
        qs = Contact.objects.filter(Q(uid=uid) | Q(email=email))
        if qs.exists():
            data = {}
            # to remove empty values
            for k, v in validated_data.items():
                if v:
                    data[k] = v
            qs.update(**data)
            return qs.first()
        return super().create(validated_data)

    class Meta:
        model = Contact
        fields = '__all__'


class InterestSerializer(ModifiedEnhancedToRepSerializer):
    fk_field_serializer_class = {
        'contact': {
            'class': ContactSerializer
        }
    }

    def validate(self, attrs):
        return attrs

    class Meta:
        model = Interest
        fields = '__all__'
