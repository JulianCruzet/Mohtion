#!/usr/bin/env python3
"""Helper script to encode your GitHub App private key to base64."""
import base64
import sys
from pathlib import Path


def encode_pem_file(pem_path: str) -> str:
    """Encode a PEM file to base64."""
    pem_file = Path(pem_path)

    if not pem_file.exists():
        print(f"Error: File not found: {pem_path}")
        sys.exit(1)

    # Read the PEM file
    pem_content = pem_file.read_bytes()

    # Encode to base64
    base64_encoded = base64.b64encode(pem_content).decode('utf-8')

    return base64_encoded


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python encode_key.py <path-to-your-private-key.pem>")
        print("\nExample:")
        print("  python encode_key.py ./my-github-app.2024-12-26.private-key.pem")
        sys.exit(1)

    pem_path = sys.argv[1]
    print(f"Encoding {pem_path}...\n")

    encoded = encode_pem_file(pem_path)

    print("=" * 60)
    print("Your base64-encoded private key:")
    print("=" * 60)
    print(encoded)
    print("=" * 60)
    print("\nCopy the above value and paste it in your .env file as:")
    print("GITHUB_PRIVATE_KEY_BASE64=<the_value_above>")


if __name__ == "__main__":
    main()
