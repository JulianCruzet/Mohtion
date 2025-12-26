#!/usr/bin/env python3
"""Debug the actual GitHub API call."""
import asyncio
import httpx
from mohtion.integrations.github_app import GitHubApp


async def main():
    """Test the GitHub API call."""
    print("Testing GitHub App API call...\n")

    github_app = GitHubApp()

    # Generate JWT
    jwt_token = github_app._generate_jwt()
    print(f"[OK] JWT generated: {jwt_token[:50]}...")
    print()

    # Try to call the API
    print("Making API call to: https://api.github.com/app/installations")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.github.com/app/installations",
                headers={
                    "Authorization": f"Bearer {jwt_token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
            )

            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text[:500]}")

            if response.status_code == 401:
                print("\n[ERROR] GitHub rejected the JWT!")
                print("This usually means:")
                print("  1. The private key doesn't match the App ID")
                print("  2. The private key was regenerated")
                print("  3. The App ID is incorrect")
                print("\nPlease verify:")
                print(f"  - App ID in .env matches your GitHub App: 2540308")
                print(f"  - Private key is the latest one for this app")

        except Exception as e:
            print(f"[ERROR] API call failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
