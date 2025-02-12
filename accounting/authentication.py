from rest_framework import authentication, exceptions
from .models import ApiKey

class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    自定义 API Key 认证：
    请求头中需包含类似 "Authorization: Api-Key <api_key>" 的内容。
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None  # 没有提供认证信息，允许其他认证方式处理
        
        try:
            prefix, provided_key = auth_header.split(' ')
        except ValueError:
            return None
        
        if prefix != 'Api-Key':
            return None
        
        # 遍历所有 API Key 记录进行匹配（如果用户数量较大，可根据其他线索进行优化）
        for api_key in ApiKey.objects.all():
            if api_key.check_key(provided_key):
                return (api_key.user, None)
        
        raise exceptions.AuthenticationFailed('无效的 API Key')