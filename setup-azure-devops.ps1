# Azure DevOps Setup Script
# Run this after creating your Azure DevOps organization and project

param(
    [Parameter(Mandatory=$true)]
    [string]$OrganizationUrl,  # Example: https://dev.azure.com/YourOrgName
    
    [Parameter(Mandatory=$true)]
    [string]$ProjectName = "social-media-ml"
)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "AZURE DEVOPS MIGRATION SCRIPT" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

# Configure Azure DevOps defaults
Write-Host "1. Configuring Azure DevOps CLI..." -ForegroundColor Green
az devops configure --defaults organization=$OrganizationUrl project=$ProjectName

# Check if repo exists, create if not
Write-Host "`n2. Setting up Azure Repos repository..." -ForegroundColor Green
$repoExists = az repos list --query "[?name=='$ProjectName']" -o json | ConvertFrom-Json

if (-not $repoExists) {
    Write-Host "   Creating new repository: $ProjectName" -ForegroundColor Yellow
    az repos create --name $ProjectName --project $ProjectName
} else {
    Write-Host "   Repository already exists ✓" -ForegroundColor Gray
}

# Get the Azure Repos URL
$repoUrl = az repos show --repository $ProjectName --query "remoteUrl" -o tsv
Write-Host "   Azure Repos URL: $repoUrl" -ForegroundColor Cyan

# Add Azure Repos as remote
Write-Host "`n3. Configuring Git remotes..." -ForegroundColor Green
$currentRemotes = git remote -v

if ($currentRemotes -match "azure-origin") {
    Write-Host "   Removing existing azure-origin..." -ForegroundColor Yellow
    git remote remove azure-origin
}

if ($currentRemotes -match "^origin\s") {
    Write-Host "   Renaming GitHub origin to github-origin..." -ForegroundColor Yellow
    git remote rename origin github-origin
}

Write-Host "   Adding Azure Repos as origin..." -ForegroundColor Yellow
git remote add origin $repoUrl

# Push to Azure Repos
Write-Host "`n4. Pushing code to Azure Repos..." -ForegroundColor Green
Write-Host "   (You may be prompted for credentials)" -ForegroundColor Gray

git push -u origin --all
git push -u origin --tags

Write-Host "`n✅ Code successfully pushed to Azure Repos!" -ForegroundColor Green

# Instructions for pipeline
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "1. Go to: $OrganizationUrl/$ProjectName/_build" -ForegroundColor White
Write-Host "2. Click 'New Pipeline'" -ForegroundColor White
Write-Host "3. Select 'Azure Repos Git'" -ForegroundColor White
Write-Host "4. Select your repository: $ProjectName" -ForegroundColor White
Write-Host "5. Select 'Existing Azure Pipelines YAML file'" -ForegroundColor White
Write-Host "6. Choose: /azure-pipelines.yml" -ForegroundColor White
Write-Host "`n7. BEFORE running, create Service Connection:" -ForegroundColor Yellow
Write-Host "   - Project Settings > Service connections" -ForegroundColor Gray
Write-Host "   - New service connection > Azure Resource Manager" -ForegroundColor Gray
Write-Host "   - Service principal (automatic)" -ForegroundColor Gray
Write-Host "   - Subscription: Azure for Students" -ForegroundColor Gray
Write-Host "   - Resource group: rg-social-media-ml" -ForegroundColor Gray
Write-Host "   - Name: Azure-Service-Connection" -ForegroundColor Cyan
Write-Host "`n8. Run the pipeline!" -ForegroundColor Green

Write-Host "`n========================================`n" -ForegroundColor Cyan

Write-Host "GitHub Mirror (optional):" -ForegroundColor Yellow
Write-Host "To keep GitHub updated, run:" -ForegroundColor White
Write-Host "  git push github-origin main`n" -ForegroundColor Gray
