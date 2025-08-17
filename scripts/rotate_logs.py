#!/usr/bin/env python3
"""
Log Rotation and Archival System for Project Monitor
Manages log files to prevent unlimited growth and preserves history
"""

import os
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import json

# Configuration
SCRIPT_DIR = Path(__file__).parent
LOG_DIR = SCRIPT_DIR
ARCHIVE_DIR = SCRIPT_DIR / "monitor_logs_archive"

# Log files to manage
LOG_FILES = {
    ".project_monitor.log": {
        "max_size_mb": 10,
        "keep_days": 30,
        "compress": True
    },
    ".project_monitor_stdout.log": {
        "max_size_mb": 5,
        "keep_days": 7,
        "compress": True
    },
    ".project_monitor_stderr.log": {
        "max_size_mb": 5,
        "keep_days": 7,
        "compress": True
    }
}

def get_file_size_mb(filepath):
    """Get file size in MB."""
    if not filepath.exists():
        return 0
    return filepath.stat().st_size / (1024 * 1024)

def compress_file(filepath, archive_path):
    """Compress a file using gzip."""
    with open(filepath, 'rb') as f_in:
        with gzip.open(archive_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Compressed {filepath.name} to {archive_path.name}")

def rotate_log(log_file, config):
    """Rotate a single log file if needed."""
    log_path = LOG_DIR / log_file
    
    if not log_path.exists():
        return
    
    size_mb = get_file_size_mb(log_path)
    
    # Check if rotation is needed
    if size_mb < config["max_size_mb"]:
        return
    
    # Create archive directory if needed
    ARCHIVE_DIR.mkdir(exist_ok=True)
    
    # Generate archive filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"{log_file}.{timestamp}"
    
    if config["compress"]:
        archive_path = ARCHIVE_DIR / f"{archive_name}.gz"
        compress_file(log_path, archive_path)
    else:
        archive_path = ARCHIVE_DIR / archive_name
        shutil.copy2(log_path, archive_path)
    
    # Clear the original log file
    with open(log_path, 'w') as f:
        f.write(f"[Log rotated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
    
    print(f"Rotated {log_file} ({size_mb:.2f}MB) to {archive_path.name}")

def clean_old_archives():
    """Remove archives older than retention period."""
    if not ARCHIVE_DIR.exists():
        return
    
    now = datetime.now()
    
    for archive_file in ARCHIVE_DIR.iterdir():
        # Extract original log name from archive
        original_name = archive_file.name.split('.')[0] + '.' + archive_file.name.split('.')[1]
        
        # Find config for this log type
        config = None
        for log_name, log_config in LOG_FILES.items():
            if archive_file.name.startswith(log_name):
                config = log_config
                break
        
        if not config:
            continue
        
        # Check age
        file_age = now - datetime.fromtimestamp(archive_file.stat().st_mtime)
        if file_age.days > config["keep_days"]:
            archive_file.unlink()
            print(f"Deleted old archive: {archive_file.name} ({file_age.days} days old)")

def generate_summary():
    """Generate a summary of log status."""
    summary = {
        "timestamp": datetime.now().isoformat(),
        "logs": {},
        "archives": {
            "count": 0,
            "total_size_mb": 0
        }
    }
    
    # Check current logs
    for log_file, config in LOG_FILES.items():
        log_path = LOG_DIR / log_file
        if log_path.exists():
            size_mb = get_file_size_mb(log_path)
            summary["logs"][log_file] = {
                "size_mb": round(size_mb, 2),
                "max_size_mb": config["max_size_mb"],
                "needs_rotation": size_mb >= config["max_size_mb"]
            }
    
    # Check archives
    if ARCHIVE_DIR.exists():
        archives = list(ARCHIVE_DIR.iterdir())
        summary["archives"]["count"] = len(archives)
        summary["archives"]["total_size_mb"] = round(
            sum(f.stat().st_size for f in archives) / (1024 * 1024), 2
        )
        
        # List recent archives
        summary["archives"]["recent"] = []
        for archive in sorted(archives, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
            summary["archives"]["recent"].append({
                "name": archive.name,
                "size_mb": round(archive.stat().st_size / (1024 * 1024), 2),
                "age_days": (datetime.now() - datetime.fromtimestamp(archive.stat().st_mtime)).days
            })
    
    return summary

def save_rotation_report():
    """Save a report of the rotation operation."""
    report_path = LOG_DIR / "log_rotation_report.json"
    summary = generate_summary()
    
    with open(report_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nLog Rotation Summary saved to: {report_path}")
    print(f"Current logs: {len(summary['logs'])}")
    print(f"Archived logs: {summary['archives']['count']} files, "
          f"{summary['archives']['total_size_mb']}MB total")

def main():
    """Main rotation process."""
    print("=" * 60)
    print(f"Log Rotation Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Rotate logs if needed
    for log_file, config in LOG_FILES.items():
        rotate_log(log_file, config)
    
    # Clean old archives
    clean_old_archives()
    
    # Generate and save report
    save_rotation_report()
    
    print("=" * 60)
    print("Log Rotation Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()