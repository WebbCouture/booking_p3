from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Tool(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # New FK field to Location model, nullable for migration safety
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='tool_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    tool = models.ForeignKey(Tool, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)  # make nullable temporarily
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    confirmation_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.tool.name} on {self.date}"
