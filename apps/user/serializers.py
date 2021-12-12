import uuid

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import get_default_password_validators
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from apps.user.models import APIUser

User = get_user_model()


def validate_password(password, user=None, password_validators=None):
    """
    Validate whether the password meets all validator requirements.

    If the password is valid, return ``None``.
    If the password is invalid, raise ValidationError with all error messages.
    """
    errors = []
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        try:
            validator.validate(password, user)
        except ValidationError as error:
            errors.append(error)
    if errors:
        raise ValidationError(errors)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    auth_token = serializers.SerializerMethodField()

    def get_auth_token(self, obj):
        return obj.token

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name',
                  'last_name', 'auth_token'
                  )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        item = super().create(validated_data)
        item.set_password(password)
        item.save()
        return item


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


class UserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    def get_auth_token(self, obj):
        return obj.token

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'auth_token']


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if attrs['old_password'] == attrs['password']:
            raise serializers.ValidationError({"password": "New password cannot be old password"})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        user.set_password(validated_data['password'])
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',)
        extra_kwargs = {
            'username': {
                'validators': []
            }
        }

    def validate_username(self, value):
        user = self.context.get('request').user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        item = UpdateUserSerializer(
            instance=user,
            data=validated_data,
            partial=True,
            context=self.context
        )
        if item.is_valid(raise_exception=True):
            instance = item.save()
            return instance


class APIUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    api_user_name = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()
    is_user_active = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.first_name

    def get_token(self, obj):
        return obj.token

    def get_is_user_active(self, obj):
        return not obj.is_token_invalidated

    def create(self, validated_data):
        user = APIUser.objects.create(username=uuid.uuid4(), first_name=validated_data.get('api_user_name'),
                                      is_api_user=True)
        return user

    class Meta:
        fields = ['id', 'api_user_name', 'name', 'token', 'is_user_active']
        model = APIUser


class AlterTokenValiditySerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=APIUser.objects.all())
    action = serializers.ChoiceField(choices=[(c, c) for c in ['validate', 'invalidate']])

    def validate(self, attrs):
        super().validate(attrs)
        current_state = 'invalidate' if attrs.get('user').is_token_invalidated else 'validate'
        if current_state == attrs.get('action'):
            raise ValidationError({'action': 'Can not {} user'.format(attrs.get('action'))})
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        user.is_token_invalidated = validated_data.get('action') == 'invalidate'
        user.save()
        Token.objects.filter(user=user).delete()
        return {'message': 'Action performed successfully'}
