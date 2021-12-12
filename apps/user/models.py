from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
# Create your models here.
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    is_api_user = models.BooleanField(default=False)
    is_token_invalidated = models.BooleanField(default=False)

    @property
    def token(self):
        refresh = RefreshToken.for_user(self)
        return dict(
            refresh=str(refresh),
            access=str(refresh.access_token)
        )

    def __str__(self):
        if self.first_name or self.last_name:
            return '{}  {}'.format(self.first_name, self.last_name)
        return self.email


class APIUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_api_user=True)


class APIUser(User):
    objects = APIUserManager()

    @property
    def token(self):
        if self.is_token_invalidated:
            return
        token, _ = Token.objects.get_or_create(user=self)
        return token.key

    class Meta:
        proxy = True
