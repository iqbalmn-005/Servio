from django.db import models
from django.utils import timezone
from provider import models as provider_models
from django.core.validators import RegexValidator

# Create your models here.


class User(models.Model):
    Name = models.CharField(max_length=30)
    phone_number = models.CharField(
        max_length=15,
        null=True,
        validators=[RegexValidator(r'^\d{10,15}$', "Phone number must be between 10 and 15 digits.")]
    )
    address = models.TextField(max_length=100)
    email = models.EmailField(max_length=50, null=True)
    password = models.CharField()


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(provider_models.Provider, on_delete=models.CASCADE)
    service = models.CharField(max_length=100, null=True)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # when request was received

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('completion_requested', 'Completion Requested'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=120)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(provider_models.Provider, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
