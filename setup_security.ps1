# ============================================================================
# Stock Analysis System - Automated Security Setup
# ============================================================================
# Run this script in PowerShell to set up secure API key management
# Usage: .\setup_security.ps1
# ============================================================================

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  Stock Analysis System - Security Setup" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if .env already exists
if (Test-Path ".env") {
    Write-Host "⚠️  .env file already exists!" -ForegroundColor Yellow
    $response = Read-Host "Do you want to overwrite it? (y/n)"
    if ($response -ne "y") {
        Write-Host "❌ Setup cancelled." -ForegroundColor Red
        exit
    }
}

# Step 2: Create .env file
Write-Host "Creating .env file..." -ForegroundColor Green
@"
# =============================================================================
# API Keys for Stock Analysis System
# =============================================================================

# FinViz Elite API Token (REQUIRED for Stage 1 screening)
FINVIZ_API_TOKEN=6a8f4866-8965-4c9e-b941-f56c97379554

# Financial Modeling Prep API Key (REQUIRED for stock data)
FMP_API_KEY=w4Fs93trTWbGi2aNzdZm3EVr4gBJcqhI

# Polygon.io API Key (OPTIONAL - for options & short interest)
POLYGON_API_KEY=Xku4p8y1mcyRiuZdIiUTmM5_p62FretY

# Claude API Key (OPTIONAL - for AI deep analysis)
CLAUDE_API_KEY=YOUR_CLAUDE_API_KEY_HERE
"@ | Out-File -FilePath ".env" -Encoding utf8

Write-Host "✅ .env file created" -ForegroundColor Green
Write-Host ""

# Step 3: Install python-dotenv
Write-Host "Installing python-dotenv..." -ForegroundColor Green
pip install python-dotenv

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ python-dotenv installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Warning: python-dotenv installation may have failed" -ForegroundColor Yellow
}
Write-Host ""

# Step 4: Check if files need updating
$needsUpdate = $false

if (Test-Path "config.py") {
    $configContent = Get-Content "config.py" -Raw
    if ($configContent -notmatch "from dotenv import load_dotenv") {
        Write-Host "⚠️  config.py needs updating to use .env" -ForegroundColor Yellow
        $needsUpdate = $true
    } else {
        Write-Host "✅ config.py already secure" -ForegroundColor Green
    }
} else {
    Write-Host "⚠️  config.py not found in current directory" -ForegroundColor Yellow
}

if (Test-Path "finviz_scraper.py") {
    $finvizContent = Get-Content "finviz_scraper.py" -Raw
    if ($finvizContent -notmatch "from dotenv import load_dotenv") {
        Write-Host "⚠️  finviz_scraper.py needs updating to use .env" -ForegroundColor Yellow
        $needsUpdate = $true
    } else {
        Write-Host "✅ finviz_scraper.py already secure" -ForegroundColor Green
    }
} else {
    Write-Host "⚠️  finviz_scraper.py not found in current directory" -ForegroundColor Yellow
}

Write-Host ""

# Step 5: Verify .gitignore
if (Test-Path ".gitignore") {
    $gitignoreContent = Get-Content ".gitignore" -Raw
    if ($gitignoreContent -match "\.env") {
        Write-Host "✅ .gitignore already protects .env" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Adding .env to .gitignore..." -ForegroundColor Yellow
        Add-Content -Path ".gitignore" -Value "`n# Environment variables`n.env`nconfig_local.py"
        Write-Host "✅ .gitignore updated" -ForegroundColor Green
    }
} else {
    Write-Host "⚠️  .gitignore not found - creating one..." -ForegroundColor Yellow
    @"
# Environment variables (API keys)
.env
config_local.py

# Python
__pycache__/
*.pyc

# Data & Output
output/
data/
*.db
"@ | Out-File -FilePath ".gitignore" -Encoding utf8
    Write-Host "✅ .gitignore created" -ForegroundColor Green
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

if ($needsUpdate) {
    Write-Host "📝 Next Steps:" -ForegroundColor Yellow
    Write-Host "   1. Replace config.py and finviz_scraper.py with secure versions" -ForegroundColor Yellow
    Write-Host "   2. Test: python finviz_scraper.py" -ForegroundColor Yellow
    Write-Host "   3. Verify: git status (ensure .env is NOT listed)" -ForegroundColor Yellow
    Write-Host "   4. Push: git add . && git commit -m 'Secure API keys' && git push" -ForegroundColor Yellow
} else {
    Write-Host "✅ All files are already secure!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Next Steps:" -ForegroundColor Cyan
    Write-Host "   1. Test: python finviz_scraper.py" -ForegroundColor Cyan
    Write-Host "   2. Verify: git status (ensure .env is NOT listed)" -ForegroundColor Cyan
    Write-Host "   3. Push: git add . && git commit -m 'Initial commit' && git push" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🔒 Your API keys are now secure!" -ForegroundColor Green
Write-Host ""
