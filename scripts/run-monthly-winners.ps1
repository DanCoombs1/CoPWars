# Automated Monthly Winners Script Runner
# This script can be scheduled to run automatically

Write-Host "Starting Automated Monthly Winners Script..." -ForegroundColor Green
Write-Host "Date: $(Get-Date -Format 'yyyy-MM-dd')" -ForegroundColor Cyan
Write-Host "Time: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Cyan

# Change to the script directory
Set-Location "C:\Users\danielbc\OneDrive - AIIMI LIMITED\Documents\Aiimi\Data CoP\Aiimi Code wars"

# Run the automated script
try {
    python automated-monthly-winners.py
    Write-Host "Script completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error running script: $_" -ForegroundColor Red
}

# Optional: Keep window open for 10 seconds to see output
Start-Sleep -Seconds 10
