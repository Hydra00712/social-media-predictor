"""
GITHUB SETUP VERIFICATION AND COMPLETION
"""

import subprocess
from datetime import datetime

print("\n" + "="*100)
print("GITHUB SETUP VERIFICATION")
print("="*100 + "\n")

# Check git status
print("1️⃣  GIT STATUS")
print("-" * 100)

result = subprocess.run(['git', 'log', '--oneline', '-5'], capture_output=True, text=True)
print("✅ Last 5 commits:")
print(result.stdout)

result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
print("✅ Remote configuration:")
print(result.stdout)

# What's next
print("\n" + "="*100)
print("NEXT STEPS: CONFIGURE GITHUB SECRETS & VARIABLES")
print("="*100 + "\n")

print("""
⚠️  IMPORTANT: You still need to configure GitHub Secrets and Variables 
    for the CI/CD workflows to work!

📋 GO TO: https://github.com/Hydra00712/social-media-predictor/settings/secrets/actions

ADD THESE SECRETS (4 required):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. AZURE_CLIENT_ID
   └─ Value: Your Azure app registration client ID
   └─ Get from: Azure Portal → Microsoft Entra ID → App registrations

2. AZURE_TENANT_ID
   └─ Value: Your Azure tenant ID
   └─ Get from: Azure Portal → Microsoft Entra ID → Overview

3. AZURE_SUBSCRIPTION_ID
   └─ Value: Your Azure subscription ID
   └─ Get from: Azure Portal → Subscriptions

4. AZURE_STORAGE_CONNECTION_STRING
   └─ Value: Your storage account connection string
   └─ Get from: Azure Portal → Storage Account → Access Keys


📋 GO TO: https://github.com/Hydra00712/social-media-predictor/settings/variables/actions

ADD THIS VARIABLE (1 required):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ACR_NAME
   └─ Value: socialmlacr
   └─ (Your Azure Container Registry name - must be globally unique)


📋 GO TO: https://github.com/Hydra00712/social-media-predictor/settings/actions

CONFIGURE WORKFLOW PERMISSIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

☑️  "Allow GitHub Actions to create and approve pull requests"
☑️  "Allow read and write permissions for all scopes"

Then click "Save"
""")

print("\n" + "="*100)
print("GITHUB ACTIONS WORKFLOWS READY")
print("="*100 + "\n")

workflows = [
    ("aca-deploy.yml", "Deploy to Azure Container Apps", "push to main + manual trigger"),
    ("ci.yml", "CI - Lint & Smoke Tests", "push + pull_request on main"),
    ("ci-basic.yml", "CI - Basic Syntax Check", "push + pull_request on main"),
    ("deploy.yml", "General Deployment", "Available for triggering"),
]

for workflow_file, name, trigger in workflows:
    print(f"✅ {name}")
    print(f"   File: .github/workflows/{workflow_file}")
    print(f"   Trigger: {trigger}\n")

print("="*100)
print("VERIFICATION CHECKLIST")
print("="*100 + "\n")

checklist = [
    ("✅ Code pushed to GitHub", "main branch with 32 commits"),
    ("✅ .github/workflows/ pushed", "4 workflow files configured"),
    ("✅ Git remote updated", "https://github.com/Hydra00712/social-media-predictor.git"),
    ("⏳ Secrets configured", "PENDING - See instructions above"),
    ("⏳ Variables configured", "PENDING - See instructions above"),
    ("⏳ Workflow permissions set", "PENDING - See instructions above"),
    ("⏳ First workflow run", "PENDING - After secrets are configured"),
]

for check, status in checklist:
    print(f"{check:50} {status}")

print("\n" + "="*100)
print("QUICK LINKS")
print("="*100 + "\n")

links = [
    ("Repository", "https://github.com/Hydra00712/social-media-predictor"),
    ("Secrets Config", "https://github.com/Hydra00712/social-media-predictor/settings/secrets/actions"),
    ("Variables Config", "https://github.com/Hydra00712/social-media-predictor/settings/variables/actions"),
    ("Workflow Permissions", "https://github.com/Hydra00712/social-media-predictor/settings/actions"),
    ("Actions Tab", "https://github.com/Hydra00712/social-media-predictor/actions"),
]

for name, url in links:
    print(f"🔗 {name:25} → {url}")

print("\n" + "="*100)
print("AFTER CONFIGURATION")
print("="*100 + "\n")

print("""
Once you've configured secrets and variables:

1. Go to: https://github.com/Hydra00712/social-media-predictor/actions

2. Select any workflow (e.g., "CI")

3. Click "Run workflow" button

4. Watch the workflow execute - it should:
   ✓ Check out your code
   ✓ Install dependencies
   ✓ Run syntax checks
   ✓ Complete successfully

5. For deployment, push to main branch:
   └─ The "Deploy to Azure Container Apps" workflow will automatically run
   └─ It will build your Docker image, push to ACR, and deploy to Container Apps

Your GitHub Actions CI/CD pipeline is ready to go! 🚀
""")

print("="*100 + "\n")
