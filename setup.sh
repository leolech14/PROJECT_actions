#!/bin/bash

# Setup script for PROJECT_actions repository

echo "🚀 Setting up PROJECT_actions repository..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d ".github/workflows" ]; then
    print_error "Please run this script from the PROJECT_actions root directory"
    exit 1
fi

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    print_success "Git repository initialized"
else
    print_success "Git repository already initialized"
fi

# Create required directories
echo ""
echo "Creating directory structure..."
mkdir -p scripts docs .github/workflows
print_success "Directory structure created"

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x scripts/*.py 2>/dev/null || true
chmod +x scripts/*.sh 2>/dev/null || true
chmod +x setup.sh
print_success "Scripts made executable"

# Check for Python
echo ""
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Create a test script
echo ""
echo "Creating test script..."
cat > scripts/test_monitor.py << 'EOF'
#!/usr/bin/env python3
"""Test script to verify monitoring setup"""

import sys
import os

def test_import():
    """Test if monitoring script can be imported"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, script_dir)
        
        # Try to import the monitoring script
        import project_monitor
        print("✅ Monitoring script imports successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import monitoring script: {e}")
        return False

def test_paths():
    """Test if required paths are accessible"""
    paths_ok = True
    
    # Check if scripts exist
    scripts = ['project_monitor.py', 'rotate_logs.py']
    for script in scripts:
        path = os.path.join(os.path.dirname(__file__), script)
        if os.path.exists(path):
            print(f"✅ Found {script}")
        else:
            print(f"❌ Missing {script}")
            paths_ok = False
    
    return paths_ok

if __name__ == "__main__":
    print("Running setup tests...")
    print("-" * 40)
    
    import_ok = test_import()
    paths_ok = test_paths()
    
    print("-" * 40)
    if import_ok and paths_ok:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
EOF

chmod +x scripts/test_monitor.py
print_success "Test script created"

# Run tests
echo ""
echo "Running tests..."
if python3 scripts/test_monitor.py; then
    print_success "Tests passed"
else
    print_warning "Some tests failed - please check the setup"
fi

# Git remote setup
echo ""
echo "Git remote setup..."
if git remote | grep -q "origin"; then
    print_success "Git remote 'origin' already configured"
    echo "  Remote URL: $(git remote get-url origin)"
else
    print_warning "No git remote configured"
    echo ""
    echo "To add a remote, run:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/PROJECT_actions.git"
fi

# Create initial commit if needed
if [ -z "$(git log --oneline 2>/dev/null)" ]; then
    echo ""
    echo "Creating initial commit..."
    git add .
    git commit -m "🎉 Initial commit - Project Actions automation setup"
    print_success "Initial commit created"
fi

# GitHub CLI check
echo ""
echo "Checking GitHub CLI..."
if command -v gh &> /dev/null; then
    print_success "GitHub CLI found"
    
    # Check authentication
    if gh auth status &> /dev/null; then
        print_success "GitHub CLI authenticated"
        
        # Offer to create repository
        echo ""
        read -p "Would you like to create the GitHub repository now? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Creating GitHub repository..."
            if gh repo create PROJECT_actions --public --source=. --remote=origin --push; then
                print_success "Repository created and pushed to GitHub"
            else
                print_warning "Failed to create repository"
            fi
        fi
    else
        print_warning "GitHub CLI not authenticated"
        echo "Run: gh auth login"
    fi
else
    print_warning "GitHub CLI not installed"
    echo "Install with: brew install gh"
fi

# Final instructions
echo ""
echo "========================================"
echo "✅ Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. If not done, create GitHub repository:"
echo "   https://github.com/new"
echo ""
echo "2. Add repository secrets:"
echo "   Go to Settings → Secrets and variables → Actions"
echo "   Add: VAULT_REPO_TOKEN (if vault is private)"
echo ""
echo "3. Push to GitHub:"
echo "   git push -u origin main"
echo ""
echo "4. Enable GitHub Actions:"
echo "   Go to Actions tab and enable workflows"
echo ""
echo "5. Test with manual run:"
echo "   Go to Actions → Project Monitor → Run workflow"
echo ""
echo "Documentation:"
echo "  - README.md - Overview"
echo "  - docs/SECRETS.md - Secrets setup"
echo "  - docs/SETUP.md - Detailed setup"
echo ""
echo "Happy automating! 🤖"