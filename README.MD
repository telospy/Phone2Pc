<div align="center">
  
# 📱 Phone2PC - Instant File Transfer

### Share Files Between Any Device Instantly

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-purple.svg)](https://render.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

[Live Demo](https://phone2pc.onrender.com) | [Report Bug](https://github.com/telospy/Phone2Pc/issues) | [Request Feature](https://github.com/telospy/Phone2Pc/issues)

</div>

---

## ✨ Features

<div align="center">
  
| Feature | Description |
|---------|-------------|
| 📱➡️💻 | **Phone to PC** - Upload photos, videos, and files from your phone directly to your computer |
| 💻➡️📱 | **PC to Phone** - Download files from your PC to your phone with one tap |
| 💻➡️💻 | **PC to PC** - Share files between computers without USB drives or cables |
| 🔒 | **Secure & Private** - End-to-end encrypted transfers, files stay on your PC |
| 📸 | **QR Code Access** - Instant connection with your phone camera |
| 📁 | **Folder Upload** - Upload entire folders (auto-compressed to ZIP) |
| 👁️ | **File Preview** - View images, PDFs, and text files in browser |
| 💬 | **Send Messages** - Send text messages between devices |
| ⏱️ | **Auto-Expiry** - Links expire after 2 hours for security |
| 📱 | **Responsive Design** - Works perfectly on mobile and desktop |

</div>

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager
- [ngrok account](https://dashboard.ngrok.com/signup) (free)

### Installation

```bash
# Clone the repository
git clone https://github.com/telospy/Phone2Pc.git
cd Phone2Pc

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py




📖 How to Use
<div align="center">
Step 1: Create Your Space

https://via.placeholder.com/800x400?text=Create+Your+Space

Enter a name (optional) and click "Create Server" to get your unique link.
Step 2: Configure Server

https://via.placeholder.com/800x400?text=Configure+Server

    Enter your free ngrok token

    Select where files will be saved on your PC

    Click "Start Server"

Step 3: Share with Phone

https://via.placeholder.com/800x400?text=Share+QR+Code

Scan the QR code with your phone or share the unique link.
Step 4: Transfer Files!

https://via.placeholder.com/800x400?text=Transfer+Files

Upload from phone to PC, download from PC to phone - both ways work!
</div>
🌐 Live Demo

Try it now: https://phone2pc.onrender.com

    Click "Create Server"

    Enter your ngrok token

    Start sharing files instantly!

🛠️ Tech Stack
<div align="center">
Technology	Purpose
Python Flask	Backend web framework
ngrok	Secure tunnels to localhost
QR Code	Generate QR codes for easy access
Pillow	Image processing
Gunicorn	Production WSGI server
HTML5/CSS3	Frontend UI
JavaScript	Interactive features
</div>
📁 Project Structure
text

Phone2PC/
├── app.py              # Main Flask application
├── wsgi.py             # Production entry point
├── requirements.txt    # Python dependencies
├── runtime.txt         # Python version specification
├── render.yaml         # Render.com deployment config
├── templates/          # HTML templates
│   ├── landing.html    # Homepage
│   ├── server.html     # PC control panel
│   ├── client.html     # Phone transfer interface
│   ├── about.html      # About page
│   └── not_found.html  # 404 page
└── static/
    └── style.css       # Stylesheet

🔒 Security & Privacy

    ✅ Files never leave your PC - All files are stored locally on your computer

    ✅ End-to-end encrypted - ngrok provides secure tunnels

    ✅ 2-hour auto-expiry - Links automatically expire for security

    ✅ Secret links - Each session has unique, unguessable URLs

    ✅ 100% open source - Inspect the code yourself

⚠️ Limitations (ngrok Free Tier)
Limitation	Description
📦 500MB	Maximum file size per transfer
⏱️ 2 hours	Session time limit
🔌 40/min	Maximum connections per minute

💡 Want to remove limitations? Upgrade ngrok plan for:

    Unlimited file size

    Custom domains

    Higher connection limits

    Reserved URLs

🚢 Deployment
Deploy to Render.com (Recommended)

    Fork/clone this repository

    Sign up at render.com

    Click "New +" → "Web Service"

    Connect your GitHub repository

    Use these settings:

        Build Command: pip install -r requirements.txt

        Start Command: gunicorn wsgi:app

    Click "Create Web Service"

Your app will be live at https://your-app.onrender.com
Deploy to Railway.app

    Sign up at railway.app

    Click "New Project" → "Deploy from GitHub"

    Select your repository

    Railway auto-detects and deploys!

🤝 Contributing

Contributions are welcome! Here's how you can help:

    🍴 Fork the repository

    🌿 Create a branch (git checkout -b feature/amazing)

    ✨ Make your changes

    📝 Commit (git commit -m 'Add amazing feature')

    📤 Push (git push origin feature/amazing)

    🔀 Open a Pull Request

Development Setup
bash

# Clone your fork
git clone https://github.com/your-username/Phone2Pc.git
cd Phone2Pc

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python app.py

📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

    ngrok for providing secure tunnels

    Flask for the amazing web framework

    All contributors who help make this project better

📧 Contact

Tsegaye (131)

    GitHub: @telospy

    Project Link: https://github.com/telospy/Phone2Pc

    Live Demo: https://phone2pc.onrender.com

<div align="center">
⭐ Show Your Support

If you find this project useful, please give it a star! ⭐

Made with ❤️ by Tsegaye (131)
</div>
