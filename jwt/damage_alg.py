# Атакующий делает токен без подписи
import base64, json

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

fake_header = b64url(json.dumps({"alg": "none", "typ": "JWT"}).encode())
fake_payload = b64url(json.dumps({"sub": "1", "role": "admin"}).encode())
fake_token = f"{fake_header}.{fake_payload}."

print(fake_token)

# Уязвимый сервер:
try:
    jwt.decode(fake_token, secret, algorithms=["none"])  # ← вот тут дыра
    print("HACKED!")
except Exception as e:
    print("OK:", e)

# Защищённый сервер:
try:
    jwt.decode(fake_token, secret, algorithms=["HS256"])  # ← явный алгоритм
    print("HACKED!")
except jwt.InvalidAlgorithmError as e:
    print("BLOCKED:", e)