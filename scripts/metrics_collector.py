#!/usr/bin/env python3
"""
Metrics Collector - Collects project and automation metrics
"""

import os
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
PROJECTS_DIR = os.path.expanduser("~/PROJECTS_all")
MONITOR_STATE_FILE = ".project_monitor_state.json"
METRICS_CACHE_FILE = ".metrics_cache.json"
METRICS_SUMMARY_FILE = ".metrics_summary.txt"

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_project_count():
    """Count PROJECT_* directories"""
    try:
        if os.path.exists(PROJECTS_DIR):
            projects = [d for d in os.listdir(PROJECTS_DIR) 
                       if d.startswith('PROJECT_') and 
                       os.path.isdir(os.path.join(PROJECTS_DIR, d))]
            return len(projects)
    except Exception as e:
        log(f"Error counting projects: {e}")
    return 0

def get_recent_git_activity():
    """Get recent git activity in current repo"""
    try:
        # Count commits in last 24 hours
        since = datetime.now() - timedelta(days=1)
        since_str = since.strftime('%Y-%m-%d')
        
        result = subprocess.run(
            ['git', 'log', '--since', since_str, '--oneline'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            commits = result.stdout.strip().split('\n')
            return len([c for c in commits if c])
        
    except Exception as e:
        log(f"Error getting git activity: {e}")
    
    return 0

def get_file_count(directory="."):
    """Count files in directory recursively"""
    try:
        count = 0
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories and common exclusions
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
            # Count non-hidden files
            count += len([f for f in files if not f.startswith('.')])
        return count
    except Exception as e:
        log(f"Error counting files: {e}")
        return 0

def get_workflow_runs_from_api():
    """Get workflow run data from GitHub API (if token available)"""
    # This would use GitHub API in production
    # For now, return mock data or empty
    return {
        'total_runs': 0,
        'successful_runs': 0,
        'failed_runs': 0,
        'last_run_time': None
    }

def analyze_monitor_state():
    """Analyze project monitor state if available"""
    metrics = {
        'projects_monitored': 0,
        'total_modifications': 0,
        'recent_changes': 0
    }
    
    if os.path.exists(MONITOR_STATE_FILE):
        try:
            with open(MONITOR_STATE_FILE, 'r') as f:
                state = json.load(f)
            
            metrics['projects_monitored'] = len(state)
            
            # Count total modifications
            for project_data in state.values():
                mods = project_data.get('modifications', [])
                metrics['total_modifications'] += len(mods)
                
                # Count recent (last 24 hours)
                cutoff = (datetime.now() - timedelta(days=1)).timestamp()
                for mod in mods:
                    if mod.get('timestamp', 0) > cutoff:
                        metrics['recent_changes'] += 1
                        
        except Exception as e:
            log(f"Error analyzing monitor state: {e}")
    
    return metrics

def collect_repository_stats():
    """Collect statistics about the current repository"""
    stats = {}
    
    # Count workflow files
    workflow_dir = Path(".github/workflows")
    if workflow_dir.exists():
        yml_files = list(workflow_dir.glob("*.yml"))
        disabled_files = list(workflow_dir.glob("*.yml.disabled"))
        stats['workflow_count'] = len(yml_files) + len(disabled_files)
        stats['active_workflows'] = len(yml_files)
        stats['disabled_workflows'] = len(disabled_files)
    
    # Count scripts
    scripts_dir = Path("scripts")
    if scripts_dir.exists():
        py_files = list(scripts_dir.glob("*.py"))
        sh_files = list(scripts_dir.glob("*.sh"))
        stats['python_scripts'] = len(py_files)
        stats['shell_scripts'] = len(sh_files)
        stats['total_scripts'] = len(py_files) + len(sh_files)
    
    # Repository size (rough estimate)
    try:
        result = subprocess.run(
            ['du', '-sh', '.'],
            capture_output=True,
            text=True,
            cwd='.'
        )
        if result.returncode == 0:
            size = result.stdout.split()[0]
            stats['repo_size'] = size
    except:
        stats['repo_size'] = 'Unknown'
    
    return stats

def generate_summary(metrics):
    """Generate summary text for GitHub Actions"""
    lines = []
    
    lines.append("**Metrics Collection Summary**")
    lines.append("")
    
    if metrics.get('project_count', 0) > 0:
        lines.append(f"- Projects monitored: {metrics['project_count']}")
    
    if metrics.get('recent_changes', 0) > 0:
        lines.append(f"- Recent changes (24h): {metrics['recent_changes']}")
    
    if metrics.get('total_files', 0) > 0:
        lines.append(f"- Total files: {metrics['total_files']}")
    
    repo_stats = metrics.get('repository_stats', {})
    if repo_stats:
        lines.append("")
        lines.append("**Repository Statistics:**")
        if 'workflow_count' in repo_stats:
            lines.append(f"- Workflows: {repo_stats.get('active_workflows', 0)}/{repo_stats.get('workflow_count', 0)} active")
        if 'total_scripts' in repo_stats:
            lines.append(f"- Scripts: {repo_stats['total_scripts']}")
        if 'repo_size' in repo_stats:
            lines.append(f"- Repository size: {repo_stats['repo_size']}")
    
    return '\n'.join(lines)

def main():
    """Main metrics collection function"""
    log("=" * 60)
    log("Starting Metrics Collection")
    
    metrics = {}
    
    # Collect project count
    log("Counting projects...")
    metrics['project_count'] = get_project_count()
    log(f"Found {metrics['project_count']} projects")
    
    # Collect git activity
    log("Analyzing git activity...")
    metrics['recent_commits'] = get_recent_git_activity()
    
    # Collect file count
    log("Counting repository files...")
    metrics['total_files'] = get_file_count()
    
    # Analyze monitor state if available
    log("Analyzing monitor state...")
    monitor_metrics = analyze_monitor_state()
    metrics.update(monitor_metrics)
    
    # Collect repository statistics
    log("Collecting repository statistics...")
    metrics['repository_stats'] = collect_repository_stats()
    
    # Add timestamp
    metrics['timestamp'] = datetime.now().isoformat()
    metrics['collection_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Save metrics cache
    log(f"Saving metrics to {METRICS_CACHE_FILE}...")
    try:
        with open(METRICS_CACHE_FILE, 'w') as f:
            json.dump(metrics, f, indent=2)
        log("Metrics saved successfully")
    except Exception as e:
        log(f"Error saving metrics: {e}")
        return 1
    
    # Generate summary
    summary = generate_summary(metrics)
    
    # Save summary file
    try:
        with open(METRICS_SUMMARY_FILE, 'w') as f:
            f.write(summary)
        log("Summary file saved successfully")
    except Exception as e:
        log(f"Error saving summary: {e}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("METRICS COLLECTION SUMMARY")
    print("=" * 60)
    print(summary)
    print("=" * 60)
    
    log("Metrics collection complete!")
    
    return 0

if __name__ == "__main__":
    exit(main())