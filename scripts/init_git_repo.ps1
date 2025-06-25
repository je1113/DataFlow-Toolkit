# Initialize Git repository and connect to GitHub

Write-Host "🔧 Initializing Git repository..." -ForegroundColor Green

# Initialize git if not already initialized
if (!(Test-Path ".git")) {
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Git repository already exists" -ForegroundColor Yellow
}

# Set up Git configuration
Write-Host "📝 Setting up Git configuration..." -ForegroundColor Yellow
git config --local user.name "DataFlow Team"
git config --local user.email "team@dataflow-toolkit.org"

# Add all files
Write-Host "📁 Adding files to Git..." -ForegroundColor Yellow
git add .

# Create initial commit
Write-Host "💾 Creating initial commit..." -ForegroundColor Yellow
git commit -m "feat: Initial project setup

- Setup project structure
- Add base classes and core components
- Configure development environment
- Add CI/CD workflows
- Create documentation templates

BREAKING CHANGE: Initial release"

# Add GitHub remote
Write-Host "🔗 Adding GitHub remote..." -ForegroundColor Yellow
$repoUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/dataflow-toolkit.git)"

if ($repoUrl) {
    git remote add origin $repoUrl
    Write-Host "✅ Remote added successfully" -ForegroundColor Green
    
    # Create and checkout develop branch
    git checkout -b develop
    Write-Host "✅ Created develop branch" -ForegroundColor Green
    
    # Push to GitHub
    Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
    git push -u origin main
    git push -u origin develop
    
    Write-Host "✨ Repository successfully initialized and pushed to GitHub!" -ForegroundColor Green
} else {
    Write-Host "⚠️  No remote URL provided. You can add it later with:" -ForegroundColor Yellow
    Write-Host "  git remote add origin <your-repo-url>" -ForegroundColor White
}

# Create initial GitHub issues
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Go to https://github.com/username/dataflow-toolkit/issues" -ForegroundColor White
Write-Host "2. Create issues from the templates in docs/issues/sprint1_issues.md" -ForegroundColor White
Write-Host "3. Set up project board for Sprint 1" -ForegroundColor White
Write-Host "4. Configure branch protection rules" -ForegroundColor White
