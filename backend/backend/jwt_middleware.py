from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from urllib.parse import parse_qs

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        token = self.get_token_from_scope(scope)

        if token:
            user = await self.get_user_from_token(token)
            scope['user'] = user  # ✅ This is important
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    def get_token_from_scope(self, scope):
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token_list = query_params.get("token", [])
        return token_list[0] if token_list else None

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            return User.objects.get(id=user_id)
        except:
            return AnonymousUser()