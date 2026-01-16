#!/bin/bash
# Setup script for Square Cafe Report application

echo "Setting up Square Cafe Report application..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Create config file if it doesn't exist
if [ ! -f config.yaml ]; then
    echo "Creating config.yaml from template..."
    cp config.example.yaml config.yaml
    echo "⚠️  Please edit config.yaml with your Square API credentials"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Edit config.yaml with your Square credentials"
echo "3. Run the app: streamlit run app.py"
echo ""
