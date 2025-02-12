from django.db import models
from django.contrib.auth import get_user_model
import secrets
from django.contrib.auth.hashers import make_password, check_password

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
    account = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.date} {self.type} {self.category}: {self.amount}"

class ApiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    key_hash = models.CharField(max_length=128, editable=False)  # 存储哈希值
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_key(self, raw_key):
        self.key_hash = make_password(raw_key)
    
    def check_key(self, raw_key):
        return check_password(raw_key, self.key_hash)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            # 生成原始 API Key（只在创建时生成一次）
            raw_key = secrets.token_hex(20)
            self.set_key(raw_key)
            # 可将原始密钥临时保存到一个属性上，以便在创建后返回给用户（注意不要写入数据库）
            self._raw_key = raw_key
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"API Key for {self.user.username}"