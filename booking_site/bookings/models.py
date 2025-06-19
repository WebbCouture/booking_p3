from django.db import models
from django.contrib.auth.models import User

class Tool(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='tool_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    confirmation_email = models.EmailField(blank=True, null=True)  # optional field for email confirmation

    def __str__(self):
        return f"{self.user.username} - {self.tool.name} on {self.date}"
