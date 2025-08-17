#!/usr/bin/env python3
"""
Project Activity Monitor
Tracks the last 20 file modifications for each project in ~/PROJECTS_all/
and updates corresponding markdown files in the Obsidian vault.
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
import subprocess
import hashlib

# Configuration
PROJECTS_DIR = os.path.expanduser("~/PROJECTS_all")
OBSIDIAN_DIR = "/Users/lech/Library/Mobile Documents/iCloud~md~obsidian/Documents/sprintx"
STATE_FILE = os.path.join(OBSIDIAN_DIR, ".project_monitor_state.json")
LOG_FILE = os.path.join(OBSIDIAN_DIR, ".project_monitor.log")

# Directories to exclude from monitoring
EXCLUDE_DIRS = {
    '.git', 'node_modules', '__pycache__', '.next', 'dist', 
    'build', '.venv', 'venv', '.cache', '.pytest_cache',
    'coverage', '.nyc_output', '.DS_Store'
}

# File extensions to exclude
EXCLUDE_EXTENSIONS = {
    '.pyc', '.pyo', '.pyd', '.so', '.dll', '.dylib',
    '.log', '.pid', '.lock', '.tmp', '.swp', '.swo'
}

def log_message(message):
    """Write a timestamped message to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def load_state():
    """Load the previous state from the state file."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            log_message(f"Error loading state: {e}")
    return {}

def save_state(state):
    """Save the current state to the state file."""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        log_message(f"Error saving state: {e}")

def should_exclude_path(path):
    """Check if a path should be excluded from monitoring."""
    path_parts = Path(path).parts
    
    # Check if any part of the path is in exclude dirs
    for part in path_parts:
        if part in EXCLUDE_DIRS:
            return True
    
    # Check file extension
    ext = os.path.splitext(path)[1]
    if ext in EXCLUDE_EXTENSIONS:
        return True
    
    return False

def get_file_modifications(project_path, limit=20):
    """Get the last N modified files in a project directory."""
    modifications = []
    
    try:
        # Use find command for efficiency
        cmd = [
            'find', project_path,
            '-type', 'f',
            '-not', '-path', '*/.*',  # Exclude hidden files/dirs
        ]
        
        # Add exclusions
        for exclude_dir in EXCLUDE_DIRS:
            cmd.extend(['-not', '-path', f'*/{exclude_dir}/*'])
        
        # Execute find command
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            files = result.stdout.strip().split('\n')
            files = [f for f in files if f and not should_exclude_path(f)]
            
            # Get modification times for each file
            for file_path in files:
                try:
                    stat = os.stat(file_path)
                    mtime = stat.st_mtime
                    relative_path = os.path.relpath(file_path, project_path)
                    modifications.append({
                        'path': relative_path,
                        'timestamp': mtime,
                        'datetime': datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S"),
                        'size': stat.st_size
                    })
                except:
                    continue
            
            # Sort by timestamp (newest first) and limit
            modifications.sort(key=lambda x: x['timestamp'], reverse=True)
            modifications = modifications[:limit]
            
    except subprocess.TimeoutExpired:
        log_message(f"Timeout scanning project: {project_path}")
    except Exception as e:
        log_message(f"Error scanning project {project_path}: {e}")
    
    return modifications

def calculate_project_hash(modifications):
    """Calculate a hash of the project's modification state."""
    if not modifications:
        return ""
    
    # Create a string representation of the top modifications
    state_string = json.dumps(modifications[:5], sort_keys=True)
    return hashlib.md5(state_string.encode()).hexdigest()

