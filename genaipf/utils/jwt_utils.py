import jwt
import datetime
from genaipf.conf.jwt import JWT_SECRET_KEY

class JWTManager:
    def __init__(self, secret_key=JWT_SECRET_KEY, expires_in_seconds=3600*24*180):
        self.secret_key = secret_key
        self.expires_in_seconds = expires_in_seconds

    def generate_token(self, user_id, email):
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=self.expires_in_seconds)
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token

    def validate_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return True, payload["user_id"], payload["email"]
        except jwt.ExpiredSignatureError:
            return False, "Token expired"
        except jwt.InvalidTokenError:
            return False, "Invalid token"
