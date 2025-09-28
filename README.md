# 🤖 Lech's Automation Actions

> Centralized GitHub Actions for automating project monitoring, maintenance, and reporting across all repositories.

<!-- AUTO-GENERATED:BADGES:START -->
![Workflow Status](https://img.shields.io/badge/workflows-4_active-green?style=for-the-badge)
![Last Update](https://img.shields.io/badge/updated-2025--09--28_12:08-blue?style=for-the-badge)
![Automation Health](https://img.shields.io/badge/health-100%25-green?style=for-the-badge)
<!-- AUTO-GENERATED:BADGES:END -->

## 🎯 Purpose

This repository contains GitHub Actions workflows that automate various tasks across my development projects:
- 📊 Project activity monitoring
- 📝 Documentation updates
- 🔄 Sync operations
- 📈 Analytics and reporting
- 🧹 Maintenance tasks

## 🚀 Workflow Status

<!-- AUTO-GENERATED:STATUS:START -->
| Workflow | Status | Schedule | Last Run | Success Rate | Actions |
|----------|--------|----------|----------|--------------|---------|
| **📅 Daily Activity Summary** | 🟢 Active | `Daily at 9 AM` | N/A | N/A | [View Runs](../../actions/workflows/daily-summary.yml) |
| **📊 Project Activity Monitor** | 🟢 Active | `Hourly at :15` | N/A | N/A | [View Runs](../../actions/workflows/project-monitor.yml) |
| **📝 Update README** | 🟢 Active | `Every 4 hours` | N/A | N/A | [View Runs](../../actions/workflows/update-readme.yml) |
| **🔄 Sync to Obsidian Vault** | 🟢 Active | `Every 6 hours` | N/A | N/A | [View Runs](../../actions/workflows/sync-vault.yml) |
<!-- AUTO-GENERATED:STATUS:END -->

## 📈 Metrics Dashboard

<!-- AUTO-GENERATED:METRICS:START -->
### 🎯 Project Statistics
| Metric | Value | Trend |
|--------|-------|-------|
| **Active Projects** | 0 | - |
| **Files Tracked** | 10 | - |
<!-- AUTO-GENERATED:METRICS:END -->

## 📝 Recent Activity

<!-- AUTO-GENERATED:ACTIVITY:START -->
### 🔄 Recent Commits
| Time | Hash | Message | Author |
|------|------|---------|--------|
| 4 hours ago | `fa6c3be` | 📝 Auto-update README with live data | GitHub Actions Bot |
| 8 hours ago | `e384b73` | 📝 Auto-update README with live data | GitHub Actions Bot |
| 12 hours ago | `e572654` | 📝 Auto-update README with live data | GitHub Actions Bot |
| 16 hours ago | `4584f94` | 📝 Auto-update README with live data | GitHub Actions Bot |
| 20 hours ago | `9b5700f` | 📝 Auto-update README with live data | GitHub Actions Bot |
<!-- AUTO-GENERATED:ACTIVITY:END -->

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
---

*Last automated update: 2025-09-28 12:08:45 UTC*