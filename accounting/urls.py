from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterAPIView,
    UserDetailAPIView,
    BookkeepingRecordViewSet,
    MonthlyStatisticsAPIView,
    YearlyStatisticsAPIView,
    ApiKeyViewSet,
)

router = DefaultRouter()
router.register(r'bookkeeping', BookkeepingRecordViewSet, basename='bookkeeping')
router.register(r'api-keys', ApiKeyViewSet, basename='api-keys')

urlpatterns = [
    # path('register/', RegisterAPIView.as_view(), name='register'),
    path('user/', UserDetailAPIView.as_view(), name='user-detail'),
    path('statistics/monthly/<int:year>/<int:month>/', MonthlyStatisticsAPIView.as_view(), name='monthly-stats'),
    path('statistics/yearly/<int:year>/', YearlyStatisticsAPIView.as_view(), name='yearly-stats'),
    path('', include(router.urls)),
]