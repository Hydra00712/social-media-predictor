# Get today's Azure costs sorted by time
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 99) -ForegroundColor Cyan
Write-Host "AZURE COSTS - TODAY (December 18, 2025)" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 99) -ForegroundColor Cyan
Write-Host ""

# Get usage data for today
$usage = az consumption usage list --start-date 2025-12-18 --end-date 2025-12-18 --output json | ConvertFrom-Json

# Filter and format the data
$costs = $usage | Where-Object { $_.pretaxCost -ne $null -and $_.pretaxCost -ne "None" } | ForEach-Object {
    $resourceName = ($_.instanceName -split '/')[-1]
    [PSCustomObject]@{
        Time = if ($_.usageStart) { (Get-Date $_.usageStart).ToString("HH:mm:ss") } else { "N/A" }
        Resource = $resourceName
        Service = $_.meterCategory
        Meter = $_.meterName
        Cost = [decimal]$_.pretaxCost
        Quantity = $_.quantity
    }
}

# Sort by time descending (most recent first)
$costs = $costs | Sort-Object Time -Descending

# Display the results
$costs | Format-Table -AutoSize

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 99) -ForegroundColor Cyan
Write-Host "TOTAL COST TODAY: $" -NoNewline -ForegroundColor Yellow
Write-Host ($costs | Measure-Object -Property Cost -Sum).Sum -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 99) -ForegroundColor Cyan

