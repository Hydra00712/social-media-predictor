"""
Quick script to check Azure costs for this month
"""
import subprocess
import json
from datetime import datetime

print("=" * 100)
print("AZURE COST SUMMARY - DECEMBER 2025")
print("=" * 100)
print()

# Get all resource groups
result = subprocess.run(
    ['az', 'group', 'list', '--query', '[].name', '-o', 'json'],
    capture_output=True,
    text=True
)

resource_groups = json.loads(result.stdout)

print(f"📊 Found {len(resource_groups)} Resource Groups")
print()

# For each resource group, list resources
for rg in resource_groups:
    print(f"\n🔹 {rg}")
    print("-" * 100)
    
    # List resources in this group
    result = subprocess.run(
        ['az', 'resource', 'list', '--resource-group', rg, '--query', '[].{Name:name, Type:type}', '-o', 'table'],
        capture_output=True,
        text=True
    )
    
    if result.stdout:
        print(result.stdout)

print("\n" + "=" * 100)
print("💡 TO CHECK ACTUAL COSTS:")
print("=" * 100)
print("1. Go to: https://portal.azure.com/#view/Microsoft_Azure_CostManagement/Menu/~/overview")
print("2. Select 'Cost analysis'")
print("3. Filter by date range: December 2025")
print("4. Group by: Resource group")
print("=" * 100)

