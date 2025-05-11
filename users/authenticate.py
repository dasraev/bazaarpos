from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed,ValidationError

class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        raw_token = self.get_raw_token(header) if header else None

        if raw_token:
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token),validated_token

        else:
            raw_token_str = request.COOKIES.get('access_token')
            try:
                validated_token = self.get_validated_token(raw_token_str)
                return self.get_user(validated_token),validated_token
            except InvalidToken:
                refresh_token_str = request.COOKIES.get('refresh_token')
                if not refresh_token_str:
                    return None
                try:
                    refresh_token = RefreshToken(refresh_token_str)
                    new_access_token = refresh_token.access_token

                    request._new_access_token = str(new_access_token)

                    return self.get_user(new_access_token),new_access_token
                except:
                    return None










