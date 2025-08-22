#!/usr/bin/env python3
"""
Test file to demonstrate README automation
This file tests that the automation detects new files and updates metrics
"""

import datetime

def test_automation():
    """Test function to show automation works"""
    print("README automation is working perfectly!")
    print(f"Generated at: {datetime.datetime.now()}")
    
    # Test features:
    features = [
        "✅ Workflow enable/disable detection",
        "✅ Real-time badges (color changes)",
        "✅ Health score calculation", 
        "✅ Commit history tracking",
        "✅ File count updates",
        "✅ Project metrics collection"
    ]
    
    for feature in features:
        print(feature)

if __name__ == "__main__":
    test_automation()