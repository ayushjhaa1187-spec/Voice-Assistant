#!/bin/bash
echo "🤖 Setting up JUNE..."
python3 -m venv june_env
source june_env/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
echo "✅ JUNE ready. Add your API keys to .env then run: python3 main.py"
