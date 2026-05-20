from django.db import models

class Task(models.Model):

    user_id = models.CharField(max_length=100)
    
    user_name = models.CharField(max_length=100, default="Unknown")
    
    title = models.CharField(max_length=255)

    completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    priority = models.CharField(max_length=50, default="None")
    
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title