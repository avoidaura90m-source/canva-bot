
## 📄 **File 4: `setup.sh`**

```bash
#!/bin/bash

echo "╔════════════════════════════╗"
echo "║  CANVA BOT SETUP FOR TERMUX ║"
echo "╚════════════════════════════╝"

echo -e "\n📦 Updating Termux..."
pkg update -y && pkg upgrade -y

echo -e "\n📦 Installing packages..."
pkg install -y python chromium

echo -e "\n🐍 Installing Python packages..."
pip install selenium webdriver-manager requests names fake-useragent

echo -e "\n📁 Creating numbers file..."
mkdir -p /sdcard/Download
cat > /sdcard/Download/numbers.txt << 'EOF'
71234567
71234568
71234569
71234570
+26371234571
EOF

echo -e "\n✅ Setup Complete!"
echo -e "\n📝 To run the bot:"
echo "   cd canva-bot"
echo "   python canva_bot.py"
echo -e "\n⚠️ Don't forget to connect VPN first!"
