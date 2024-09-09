from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    username = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=False, unique=True)
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)
    created_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='receiver')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.sender.username} is send friend request to {self.receiver.username}"

    class meta:
        unique_together = ('sender', 'receiver')