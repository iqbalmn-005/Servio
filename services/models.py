from django.db import models
from provider import models as provider_models

# Create your models here.


class Plumbing(models.Model):
    plumber = models.OneToOneField(
        provider_models.Provider,
        on_delete=models.CASCADE,
        related_name='plumbing_profile',
        null=True
    )

class Wiring(models.Model):
    electrician = models.OneToOneField(
        provider_models.Provider,
        on_delete=models.CASCADE,
        related_name='wiring_profile',
        null=True
    )

class AcMechanic(models.Model):
    ac_mechanic = models.OneToOneField(
        provider_models.Provider,
        on_delete=models.CASCADE,
        related_name='ac_mechanic_profile',
        null=True
    )
