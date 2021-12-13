from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.

# "contact": {
# email or uID required, all other fields optional
# first_name: 'Daniel',
# last_name: ‘Dulgerian’,
# email: ‘daniel@genedx.com’,
# phone: ‘845-270-9838’,
# company: ‘Gene Dx’,
# uID: ‘21334’ //User ID on customer's site
# },
class Contact(models.Model):
    uid = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)

    def clean(self):
        super().clean()
        if not self.uid and not self.email:
            raise ValidationError('Either uid or email is required')

    def __str__(self):
        return self.uid if self.uid else self.email
