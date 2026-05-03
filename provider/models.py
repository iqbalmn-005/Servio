from django.db import models

# Create your models here.

class Provider(models.Model):
    Name=models.CharField(max_length=30)
    phone_number=models.CharField(max_length=10,null=True)
    SERVICE_CHOICE = (
        ('plumbing', 'Plumbing'),
        ('wiring', 'Wiring'),
        ('ac', 'AC'),
    )
    service=models.CharField(max_length=20,choices=SERVICE_CHOICE)
    email=models.EmailField(max_length=50,null=True)
    password=models.CharField()
    photo=models.ImageField(upload_to='provider_photos/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Name} ({self.service})"



# class AcceptedJobs(models.Model):
#     provider = models.ForeignKey('provider.Provider', on_delete=models.DO_NOTHING, null=True)
#     booking = models.OneToOneField('user.Booking', on_delete=models.DO_NOTHING, null=True)
