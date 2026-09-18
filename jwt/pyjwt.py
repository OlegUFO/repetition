import jwt
import time

secret = "super-secret-key-at-least-32-bytes-long!"

token = jwt.encode(
    {"sub": "123", "exp": int(time.time()) + 3600},
    secret,
    algorithm="HS256",
)
print(token)

# Декодирование с проверкой
payload = jwt.decode(token, secret, algorithms=["HS256"])
print(payload)

# Просроченный токен
expired = jwt.encode(
    {"sub": "123", "exp": int(time.time()) - 10},
    secret,
    algorithm="HS256",
)
try:
    jwt.decode(expired, secret, algorithms=["HS256"])
except jwt.ExpiredSignatureError:
    print("Expired!")