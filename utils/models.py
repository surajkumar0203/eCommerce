from django.db import models

class BaseModel(models.Model):
    # This is an abstract class that will be inherited by other models to avoid redundancy
    class Meta:
        abstract = True
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)