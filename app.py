#!/usr/bin/env python3
"""
Phone to PC File Transfer - Professional File Sharing Platform
Author: Tsegaye (131)
GitHub: https://github.com/telospy/Phone2Pc
"""

import os
import sys
import json
import threading
import webbrowser
from pathlib import Path
from datetime import datetime, timedelta
import re
import base64
from io import BytesIO
import subprocess
import tempfile
import time
import platform
import socket
import zipfile
import uuid
import shutil
import hashlib
import secrets
import mimetypes
from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from flask_cors import CORS
import qrcode
from pyngrok import ngrok, conf

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)

user_data_path = Path.home() / 'phone2pc_users'
user_data_path.mkdir(exist_ok=True)

ngrok_processes = {}

def generate_random_id():
    return secrets.token_hex(4)

def generate_secret_key():
    return secrets.token_hex(12)

def save_user(user_id, data):
    user_dir = user_data_path / user_id
    user_dir.mkdir(exist_ok=True)
    with open(user_dir / 'config.json', 'w') as f:
        json.dump(data, f)

def load_user(user_id):
    config_file = user_data_path / user_id / 'config.json'
    if config_file.exists():
        with open(config_file, 'r') as f:
            return json.load(f)
    return None

def get_ngrok_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    ngrok_name = 'ngrok.exe' if platform.system() == 'Windows' else 'ngrok'
    ngrok_path = os.path.join(base_path, ngrok_name)
    
    if os.path.exists(ngrok_path):
        return ngrok_path
    
    import shutil
    return shutil.which('ngrok')

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        custom_name = data.get('name', '').strip().lower()
        
        user_id = generate_random_id()
        secret_key = generate_secret_key()
        user_folder = Path.home() / 'Phone2PC_Uploads' / user_id
        
        user_data = {
            'id': user_id,
            'secret_key': secret_key,
            'created_at': datetime.now().isoformat(),
            'server_running': False,
            'public_url': None,
            'start_time': None,
            'ngrok_token': '',
            'save_folder': str(user_folder)
        }
        
        save_user(user_id, user_data)
        
        upload_folder = Path(user_data['save_folder'])
        upload_folder.mkdir(parents=True, exist_ok=True)
        
        categories = ['Images', 'Videos', 'Audio', 'Archives', 'Documents', 'Messages', 'Folder_Uploads', 'Others']
        for cat in categories:
            (upload_folder / cat).mkdir(exist_ok=True)
        
        base_url = request.host_url.rstrip('/')
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'secret_key': secret_key,
            'server_url': f"{base_url}/server/{user_id}",
            'client_url': f"{base_url}/client/{secret_key}",
            'save_folder': str(user_folder)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/server/<user_id>')
def server_view(user_id):
    user_data = load_user(user_id)
    if not user_data:
        return render_template('not_found.html', user_id=user_id), 404
    
    return render_template('server.html', user_id=user_id, user_data=user_data)

@app.route('/client/<secret_key>')
def client_view(secret_key):
    user_data = None
    user_id = None
    
    for user_dir in user_data_path.iterdir():
        if user_dir.is_dir():
            config_file = user_dir / 'config.json'
            if config_file.exists():
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    if data.get('secret_key') == secret_key:
                        user_data = data
                        user_id = user_dir.name
                        break
    
    if not user_data:
        return render_template('not_found.html', user_id=secret_key), 404
    
    return render_template('client.html', user_id=user_id, user_data=user_data)

