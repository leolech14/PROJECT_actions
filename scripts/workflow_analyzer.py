#!/usr/bin/env python3
"""
Workflow Analyzer - Analyzes GitHub Actions workflow states
"""

import os
import json
import re
try:
    import yaml
except ImportError:
    # Will be installed by GitHub Actions
    yaml = None
from pathlib import Path
from datetime import datetime

# Configuration
WORKFLOW_DIR = ".github/workflows"
STATE_FILE = ".workflow_state.json"
SUMMARY_FILE = ".workflow_summary.txt"

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def extract_workflow_name(content):
    """Extract workflow name from YAML content"""
    if yaml:
        try:
            # Try to parse as YAML
            data = yaml.safe_load(content)
            if data and 'name' in data:
                return data['name']
        except:
            pass
    # Fallback to regex
    match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip().strip('"\'')
    return None

def extract_schedule(content):
    """Extract schedule from workflow content"""
    if yaml:
        try:
            data = yaml.safe_load(content)
            if data and 'on' in data:
                on_section = data['on']
                if isinstance(on_section, dict) and 'schedule' in on_section:
                    schedule = on_section['schedule']
                    if isinstance(schedule, list) and len(schedule) > 0:
                        cron = schedule[0].get('cron', '')
                        # Parse cron expression to human-readable
                        return parse_cron_to_human(cron)
        except:
            pass
    
    # Fallback to regex
    match = re.search(r'cron:\s*[\'"]([^\'"]+)[\'"]', content)
    if match:
        return parse_cron_to_human(match.group(1))
    
    return "Manual only"

def parse_cron_to_human(cron):
    """Convert cron expression to human-readable format"""
    if not cron:
        return "Manual only"
    
    # Common patterns
    patterns = {
        '0 * * * *': 'Hourly',
        '15 * * * *': 'Hourly at :15',
        '0 */2 * * *': 'Every 2 hours',
        '0 */4 * * *': 'Every 4 hours',
        '0 */6 * * *': 'Every 6 hours',
        '0 0 * * *': 'Daily at midnight',
        '0 9 * * *': 'Daily at 9 AM',
        '0 0 * * 0': 'Weekly on Sunday',
        '0 0 1 * *': 'Monthly on 1st',
    }
    
    if cron in patterns:
        return patterns[cron]
    
    # Return raw cron if no pattern matches
    return f"Cron: {cron}"

def analyze_workflow_file(filepath):
    """Analyze a single workflow file"""
    filename = os.path.basename(filepath)
    
    # Determine if enabled or disabled
    enabled = filename.endswith('.yml')
    actual_filename = filename.replace('.disabled', '') if filename.endswith('.disabled') else filename
    
    # Read file content
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception as e:
        log(f"Error reading {filepath}: {e}")
        return None
    
    # Extract information
    name = extract_workflow_name(content)
    if not name:
        # Use filename as fallback
        name = actual_filename.replace('.yml', '').replace('-', ' ').title()
    
    schedule = extract_schedule(content)
    
    # Check for various triggers
    has_push = 'push:' in content
    has_pull_request = 'pull_request:' in content
    has_workflow_dispatch = 'workflow_dispatch:' in content
    has_schedule = schedule != "Manual only"
    
    triggers = []
    if has_schedule:
        triggers.append("schedule")
    if has_push:
        triggers.append("push")
    if has_pull_request:
        triggers.append("PR")
    if has_workflow_dispatch:
        triggers.append("manual")
    
    return {
        'filename': actual_filename,
        'name': name,
        'enabled': enabled,
        'schedule': schedule,
        'triggers': triggers,
        'has_schedule': has_schedule,
        'has_manual': has_workflow_dispatch,
        'file_size': os.path.getsize(filepath),
        'last_modified': os.path.getmtime(filepath)
    }

def analyze_all_workflows():
    """Analyze all workflows in the directory"""
    workflow_path = Path(WORKFLOW_DIR)
    
    if not workflow_path.exists():
        log(f"Workflow directory {WORKFLOW_DIR} not found")
        return []
    
    workflows = []
    
    # Find all .yml and .yml.disabled files
    for file in workflow_path.glob('*.yml*'):
        if file.name.startswith('.'):
            continue  # Skip hidden files
        
        log(f"Analyzing {file.name}...")
        workflow_info = analyze_workflow_file(str(file))
        
        if workflow_info:
            workflows.append(workflow_info)
    
    # Sort by enabled status, then by name
    workflows.sort(key=lambda x: (not x['enabled'], x['name']))
    
    return workflows

def generate_summary(workflows):
    """Generate summary text for GitHub Actions"""
    lines = []
    
    active_count = sum(1 for w in workflows if w['enabled'])
    total_count = len(workflows)
    
    lines.append(f"**Total Workflows**: {total_count}")
    lines.append(f"**Active**: {active_count}")
    lines.append(f"**Disabled**: {total_count - active_count}")
    lines.append("")
    
    if workflows:
        lines.append("**Workflow Details:**")
        for w in workflows:
            status = "✅" if w['enabled'] else "❌"
            triggers = ', '.join(w['triggers']) if w['triggers'] else 'none'
            lines.append(f"- {status} **{w['name']}** ({triggers})")
    
    return '\n'.join(lines)

def main():
    """Main analysis function"""
    log("=" * 60)
    log("Starting Workflow Analysis")
    
    # Analyze workflows
    workflows = analyze_all_workflows()
    
    if not workflows:
        log("No workflows found")
        return 1
    
    log(f"Found {len(workflows)} workflows")
    
    # Prepare state data
    state_data = {
        'timestamp': datetime.now().isoformat(),
        'workflow_count': len(workflows),
        'active_count': sum(1 for w in workflows if w['enabled']),
        'workflows': workflows
    }
    
    # Save state file
    log(f"Saving state to {STATE_FILE}...")
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state_data, f, indent=2)
        log("State file saved successfully")
    except Exception as e:
        log(f"Error saving state file: {e}")
        return 1
    
    # Generate summary
    summary = generate_summary(workflows)
    
    # Save summary file
    try:
        with open(SUMMARY_FILE, 'w') as f:
            f.write(summary)
        log("Summary file saved successfully")
    except Exception as e:
        log(f"Error saving summary file: {e}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("WORKFLOW ANALYSIS SUMMARY")
    print("=" * 60)
    print(summary)
    print("=" * 60)
    
    log("Workflow analysis complete!")
    
    return 0

if __name__ == "__main__":
    exit(main())