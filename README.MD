# 📱 Phone2PC - Instant File Transfer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-green.svg)](https://flask.palletsprojects.com/)

**Phone2PC** is a free, open-source file transfer tool that lets you share files between any devices - Phone to PC, PC to Phone, and PC to PC - instantly with a QR code.

## ✨ Features

- 📱 **Phone to PC** - Upload photos, videos, and files from your phone directly to your computer
- 💻 **PC to Phone** - Download files from your PC to your phone with one tap
- 🔄 **PC to PC** - Share files between computers without USB drives or cables
- 🔒 **Secure & Private** - End-to-end encrypted transfers, files stay on your PC
- 📸 **QR Code Access** - Instant connection with your phone camera
- 📁 **Folder Upload** - Upload entire folders (auto-compressed to ZIP)
- 👁️ **File Preview** - View images, PDFs, and text files in browser
- 💬 **Send Messages** - Send text messages between devices
- ⏱️ **Auto-Expiry** - Links expire after 2 hours for security
- 📱 **Responsive Design** - Works perfectly on mobile and desktop

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- ngrok account (free) - [Get token here](https://dashboard.ngrok.com/signup)

### Installation

```bash
# Clone the repository
git clone https://github.com/telospy/Phone2Pc.git
cd Phone2Pc

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py