# Launch script for Streamlit app
Write-Host "🚀 Starting Shortest Path Finder Application..." -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
& ".\.venv\Scripts\Activate.ps1"

# Run Streamlit
Write-Host "📊 Launching Streamlit..." -ForegroundColor Green
streamlit run app.py
