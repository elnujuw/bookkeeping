from rest_framework import authentication, exceptions
from .models import ApiKey

class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    自定义 API Key 认证。
    客户端在请求头中需提供：
      Authorization: Api-Key <your_api_key>
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None  # 没有提供认证信息，后续其他认证类可能生效
        
        try:
            prefix, key = auth_header.split(' ')
        except ValueError:
            return None
        if prefix != 'Api-Key':
            return None
        
        try:
            api_key = ApiKey.objects.get(key=key)
        except ApiKey.DoesNotExist:
            raise exceptions.AuthenticationFailed('无效的 API Key')
        
        return (api_key.user, None)