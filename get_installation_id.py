#!/usr/bin/env python3
"""Helper script to get your GitHub App installation ID."""
import asyncio
from mohtion.integrations.github_app import GitHubApp


async def main():
    """Get all installations of your GitHub App."""
    print("Fetching GitHub App installations...\n")

    github_app = GitHubApp()

    try:
        installations = await github_app.get_installations()

        if not installations:
            print("No installations found.")
            print("\nTo install your GitHub App:")
            print("1. Go to https://github.com/settings/apps/YOUR_APP_NAME")
            print("2. Click 'Install App' in the left sidebar")
            print("3. Choose a repository to install on")
            return

        print(f"Found {len(installations)} installation(s):\n")

        for install in installations:
            print(f"Installation ID: {install['id']}")
            print(f"  Account: {install['account']['login']}")
            print(f"  Type: {install['account']['type']}")
            print(f"  Repositories: {install.get('repository_selection', 'unknown')}")
            print()

        # If there's only one installation, suggest using it
        if len(installations) == 1:
            install_id = installations[0]['id']
            account = installations[0]['account']['login']
            print(f"✓ Use Installation ID: {install_id} (for {account})")

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure your .env file has:")
        print("  - GITHUB_APP_ID")
        print("  - GITHUB_PRIVATE_KEY_BASE64")


if __name__ == "__main__":
    asyncio.run(main())
