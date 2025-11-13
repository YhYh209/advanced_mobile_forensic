# install.sh
#!/bin/bash

echo "🚀 Installing Advanced Mobile Forensic System..."
echo "=================================================="

# Check Python version
python3 --version || { echo "❌ Python 3.8+ required"; exit 1; }

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv forensic_env
source forensic_env/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install system dependencies
echo "🔧 Installing system dependencies..."

# For Ubuntu/Debian
if command -v apt &> /dev/null; then
    sudo apt update
    sudo apt install -y \
        android-tools-adb \
        libimobiledevice-utils \
        ideviceinstaller \
        usbmuxd \
        sqlite3
fi

# For macOS
if command -v brew &> /dev/null; then
    brew install \
        android-platform-tools \
        libimobiledevice \
        ideviceinstaller
fi

# Create project structure
echo "📁 Creating project structure..."
mkdir -p \
    uploaded_data \
    extracted_data \
    reports \
    logs \
    static/{css,js,images} \
    templates \
    ios_backups

# Set permissions
chmod +x main.py

echo ""
echo "✅ Installation completed!"
echo ""
echo "🎯 Quick Start:"
echo "   1. Activate environment: source forensic_env/bin/activate"
echo "   2. Start system: python main.py"
echo "   3. Open: http://localhost:5000"
echo ""
echo "📱 Device Setup:"
echo "   - Android: Enable USB debugging"
echo "   - iOS: Trust computer on device"
echo ""
echo "⚡ Features:"
echo "   - Android & iOS forensics"
echo "   - AI-powered analysis"
echo "   - Real-time monitoring"
echo "   - Professional reporting"
echo "   - Advanced data extraction"