def format_modifications_for_markdown(modifications):
    """Format the modifications list for insertion into markdown."""
    if not modifications:
        return "No recent modifications found."
    
    lines = ["## Recent Activity (Last 20 Edits)\n"]
    lines.append("| Date & Time | File | Size |")
    lines.append("|-------------|------|------|")
    
    for mod in modifications:
        size_kb = mod['size'] / 1024
        size_str = f"{size_kb:.1f}KB" if size_kb < 1024 else f"{size_kb/1024:.1f}MB"
        # Truncate long paths
        path = mod['path']
        if len(path) > 60:
            path = "..." + path[-57:]
        lines.append(f"| {mod['datetime']} | `{path}` | {size_str} |")
    
    lines.append(f"\n*Last scan: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    return "\n".join(lines)

def update_markdown_file(project_name, modifications):
    """Update the project's markdown file with modification history."""
    md_file = os.path.join(OBSIDIAN_DIR, f"{project_name}.md")
    
    if not os.path.exists(md_file):
        log_message(f"Markdown file not found for {project_name}")
        return False
    
    try:
        # Read current content
        with open(md_file, 'r') as f:
            content = f.read()
        
        # Format new activity section
        activity_section = format_modifications_for_markdown(modifications)
        
        # Check if Recent Activity section exists
        if "## Recent Activity" in content:
            # Replace existing section
            # Find the section and replace it
            start_marker = "## Recent Activity"
            end_markers = ["\n## ", "\n# ", "\n---", "\n*Last scan:"]
            
            start_idx = content.find(start_marker)
            if start_idx != -1:
                # Find where this section ends
                remaining = content[start_idx:]
                end_idx = len(content)
                
                # Look for the next section
                for marker in ["\n## ", "\n# "]:
                    idx = remaining.find(marker, 1)  # Skip the first char to avoid matching current section
                    if idx != -1:
                        end_idx = start_idx + idx
                        break
                
                # Also check for last scan line
                last_scan_idx = remaining.find("\n*Last scan:")
                if last_scan_idx != -1:
                    # Find the end of this line
                    line_end = remaining.find("\n", last_scan_idx + 1)
                    if line_end != -1:
                        potential_end = start_idx + line_end + 1
                        if potential_end < end_idx:
                            end_idx = potential_end
                
                # Replace the section
                new_content = content[:start_idx] + activity_section
                if end_idx < len(content):
                    new_content += content[end_idx:]
                content = new_content
        else:
            # Add new section before Context or at the end
            if "## Context" in content:
                idx = content.find("## Context")
                content = content[:idx] + activity_section + "\n\n" + content[idx:]
            else:
                # Add at the end
                if not content.endswith('\n'):
                    content += '\n'
                content += '\n' + activity_section
        
        # Write updated content
        with open(md_file, 'w') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        log_message(f"Error updating markdown for {project_name}: {e}")
        return False

def process_project(project_name, project_path, previous_state):
    """Process a single project directory."""
    log_message(f"Processing {project_name}...")
    
    # Get current modifications
    modifications = get_file_modifications(project_path)
    
    if not modifications:
        log_message(f"  No files found in {project_name}")
        return None
    
    # Calculate current hash
    current_hash = calculate_project_hash(modifications)
    
    # Check if project has changed
    previous_hash = previous_state.get(project_name, {}).get('hash', '')
    
    if current_hash == previous_hash:
        log_message(f"  No changes detected in {project_name}")
        return {
            'hash': current_hash,
            'last_checked': time.time(),
            'modifications': modifications
        }
    
    # Project has changed, update markdown
    log_message(f"  Changes detected in {project_name}, updating markdown...")
    if update_markdown_file(project_name, modifications):
        log_message(f"  Successfully updated {project_name}.md")
    else:
        log_message(f"  Failed to update {project_name}.md")
    
    return {
        'hash': current_hash,
        'last_checked': time.time(),
        'last_updated': time.time(),
        'modifications': modifications
    }

def main():
    """Main monitoring function."""
    log_message("=" * 60)
    log_message("Starting Project Activity Monitor")
    
    # Load previous state
    state = load_state()
    new_state = {}
    
    # Get all project directories
    try:
        projects = [d for d in os.listdir(PROJECTS_DIR) 
                   if d.startswith('PROJECT') and 
                   os.path.isdir(os.path.join(PROJECTS_DIR, d))]
        projects.sort()
        
        log_message(f"Found {len(projects)} projects to monitor")
        
        # Process each project
        updated_count = 0
        for project_name in projects:
            project_path = os.path.join(PROJECTS_DIR, project_name)
            result = process_project(project_name, project_path, state)
            
            if result:
                new_state[project_name] = result
                if 'last_updated' in result:
                    updated_count += 1
        
        # Save new state
        save_state(new_state)
        
        log_message(f"Monitoring complete. Updated {updated_count} projects.")
        log_message("=" * 60)
        
    except Exception as e:
        log_message(f"Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    result = main()
    
    # Run log rotation if main monitoring succeeded
    if result == 0:
        try:
            # Check if rotation is needed (every 24 hours or if logs are large)
            import subprocess
            rotation_script = os.path.join(os.path.dirname(__file__), "rotate_logs.py")
            if os.path.exists(rotation_script):
                # Check log sizes
                main_log = os.path.join(os.path.dirname(__file__), ".project_monitor.log")
                if os.path.exists(main_log):
                    size_mb = os.path.getsize(main_log) / (1024 * 1024)
                    if size_mb > 8:  # Rotate if approaching 10MB limit
                        subprocess.run(["python3", rotation_script], capture_output=True)
        except:
            pass  # Don't fail main process if rotation fails
    
    exit(result)