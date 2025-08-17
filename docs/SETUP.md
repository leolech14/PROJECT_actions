# 🚀 Complete Setup Guide for PROJECT_actions

## Prerequisites

- GitHub account
- Git installed locally
- Python 3.8+ (for local testing)
- GitHub CLI (optional, for easier setup)

## Step 1: Create GitHub Repository

### Option A: Using GitHub CLI (Recommended)
```bash
cd ~/PROJECTS_all/PROJECT_actions
gh repo create PROJECT_actions --public --source=. --remote=origin --push
```

### Option B: Manual Creation
1. Go to https://github.com/new
2. Repository name: `PROJECT_actions`
3. Description: "Automated monitoring and maintenance workflows"
4. Visibility: Public (or Private if you prefer)
5. Initialize: Don't add README, .gitignore, or license
6. Create repository

## Step 2: Initial Setup

### Clone and Configure
```bash
# If creating new
cd ~/PROJECTS_all/
git clone https://github.com/YOUR_USERNAME/PROJECT_actions.git
cd PROJECT_actions

# Or if you already have the files
cd ~/PROJECTS_all/PROJECT_actions
git init
git remote add origin https://github.com/YOUR_USERNAME/PROJECT_actions.git
```

### Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

## Step 3: Configure Secrets

### Required Secrets

1. **Navigate to Secrets**
   - Go to your repository on GitHub
   - Settings → Secrets and variables → Actions

2. **Add VAULT_REPO_TOKEN** (if vault is private)
   - Click "New repository secret"
   - Name: `VAULT_REPO_TOKEN`
   - Value: Your Personal Access Token
   
   To create PAT:
   - GitHub → Settings → Developer settings
   - Personal access tokens → Tokens (classic)
   - Generate new token
   - Select `repo` scope
   - Copy and paste as secret value

## Step 4: Repository Structure

Ensure you have this structure:
```
PROJECT_actions/
├── .github/
│   └── workflows/
│       ├── project-monitor.yml
│       ├── sync-vault.yml
│       └── daily-summary.yml
├── scripts/
│   ├── project_monitor.py
│   └── rotate_logs.py
├── docs/
│   ├── SETUP.md
│   └── SECRETS.md
├── .gitignore
├── README.md
└── setup.sh
```

## Step 5: Enable GitHub Actions

1. Go to repository on GitHub
2. Click "Actions" tab
3. If prompted, enable GitHub Actions
4. You should see your workflows listed

## Step 6: Test Workflows

### Test Project Monitor
1. Go to Actions tab
2. Select "📊 Project Activity Monitor"
3. Click "Run workflow"
4. Select branch: main
5. Click "Run workflow" button
6. Monitor the run progress

### Test Sync Workflow
1. Go to Actions tab
2. Select "🔄 Sync to Obsidian Vault"
3. Click "Run workflow"
4. Choose sync type: "full-sync"
5. Run and monitor

## Step 7: Verify Automation

### Check Scheduled Runs
Workflows will run automatically:
- **Project Monitor**: Every hour at :15
- **Daily Summary**: Daily at 9 AM UTC
- **Sync Vault**: Every 6 hours

### Monitor Status
- Go to Actions tab to see run history
- Green checkmark = success
- Red X = failure (check logs)

## Step 8: Customize Settings

### Adjust Schedule Times
Edit `.github/workflows/project-monitor.yml`:
```yaml
schedule:
  - cron: '15 * * * *'  # Change this cron expression
```

Cron format: `minute hour day month weekday`
- `0 */2 * * *` = Every 2 hours
- `0 9 * * *` = Daily at 9 AM
- `0 0 * * 0` = Weekly on Sunday

### Add Notifications
Add to workflow:
```yaml
- name: Send Notification
  if: failure()
  run: |
    curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
      -H 'Content-Type: application/json' \
      -d '{"text":"Workflow failed!"}'
```

## Step 9: Local Testing

### Test Scripts Locally
```bash
# Test monitoring script
cd scripts
python3 project_monitor.py

# Test with specific project
python3 project_monitor.py --project PROJECT_finapp
```

### Test Workflows Locally
Use [act](https://github.com/nektos/act) to test workflows:
```bash
brew install act
act -j monitor  # Test monitor job
```

## Step 10: Troubleshooting

### Common Issues and Solutions

#### Workflow Not Running
- Check Actions are enabled
- Verify cron syntax is correct
- Check for workflow errors in Actions tab

#### Permission Denied
- Ensure VAULT_REPO_TOKEN has correct permissions
- Token needs `repo` scope for private repos
- Check token hasn't expired

#### Script Errors
- View workflow run logs
- Check Python version compatibility
- Verify file paths are correct

#### No Changes Detected
- Normal if no project activity
- Check `.project_monitor_state.json` exists
- Verify projects path is correct

## Maintenance

### Regular Tasks
- **Weekly**: Check workflow success rate
- **Monthly**: Review and rotate tokens
- **Quarterly**: Update dependencies

### Monitoring Health
```bash
# Check recent runs
gh run list --workflow=project-monitor.yml --limit 10

# View specific run
gh run view [RUN_ID]

# Download logs
gh run download [RUN_ID]
```

## Advanced Configuration

### Custom Project Paths
Modify in workflows:
```yaml
env:
  PROJECTS_PATH: /custom/path/to/projects
  VAULT_PATH: /custom/path/to/vault
```

### Multiple Vaults
Create separate workflows for each vault:
```yaml
- name: Checkout Vault 2
  uses: actions/checkout@v4
  with:
    repository: owner/vault2
    path: vault2
```

### Conditional Monitoring
Only monitor specific projects:
```yaml
- name: Monitor Specific Projects
  run: |
    for project in PROJECT_finapp PROJECT_obsidian; do
      python scripts/project_monitor.py --project $project
    done
```

## Security Best Practices

1. **Minimal Permissions**: Only grant required token scopes
2. **Secret Rotation**: Update tokens every 90 days
3. **Audit Logs**: Review Action logs regularly
4. **Branch Protection**: Protect main branch
5. **Code Review**: Review workflow changes

## Getting Help

### Resources
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Workflow Syntax](https://docs.github.com/actions/reference/workflow-syntax-for-github-actions)
- [Secrets Management](https://docs.github.com/actions/security-guides/encrypted-secrets)

### Support
- Check workflow logs for errors
- Open issue in repository
- Review GitHub Actions status page

## Success Checklist

- [ ] Repository created on GitHub
- [ ] Files pushed to repository
- [ ] Secrets configured
- [ ] Actions enabled
- [ ] Test workflow successful
- [ ] Scheduled runs working
- [ ] Vault updates visible

---

**Congratulations! Your automation system is ready! 🎉**

*Last Updated: 2025-08-17*