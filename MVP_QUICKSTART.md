# Mohtion MVP Quickstart Guide

This guide walks you through setting up and running the Mohtion MVP (Minimum Viable Product) to test the autonomous tech debt hunting agent.

## Prerequisites

- Python 3.12+
- Git installed
- A GitHub account
- An Anthropic API account (with $5-10 in credits)

## Step 1: Register a GitHub App

1. Go to https://github.com/settings/apps/new
2. Fill in the app details:
   - **App name**: `mohtion-dev` (or your preferred name)
   - **Homepage URL**: `https://github.com/your-username/mohtion`
   - **Webhook URL**: Leave blank for now (you'll add this later when deploying)
   - **Webhook secret**: Generate a random string (e.g., using `openssl rand -hex 20`)

3. Set **Repository permissions**:
   - **Contents**: Read & write
   - **Metadata**: Read-only (automatically selected)
   - **Pull requests**: Read & write

4. Click **Create GitHub App**

5. **Save your App ID** (you'll need this)

6. **Generate a private key**:
   - Scroll down to "Private keys"
   - Click "Generate a private key"
   - Save the `.pem` file that downloads

## Step 2: Install the GitHub App

1. In your GitHub App settings, click **Install App** (left sidebar)
2. Choose your account
3. Select **"Only select repositories"**
4. Choose a test repository (preferably one with Python code and tests)
5. Click **Install**
6. **Note the Installation ID** from the URL: `https://github.com/settings/installations/[INSTALLATION_ID]`

## Step 3: Set Up Anthropic API

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Go to **API Keys** in settings
4. Create a new API key
5. **Add credits**: Go to Plans & Billing and add at least $5-10 in credits

## Step 4: Clone and Set Up the Project

```bash
# Clone the repository
git clone https://github.com/your-username/Mohtion.git
cd Mohtion

# Install dependencies
pip install -e ".[dev]"
```

## Step 5: Configure Environment Variables

### Encode your private key

First, encode your GitHub App private key to base64:

```bash
python encode_key.py path/to/your-github-app-private-key.pem
```

This will output a long base64 string. Copy it.

### Create `.env` file

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
# GitHub App Configuration
GITHUB_APP_ID=your_app_id_here
GITHUB_PRIVATE_KEY_BASE64=your_base64_encoded_key_here
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here

# Anthropic API
ANTHROPIC_API_KEY=sk-ant-api03-your_key_here

# Redis (for job queue - not needed for MVP testing)
REDIS_URL=redis://localhost:6379

# App Settings
DEBUG=true
LOG_LEVEL=INFO

# Agent Settings
MAX_RETRIES=2
MAX_PRS_PER_DAY=3
DEFAULT_COMPLEXITY_THRESHOLD=10
```

**IMPORTANT**:
- `GITHUB_PRIVATE_KEY_BASE64` must be on ONE line (no line breaks!)
- Make sure there are no extra spaces before or after the `=` sign

### Verify your credentials

Test that everything loads correctly:

```bash
python debug_credentials.py
```

You should see:
```
[OK] GITHUB_APP_ID loaded: 12345678
[OK] GITHUB_WEBHOOK_SECRET loaded: whsec_...
[OK] ANTHROPIC_API_KEY loaded: sk-ant-...
[OK] Private key decoded successfully
```

## Step 6: Test the MVP

### Option A: Simple Scan Test (No PR creation)

Test just the scanner to see what tech debt it finds:

```bash
python test_mvp_low_threshold.py
```

Edit the file first to set your repository details:
- `OWNER`: Your GitHub username
- `REPO`: Your repository name
- `INSTALLATION_ID`: From Step 2

This will scan the repository and show you what tech debt targets were found.

### Option B: Full Agent Loop Test

**WARNING**: This will attempt to create a real PR on your repository!

1. Edit `test_full_loop.py` and set:
   - `OWNER`: Your GitHub username
   - `REPO`: Your repository name (must have tests!)
   - `INSTALLATION_ID`: From Step 2

2. Run the test:
```bash
python test_full_loop.py
```

This executes the full Plan-Act-Verify loop:
1. **Reconnaissance**: Scans for tech debt
2. **Refactoring**: Uses Claude to fix the code
3. **Verification**: Runs tests
4. **Self-healing**: Retries if tests fail (max 2 times)
5. **PR Creation**: Opens a PR if tests pass

## Step 7: Start the Web Service (Optional)

To run the FastAPI web service for webhook handling:

```bash
python -m uvicorn mohtion.web.app:app --host 0.0.0.0 --port 8000 --reload
```

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

API documentation available at: http://localhost:8000/docs

## Troubleshooting

### "401 Unauthorized" from GitHub API

**Cause**: JWT timing issue or invalid credentials

**Fix**:
1. Verify your `GITHUB_APP_ID` matches your app
2. Ensure the private key is correctly base64 encoded
3. Make sure the private key is on ONE line in `.env`
4. Check that you downloaded the key for the correct app

### "invalid x-api-key" from Anthropic

**Cause**: Invalid or expired API key

**Fix**:
1. Generate a new API key at https://console.anthropic.com/settings/keys
2. Make sure you have credits in your account
3. Update `ANTHROPIC_API_KEY` in `.env`

### "Your credit balance is too low"

**Cause**: Anthropic account has no credits

**Fix**:
1. Go to https://console.anthropic.com/settings/billing
2. Add at least $5-10 in credits

### Tests fail / No PR created

**Cause**: Repository has no tests or tests are failing

**Expected behavior**: Mohtion will NOT create a PR if tests fail (safety feature)

**Fix**:
1. Test on a repository with a working test suite
2. Add tests to your repository
3. Check test output in the logs to see why tests failed

### Windows Permission Errors

**Cause**: Git files locked by Windows

**Fix**: This is a known issue on Windows when cleaning up temp directories. It doesn't affect functionality - just ignore the cleanup errors.

## Understanding the Output

When you run `test_full_loop.py`, you'll see output like:

```
Phase 1: Reconnaissance
  Found 3 tech debt targets
  Target acquired: main() - complexity 10

Phase 2: Refactoring
  Refactoring NewtonCradle.py:main (lines 194-239)
  Applied refactoring

Phase 3: Verification
  Running tests: pytest
  Tests passed: ✓

Phase 4: Opening PR
  PR opened: https://github.com/user/repo/pull/123
```

### Success indicators:
- ✅ All phases complete
- ✅ Tests passed
- ✅ PR URL returned

### Expected failures:
- ⚠️ No tech debt found (code is too clean!)
- ⚠️ Tests failed (safety mechanism working correctly)

## Next Steps

Once the MVP is working:

1. **Test on a real repository** with a proper test suite
2. **Enable Docker** (requires enabling virtualization in BIOS)
3. **Set up webhooks** for automatic scanning on push events
4. **Deploy to production** (Railway, Fly.io, or AWS)
5. **Add more analyzers** (type hints, duplicates, deprecations)

## Key Files

- `test_mvp.py` - Basic MVP test script
- `test_mvp_low_threshold.py` - Scan-only test (no PR)
- `test_full_loop.py` - Full agent loop test (creates PR)
- `debug_credentials.py` - Verify credentials are loaded correctly
- `encode_key.py` - Helper to encode GitHub private key
- `get_installation_id.py` - Get your GitHub App installation ID

## Configuration

You can customize the agent behavior by editing `.env`:

- `MAX_RETRIES`: How many times to retry self-healing (default: 2)
- `MAX_PRS_PER_DAY`: Limit PRs per repository per day (default: 3)
- `DEFAULT_COMPLEXITY_THRESHOLD`: Cyclomatic complexity threshold (default: 10)

Lower the threshold to catch simpler issues:
```env
DEFAULT_COMPLEXITY_THRESHOLD=5
```

## Support

- Check `LOGBOOK.md` for session history and known issues
- Check `TODO.md` for roadmap and upcoming features
- Review `CLAUDE.md` for architecture details
- See `README.md` for project overview

## Limitations (MVP)

- Only analyzes Python files (JavaScript/TypeScript support planned)
- Only detects cyclomatic complexity (more analyzers planned)
- Requires passing tests to create PR (by design!)
- Local execution only (cloud deployment in Phase 12)
- No database persistence yet (tracked in memory only)
- No webhook automation yet (manual trigger via test scripts)

## Success Criteria

The MVP is working correctly if:
1. ✅ Scanner finds tech debt targets in Python code
2. ✅ Claude API generates refactored code
3. ✅ Tests are executed automatically
4. ✅ Self-healing attempts when tests fail
5. ✅ PR is NOT created when tests fail (safety!)
6. ✅ PR IS created when tests pass

**Note**: It's normal (and good!) if no PR is created when tests fail. This proves the safety mechanism works!
