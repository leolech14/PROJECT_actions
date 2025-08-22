#!/usr/bin/env python3
"""
README Generator - Automatically updates README with live data
"""

import os
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path

# Configuration
README_PATH = "README.md"
WORKFLOW_STATE_FILE = ".workflow_state.json"
METRICS_CACHE_FILE = ".metrics_cache.json"

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def load_json_file(filepath):
    """Load JSON file safely"""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            log(f"Error loading {filepath}: {e}")
    return {}

def save_json_file(filepath, data):
    """Save JSON file safely"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        log(f"Error saving {filepath}: {e}")
        return False

def get_recent_commits(limit=10):
    """Get recent Git commits"""
    try:
        result = subprocess.run(
            ['git', 'log', '--oneline', f'-{limit}', '--pretty=format:%h|%s|%ar|%an'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        commits = []
        if result.returncode == 0 and result.stdout:
            for line in result.stdout.strip().split('\n'):
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        commits.append({
                            'hash': parts[0],
                            'message': parts[1][:50],  # Truncate long messages
                            'time_ago': parts[2],
                            'author': parts[3]
                        })
        return commits
    except Exception as e:
        log(f"Error getting commits: {e}")
        return []

def generate_badges(workflow_data, metrics_data):
    """Generate status badges"""
    active_count = sum(1 for w in workflow_data.get('workflows', []) if w.get('enabled'))
    total_count = len(workflow_data.get('workflows', []))
    
    if total_count == 0:
        status_color = "lightgrey"
        status_text = "no_workflows"
    elif active_count == total_count:
        status_color = "green"
        status_text = f"{active_count}_active"
    elif active_count == 0:
        status_color = "red"
        status_text = f"{total_count}_disabled"
    else:
        status_color = "yellow"
        status_text = f"{active_count}%2F{total_count}_active"  # URL encode "/"
    
    update_time = datetime.now().strftime("%Y--%m--%d_%H:%M")
    
    badges = [
        f"![Workflow Status](https://img.shields.io/badge/workflows-{status_text}-{status_color}?style=for-the-badge)",
        f"![Last Update](https://img.shields.io/badge/updated-{update_time}-blue?style=for-the-badge)",
    ]
    
    # Add project count if available
    project_count = metrics_data.get('project_count', 0)
    if project_count > 0:
        badges.append(f"![Projects](https://img.shields.io/badge/projects-{project_count}_monitored-green?style=for-the-badge)")
    
    # Add automation health
    if active_count > 0:
        health_percent = int((active_count / total_count) * 100)
        health_color = "green" if health_percent >= 75 else "orange" if health_percent >= 50 else "red"
        badges.append(f"![Automation Health](https://img.shields.io/badge/health-{health_percent}%25-{health_color}?style=for-the-badge)")
    
    return '\n'.join(badges)

def generate_workflow_table(workflow_data):
    """Generate workflow status table"""
    workflows = workflow_data.get('workflows', [])
    
    if not workflows:
        return "No workflows found in `.github/workflows/`"
    
    lines = []
    lines.append("| Workflow | Status | Schedule | Last Run | Success Rate | Actions |")
    lines.append("|----------|--------|----------|----------|--------------|---------|")
    
    for workflow in workflows:
        name = workflow.get('name', 'Unknown')
        
        # Status indicator
        if workflow.get('enabled'):
            status = "🟢 Active"
            actions = f"[View Runs](../../actions/workflows/{workflow.get('filename', '')})"
        else:
            status = "🔴 Disabled"
            actions = f"[Enable](.github/workflows/{workflow.get('filename', '')})"
        
        # Schedule
        schedule = workflow.get('schedule', 'Manual only')
        if schedule and schedule != 'Manual only':
            schedule = f"`{schedule}`"
        
        # Last run (would come from API in production)
        last_run = workflow.get('last_run', 'N/A')
        
        # Success rate (would come from API in production)
        success_rate = workflow.get('success_rate', 'N/A')
        
        lines.append(f"| **{name}** | {status} | {schedule} | {last_run} | {success_rate} | {actions} |")
    
    # Add attention section if workflows are disabled
    disabled_count = sum(1 for w in workflows if not w.get('enabled'))
    if disabled_count > 0:
        lines.append("")
        lines.append("### ⚠️ Attention Required")
        lines.append(f"- **{disabled_count} workflow{'s' if disabled_count != 1 else ''} currently disabled** - [View disabled workflows](.github/workflows/)")
    
    return '\n'.join(lines)

def generate_metrics_section(metrics_data):
    """Generate metrics dashboard"""
    lines = []
    
    # Project statistics
    lines.append("### 🎯 Project Statistics")
    lines.append("| Metric | Value | Trend |")
    lines.append("|--------|-------|-------|")
    
    project_count = metrics_data.get('project_count', 0)
    lines.append(f"| **Active Projects** | {project_count} | - |")
    
    total_files = metrics_data.get('total_files', 0)
    if total_files > 0:
        lines.append(f"| **Files Tracked** | {total_files:,} | - |")
    
    recent_changes = metrics_data.get('recent_changes', 0)
    if recent_changes > 0:
        lines.append(f"| **Recent Changes (24h)** | {recent_changes} | - |")
    
    return '\n'.join(lines)

def generate_recent_activity(limit=5):
    """Generate recent activity section"""
    commits = get_recent_commits(limit)
    
    if not commits:
        return "No recent commits found."
    
    lines = []
    lines.append("### 🔄 Recent Commits")
    lines.append("| Time | Hash | Message | Author |")
    lines.append("|------|------|---------|--------|")
    
    for commit in commits:
        lines.append(f"| {commit['time_ago']} | `{commit['hash']}` | {commit['message']} | {commit['author']} |")
    
    return '\n'.join(lines)

def update_readme_section(content, section_name, new_data):
    """Update a specific section in README"""
    start_marker = f"<!-- AUTO-GENERATED:{section_name}:START -->"
    end_marker = f"<!-- AUTO-GENERATED:{section_name}:END -->"
    
    # Check if markers exist
    if start_marker not in content:
        log(f"Warning: Start marker for {section_name} not found")
        return content
    
    if end_marker not in content:
        log(f"Warning: End marker for {section_name} not found")
        return content
    
    # Find positions
    start_pos = content.index(start_marker) + len(start_marker)
    end_pos = content.index(end_marker)
    
    # Replace content between markers
    new_content = (
        content[:start_pos] + 
        "\n" + new_data + "\n" + 
        content[end_pos:]
    )
    
    return new_content

def prepare_readme_with_markers():
    """Ensure README has necessary markers"""
    if not os.path.exists(README_PATH):
        log("README.md not found, creating new one")
        content = """# 🤖 PROJECT_actions

