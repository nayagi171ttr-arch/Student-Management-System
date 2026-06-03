
from django.db import models
import uuid
from django.contrib.auth.models import User
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('student', 'Student'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICES, max_length=10)
    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    def __str__(self):
        return f"{self.user.username} - {self.role} ({self.user_uuid})"
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    section = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=100)
    section = models.CharField(max_length=20)
    class_teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='my_students')
                                                                                    #related_name is a parameter of foreignnKey    
    def __str__(self):
        return f"{self.user.username}"

