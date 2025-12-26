#!/usr/bin/env python3
"""Debug script to verify GitHub App credentials."""
import base64
from mohtion.config import get_settings


def main():
    """Check if credentials can be loaded."""
    print("Checking .env credentials...\n")

    try:
        settings = get_settings()

        print(f"[OK] GITHUB_APP_ID loaded: {settings.github_app_id}")
        print(f"[OK] GITHUB_WEBHOOK_SECRET loaded: {settings.github_webhook_secret[:10]}...")
        print(f"[OK] ANTHROPIC_API_KEY loaded: {settings.anthropic_api_key[:20]}...")

        # Check private key
        try:
            private_key = settings.github_private_key
            if private_key.startswith("-----BEGIN"):
                print(f"[OK] Private key decoded successfully")
                print(f"  Key starts with: {private_key[:50]}...")
                print(f"  Key length: {len(private_key)} characters")
            else:
                print("[ERROR] Private key doesn't look like a PEM file")
                print(f"  Starts with: {private_key[:50]}")
        except Exception as e:
            print(f"[ERROR] Failed to decode private key: {e}")

    except Exception as e:
        print(f"[ERROR] Error loading settings: {e}")


if __name__ == "__main__":
    main()
