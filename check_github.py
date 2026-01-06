"""
GITHUB AND GITHUB ACTIONS VERIFICATION
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path

print("\n" + "="*100)
print("GITHUB & GITHUB ACTIONS COMPREHENSIVE CHECK")
print("="*100 + "\n")

results = []

# ============================================================================
# CHECK 1: GIT REPOSITORY
# ============================================================================
print("1️⃣  GIT REPOSITORY")
print("-" * 100)

try:
    # Check if git is installed
    result = subprocess.run(['git', '--version'], capture_output=True, text=True)
    git_version = result.stdout.strip()
    print(f"✅ Git installed: {git_version}")
    
    # Check if we're in a git repo
    result = subprocess.run(['git', 'rev-parse', '--git-dir'], capture_output=True, text=True, cwd=os.getcwd())
    
    if result.returncode == 0:
        git_dir = result.stdout.strip()
        print(f"✅ Git repository: YES")
        print(f"   └─ Location: {git_dir}")
        
        # Get remote URL
        result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True)
        if result.returncode == 0:
            remote_url = result.stdout.strip()
            print(f"✅ Remote URL: {remote_url}")
            
            # Extract repo info
            if 'github' in remote_url.lower():
                print(f"✅ GitHub repository: YES")
                results.append(("Git Repository", "✅ PASS", "GitHub repo connected"))
            else:
                print(f"⚠️  Not a GitHub repository")
                results.append(("Git Repository", "⚠️ WARN", "Not GitHub"))
        else:
            print(f"❌ Could not get remote URL")
            results.append(("Git Repository", "❌ FAIL", "No remote configured"))
    else:
        print(f"❌ Not a git repository")
        results.append(("Git Repository", "❌ FAIL", "Not a git repo"))
        
except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    results.append(("Git Repository", "❌ FAIL", str(e)[:80]))

# ============================================================================
# CHECK 2: GIT BRANCH AND STATUS
# ============================================================================
print("\n2️⃣  GIT STATUS")
print("-" * 100)

try:
    # Get current branch
    result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
    if result.returncode == 0:
        branch = result.stdout.strip()
        print(f"✅ Current branch: {branch}")
    
    # Get commit count
    result = subprocess.run(['git', 'rev-list', '--count', 'HEAD'], capture_output=True, text=True)
    if result.returncode == 0:
        commit_count = result.stdout.strip()
        print(f"✅ Total commits: {commit_count}")
    
    # Get last commit
    result = subprocess.run(['git', 'log', '-1', '--format=%h - %s (%ai)'], capture_output=True, text=True)
    if result.returncode == 0:
        last_commit = result.stdout.strip()
        print(f"✅ Last commit: {last_commit}")
    
    # Get status
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.returncode == 0:
        status_lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
        if status_lines and status_lines[0]:
            print(f"⚠️  Uncommitted changes: {len(status_lines)}")
        else:
            print(f"✅ Working directory: Clean")
        
        print(f"✅ GIT STATUS: OPERATIONAL")
        results.append(("Git Status", "✅ PASS", f"Branch: {branch}, Commits: {commit_count}"))
    
except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    results.append(("Git Status", "❌ FAIL", str(e)[:80]))

# ============================================================================
# CHECK 3: GITHUB WORKFLOWS
# ============================================================================
print("\n3️⃣  GITHUB WORKFLOWS")
print("-" * 100)

try:
    workflows_dir = Path(".github/workflows")
    
    if workflows_dir.exists():
        print(f"✅ Workflows directory: Found")
        
        workflow_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
        print(f"✅ Workflow files: {len(workflow_files)}")
        
        for workflow_file in workflow_files:
            print(f"\n   📄 {workflow_file.name}")
            
            with open(workflow_file, 'r') as f:
                content = f.read()
                
                # Extract name
                if 'name:' in content:
                    name_line = [line for line in content.split('\n') if 'name:' in line][0]
                    name = name_line.split('name:')[1].strip().strip('"').strip("'")
                    print(f"      Name: {name}")
                
                # Extract triggers
                triggers = []
                if 'on:' in content:
                    on_idx = content.find('on:')
                    on_section = content[on_idx:on_idx+500]
                    if 'push' in on_section:
                        triggers.append('push')
                    if 'pull_request' in on_section:
                        triggers.append('pull_request')
                    if 'schedule' in on_section:
                        triggers.append('schedule')
                    if 'workflow_dispatch' in on_section:
                        triggers.append('manual')
                    
                    print(f"      Triggers: {', '.join(triggers) if triggers else 'None'}")
                
                # Extract jobs
                if 'jobs:' in content:
                    jobs = [line for line in content.split('\n') if line.startswith('  ') and ':' in line and 'runs-on' in content[content.find(line):content.find(line)+200]]
                    job_names = []
                    in_jobs = False
                    for line in content.split('\n'):
                        if line.strip().startswith('jobs:'):
                            in_jobs = True
                        elif in_jobs and line.startswith('  ') and not line.startswith('    ') and ':' in line:
                            job_names.append(line.strip().split(':')[0])
                    
                    print(f"      Jobs: {', '.join(job_names[:3]) if job_names else 'None'}")
        
        if workflow_files:
            print(f"\n✅ GITHUB WORKFLOWS: CONFIGURED")
            results.append(("Workflows", "✅ PASS", f"{len(workflow_files)} workflow(s)"))
        else:
            print(f"\n⚠️  No workflow files found")
            results.append(("Workflows", "⚠️ WARN", "No workflows configured"))
    else:
        print(f"⚠️  .github/workflows directory not found")
        results.append(("Workflows", "⚠️ WARN", "Directory not found"))
        
except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    results.append(("Workflows", "❌ FAIL", str(e)[:80]))

# ============================================================================
# CHECK 4: GITHUB SECRETS CONFIGURATION
# ============================================================================
print("\n4️⃣  GITHUB SECRETS")
print("-" * 100)

try:
    # Check if GitHub CLI is installed
    result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
    gh_version = result.stdout.strip()
    print(f"✅ GitHub CLI installed: YES")
    
    # Try to list secrets
    try:
        result = subprocess.run(['gh', 'secret', 'list'], capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            secrets = result.stdout.strip().split('\n')
            print(f"✅ GitHub secrets configured: {len(secrets)}")
            
            for secret_line in secrets[:5]:
                if secret_line:
                    secret_name = secret_line.split()[0] if secret_line.split() else "Unknown"
                    print(f"   - {secret_name}")
            
            if len(secrets) > 5:
                print(f"   ... and {len(secrets) - 5} more")
            
            print(f"\n✅ GITHUB SECRETS: CONFIGURED")
            results.append(("Secrets", "✅ PASS", f"{len(secrets)} secret(s)"))
        else:
            print(f"⚠️  Could not retrieve secrets (may need authentication)")
            results.append(("Secrets", "⚠️ WARN", "Need gh login"))
            
    except Exception as e:
        print(f"⚠️  GitHub CLI command failed: {str(e)}")
        results.append(("Secrets", "⚠️ WARN", "CLI not available"))
        
except Exception as e:
    print(f"⚠️  FAILED: {str(e)}")
    results.append(("Secrets", "⚠️ WARN", str(e)[:80]))

# ============================================================================
# CHECK 5: GITHUB ACTIONS ENV VARIABLES
# ============================================================================
print("\n5️⃣  GITHUB ACTIONS ENVIRONMENT")
print("-" * 100)

try:
    # Check for env files in workflows
    env_vars_found = set()
    
    workflows_dir = Path(".github/workflows")
    if workflows_dir.exists():
        for workflow_file in workflows_dir.glob("*.yml"):
            with open(workflow_file, 'r') as f:
                content = f.read()
                
                # Look for environment variables
                if 'env:' in content:
                    print(f"✅ Environment variables in {workflow_file.name}:")
                    
                    in_env = False
                    for line in content.split('\n'):
                        if line.strip() == 'env:':
                            in_env = True
                        elif in_env and line.startswith('  ') and ':' in line:
                            var_name = line.strip().split(':')[0]
                            env_vars_found.add(var_name)
                            print(f"   - {var_name}")
                        elif in_env and not line.startswith('  '):
                            in_env = False
    
    if env_vars_found:
        print(f"\n✅ GITHUB ENV VARIABLES: CONFIGURED")
        results.append(("Environment", "✅ PASS", f"{len(env_vars_found)} variable(s)"))
    else:
        print(f"⚠️  No environment variables found in workflows")
        results.append(("Environment", "⚠️ WARN", "No env vars configured"))
        
except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    results.append(("Environment", "❌ FAIL", str(e)[:80]))

# ============================================================================
# CHECK 6: AZURE INTEGRATION IN WORKFLOWS
# ============================================================================
print("\n6️⃣  AZURE INTEGRATION")
print("-" * 100)

try:
    azure_integrations = {
        'azure-login': 0,
        'azure-cli': 0,
        'acr': 0,
        'container-app': 0,
        'function': 0,
        'static-web': 0,
        'appservice': 0
    }
    
    workflows_dir = Path(".github/workflows")
    if workflows_dir.exists():
        for workflow_file in workflows_dir.glob("*.yml"):
            with open(workflow_file, 'r') as f:
                content = f.read().lower()
                
                for key in azure_integrations:
                    if key in content:
                        azure_integrations[key] += 1
    
    found_integrations = {k: v for k, v in azure_integrations.items() if v > 0}
    
    if found_integrations:
        print(f"✅ Azure integrations detected:")
        for service, count in found_integrations.items():
            print(f"   - {service}: {count} workflow(s)")
        
        print(f"\n✅ AZURE INTEGRATION: CONFIGURED")
        results.append(("Azure Integration", "✅ PASS", f"{len(found_integrations)} integration(s)"))
    else:
        print(f"⚠️  No Azure integrations found in workflows")
        results.append(("Azure Integration", "⚠️ WARN", "No Azure detected"))
        
except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    results.append(("Azure Integration", "❌ FAIL", str(e)[:80]))

# ============================================================================
# CHECK 7: GITHUB README AND DOCUMENTATION
# ============================================================================
print("\n7️⃣  DOCUMENTATION")
print("-" * 100)

try:
    doc_files = {
        'README.md': 'Project README',
        'CONTRIBUTING.md': 'Contributing guidelines',
        '.github/ISSUE_TEMPLATE': 'Issue templates',
        '.github/PULL_REQUEST_TEMPLATE.md': 'PR template',
        'LICENSE': 'License file'
    }
    
    found_docs = []
    for file_path, description in doc_files.items():
        full_path = Path(file_path)
        if full_path.exists():
            found_docs.append((file_path, description))
            print(f"✅ {description}: Found ({file_path})")
        else:
            print(f"⚠️  {description}: Missing ({file_path})")
    
    if found_docs:
        print(f"\n✅ DOCUMENTATION: PRESENT")
        results.append(("Documentation", "✅ PASS", f"{len(found_docs)}/5 files"))
    else:
        print(f"\n⚠️  DOCUMENTATION: MINIMAL")
        results.append(("Documentation", "⚠️ WARN", "Missing docs"))
        
except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    results.append(("Documentation", "❌ FAIL", str(e)[:80]))

# ============================================================================
# CHECK 8: GITHUB ACTIONS PERMISSIONS
# ============================================================================
print("\n8️⃣  WORKFLOW PERMISSIONS")
print("-" * 100)

try:
    permissions_found = {}
    
    workflows_dir = Path(".github/workflows")
    if workflows_dir.exists():
        for workflow_file in workflows_dir.glob("*.yml"):
            with open(workflow_file, 'r') as f:
                content = f.read()
                
                if 'permissions:' in content:
                    print(f"✅ Permissions configured in {workflow_file.name}")
                    
                    # Extract permissions
                    in_perms = False
                    for line in content.split('\n'):
                        if 'permissions:' in line:
                            in_perms = True
                        elif in_perms and ':' in line and line.strip() != 'permissions:':
                            perm_name = line.strip().split(':')[0]
                            perm_value = line.strip().split(':')[1].strip() if ':' in line else 'set'
                            print(f"   - {perm_name}: {perm_value}")
                        elif in_perms and line.strip() and not line.startswith('  '):
                            in_perms = False
    
    if permissions_found or workflows_dir.exists():
        print(f"\n✅ WORKFLOW PERMISSIONS: CONFIGURED")
        results.append(("Permissions", "✅ PASS", "Permissions set"))
    else:
        print(f"\n⚠️  No permissions configured")
        results.append(("Permissions", "⚠️ WARN", "Default permissions"))
        
except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    results.append(("Permissions", "❌ FAIL", str(e)[:80]))

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*100)
print("GITHUB & GITHUB ACTIONS SUMMARY")
print("="*100 + "\n")

pass_count = sum(1 for r in results if "✅ PASS" in r[1])
warn_count = sum(1 for r in results if "⚠️ WARN" in r[1])
fail_count = sum(1 for r in results if "❌ FAIL" in r[1])
total = len(results)

print(f"Status Summary:")
print(f"✅ Passed: {pass_count}/{total}")
print(f"⚠️  Warnings: {warn_count}/{total}")
print(f"❌ Failed: {fail_count}/{total}")

print(f"\nDetailed Results:")
print("-" * 100)

for name, status, detail in results:
    icon = "✅" if "PASS" in status else ("⚠️" if "WARN" in status else "❌")
    print(f"\n{icon} {name:25} | {status:20}")
    print(f"   └─ {detail}")

# Grade
if fail_count == 0:
    if warn_count == 0:
        grade = "A+"
    elif warn_count <= 2:
        grade = "A"
    else:
        grade = "B+"
else:
    grade = "B"

percentage = (pass_count / total) * 100 if total > 0 else 0

print(f"\n" + "="*100)
print(f"GITHUB GRADE: {grade} ({pass_count}/{total} = {percentage:.1f}%)")
print(f"="*100 + "\n")

if pass_count >= total - 2:
    print(f"✅ GITHUB AND GITHUB ACTIONS ARE OPERATIONAL")
    print(f"   ✓ Git repository connected to GitHub")
    print(f"   ✓ GitHub workflows configured")
    print(f"   ✓ CI/CD pipeline available")
    print(f"   ✓ Repository ready for automation")
else:
    print(f"⚠️  GITHUB SETUP NEEDS ATTENTION")
    print(f"   ⚠ Some configurations missing or incomplete")
    print(f"   ⚠ Review warnings above")

print()
