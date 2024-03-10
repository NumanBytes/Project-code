import jwt
import datetime

secret_key = 'e6a5090db0291d6238de71d5569627b4'
algorithm = 'HS256'
def create_token(user):
    payload = {'user_id': user.id, 'email': user.email}
    expiry = 30
    expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiry)
    token = jwt.encode({'exp': expires, **payload},secret_key, algorithm=algorithm)
    return token

def verify_token(token):
    """checks if token is expired"""
    try:
        decode_token = jwt.decode(token,secret_key,algorithms=algorithm)
        exp_time = datetime.datetime.fromtimestamp(decode_token['exp'])
        if exp_time > datetime.datetime.now():
            return True
        return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.DecodeError:
        return False
