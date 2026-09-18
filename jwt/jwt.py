import base64
import hashlib
import hmac
import json
import time


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def create_jwt(payload: dict, secret: str, alg: str = "HS256") -> str:
    header = {"alg": alg, "typ": "JWT"}

    header_b64 = b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    payload_b64 = b64url_encode(json.dumps(payload, separators=(",", ":")).encode())

    signing_input = f"{header_b64}.{payload_b64}".encode()

    if alg == "HS256":
        signature = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    else:
        raise ValueError(f"Unsupported alg: {alg}")
    signature_b64 = b64url_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"


def verify_jwt(token: str, secret: str, expected_alg: str = "HS256") -> dict:
    """Проверяем подпись и exp. Возвращаем payload или кидаем исключение."""
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid token format")

    header_b64, payload_b64, signature_b64 = parts

    # ВАЖНО: фиксируем алгоритм, а не доверяем header'у!
    header = json.loads(b64url_decode(header_b64))
    if header.get("alg") != expected_alg:
        raise ValueError(f"Unexpected alg: {header.get('alg')}")

    # Пересчитываем подпись
    signing_input = f"{header_b64}.{payload_b64}".encode()
    expected_sig = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    actual_sig = b64url_decode(signature_b64)

    # Сравнение с постоянным временем — защита от timing-атак!
    if not hmac.compare_digest(expected_sig, actual_sig):
        raise ValueError("Invalid signature")

    payload = json.loads(b64url_decode(payload_b64))

    # Проверка exp
    if "exp" in payload and payload["exp"] < time.time():
        raise ValueError("Token expired")

    return payload


if __name__ == "__main__":
    secret = "super-secret-key-at-least-32-bytes-long!"
    payload = {
        "sub": "123",
        "name": "Alice",
        "role": "admin",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
    }

    token = create_jwt(payload, secret)
    print("TOKEN:", token)

    # Декодируем и смотрим, что внутри (без проверки подписи!)
    header_b64, payload_b64, _ = token.split(".")
    print("HEADER :", json.loads(b64url_decode(header_b64)))
    print("PAYLOAD:", json.loads(b64url_decode(payload_b64)))

    # Проверяем
    decoded = verify_jwt(token, secret)
    print("VERIFIED:", decoded)

    # Ломаем токен — меняем payload
    tampered = token[:-5] + "AAAAA"
    try:
        verify_jwt(tampered, secret)
    except ValueError as e:
        print("TAMPERED DETECTED:", e)
