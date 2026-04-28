Write-Host "=================================="
Write-Host "      SOAR Cleanup Utility"
Write-Host "=================================="
Write-Host ""

Write-Host "[1/6] Removing __pycache__ ..."
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "[2/6] Removing *.pyc ..."
Get-ChildItem -Recurse -File -Include *.pyc,*.pyo | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "[3/6] Removing virtual environments ..."
Remove-Item -Recurse -Force venv,.venv -ErrorAction SilentlyContinue

Write-Host "[4/6] Removing runtime data ..."
Remove-Item -Force .\backend\data\*.gz -ErrorAction SilentlyContinue
Remove-Item -Force .\data\*.gz -ErrorAction SilentlyContinue
Remove-Item -Force .\ml_baseline.json -ErrorAction SilentlyContinue

Write-Host "[5/6] Removing temp files ..."
Remove-Item -Force *.log,*.tmp -ErrorAction SilentlyContinue

Write-Host "[6/6] Cleanup complete."
Write-Host ""
Write-Host "Project cleaned successfully."