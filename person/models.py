from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError


# Create your models here.
class PersonalInfo(models.Model):
    """
    Personal Information Model
    """

    # name
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)

    # birthday
    birth_date = models.DateField(blank=True, null=True)

    # address
    address1 = models.CharField(max_length=50, blank=True, null=True)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    county = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)

    # contact information
    email_validator = EmailValidator()
    email = models.EmailField(validators=[email_validator], blank=True, null=True)

    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(max_length=17, validators=[phone_validator], blank=True, null=True)


    def clean(self):
        """
        check validation
        """
        if (self.first_name == None or self.last_name == None) and self.email == None and self.phone == None:
            raise ValidationError('At least input first and last name or email address or phone number.')
