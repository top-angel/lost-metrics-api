from django.contrib.auth.models import AbstractUser
# Create your models here.
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):

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
