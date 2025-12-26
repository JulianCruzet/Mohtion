"""GitHub webhook handlers."""

import logging

from fastapi import APIRouter, Header, HTTPException, Request

from mohtion.integrations.github_app import GitHubApp

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/github")
async def github_webhook(
    request: Request,
    x_github_event: str = Header(...),
    x_hub_signature_256: str = Header(...),
) -> dict[str, str]:
    """Handle incoming GitHub webhooks."""
    # Get raw body for signature verification
    body = await request.body()

    # Verify webhook signature
    github_app = GitHubApp()
    is_valid = await github_app.verify_webhook_signature(body, x_hub_signature_256)
    if not is_valid:
        logger.warning("Invalid webhook signature")
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse payload
    payload = await request.json()

    # Handle different event types
    match x_github_event:
        case "installation":
            return await handle_installation(payload)
        case "push":
            return await handle_push(payload)
        case "ping":
            return {"status": "pong"}
        case _:
            logger.debug(f"Ignoring event type: {x_github_event}")
            return {"status": "ignored", "event": x_github_event}


async def handle_installation(payload: dict) -> dict[str, str]:
    """Handle GitHub App installation events."""
    action = payload.get("action")
    installation_id = payload.get("installation", {}).get("id")
    account = payload.get("installation", {}).get("account", {}).get("login")

    logger.info(f"Installation {action}: {account} (ID: {installation_id})")

    match action:
        case "created":
            # New installation - could trigger initial scan
            logger.info(f"New installation from {account}")
            # TODO: Queue initial scan job
        case "deleted":
            logger.info(f"Installation removed by {account}")
        case _:
            logger.debug(f"Installation action: {action}")

    return {"status": "ok", "action": action}


async def handle_push(payload: dict) -> dict[str, str]:
    """Handle push events - optionally trigger scans."""
    repo = payload.get("repository", {})
    repo_name = repo.get("full_name")
    ref = payload.get("ref", "")
    default_branch = repo.get("default_branch", "main")

    # Only process pushes to default branch
    if ref != f"refs/heads/{default_branch}":
        logger.debug(f"Ignoring push to non-default branch: {ref}")
        return {"status": "ignored", "reason": "not default branch"}

    installation_id = payload.get("installation", {}).get("id")
    logger.info(f"Push to {repo_name} (installation: {installation_id})")

    # TODO: Queue scan job via ARQ
    # For MVP, we'll trigger scans manually or on schedule

    return {"status": "ok", "repo": repo_name}
