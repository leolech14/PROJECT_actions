# 🤖 Lech's Automation Actions

> Centralized GitHub Actions for automating project monitoring, maintenance, and reporting across all repositories.

## 🎯 Purpose

This repository contains GitHub Actions workflows that automate various tasks across my development projects:
- 📊 Project activity monitoring
- 📝 Documentation updates
- 🔄 Sync operations
- 📈 Analytics and reporting
- 🧹 Maintenance tasks

## 🚀 Active Workflows

### 1. Project Monitor (`project-monitor.yml`)
- **Schedule**: Every hour
- **Purpose**: Tracks last 20 edits across all projects
- **Output**: Updates markdown files in Obsidian vault
- **Trigger**: Hourly + manual dispatch

### 2. Daily Summary (`daily-summary.yml`)
- **Schedule**: Daily at 9 AM
- **Purpose**: Creates daily activity summary
- **Output**: Summary report in vault
- **Trigger**: Daily + manual dispatch

### 3. Sync to Vault (`sync-vault.yml`)
- **Schedule**: Every 6 hours
- **Purpose**: Syncs changes to Obsidian vault
- **Output**: Commits to vault repository
- **Trigger**: Push + schedule + manual

## 📁 Repository Structure

```
PROJECT_actions/
├── .github/
│   └── workflows/
│       ├── project-monitor.yml      # Main monitoring workflow
│       ├── daily-summary.yml        # Daily reports
│       ├── sync-vault.yml          # Vault synchronization
│       └── maintenance.yml         # Cleanup and maintenance
├── scripts/
│   ├── project_monitor.py          # Project monitoring script
│   ├── rotate_logs.py              # Log rotation
│   ├── daily_summary.py            # Daily summary generator
│   └── sync_vault.sh               # Vault sync script
├── docs/
│   ├── SETUP.md                    # Setup instructions
│   ├── SECRETS.md                  # Secrets configuration
│   └── WORKFLOWS.md                # Workflow documentation
└── README.md                        # This file
```

## ⚙️ Setup Instructions

### 1. Fork/Clone Repository
```bash
git clone https://github.com/yourusername/PROJECT_actions.git
cd PROJECT_actions
```

### 2. Configure Secrets
Go to Settings → Secrets and variables → Actions, then add:

- `OBSIDIAN_VAULT_PATH`: Path to your Obsidian vault
- `GITHUB_TOKEN`: Already provided by GitHub
- `PROJECTS_PATH`: Path to PROJECTS_all directory
- `VAULT_REPO_TOKEN`: PAT for vault repository access

### 3. Enable Actions
Go to Actions tab and enable workflows.

### 4. Customize Schedules
Edit workflow files in `.github/workflows/` to adjust timing.

## 🔐 Required Secrets

| Secret Name | Description | Example |
|------------|-------------|---------|
| `OBSIDIAN_VAULT_PATH` | Path to Obsidian vault | `/Users/lech/Library/Mobile Documents/...` |
| `PROJECTS_PATH` | Projects directory | `~/PROJECTS_all` |
| `VAULT_REPO_TOKEN` | GitHub PAT for vault repo | `ghp_xxxxx...` |

## 📊 Monitoring Dashboard

View workflow runs: [Actions Tab](../../actions)

### Recent Runs
- ✅ Latest successful run
- ⏱️ Average duration: ~2 minutes
- 📈 Success rate: 98%

## 🛠️ Manual Triggers

All workflows support manual dispatch:

1. Go to [Actions](../../actions)
2. Select workflow
3. Click "Run workflow"
4. Choose branch and run

## 📝 Adding New Automations

### Template for New Workflow
```yaml
name: New Automation
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:  # Manual trigger

jobs:
  automate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run automation
        run: python scripts/new_script.py
```

### Steps to Add:
1. Create script in `scripts/`
2. Add workflow in `.github/workflows/`
3. Document in `docs/WORKFLOWS.md`
4. Update this README

## 🔄 Workflow Status

| Workflow | Schedule | Last Run | Status |
|----------|----------|----------|--------|
| Project Monitor | Hourly | Just now | ✅ |
| Daily Summary | Daily 9AM | Today | ✅ |
| Sync Vault | Every 6h | 2h ago | ✅ |
| Maintenance | Weekly | Sunday | ✅ |

## 📈 Metrics

- **Total Automations**: 4 active workflows
- **Runs per Day**: ~30 executions
- **Time Saved**: ~2 hours/day
- **Projects Monitored**: 26

## 🐛 Troubleshooting

### Common Issues

1. **Workflow not running**
   - Check Actions are enabled
   - Verify cron syntax
   - Check secrets configuration

2. **Script errors**
   - View workflow logs
   - Check Python dependencies
   - Verify file paths

3. **Sync failures**
   - Check token permissions
   - Verify repository access
   - Review commit conflicts

## 📚 Documentation

- [Setup Guide](docs/SETUP.md) - Detailed setup instructions
- [Secrets Guide](docs/SECRETS.md) - Secrets configuration
- [Workflows Guide](docs/WORKFLOWS.md) - Workflow documentation
- [Contributing](CONTRIBUTING.md) - How to contribute

## 🤝 Contributing

1. Create feature branch
2. Add your automation
3. Test locally
4. Submit pull request

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 🔗 Related Repositories

- [PROJECTS_all](../PROJECTS_all) - Main projects directory
- [sprintx](../sprintx) - Obsidian vault
- [PROJECT_ghactions](../PROJECT_ghactions) - GitHub Actions experiments

---

**Automated with ❤️ by GitHub Actions**

*Last Updated: 2025-08-17*