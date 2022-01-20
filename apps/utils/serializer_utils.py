from rest_framework import serializers
from django.db import ProgrammingError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        elif exclude is not None:  # drop fields that are specified in the 'exclude' argument
            for field_name in set(exclude):
                self.fields.pop(field_name)


class AutomaticAssignUserSerializer(DynamicFieldsModelSerializer):

    @property
    def user_field(self):
        if hasattr(self, 'user_field_name'):
            return self.user_field_name
        else:
            raise NotImplementedError("Serializer must define a user_field_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_field in self.fields:
            self.fields.pop(self.user_field)
        else:
            raise ProgrammingError(
                "%s is not present in the model fields, Choices are %s" % (
                    self.user_field, ', '.join(self.fields.keys())))

    def save(self, **kwargs):
        user_field = self.user_field
        self.validated_data[user_field] = self.context.get('request').user
        super().save(**kwargs)

    class Meta:
        exclude = ()


def get_list_of_fk_fields(instance):
    l = []
    for field in instance._meta.fields:
        if field.get_internal_type() in ['ForeignKey', 'OneToOneField']:
            l.append(field.name)
    return l


class EnhancedToRepSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        d = super().to_representation(instance)
        for field in get_list_of_fk_fields(instance):
            d[field] = str(getattr(instance, field)) if getattr(instance, field) else None
        return d


class ModifiedEnhancedToRepSerializer(EnhancedToRepSerializer):
    fk_field_serializer_class = {
    }

    # def validate(self, attrs):
    #     attrs = super().validate(attrs)
    #     model = self.Meta.model(**attrs)
    #     model.clean()
    #     return attrs

    def to_representation(self, instance):
        d = super().to_representation(instance)
        for field in self.fields:
            if hasattr(instance, field):
                if field in self.fk_field_serializer_class:
                    serializer_class = self.fk_field_serializer_class.get(field).get('class')
                    extra_kwargs = self.fk_field_serializer_class.get(field).get('extra_kwargs', {})
                    many = self.fk_field_serializer_class.get(field).get('many', False)
                    data = serializer_class(getattr(instance, field), many=many, context=self.context,
                                            **extra_kwargs).data
                    d[field] = data
        return d


def generate_serializer_class(model_class):
    class ModelSerializer(DynamicFieldsModelSerializer):
        class Meta:
            model = model_class
            fields = '__all__'

    return ModelSerializer


class ActiveUserSerializer(serializers.Serializer):
    def validate(self, attrs):
        request = self.context.get('request')
        if request:
            if request.user.is_authenticated:
                if not request.user.is_active_user:
                    raise ValidationError('Your account is blocked for the moment. Please contact T-Teet')
            else:
                raise ValidationError('Authentication is required.')
        attrs = super().validate(attrs)
        return attrs


class AutomaticAssignUserSerializer(DynamicFieldsModelSerializer):

    @property
    def user_field(self):
        if hasattr(self.Meta.model, 'user_field_name'):
            return self.Meta.model.user_field_name
        else:
            raise NotImplementedError("Model must define a user_field_name")

    def validate(self, attrs):
        attrs[self.user_field] = self.context.get('request').user
        attrs = super().validate(attrs)
        model = self.Meta.model(**attrs)
        model.clean()
        return attrs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_field in self.fields:
            self.fields.pop(self.user_field)
        else:
            raise ProgrammingError(
                "%s is not present in the model fields, Choices are %s" % (
                    self.user_field, ', '.join(self.fields.keys())))

    def save(self, **kwargs):
        super().save(**kwargs)

    class Meta:
        exclude = ()
