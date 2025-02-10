from django.db import models
from django.contrib.auth import get_user_model
import secrets

User = get_user_model()

class BookkeepingRecord(models.Model):
    INCOME = '收入'
    EXPENSE = '支出'
    TYPE_CHOICES = [
        (INCOME, '收入'),
        (EXPENSE, '支出'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records')
    date = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.date} {self.type} {self.category}: {self.amount}"

class ApiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    key = models.CharField(max_length=40, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)
    
    def generate_key(self):
        return secrets.token_hex(20)
    
    def __str__(self):
        return f"API Key for {self.user.username}"