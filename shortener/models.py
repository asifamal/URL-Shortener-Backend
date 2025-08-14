from django.db import models
import string
import random

# Create your models here.
def generate_short_code():
    characters = string.ascii_letters + string.digits
    while True:
        short_code = ''.join(random.choices(characters, k=6))
        if not URL.objects.filter(short_code=short_code).exists():
            return short_code
        
class URL(models.Model):
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=6, unique=True, default=generate_short_code)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"