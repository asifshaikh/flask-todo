#!/bin/bash
set -e  # Exit on any error

APP_DIR=/home/ec2-user/todos-deploy

echo "🔧 Deploying Flask App in $APP_DIR"
cd $APP_DIR

# Kill any existing Flask process
echo "🛑 Stopping old Flask process..."
sudo pkill -f "flask run" || true

# Create virtual environment if missing
if [ ! -d "venv" ]; then
  echo "📦 Creating new virtual environment..."
  python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Start Flask app
echo "🚀 Starting Flask app..."
nohup flask run --host=0.0.0.0 --port=5000 > app.log 2>&1 &

echo "✅ Deployment complete!"
