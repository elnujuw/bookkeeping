from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from django.db.models import Sum
from .serializers import UserRegistrationSerializer, UserSerializer, BookkeepingRecordSerializer, ApiKeySerializer
from .models import BookkeepingRecord, ApiKey
from .authentication import APIKeyAuthentication
from rest_framework.authentication import SessionAuthentication

# 用户注册接口
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

# 用户信息查询/更新接口
class UserDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

# 记账记录 CRUD（通过 API Key 认证）
class BookkeepingRecordViewSet(viewsets.ModelViewSet):
    serializer_class = BookkeepingRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, APIKeyAuthentication]
    
    def get_queryset(self):
        return BookkeepingRecord.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 月度统计报表接口
class MonthlyStatisticsAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, APIKeyAuthentication]
    
    def get(self, request, year, month):
        records = BookkeepingRecord.objects.filter(
            user=request.user,
            date__year=year,
            date__month=month
        )
        income = records.filter(type=BookkeepingRecord.INCOME).aggregate(total=Sum('amount'))['total'] or 0
        expense = records.filter(type=BookkeepingRecord.EXPENSE).aggregate(total=Sum('amount'))['total'] or 0
        data = {
            'year': year,
            'month': month,
            'income': income,
            'expense': expense,
            'balance': income - expense,
        }
        return Response(data)

# 年度统计报表接口
class YearlyStatisticsAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, APIKeyAuthentication]
    
    def get(self, request, year):
        records = BookkeepingRecord.objects.filter(
            user=request.user,
            date__year=year
        )
        income = records.filter(type=BookkeepingRecord.INCOME).aggregate(total=Sum('amount'))['total'] or 0
        expense = records.filter(type=BookkeepingRecord.EXPENSE).aggregate(total=Sum('amount'))['total'] or 0
        data = {
            'year': year,
            'income': income,
            'expense': expense,
            'balance': income - expense,
        }
        return Response(data)

# API Key 管理（生成、列出）
class ApiKeyViewSet(viewsets.ModelViewSet):
    serializer_class = ApiKeySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ApiKey.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        # 每次请求创建一个新的 API Key
        api_key = ApiKey.objects.create(user=request.user)
        serializer = self.get_serializer(api_key)
        return Response(serializer.data, status=status.HTTP_201_CREATED)