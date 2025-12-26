#!/usr/bin/env python3
"""Debug JWT generation."""
import jwt
import time
from mohtion.config import get_settings


def main():
    """Test JWT generation."""
    settings = get_settings()

    print(f"App ID: {settings.github_app_id}")
    print(f"Private key length: {len(settings.github_private_key)} chars")
    print()

    # Try to generate a JWT
    try:
        now = int(time.time())
        payload = {
            "iat": now - 60,
            "exp": now + 600,
            "iss": settings.github_app_id,
        }

        token = jwt.encode(payload, settings.github_private_key, algorithm="RS256")
        print(f"[OK] JWT generated successfully")
        print(f"JWT: {token[:50]}...")
        print()

        # Decode to verify
        decoded = jwt.decode(token, settings.github_private_key, algorithms=["RS256"], options={"verify_signature": False})
        print(f"[OK] JWT decoded:")
        print(f"  Issuer (app_id): {decoded['iss']}")
        print(f"  Issued at: {decoded['iat']}")
        print(f"  Expires: {decoded['exp']}")

    except Exception as e:
        print(f"[ERROR] Failed to generate JWT: {e}")


if __name__ == "__main__":
    main()
