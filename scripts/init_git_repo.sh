#!/bin/bash

# Initialize Git repository and connect to GitHub

echo "🔧 Initializing Git repository..."

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "ℹ️  Git repository already exists"
fi

# Set up Git configuration
echo "📝 Setting up Git configuration..."
git config --local user.name "DataFlow Team"
git config --local user.email "team@dataflow-toolkit.org"

# Add all files
echo "📁 Adding files to Git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "feat: Initial project setup

- Setup project structure
- Add base classes and core components
- Configure development environment
- Add CI/CD workflows
- Create documentation templates

BREAKING CHANGE: Initial release"

# Add GitHub remote
echo "🔗 Adding GitHub remote..."
read -p "Enter your GitHub repository URL (e.g., https://github.com/username/dataflow-toolkit.git): " REPO_URL

if [ ! -z "$REPO_URL" ]; then
    git remote add origin "$REPO_URL"
    echo "✅ Remote added successfully"
    
    # Create and checkout develop branch
    git checkout -b develop
    echo "✅ Created develop branch"
    
    # Push to GitHub
    echo "🚀 Pushing to GitHub..."
    git push -u origin main
    git push -u origin develop
    
    echo "✨ Repository successfully initialized and pushed to GitHub!"
else
    echo "⚠️  No remote URL provided. You can add it later with:"
    echo "  git remote add origin <your-repo-url>"
fi

# Create initial GitHub issues
echo ""
echo "📋 Next steps:"
echo "1. Go to https://github.com/username/dataflow-toolkit/issues"
echo "2. Create issues from the templates in docs/issues/sprint1_issues.md"
echo "3. Set up project board for Sprint 1"
echo "4. Configure branch protection rules"