> GitHub Actions automation repository

<!-- AUTO-GENERATED:BADGES:START -->
<!-- AUTO-GENERATED:BADGES:END -->

## 📊 Workflow Status

<!-- AUTO-GENERATED:STATUS:START -->
<!-- AUTO-GENERATED:STATUS:END -->

## 📈 Metrics

<!-- AUTO-GENERATED:METRICS:START -->
<!-- AUTO-GENERATED:METRICS:END -->

## 📝 Recent Activity

<!-- AUTO-GENERATED:ACTIVITY:START -->
<!-- AUTO-GENERATED:ACTIVITY:END -->

---

*This README is automatically updated by GitHub Actions*
"""
        with open(README_PATH, 'w') as f:
            f.write(content)
        return content
    
    with open(README_PATH, 'r') as f:
        content = f.read()
    
    # Check if markers exist, add them if not
    markers_to_add = []
    
    if "<!-- AUTO-GENERATED:BADGES:START -->" not in content:
        markers_to_add.append(("BADGES", "## 🎯 Purpose"))
    
    if "<!-- AUTO-GENERATED:STATUS:START -->" not in content:
        markers_to_add.append(("STATUS", "## 🚀 Active Workflows"))
    
    if "<!-- AUTO-GENERATED:METRICS:START -->" not in content:
        markers_to_add.append(("METRICS", "## 📊 Monitoring Dashboard"))
    
    if "<!-- AUTO-GENERATED:ACTIVITY:START -->" not in content:
        markers_to_add.append(("ACTIVITY", "## 🔄 Workflow Status"))
    
    # Add missing markers
    for marker_name, search_text in markers_to_add:
        if search_text in content:
            # Add before the section
            pos = content.index(search_text)
            marker_block = f"\n<!-- AUTO-GENERATED:{marker_name}:START -->\n<!-- AUTO-GENERATED:{marker_name}:END -->\n\n"
            content = content[:pos] + marker_block + content[pos:]
            log(f"Added {marker_name} markers to README")
    
    return content

def main():
    """Main README generation function"""
    log("=" * 60)
    log("Starting README Generator")
    
    # Ensure README has markers
    readme_content = prepare_readme_with_markers()
    
    # Load state files
    workflow_data = load_json_file(WORKFLOW_STATE_FILE)
    metrics_data = load_json_file(METRICS_CACHE_FILE)
    
    # Check if forced update
    force_update = os.environ.get('FORCE_UPDATE', 'false').lower() == 'true'
    
    if not workflow_data and not force_update:
        log("No workflow data found, run workflow_analyzer.py first")
        return 1
    
    # Generate sections
    log("Generating badges...")
    badges = generate_badges(workflow_data, metrics_data)
    
    log("Generating workflow table...")
    status_table = generate_workflow_table(workflow_data)
    
    log("Generating metrics...")
    metrics = generate_metrics_section(metrics_data)
    
    log("Generating recent activity...")
    activity = generate_recent_activity()
    
    # Update README sections
    log("Updating README sections...")
    readme_content = update_readme_section(readme_content, "BADGES", badges)
    readme_content = update_readme_section(readme_content, "STATUS", status_table)
    readme_content = update_readme_section(readme_content, "METRICS", metrics)
    readme_content = update_readme_section(readme_content, "ACTIVITY", activity)
    
    # Add footer timestamp
    footer = f"\n---\n\n*Last automated update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*"
    if "*Last automated update:" in readme_content:
        # Replace existing footer
        readme_content = re.sub(
            r'\*Last automated update:.*?\*',
            f"*Last automated update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*",
            readme_content
        )
    else:
        # Add footer
        readme_content += footer
    
    # Write updated README
    log("Writing updated README...")
    with open(README_PATH, 'w') as f:
        f.write(readme_content)
    
    log("README successfully updated!")
    log("=" * 60)
    
    return 0

if __name__ == "__main__":
    exit(main())