@app.route('/api/<user_id>/save_settings', methods=['POST'])
def save_user_settings(user_id):
    try:
        user_data = load_user(user_id)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if 'ngrok_token' in data:
            user_data['ngrok_token'] = data['ngrok_token']
        
        if 'save_folder' in data:
            save_folder = data['save_folder']
            user_data['save_folder'] = save_folder
            Path(save_folder).mkdir(parents=True, exist_ok=True)
            
            categories = ['Images', 'Videos', 'Audio', 'Archives', 'Documents', 'Messages', 'Folder_Uploads', 'Others']
            for cat in categories:
                (Path(save_folder) / cat).mkdir(exist_ok=True)
        
        save_user(user_id, user_data)
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/<user_id>/start_server', methods=['POST'])
def start_user_server(user_id):
    global ngrok_processes
    
    try:
        user_data = load_user(user_id)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        ngrok_token = data.get('ngrok_token', '').strip()
        save_folder = data.get('save_folder', user_data.get('save_folder'))
        
        if not ngrok_token:
            return jsonify({'error': 'Ngrok token required'}), 400
        
        user_data['ngrok_token'] = ngrok_token
        user_data['save_folder'] = save_folder
        user_data['server_running'] = True
        user_data['start_time'] = datetime.now().isoformat()
        
        Path(save_folder).mkdir(parents=True, exist_ok=True)
        
        categories = ['Images', 'Videos', 'Audio', 'Archives', 'Documents', 'Messages', 'Folder_Uploads', 'Others']
        for cat in categories:
            (Path(save_folder) / cat).mkdir(exist_ok=True)
        
        if user_id in ngrok_processes:
            try:
                if platform.system() == "Windows":
                    subprocess.run(['taskkill', '/F', '/PID', str(ngrok_processes[user_id].pid)], capture_output=True)
                else:
                    ngrok_processes[user_id].terminate()
            except:
                pass
        
        conf.get_default().auth_token = ngrok_token
        conf.get_default().region = "us"
        
        regions = ["us", "eu", "ap", "au", "sa"]
        public_url = None
        
        for region in regions:
            try:
                conf.get_default().region = region
                try:
                    ngrok.kill()
                except:
                    pass
                time.sleep(1)
                tunnel = ngrok.connect(5000, "http")
                public_url = tunnel.public_url
                break
            except:
                continue
        
        if not public_url:
            try:
                ngrok_path = get_ngrok_path()
                if ngrok_path:
                    process = subprocess.Popen(
                        [ngrok_path, 'http', '5000', '--authtoken', ngrok_token],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
                    )
                    ngrok_processes[user_id] = process
                    time.sleep(3)
                    import urllib.request
                    try:
                        with urllib.request.urlopen('http://127.0.0.1:4040/api/tunnels', timeout=5) as response:
                            tunnel_data = json.loads(response.read().decode())
                            if tunnel_data['tunnels']:
                                public_url = tunnel_data['tunnels'][0]['public_url']
                    except:
                        pass
            except:
                pass
        
        if not public_url:
            user_data['server_running'] = False
            save_user(user_id, user_data)
            return jsonify({'error': 'Failed to start ngrok. Check your token and internet.'}), 500
        
        user_data['public_url'] = public_url
        save_user(user_id, user_data)
        
        base_url = request.host_url.rstrip('/')
        
        return jsonify({
            'success': True,
            'url': public_url,
            'client_url': f"{base_url}/client/{user_data['secret_key']}",
            'folder': save_folder
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/<user_id>/stop_server', methods=['POST'])
def stop_user_server(user_id):
    global ngrok_processes
    
    try:
        user_data = load_user(user_id)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
        
        if user_id in ngrok_processes:
            try:
                if platform.system() == "Windows":
                    subprocess.run(['taskkill', '/F', '/PID', str(ngrok_processes[user_id].pid)], capture_output=True)
                else:
                    ngrok_processes[user_id].terminate()
                del ngrok_processes[user_id]
            except:
                pass
        
        try:
            ngrok.kill()
        except:
            pass
        
        user_data['server_running'] = False
        user_data['public_url'] = None
        user_data['start_time'] = None
        save_user(user_id, user_data)
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/<user_id>/status')
def user_status(user_id):
    user_data = load_user(user_id)
    if not user_data:
        return jsonify({'error': 'User not found'}), 404
    
    remaining = 0
    if user_data.get('server_running') and user_data.get('start_time'):
        try:
            start = datetime.fromisoformat(user_data['start_time'])
            elapsed = datetime.now() - start
            remaining = max(0, int((timedelta(hours=2) - elapsed).total_seconds()))
        except:
            pass
    
    return jsonify({
        'running': user_data.get('server_running', False),
        'url': user_data.get('public_url'),
        'remaining_seconds': remaining,
        'save_folder': user_data.get('save_folder', ''),
        'ngrok_token': user_data.get('ngrok_token', '')
    })

@app.route('/api/<user_id>/upload', methods=['POST'])
def user_upload(user_id):
    try:
        user_data = load_user(user_id)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
        
        upload_folder = Path(user_data.get('save_folder'))
        upload_type = request.form.get('type', 'files')
        files_received = []
        
        if upload_type == 'message':
            message = request.form.get('message', '')
            if message:
                msg_folder = upload_folder / 'Messages'
                msg_folder.mkdir(exist_ok=True)
                
                letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                used = set()
                for file in msg_folder.glob('message_*.txt'):
                    if len(file.stem) > 8:
                        used.add(file.stem[8])
                
                selected = None
                for letter in letters:
                    if letter not in used:
                        selected = letter
                        break
                
                if not selected:
                    selected = 'Z'
                
                msg_file = msg_folder / f'message_{selected}.txt'
                with open(msg_file, 'w', encoding='utf-8') as f:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    f.write(f"[{timestamp}]\n{message}")
                
                files_received.append(f'message_{selected}.txt')
        
        elif upload_type == 'folder':
            folder_base = upload_folder / 'Folder_Uploads'
            folder_base.mkdir(exist_ok=True)
            
            folder_files = {}
            folder_name = None
            
            for key in request.files:
                if key.startswith('folder_files'):
                    file = request.files[key]
                    if file and file.filename:
                        file_path = file.filename
                        file_data = file.read()
                        path_parts = file_path.split('/')
                        if folder_name is None:
                            folder_name = path_parts[0]
                        folder_files[file_path] = file_data
            
            if folder_files:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                zip_name = f"{folder_name}_{timestamp}.zip" if folder_name else f"folder_{timestamp}.zip"
                zip_path = folder_base / zip_name
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for original, data in folder_files.items():
                        parts = original.split('/')
                        internal = '/'.join(parts[1:]) if len(parts) > 1 else original
                        zipf.writestr(internal, data)
                
                files_received.append(zip_name)
        
        else:
            for file in request.files.getlist('files'):
                if file and file.filename:
                    clean_name = re.sub(r'[<>:"/\\|?*]', '', file.filename)
                    ext = os.path.splitext(clean_name)[1].lower()
                    
                    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                        subfolder = 'Images'
                    elif ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv']:
                        subfolder = 'Videos'
                    elif ext in ['.mp3', '.wav', '.ogg', '.m4a']:
                        subfolder = 'Audio'
                    elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
                        subfolder = 'Archives'
                    elif ext in ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx']:
                        subfolder = 'Documents'
                    else:
                        subfolder = 'Others'
                    
                    category_folder = upload_folder / subfolder
                    category_folder.mkdir(exist_ok=True)
                    
                    filepath = category_folder / clean_name
                    counter = 1
                    while filepath.exists():
                        name, ext = os.path.splitext(clean_name)
                        filepath = category_folder / f"{name}_{counter}{ext}"
                        counter += 1
                    
                    file.save(filepath)
                    files_received.append(filepath.name)
        
        return jsonify({'success': True, 'count': len(files_received)})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/<user_id>/files')
def user_files(user_id):
    try:
        user_data = load_user(user_id)
        if not user_data:
            return jsonify({'categories': []}), 404
        
        upload_folder = Path(user_data.get('save_folder'))
        
        if not upload_folder.exists():
            return jsonify({'categories': []})
        
        categories = {
            'Images': [], 'Videos': [], 'Audio': [], 
            'Archives': [], 'Documents': [], 'Messages': [], 'Folder_Uploads': [], 'Others': []
        }
        
        for root, dirs, files in os.walk(upload_folder):
            for filename in files:
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, upload_folder)
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                ext = os.path.splitext(filename)[1].lower()
                can_preview = ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.pdf', '.txt']
                
                file_info = {
                    'name': filename,
                    'path': rel_path,
                    'size': f"{size_mb:.2f}",
                    'can_preview': can_preview
                }
                
                if filename.startswith('message_') and filename.endswith('.txt'):
                    categories['Messages'].append(file_info)
                elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                    categories['Images'].append(file_info)
                elif ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv']:
                    categories['Videos'].append(file_info)
                elif ext in ['.mp3', '.wav', '.ogg', '.m4a']:
                    categories['Audio'].append(file_info)
                elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
                    categories['Archives'].append(file_info)
                elif ext in ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx']:
                    categories['Documents'].append(file_info)
                elif 'Folder_Uploads' in root and ext == '.zip':
                    categories['Folder_Uploads'].append(file_info)
                else:
                    categories['Others'].append(file_info)
        
        for cat in categories:
            categories[cat].sort(key=lambda x: x['name'])
        
        categories_list = []
        category_order = ['Folder_Uploads', 'Images', 'Videos', 'Audio', 'Archives', 'Documents', 'Messages', 'Others']
        category_names = {
            'Folder_Uploads': '📦 Folder Uploads',
            'Images': '🖼️ Images',
            'Videos': '🎬 Videos',
            'Audio': '🎵 Audio',
            'Archives': '🗜️ Archives',
            'Documents': '📄 Documents',
            'Messages': '💬 Messages',
            'Others': '📁 Others'
        }
        
        for cat in category_order:
            if categories.get(cat):
                categories_list.append({
                    'name': category_names[cat],
                    'files': categories[cat]
                })
        
        return jsonify({'categories': categories_list})
        
    except Exception as e:
        return jsonify({'categories': []})

@app.route('/api/<user_id>/preview')
def user_preview(user_id):
    try:
        user_data = load_user(user_id)
        if not user_data:
            return 'User not found', 404
        
        file_path = request.args.get('file')
        upload_folder = Path(user_data.get('save_folder'))
        full_path = os.path.join(upload_folder, file_path)
        
        if not os.path.exists(full_path):
            return 'File not found', 404
        
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            return send_file(full_path, mimetype=f'image/{ext[1:]}')
        elif ext == '.pdf':
            return send_file(full_path, mimetype='application/pdf')
        elif ext == '.txt':
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read(), 200, {'Content-Type': 'text/plain; charset=utf-8'}
        else:
            return send_file(full_path, as_attachment=True)
        
    except Exception as e:
        return 'Error', 500

@app.route('/api/<user_id>/download')
def user_download(user_id):
    try:
        user_data = load_user(user_id)
        if not user_data:
            return 'User not found', 404
        
        file_path = request.args.get('file')
        upload_folder = Path(user_data.get('save_folder'))
        full_path = os.path.join(upload_folder, file_path)
        
        if not os.path.exists(full_path):
            return 'File not found', 404
        
        return send_file(full_path, as_attachment=True, download_name=os.path.basename(full_path))
        
    except Exception as e:
        return 'Error', 500

@app.route('/api/<user_id>/delete', methods=['POST'])
def user_delete(user_id):
    try:
        user_data = load_user(user_id)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        file_path = data.get('file')
        upload_folder = Path(user_data.get('save_folder'))
        full_path = os.path.join(upload_folder, file_path)
        
        if os.path.exists(full_path):
            os.remove(full_path)
            return jsonify({'success': True})
        
        return jsonify({'error': 'File not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/<user_id>/clear', methods=['POST'])
def user_clear(user_id):
    try:
        user_data = load_user(user_id)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
        
        upload_folder = Path(user_data.get('save_folder'))
        
        if upload_folder.exists():
            for item in upload_folder.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            
            categories = ['Images', 'Videos', 'Audio', 'Archives', 'Documents', 'Messages', 'Folder_Uploads', 'Others']
            for cat in categories:
                (upload_folder / cat).mkdir(exist_ok=True)
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/<user_id>/qr')
def user_qr(user_id):
    url = request.args.get('url', '')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({'qr_code': img_str})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)