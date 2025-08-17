# 🔐 GitHub Actions Secrets Configuration

## Required Secrets

### 1. `VAULT_REPO_TOKEN` (Required if vault is private)
Personal Access Token for accessing your Obsidian vault repository.

**How to create:**
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Name: "Vault Access for Actions"
4. Select scopes:
   - `repo` (full control)
   - `workflow` (if vault has actions)
5. Generate and copy token
6. Add to repository secrets

**Add to repository:**
```
Settings → Secrets and variables → Actions → New repository secret
Name: VAULT_REPO_TOKEN
Value: [paste your token]
```

### 2. `PROJECTS_PATH` (Optional)
Path to your projects directory. Default: `~/PROJECTS_all`

### 3. `OBSIDIAN_VAULT_PATH` (Optional)
Path to your Obsidian vault. Default: `sprintx` repository

## Setting Up Secrets

### Step 1: Navigate to Secrets
1. Go to your `PROJECT_actions` repository
2. Click Settings tab
3. Navigate to Secrets and variables → Actions

### Step 2: Add Repository Secrets

#### Essential Secret (for private vault):
```
VAULT_REPO_TOKEN = ghp_xxxxxxxxxxxxxxxxxxxx
```

#### Optional Secrets:
```
PROJECTS_PATH = /custom/path/to/projects
NOTIFICATION_EMAIL = your-email@example.com
SLACK_WEBHOOK = https://hooks.slack.com/services/xxx
```

## Repository Permissions

### For Public Repositories
No additional tokens needed - `GITHUB_TOKEN` is sufficient.

### For Private Repositories
You need `VAULT_REPO_TOKEN` with these permissions:
- Read access to code
- Write access to code
- Read access to metadata
- Read and write access to actions (if applicable)

## Testing Secrets

### Manual Test Workflow
Create `.github/workflows/test-secrets.yml`:

```yaml
name: Test Secrets
on:
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Test Vault Access
        env:
          TOKEN: ${{ secrets.VAULT_REPO_TOKEN || secrets.GITHUB_TOKEN }}
        run: |
          if [ -z "$TOKEN" ]; then
            echo "❌ No token available"
            exit 1
          else
            echo "✅ Token is configured"
          fi
      
      - name: Test Checkout
        uses: actions/checkout@v4
        with:
          repository: ${{ github.repository_owner }}/sprintx
          token: ${{ secrets.VAULT_REPO_TOKEN || secrets.GITHUB_TOKEN }}
```

## Environment Variables

These are automatically available:
- `GITHUB_TOKEN` - Default token with repo permissions
- `GITHUB_REPOSITORY` - Current repository
- `GITHUB_REPOSITORY_OWNER` - Repository owner
- `GITHUB_SHA` - Commit SHA
- `GITHUB_REF` - Branch/tag reference

## Security Best Practices

### Do's ✅
- Use minimal required permissions
- Rotate tokens regularly (every 90 days)
- Use repository secrets, not organization secrets
- Test with minimal permissions first
- Use `GITHUB_TOKEN` when possible

### Don'ts ❌
- Never commit tokens to code
- Don't use classic PATs if fine-grained work
- Avoid using admin tokens
- Don't share tokens between projects
- Never log secret values

## Troubleshooting

### Issue: "Resource not accessible by integration"
**Solution**: Token lacks required permissions. Check scopes.

### Issue: "Bad credentials"
**Solution**: Token expired or incorrect. Regenerate token.

### Issue: "Repository not found"
**Solution**: Token lacks access to private repo. Add repo scope.

### Issue: "Push rejected"
**Solution**: Token needs write permissions. Update scopes.

## Token Scopes Reference

### Minimal Scopes
For basic monitoring:
- `repo:status` - Access commit status
- `public_repo` - Access public repositories

### Standard Scopes
For full functionality:
- `repo` - Full control of private repositories
- `workflow` - Update GitHub Action workflows

### Extended Scopes
For advanced features:
- `write:packages` - Upload packages
- `delete:packages` - Delete packages
- `admin:org` - Manage organization

## Verification Checklist

- [ ] Created Personal Access Token
- [ ] Added `VAULT_REPO_TOKEN` to secrets
- [ ] Tested vault checkout works
- [ ] Verified write permissions
- [ ] Confirmed workflows can run
- [ ] Set up token expiration reminder

## Token Rotation Schedule

1. **Create reminder**: Set calendar reminder for 80 days
2. **Generate new token**: Create before old expires
3. **Update secret**: Replace in repository settings
4. **Test workflows**: Run manual test
5. **Delete old token**: Remove from GitHub settings

## Support

If you encounter issues:
1. Check workflow logs for specific errors
2. Verify token permissions match requirements
3. Test with manual workflow dispatch
4. Review GitHub Actions documentation

---

*Last Updated: 2025-08-17*