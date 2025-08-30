import streamlit as st
import json
import uuid
import datetime
import base64
import pandas as pd
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import qrcode
import cv2
import numpy as np
import time
import math
import random
import os
import PyPDF2
import csv
import threading

# Page configuration
st.set_page_config(
    page_title="Aegis Vita Nexus",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# New color scheme - Deep Blue & Silver Medical Theme
st.markdown("""
<style>
    /* Main background with deep blue medical theme */
    .main {
        background: linear-gradient(135deg, #0a1929 0%, #122b4a 50%, #0a1929 100%);
        color: #e0e6ed;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Silver accents */
    .silver-accent {
        color: #c0c0c0;
        text-shadow: 0 0 5px rgba(192, 192, 192, 0.5);
    }
    
    /* Medical blue accents */
    .medical-blue {
        color: #1e90ff;
        text-shadow: 0 0 5px rgba(30, 144, 255, 0.5);
    }
    
    /* Luxury header with medical blue gradient */
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(90deg, #1e90ff, #87cefa, #1e90ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        letter-spacing: 2px;
        font-family: 'Arial', sans-serif;
        position: relative;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 25%;
        width: 50%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #1e90ff, transparent);
    }
    
    /* Sub-header styling */
    .sub-header {
        font-size: 2rem;
        background: linear-gradient(90deg, #e0e6ed, #87cefa, #e0e6ed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Luxury buttons with medical theme */
    .stButton button {
        border-radius: 8px;
        background: linear-gradient(135deg, #122b4a, #1e3b5a);
        color: #e0e6ed;
        border: 1px solid #1e90ff;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        font-family: 'Segoe UI', sans-serif;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 144, 255, 0.5);
        background: linear-gradient(135deg, #1e3b5a, #122b4a);
        color: #87cefa;
    }
    
    /* Luxury card styling with medical theme */
    .luxury-card {
        background: linear-gradient(145deg, #122b4a, #1e3b5a);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #2a4b6a;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
        position: relative;
        overflow: hidden;
    }
    
    .luxury-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0h100v100H0z' fill='%23122b4a'/%3E%3Cpath d='M0 0l100 100M100 0L0 100' stroke='%231e3b5a' stroke-width='1'/%3E%3C/svg%3E");
        opacity: 0.1;
        pointer-events: none;
    }
    
    /* New card style - Medical Professional Card */
    .professional-card {
        background: linear-gradient(145deg, #1c3b5a, #2a4b6a);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #1e90ff;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .professional-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0h100v100H0z' fill='%231c3b5a'/%3E%3Cpath d='M0 0l100 100M100 0L0 100' stroke='%232a4b6a' stroke-width='1'/%3E%3C/svg%3E");
        opacity: 0.1;
        pointer-events: none;
    }
    
    .professional-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(30, 144, 255, 0.4);
        border-left: 5px solid #87cefa;
    }
    
    /* Chat container */
    .chat-container {
        background: linear-gradient(145deg, #122b4a, #1e3b5a);
        border-radius: 12px;
        padding: 20px;
        height: 500px;
        overflow-y: auto;
        margin-bottom: 20px;
        border: 1px solid #2a4b6a;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
    }
    
    /* Message styling */
    .message {
        padding: 12px 18px;
        border-radius: 12px;
        margin-bottom: 15px;
        display: inline-block;
        max-width: 85%;
        position: relative;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        word-wrap: break-word;
        border: 1px solid rgba(30, 144, 255, 0.3);
    }
    
    .user-message {
        background: linear-gradient(135deg, #1e3b5a, #2a4b6a);
        margin-left: auto;
        margin-right: 0;
        text-align: right;
        color: #e0e6ed;
        border-bottom-right-radius: 5px;
        border: 1px solid #1e90ff;
    }
    
    .other-message {
        background: linear-gradient(135deg, #2a4b6a, #1e3b5a);
        color: #e0e6ed;
        border-bottom-left-radius: 5px;
        border: 1px solid #2a4b6a;
    }
    
    .priority-message {
        border: 2px solid #ff6b6b;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { border-color: #ff6b6b; }
        50% { border-color: #ff8e8e; }
        100% { border-color: #ff6b6b; }
    }
    
    .timestamp {
        font-size: 0.7rem;
        color: rgba(224, 230, 237, 0.6);
        margin-top: 5px;
        font-weight: 300;
    }
    
    /* ID Card styling */
    .id-card {
        background: linear-gradient(145deg, #122b4a, #1e3b5a);
        border-radius: 15px;
        padding: 25px;
        color: #e0e6ed;
        width: 400px;
        margin: 0 auto;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        border: 2px solid #2a4b6a;
        position: relative;
        overflow: hidden;
    }
    
    .id-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0h100v100H0z' fill='%23122b4a'/%3E%3Cpath d='M0 0l100 100M100 0L0 100' stroke='%231e3b5a' stroke-width='1'/%3E%3C/svg%3E");
        opacity: 0.1;
        pointer-events: none;
    }
    
    .id-card-header {
        text-align: center;
        margin-bottom: 20px;
        border-bottom: 1px solid #1e90ff;
        padding-bottom: 10px;
        position: relative;
        z-index: 1;
    }
    
    .id-card-photo {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 3px solid #1e90ff;
        margin: 0 auto 15px;
        object-fit: cover;
        box-shadow: 0 0 15px rgba(30, 144, 255, 0.5);
        position: relative;
        z-index: 1;
    }
    
    .id-card-field {
        margin-bottom: 12px;
        display: flex;
        border-bottom: 1px solid rgba(30, 144, 255, 0.2);
        padding-bottom: 8px;
        position: relative;
        z-index: 1;
    }
    
    .id-card-label {
        font-weight: bold;
        min-width: 120px;
        color: #1e90ff;
    }
    
    .id-card-value {
        font-weight: 500;
    }
    
    /* Scanner styling */
    .scanner-container {
        background: linear-gradient(145deg, #122b4a, #1e3b5a);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #2a4b6a;
        position: relative;
        overflow: hidden;
    }
    
    .scanner-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0h100v100H0z' fill='%23122b4a'/%3E%3Cpath d='M0 0l100 100M100 0L0 100' stroke='%231e3b5a' stroke-width='1'/%3E%3C/svg%3E");
        opacity: 0.1;
        pointer-events: none;
    }
    
    /* Verification status */
    .verification-success {
        background: linear-gradient(145deg, #122b4a, #1e3b5a);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        border: 2px solid #28a745;
        box-shadow: 0 8px 32px rgba(40, 167, 69, 0.3);
    }
    
    .verification-failed {
        background: linear-gradient(145deg, #122b4a, #1e3b5a);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        border: 2px solid #dc3545;
        box-shadow: 0 8px 32px rgba(220, 53, 69, 0.3);
    }
    
    /* Room card styling */
    .room-card {
        background: linear-gradient(145deg, #122b4a, #1e3b5a);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        border-left: 4px solid #1e90ff;
        color: #e0e6ed;
        transition: all 0.3s ease;
        border: 1px solid #2a4b6a;
        position: relative;
        overflow: hidden;
    }
    
    .room-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org2000/svg'%3E%3Cpath d='M0 0h100v100H0z' fill='%23122b4a'/%3E%3Cpath d='M0 0l100 100M100 0L0 100' stroke='%231e3b5a' stroke-width='1'/%3E%3C/svg%3E");
        opacity: 0.1;
        pointer-events: none;
    }
    
    .room-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 144, 255, 0.4);
        border-left: 4px solid #87cefa;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(145deg, #122b4a, #1e3b5a);
        border-radius: 8px 8px 0 0;
        border: 1px solid #2a4b6a;
        border-bottom: none;
        padding: 10px 20px;
        color: #e0e6ed;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(145deg, #1e3b5a, #2a4b6a);
        color: #1e90ff;
        border-bottom: 2px solid #1e90ff;
    }
    
    /* Selectbox styling */
    .stSelectbox [data-baseweb="select"] {
        background: linear-gradient(145deg, #122b4a, #1e3b5a);
        border: 1px solid #2a4b6a;
        color: #e0e6ed;
        border-radius: 8px;
    }
    
    /* Text input styling */
    .stTextInput input {
        background: linear-gradient(145deg, #122b4a, #1e3b5a);
        border: 1px solid #2a4b6a;
        color: #e0e6ed;
        border-radius: 8px;
    }
    
    /* Camera permission popup */
    .camera-permission-popup {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(145deg, #1e3b5a, #2a4b6a);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7);
        z-index: 1000;
        border: 2px solid #1e90ff;
        width: 80%;
        max-width: 500px;
        text-align: center;
    }
    
    .camera-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(10, 25, 41, 0.9);
        z-index: 999;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem !important;
        }
        
        .sub-header {
            font-size: 1.5rem !important;
        }
        
        .chat-container {
            height: 400px !important;
        }
        
        .id-card {
            width: 100% !important;
            max-width: 350px !important;
        }
        
        .stButton button {
            padding: 8px 16px !important;
            font-size: 0.9rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Database file path
DB_FILE = "aegis_data.json"

# Initialize session state with database loading
def load_database():
    """Load data from JSON database file"""
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        else:
            return {
                'users': {},
                'rooms': {},
                'messages': {},
                'files': {},
                'admin_password': "admin123",
                'user_status': {},
                'id_cards': {},
                'interns': {},
                'mentors': {},
                'tasks': {},
                'backup_data': None
            }
    except Exception as e:
        st.error(f"Error loading database: {str(e)}")
        return {
            'users': {},
            'rooms': {},
            'messages': {},
            'files': {},
            'admin_password': "admin123",
            'user_status': {},
            'id_cards': {},
            'interns': {},
            'mentors': {},
            'tasks': {},
            'backup_data': None
        }

def save_database():
    """Save data to JSON database file"""
    try:
        data = {
            'users': st.session_state.users,
            'rooms': st.session_state.rooms,
            'messages': st.session_state.messages,
            'files': st.session_state.files,
            'admin_password': st.session_state.admin_password,
            'user_status': st.session_state.user_status,
            'id_cards': st.session_state.id_cards,
            'interns': st.session_state.interns,
            'mentors': st.session_state.mentors,
            'tasks': st.session_state.tasks,
            'backup_data': st.session_state.backup_data
        }
        
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving database: {str(e)}")
        return False

# Initialize session state from database
if 'initialized' not in st.session_state:
    db_data = load_database()
    
    # Initialize all session state variables
    if 'users' not in st.session_state:
        st.session_state.users = db_data.get('users', {})
    if 'rooms' not in st.session_state:
        st.session_state.rooms = db_data.get('rooms', {})
    if 'messages' not in st.session_state:
        st.session_state.messages = db_data.get('messages', {})
    if 'files' not in st.session_state:
        st.session_state.files = db_data.get('files', {})
    if 'admin_password' not in st.session_state:
        st.session_state.admin_password = db_data.get('admin_password', "admin123")
    if 'user_status' not in st.session_state:
        st.session_state.user_status = db_data.get('user_status', {})
    if 'id_cards' not in st.session_state:
        st.session_state.id_cards = db_data.get('id_cards', {})
    if 'interns' not in st.session_state:
        st.session_state.interns = db_data.get('interns', {})
    if 'mentors' not in st.session_state:
        st.session_state.mentors = db_data.get('mentors', {})
    if 'tasks' not in st.session_state:
        st.session_state.tasks = db_data.get('tasks', {})
    if 'backup_data' not in st.session_state:
        st.session_state.backup_data = db_data.get('backup_data', None)
    
    # Initialize other session state variables
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'qr_verified' not in st.session_state:
        st.session_state.qr_verified = False
    if 'qr_scanned_data' not in st.session_state:
        st.session_state.qr_scanned_data = None
    if 'show_qr_scanner' not in st.session_state:
        st.session_state.show_qr_scanner = False
    if 'current_room' not in st.session_state:
        st.session_state.current_room = None
    if 'show_admin_panel' not in st.session_state:
        st.session_state.show_admin_panel = False
    if 'show_id_card' not in st.session_state:
        st.session_state.show_id_card = False
    if 'auto_scan_enabled' not in st.session_state:
        st.session_state.auto_scan_enabled = True
    if 'last_scan_time' not in st.session_state:
        st.session_state.last_scan_time = 0
    if 'show_intern_management' not in st.session_state:
        st.session_state.show_intern_management = False
    if 'camera_active' not in st.session_state:
        st.session_state.camera_active = False
    if 'scanning_status' not in st.session_state:
        st.session_state.scanning_status = "Waiting for camera..."
    if 'camera_permission_granted' not in st.session_state:
        st.session_state.camera_permission_granted = False
    if 'camera_permission_requested' not in st.session_state:
        st.session_state.camera_permission_requested = False
    if 'show_camera_popup' not in st.session_state:
        st.session_state.show_camera_popup = False
    
    st.session_state.initialized = True

# Utility functions
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create a QR code with medical blue color on dark background
    img = qr.make_image(fill_color="#1e90ff", back_color="#0a1929")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')
    
def create_user(username, password, full_name="", specialty="", role="", department="", photo=None, access_level="Standard", is_intern=False, mentor=None):
    if username in st.session_state.users:
        return False, "Username already exists"
    
    # Handle photo
    photo_data = None
    if photo is not None:
        photo_data = base64.b64encode(photo.getvalue()).decode('utf-8')
    
    # Generate unique staff ID
    prefix = "INT" if is_intern else "AVN"
    staff_id = f"{prefix}-{datetime.datetime.now().strftime('%Y%m')}-{len(st.session_state.users):03d}"
    
    # Generate QR code
    qr_code = generate_qr_code(staff_id)
    
    st.session_state.users[username] = {
        'password': password,
        'full_name': full_name,
        'specialty': specialty,
        'role': role,
        'department': department,
        'photo': photo_data,
        'staff_id': staff_id,
        'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'qr_code': qr_code,
        'last_login': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'access_level': access_level,
        'status': 'active',
        'is_intern': is_intern,
        'mentor': mentor
    }
    
    st.session_state.user_status[username] = "online"
    
    # Add to interns if applicable
    if is_intern:
        st.session_state.interns[username] = {
            'mentor': mentor,
            'start_date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'performance_rating': 0,
            'completed_tasks': 0,
            'assigned_tasks': []
        }
        
        if mentor and mentor in st.session_state.users:
            if mentor not in st.session_state.mentors:
                st.session_state.mentors[mentor] = []
            st.session_state.mentors[mentor].append(username)
    
    # Generate ID card
    generate_id_card(username)
    
    # Save to database
    save_database()
    
    return True, "User created successfully"

def generate_id_card(username):
    if username not in st.session_state.users:
        return False
    
    user_data = st.session_state.users[username]
    
    # Create portrait ID card image with medical design
    width, height = 600, 800  # Portrait dimensions
    img = Image.new('RGB', (width, height), color=(10, 25, 41))
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to load fonts
        try:
            title_font = ImageFont.truetype("arial.ttf", 28)
            header_font = ImageFont.truetype("arial.ttf", 20)
            normal_font = ImageFont.truetype("arial.ttf", 16)
            small_font = ImageFont.truetype("arial.ttf", 12)
        except:
            # Use default font if custom fonts not available
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Draw medical header with blue gradient
        for i in range(width):
            r = int(10 + (30-10) * i / width)
            g = int(25 + (144-25) * i / width)
            b = int(41 + (255-41) * i / width)
            draw.line([(i, 0), (i, 150)], fill=(r, g, b))
        
        # Add text with shadow effect
        draw.text((width//2+2, 40), "AEGIS VITA NEXUS", fill=(0, 0, 0), font=title_font, anchor="mm")
        draw.text((width//2, 38), "AEGIS VITA NEXUS", fill=(30, 144, 255), font=title_font, anchor="mm")
        
        draw.text((width//2+1, 80), "BIOMEDICAL EXCELLENCE NETWORK", fill=(0, 0, 0), font=header_font, anchor="mm")
        draw.text((width//2, 78), "BIOMEDICAL EXCELLENCE NETWORK", fill=(255, 255, 255), font=header_font, anchor="mm")
        
        # Draw blue accent line
        draw.line([(0, 150), (width, 150)], fill=(30, 144, 255), width=3)
        
        # Draw photo area
        photo_size = 180
        photo_x = (width - photo_size) // 2
        photo_y = 180
        draw.rectangle([photo_x-5, photo_y-5, photo_x+photo_size+5, photo_y+photo_size+5], 
                      fill=(40, 40, 40), outline=(30, 144, 255), width=2)
        
        if user_data.get('photo'):
            try:
                photo_data = base64.b64decode(user_data['photo'])
                photo = Image.open(BytesIO(photo_data))
                photo = photo.resize((photo_size, photo_size))
                img.paste(photo, (photo_x, photo_y))
            except:
                draw.text((width//2, photo_y+photo_size//2), "PHOTO", fill=(100, 100, 100), font=normal_font, anchor="mm")
        else:
            draw.text((width//2, photo_y+photo_size//2), "PHOTO", fill=(100, 100, 100), font=normal_font, anchor="mm")
        
        # Draw user info
        y_position = photo_y + photo_size + 30
        info = [
            ("Name:", user_data.get('full_name', username)),
            ("Staff ID:", user_data.get('staff_id', '')),
            ("Role:", user_data.get('role', 'Healthcare Professional')),
            ("Specialty:", user_data.get('specialty', 'Not specified')),
            ("Department:", user_data.get('department', 'Not specified')),
            ("Access Level:", user_data.get('access_level', 'Standard'))
        ]
        
        if user_data.get('is_intern', False):
            info.append(("Status:", "Intern"))
            if user_data.get('mentor'):
                info.append(("Mentor:", user_data.get('mentor')))
        
        for label, value in info:
            draw.text((50, y_position), label, fill=(30, 144, 255), font=normal_font)
            draw.text((200, y_position), value, fill=(255, 255, 255), font=normal_font)
            y_position += 30
        
        # Draw QR code
        if user_data.get('qr_code'):
            try:
                qr_data = base64.b64decode(user_data['qr_code'])
                qr_img = Image.open(BytesIO(qr_data))
                qr_img = qr_img.resize((150, 150))
                
                # Position QR code at bottom left
                qr_x = 50
                qr_y = height - 200
                draw.rectangle([qr_x-10, qr_y-10, qr_x+160, qr_y+160], fill=(30, 30, 30), outline=(30, 144, 255), width=2)
                img.paste(qr_img, (qr_x, qr_y))
                
                # Add text below QR code
                draw.text((qr_x+75, qr_y+160), "QR Code", fill=(255, 255, 255), font=small_font, anchor="mm")
            except Exception as e:
                st.error(f"Error with QR code: {str(e)}")
        
        # Convert to bytes
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        
        st.session_state.id_cards[username] = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        # Save to database
        save_database()
        
        return True
    except Exception as e:
        st.error(f"Error generating ID card: {str(e)}")
        return False

def create_room(room_name, room_type, password=None, description="", room_category="General", access_level="All"):
    if room_name in st.session_state.rooms:
        return False, "Room already exists"
    
    st.session_state.rooms[room_name] = {
        'type': room_type,
        'password': password,
        'created_by': st.session_state.current_user,
        'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'members': [st.session_state.current_user],
        'description': description,
        'category': room_category,
        'access_level': access_level
    }
    st.session_state.messages[room_name] = []
    st.session_state.files[room_name] = []
    
    # Save to database
    save_database()
    
    return True, f"{room_type.capitalize()} room created successfully"

def send_message(room, message, file=None, priority=False, message_type="text"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    message_data = {
        'id': str(uuid.uuid4()),
        'sender': st.session_state.current_user,
        'message': message,
        'timestamp': timestamp,
        'priority': priority,
        'type': message_type
    }
    
    if file is not None:
        file_content = base64.b64encode(file.getvalue()).decode('utf-8')
        
        message_data['file'] = {
            'name': file.name,
            'type': file.type,
            'size': file.size,
            'content': file_content,
            'preview': f"File: {file.name} ({file.size} bytes)"  # Simple preview without reading content
        }
        st.session_state.files[room].append(message_data['file'])
    
    st.session_state.messages[room].append(message_data)
    
    # Save to database
    save_database()
    
    return True

# Enhanced QR Code Scanner Component with automatic detection
class QRScanner:
    def __init__(self):
        self.scanned_data = None
        self.last_scan_time = 0
        self.scan_interval = 0.3  # Faster scanning for better responsiveness
        self.failed_attempts = 0
        self.max_failed_attempts = 5
        self.last_frame = None
        self.is_scanning = False
    
    def enhance_image(self, image):
        """Enhance image for better QR code detection"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply histogram equalization to improve contrast
            equalized = cv2.equalizeHist(gray)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(equalized, (5, 5), 0)
            
            # Apply adaptive thresholding to handle different lighting conditions
            thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                          cv2.THRESH_BINARY, 11, 2)
            
            return thresh
        except Exception as e:
            return image
        
    def scan_qr_code(self, image):
        try:
            current_time = time.time()
            # Only scan if enough time has passed since last scan
            if current_time - self.last_scan_time < self.scan_interval:
                return False, None
                
            self.last_frame = image
            self.is_scanning = True
                
            # Enhance the image for better detection
            enhanced = self.enhance_image(image)
            
            # Initialize the QRCode detector
            detector = cv2.QRCodeDetector()
            
            # Detect and decode the QR code with enhanced image
            data, vertices_array, _ = detector.detectAndDecode(enhanced)
            
            # If not detected with enhanced image, try with original
            if vertices_array is None or not data:
                data, vertices_array, _ = detector.detectAndDecode(image)
            
            # Try different preprocessing techniques if still not detected
            if vertices_array is None or not data:
                # Try with different thresholding
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                _, thresh_binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                data, vertices_array, _ = detector.detectAndDecode(thresh_binary)
            
            if vertices_array is not None and data:
                self.scanned_data = data
                self.last_scan_time = current_time
                self.failed_attempts = 0  # Reset failed attempts on success
                self.is_scanning = False
                return True, data
            else:
                self.failed_attempts += 1
                self.is_scanning = False
                return False, None
        except Exception as e:
            self.failed_attempts += 1
            self.is_scanning = False
            return False, str(e)
    
    def should_show_manual_option(self):
        """Determine if manual entry option should be shown"""
        return self.failed_attempts >= self.max_failed_attempts

# Backup and Restore Functions
def create_backup():
    """Create a complete backup of all application data"""
    backup_data = {
        'users': st.session_state.users,
        'rooms': st.session_state.rooms,
        'messages': st.session_state.messages,
        'files': st.session_state.files,
        'admin_password': st.session_state.admin_password,
        'user_status': st.session_state.user_status,
        'id_cards': st.session_state.id_cards,
        'interns': st.session_state.interns,
        'mentors': st.session_state.mentors,
        'tasks': st.session_state.tasks,
        'backup_timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'version': '2.0'
    }
    
    # Convert to JSON string
    backup_json = json.dumps(backup_data, indent=2)
    return backup_json

def restore_backup(backup_file):
    """Restore application data from a backup file"""
    try:
        backup_data = json.load(backup_file)
        
        # Validate backup file
        if 'users' not in backup_data or 'version' not in backup_data:
            return False, "Invalid backup file format"
        
        # Restore all data
        st.session_state.users = backup_data['users']
        st.session_state.rooms = backup_data['rooms']
        st.session_state.messages = backup_data['messages']
        st.session_state.files = backup_data['files']
        st.session_state.admin_password = backup_data['admin_password']
        st.session_state.user_status = backup_data['user_status']
        st.session_state.id_cards = backup_data['id_cards']
        st.session_state.interns = backup_data['interns']
        st.session_state.mentors = backup_data['mentors']
        st.session_state.tasks = backup_data['tasks']
        
        # Save to database
        save_database()
        
        return True, f"Backup restored successfully from {backup_data.get('backup_timestamp', 'unknown time')}"
    
    except Exception as e:
        return False, f"Error restoring backup: {str(e)}"

def render_camera_permission_popup():
    """Render a popup to request camera permissions"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="camera-permission-popup">
            <h2 style="color: #1e90ff; margin-bottom: 20px;">📷 Camera Access Required</h2>
            <p style="margin-bottom: 25px;">Aegis Vita Nexus needs access to your camera for QR code verification.</p>
            <p style="margin-bottom: 30px; color: #87cefa;">Please allow camera access when prompted by your browser.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("I've Granted Access", use_container_width=True):
                st.session_state.show_camera_popup = False
                st.rerun()
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_camera_popup = False
                st.session_state.show_qr_scanner = False
                st.session_state.current_user = None
                st.rerun()

def render_login():
    st.markdown('<h1 class="main-header">AEGIS VITA NEXUS</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Biomedical Collaboration Platform</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form", clear_on_submit=True):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            login_btn = st.form_submit_button("Login", use_container_width=True)
            
            if login_btn:
                if username == "admin" and password == st.session_state.admin_password:
                    st.session_state.current_user = "admin"
                    st.session_state.qr_verified = True  # Admin doesn't need QR verification
                    st.rerun()
                elif username in st.session_state.users and st.session_state.users[username]['password'] == password:
                    if st.session_state.users[username].get('status') == 'suspended':
                        st.error("Your account has been suspended. Please contact administrator.")
                    else:
                        st.session_state.current_user = username
                        st.session_state.users[username]['last_login'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state.qr_verified = False
                        st.session_state.show_qr_scanner = True
                        st.session_state.show_camera_popup = True
                        
                        # Save to database
                        save_database()
                        
                        st.rerun()
                else:
                    st.error("Invalid username or password")
    
    # Admin creation (first time setup)
    if "admin" not in st.session_state.users:
        st.markdown("---")
        st.markdown("### First Time Setup")
        st.info("No admin account found. Please set up the admin account.")
        
        with st.form("admin_setup"):
            admin_password = st.text_input("Admin Password", type="password")
            confirm_password = st.text_input("Confirm Admin Password", type="password")
            setup_btn = st.form_submit_button("Setup Admin Account", use_container_width=True)
            
            if setup_btn:
                if admin_password and admin_password == confirm_password:
                    st.session_state.admin_password = admin_password
                    st.session_state.users["admin"] = {
                        'password': admin_password,
                        'full_name': "System Administrator",
                        'specialty': "System Administration",
                        'role': "Administrator",
                        'department': "IT",
                        'staff_id': "ADMIN-001",
                        'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'qr_code': generate_qr_code("ADMIN-001"),
                        'access_level': "Admin",
                        'status': 'active',
                        'is_intern': False
                    }
                    
                    # Save to database
                    save_database()
                    
                    st.success("Admin account created successfully. Please login.")
                    st.rerun()
                else:
                    st.error("Passwords do not match")

def render_qr_verification():
    st.markdown('<h2 class="sub-header">QR Code Verification</h2>', unsafe_allow_html=True)
    
    if st.session_state.current_user in st.session_state.users:
        user_data = st.session_state.users[st.session_state.current_user]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Your Verification Status")
            st.info("Your QR code is registered in the system. Please present it to the camera for verification.")
            
            # Don't show the actual QR code or staff ID
            st.markdown("""
            <div style="text-align: center; padding: 20px; background: #122b4a; border-radius: 10px; border: 1px solid #1e90ff;">
                <div style="font-size: 48px;">🔒</div>
                <h3>Secure QR Code</h3>
                <p>Your verification code is securely stored in the system.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Tips for better scanning
            st.markdown("### 📝 Scanning Tips")
            st.info("""
            - Ensure good lighting
            - Avoid reflections on screen
            - Hold device steady
            - Position QR code within the frame
            - If scanning fails, use manual entry option below
            """)
        
        with col2:
            st.markdown("### Verify Your Identity")
            st.info("Position your QR code in front of the camera. The system will automatically detect and verify it.")
            
            # Initialize scanner in session state if not exists
            if 'qr_scanner_obj' not in st.session_state:
                st.session_state.qr_scanner_obj = QRScanner()
            
            scanner = st.session_state.qr_scanner_obj
            
            # Camera input for QR scanning - automatically processes without button click
            camera_img = st.camera_input("Scan your QR code", key="qr_scanner", label_visibility="collapsed",
                                       help="Position your QR code in the camera view. Scanning is automatic.")

            # Display scanning status
            status_placeholder = st.empty()
            
            if camera_img is not None:
                # Process the image
                img = Image.open(camera_img)
                img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                
                # Update scanning status
                if scanner.is_scanning:
                    status_placeholder.info("🔍 Scanning QR code...")
                else:
                    status_placeholder.info("📷 Camera active - position your QR code")
                
                # Scan for QR code
                success, data = scanner.scan_qr_code(img_cv)
                
                if success:
                    st.session_state.qr_scanned_data = data
                    # Check if the QR code matches the user's staff ID
                    if data == user_data.get('staff_id', ''):
                        st.session_state.qr_verified = True
                        status_placeholder.success("✅ Verification successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        status_placeholder.error("❌ Verification failed. The scanned QR code does not match your account.")
                else:
                    # Show scanning status
                    if scanner.failed_attempts > 0:
                        status_placeholder.info(f"🔍 Scanning... (Attempt {scanner.failed_attempts})")
                    
                    # Show manual entry option if scanning fails multiple times
                    if scanner.should_show_manual_option():
                        status_placeholder.warning("QR scanning seems difficult. Please try manual entry below.")
            
            # Manual entry option (always visible but emphasized after failed attempts)
            st.markdown("---")
            st.markdown("### 🔢 Manual Verification")
            
            if scanner.should_show_manual_option():
                st.warning("Having trouble with QR scanning? Enter your AVN ID manually:")
            else:
                st.info("Alternatively, enter your AVN ID manually:")
            
            manual_id = st.text_input("Enter your AVN ID", placeholder="e.g., AVN-202405-001", key="manual_id_input")
            if st.button("Verify Manually", use_container_width=True, type="secondary", key="manual_verify_btn"):
                if manual_id:
                    if manual_id == user_data.get('staff_id', ''):
                        st.session_state.qr_verified = True
                        st.success("✅ Manual verification successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid AVN ID. Please check and try again.")
                else:
                    st.error("Please enter your AVN ID")
    
    # Show camera permission popup if needed
    if st.session_state.show_camera_popup:
        render_camera_permission_popup()

def render_sidebar():
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.current_user}")
        
        if st.session_state.current_user in st.session_state.users:
            user_data = st.session_state.users[st.session_state.current_user]
            st.caption(f"{user_data.get('role', 'User')} • {user_data.get('department', '')}")
        
        # User status
        status = st.selectbox(
            "Status",
            ["online", "away", "busy", "offline"],
            index=["online", "away", "busy", "offline"].index(st.session_state.user_status.get(st.session_state.current_user, "online"))
        )
        st.session_state.user_status[st.session_state.current_user] = status
        
        # Save to database
        save_database()
        
        st.markdown("---")
        st.markdown("### 🏠 Rooms")
        
        # Create new room
        with st.expander("Create New Room"):
            with st.form("create_room_form"):
                room_name = st.text_input("Room Name")
                room_type = st.selectbox("Room Type", ["public", "private"])
                room_password = None
                if room_type == "private":
                    room_password = st.text_input("Room Password", type="password")
                
                room_description = st.text_input("Room Description")
                room_category = st.selectbox("Category", ["General", "Cardiology", "Neurology", "Research", "Administration", "Emergency", "Internship"])
                access_level = st.selectbox("Access Level", ["All", "Doctors Only", "Researchers Only", "Administrators Only", "Interns Only"])
                
                create_room_btn = st.form_submit_button("Create Room", use_container_width=True)
                
                if create_room_btn and room_name:
                    success, message = create_room(room_name, room_type, room_password, room_description, room_category, access_level)
                    if success:
                        st.success(message)
                        st.session_state.current_room = room_name
                        st.rerun()
                    else:
                        st.error(message)
        
        # List available rooms
        st.markdown("**Available Rooms:**")
        for room_name, room_data in st.session_state.rooms.items():
            # Check access level
            user_access = st.session_state.users[st.session_state.current_user].get('access_level', 'Standard')
            room_access = room_data.get('access_level', 'All')
            is_intern = st.session_state.users[st.session_state.current_user].get('is_intern', False)
            
            access_granted = False
            if room_access == "All":
                access_granted = True
            elif room_access == "Doctors Only" and user_access in ["Doctor", "Admin"]:
                access_granted = True
            elif room_access == "Researchers Only" and user_access in ["Researcher", "Admin"]:
                access_granted = True
            elif room_access == "Administrators Only" and user_access == "Admin":
                access_granted = True
            elif room_access == "Interns Only" and is_intern:
                access_granted = True
            
            if access_granted and (st.session_state.current_user in room_data['members'] or room_data['type'] == 'public'):
                room_btn = st.button(
                    f"{'🔒' if room_data['type'] == 'private' else '🌐'} {room_name} ({len(room_data['members'])} members)",
                    key=f"room_{room_name}",
                    use_container_width=True
                )
                
                if room_btn:
                    # Check if password is required
                    if room_data['type'] == 'private' and st.session_state.current_user not in room_data['members']:
                        password = st.text_input(f"Enter password for {room_name}", type="password", key=f"pwd_{room_name}")
                        if password == room_data['password']:
                            room_data['members'].append(st.session_state.current_user)
                            st.session_state.current_room = room_name
                            
                            # Save to database
                            save_database()
                            
                            st.rerun()
                        elif password:
                            st.error("Incorrect password")
                    else:
                        st.session_state.current_room = room_name
                        st.rerun()
        
        st.markdown("---")
        
        # View ID Card
        if st.button("🪪 View My ID Card", use_container_width=True):
            st.session_state.show_id_card = True
            st.rerun()
        
        # Intern Management (for mentors and admins)
        user_data = st.session_state.users.get(st.session_state.current_user, {})
        is_mentor = st.session_state.current_user in st.session_state.mentors
        is_admin = st.session_state.current_user == "admin"
        
        if (is_mentor or is_admin) and st.session_state.current_user not in st.session_state.interns:
            if st.button("👨‍🏫 Intern Management", use_container_width=True):
                st.session_state.show_intern_management = True
                st.rerun()
        
        # Admin panel access
        if st.session_state.current_user == "admin":
            if st.button("👑 Admin Panel", use_container_width=True):
                st.session_state.show_admin_panel = True
                st.rerun()
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.current_user = None
            st.session_state.current_room = None
            st.session_state.qr_verified = False
            st.session_state.camera_active = False
            st.rerun()

def render_chat_interface():
    if 'current_room' not in st.session_state or st.session_state.current_room is None:
        st.info("Please select a room from the sidebar to start chatting")
        return
    
    room_name = st.session_state.current_room
    room_data = st.session_state.rooms[room_name]
    
    # Room header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f"### 💬 {room_name}")
        st.caption(f"{room_data['type'].capitalize()} room • {len(room_data['members'])} members • {room_data.get('category', 'General')}")
        if room_data.get('description'):
            st.caption(f"Description: {room_data['description']}")
    
    with col2:
        if st.button("👥 Members", use_container_width=True):
            # Show room members
            with st.expander("Room Members"):
                for member in room_data['members']:
                    status = st.session_state.user_status.get(member, "offline")
                    status_color = {
                        "online": "🟢",
                        "away": "🟡",
                        "busy": "🔴",
                        "offline": "⚫"
                    }
                    st.write(f"{status_color[status]} {member}")
    
    with col3:
        if st.button("Leave Room", use_container_width=True):
            if st.session_state.current_user in room_data['members']:
                room_data['members'].remove(st.session_state.current_user)
                st.session_state.current_room = None
                
                # Save to database
                save_database()
                
                st.rerun()
    
    # Chat messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if room_name in st.session_state.messages:
        for msg in st.session_state.messages[room_name]:
            message_class = "user-message" if msg['sender'] == st.session_state.current_user else "other-message"
            if msg['priority']:
                message_class += " priority-message"
            
            message_html = f"""
            <div class="message {message_class}">
                <strong>{msg['sender']}</strong><br>
                {msg['message']}
                <div class="timestamp">{msg['timestamp']}</div>
            </div>
            """
            
            if 'file' in msg:
                file = msg['file']
                file_size_kb = file['size'] / 1024
                file_icon = "📄"  # Default icon
                
                # Different icons for different file types
                if file['type'].startswith('image/'):
                    file_icon = "🖼️"
                elif file['type'] in ['application/pdf']:
                    file_icon = "📕"
                elif file['type'] in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
                    file_icon = "📝"
                elif file['type'] in ['text/csv', 'application/vnd.ms-excel']:
                    file_icon = "📊"
                elif file['type'].startswith('audio/'):
                    file_icon = "🎵"
                elif file['type'].startswith('video/'):
                    file_icon = "🎬"
                elif file['type'] in ['application/zip', 'application/x-zip-compressed']:
                    file_icon = "📦"
                
                message_html += f"""
                <div class="message {message_class}">
                    <strong>{file_icon} Attachment:</strong> {file['name']} ({file_size_kb:.1f} KB)<br>
                    <a href="data:{file['type']};base64,{file['content']}" download="{file['name']}">Download File</a>
                </div>
                """
            
            st.markdown(message_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Message input with advanced options
    with st.form("message_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            message = st.text_input("Type your message", label_visibility="collapsed", placeholder="Type your message here...")
        with col2:
            priority = st.checkbox("Priority", help="Send as priority message")
        with col3:
            send_btn = st.form_submit_button("Send", use_container_width=True)
        
        if send_btn and message:
            send_message(room_name, message, priority=priority)
            st.rerun()
    
    # Enhanced file upload with more types
    uploaded_file = st.file_uploader("Upload file", type=[
        "pdf", "docx", "txt", "jpg", "png", "jpeg", "xlsx", "csv", 
        "pptx", "zip", "mp3", "mp4", "wav", "mov", "avi"
    ], help="Supported formats: PDF, Word, Text, Images, Excel, CSV, PowerPoint, ZIP, Audio, Video")
    
    if uploaded_file is not None:
        send_message(room_name, f"Shared file: {uploaded_file.name}", file=uploaded_file)
        st.rerun()

def render_admin_panel():
    st.markdown("### 👑 Admin Panel")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["User Management", "System Settings", "ID Card Management", "Intern Management", "Backup & Restore"])
    
    with tab1:
        st.write("Registered Users:")
        
        # User table
        user_data = []
        for username, user_info in st.session_state.users.items():
            user_data.append({
                'Username': username,
                'Full Name': user_info.get('full_name', ''),
                'Specialty': user_info.get('specialty', ''),
                'Role': user_info.get('role', ''),
                'Staff ID': user_info.get('staff_id', ''),
                'Access Level': user_info.get('access_level', 'Standard'),
                'Status': user_info.get('status', 'active'),
                'Is Intern': user_info.get('is_intern', False),
                'Last Login': user_info.get('last_login', 'Never')
            })
        
        if user_data:
            df = pd.DataFrame(user_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No users registered yet")
            
        # Create user section
        st.subheader("Create New User")
        with st.form("create_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input("Username*")
                new_password = st.text_input("Password*", type="password")
                confirm_password = st.text_input("Confirm Password*", type="password")
                access_level = st.selectbox("Access Level*", ["Standard", "Doctor", "Researcher", "Administrator"])
                is_intern = st.checkbox("Is Intern")
                
            with col2:
                full_name = st.text_input("Full Name*")
                specialty = st.selectbox("Specialty*", [
                    "Cardiology", "Neurology", "Oncology", "Pediatrics", 
                    "Surgery", "Radiology", "Pathology", "Biotech Research",
                    "Pharmacology", "Genetics", "Immunology", "Other"
                ])
                role = st.selectbox("Role*", ["Doctor", "Researcher", "Nurse", "Technician", "Administrator", "Intern"])
                department = st.text_input("Department")
                
                # Mentor selection for interns
                mentor = None
                if is_intern:
                    mentor_options = [u for u in st.session_state.users.keys() 
                                    if not st.session_state.users[u].get('is_intern', False) and u != "admin"]
                    mentor = st.selectbox("Assign Mentor", [""] + mentor_options)
                
                photo = st.file_uploader("Upload Photo", type=["png", "jpg", "jpeg"])
            
            create_user_btn = st.form_submit_button("Create User", use_container_width=True)
            
            if create_user_btn:
                if new_username and new_password and full_name and specialty and role:
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        success, message = create_user(
                            new_username, new_password, full_name, specialty, role, 
                            department, photo, access_level, is_intern, mentor
                        )
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                else:
                    st.error("Please fill all required fields (*)")
        
        # User management section
        st.subheader("User Management")
        user_to_manage = st.selectbox("Select user to manage", 
                                    [""] + [u for u in st.session_state.users.keys()])
        
        if user_to_manage:
            user_info = st.session_state.users[user_to_manage]
            
            col1, col2 = st.columns(2)
            
            with col1:
                new_status = st.selectbox("Status", ["active", "suspended"], 
                                        index=0 if user_info.get('status') == 'active' else 1)
                
            with col2:
                new_access = st.selectbox("Access Level", ["Standard", "Doctor", "Researcher", "Administrator"],
                                        index=["Standard", "Doctor", "Researchers", "Administrator"].index(
                                            user_info.get('access_level', 'Standard')))
            
            if st.button("Update User", use_container_width=True):
                st.session_state.users[user_to_manage]['status'] = new_status
                st.session_state.users[user_to_manage]['access_level'] = new_access
                
                # Save to database
                save_database()
                
                st.success(f"User {user_to_manage} updated successfully")
                st.rerun()
            
            if st.button("Delete User", type="primary"):
                if user_to_manage in st.session_state.users:
                    del st.session_state.users[user_to_manage]
                    if user_to_manage in st.session_state.id_cards:
                        del st.session_state.id_cards[user_to_manage]
                    
                    # Save to database
                    save_database()
                    
                    st.success(f"User {user_to_manage} deleted successfully")
                    st.rerun()
    
    with tab2:
        st.markdown("#### ⚙️ System Settings")
        
        st.subheader("Security Settings")
        new_admin_password = st.text_input("Change Admin Password", type="password")
        confirm_admin_password = st.text_input("Confirm New Admin Password", type="password")
        
        if st.button("Update Admin Password", use_container_width=True):
            if new_admin_password and new_admin_password == confirm_admin_password:
                st.session_state.admin_password = new_admin_password
                st.session_state.users["admin"]["password"] = new_admin_password
                
                # Save to database
                save_database()
                
                st.success("Admin password updated successfully")
            else:
                st.error("Passwords do not match")
        
        st.subheader("QR Code Settings")
        st.session_state.auto_scan_enabled = st.checkbox("Enable Auto QR Code Scanning", value=st.session_state.auto_scan_enabled)
        
        st.subheader("System Information")
        st.info(f"**Total Users:** {len(st.session_state.users)}")
        st.info(f"**Total Rooms:** {len(st.session_state.rooms)}")
        total_messages = sum(len(messages) for messages in st.session_state.messages.values())
        st.info(f"**Total Messages:** {total_messages}")
        total_files = sum(len(files) for files in st.session_state.files.values())
        st.info(f"**Total Files:** {total_files}")
        st.info(f"**System Version:** 2.0")
        
        if st.button("Back to Chat", use_container_width=True):
            st.session_state.show_admin_panel = False
            st.rerun()
    
    with tab3:
        st.markdown("#### 🪪 ID Card Management")
        
        # Generate ID cards for all users
        if st.button("Generate All ID Cards", use_container_width=True):
            with st.spinner("Generating ID cards for all users..."):
                for username in st.session_state.users.keys():
                    generate_id_card(username)
                st.success("All ID cards generated successfully!")
        
        # View specific user's ID card
        user_to_view = st.selectbox("Select user to view ID card", 
                                  [""] + [u for u in st.session_state.users.keys()])
        
        if user_to_view and user_to_view in st.session_state.id_cards:
            st.image(BytesIO(base64.b64decode(st.session_state.id_cards[user_to_view])), use_column_width=True)
            
            # Download button
            buf = BytesIO(base64.b64decode(st.session_state.id_cards[user_to_view]))
            st.download_button(
                label=f"Download {user_to_view}'s ID Card",
                data=buf,
                file_name=f"{user_to_view}_id_card.png",
                mime="image/png",
                use_container_width=True
            )
            
            # QR code download (only in admin panel)
            if user_to_view in st.session_state.users and 'qr_code' in st.session_state.users[user_to_view]:
                qr_buf = BytesIO(base64.b64decode(st.session_state.users[user_to_view]['qr_code']))
                st.download_button(
                    label=f"Download {user_to_view}'s QR Code",
                    data=qr_buf,
                    file_name=f"{user_to_view}_qr_code.png",
                    mime="image/png",
                    use_container_width=True
                )
            
            # Barcode download (only in admin panel)
            if user_to_view in st.session_state.users and 'barcode' in st.session_state.users[user_to_view]:
                barcode_buf = BytesIO(base64.b64decode(st.session_state.users[user_to_view]['barcode']))
                st.download_button(
                    label=f"Download {user_to_view}'s Barcode",
                    data=barcode_buf,
                    file_name=f"{user_to_view}_barcode.png",
                    mime="image/png",
                    use_container_width=True
                )
        elif user_to_view:
            st.info("ID card not available for this user. Generate it first.")
    
    with tab4:
        render_intern_management()
        
    with tab5:
        st.markdown("#### 💾 Backup & Restore")
        
        # Create backup
        st.subheader("Create Backup")
        if st.button("Create System Backup", use_container_width=True):
            backup_json = create_backup()
            st.session_state.backup_data = backup_json
            
            # Save to database
            save_database()
            
            st.success("Backup created successfully!")
            
            # Download backup file
            st.download_button(
                label="Download Backup File",
                data=backup_json,
                file_name=f"aegis_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Restore backup
        st.subheader("Restore Backup")
        st.warning("⚠️ Restoring a backup will overwrite all current data. This action cannot be undone!")
        
        uploaded_backup = st.file_uploader("Upload backup file", type=["json"])
        
        if uploaded_backup is not None:
            if st.button("Restore from Backup", type="secondary", use_container_width=True):
                success, message = restore_backup(uploaded_backup)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

def render_intern_management():
    st.markdown("#### 👨‍🎓 Intern Management")
    
    # Show all interns
    if st.session_state.interns:
        st.write("Current Interns:")
        intern_data = []
        for username, intern_info in st.session_state.interns.items():
            user_info = st.session_state.users[username]
            intern_data.append({
                'Username': username,
                'Full Name': user_info.get('full_name', ''),
                'Mentor': intern_info.get('mentor', 'Not assigned'),
                'Start Date': intern_info.get('start_date', ''),
                'Performance Rating': intern_info.get('performance_rating', 0),
                'Completed Tasks': intern_info.get('completed_tasks', 0),
                'Assigned Tasks': len(intern_info.get('assigned_tasks', []))
            })
        
        df = pd.DataFrame(intern_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No interns registered yet")
    
    # Task management
    st.subheader("Task Management")
    
    # Create new task
    with st.form("create_task_form"):
        task_title = st.text_input("Task Title*")
        task_description = st.text_area("Task Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_deadline = st.date_input("Deadline")
        
        # Assign to intern
        intern_options = list(st.session_state.interns.keys())
        assigned_intern = st.selectbox("Assign to Intern", [""] + intern_options)
        
        create_task_btn = st.form_submit_button("Create Task", use_container_width=True)
        
        if create_task_btn and task_title and assigned_intern:
            task_id = str(uuid.uuid4())
            if assigned_intern not in st.session_state.tasks:
                st.session_state.tasks[assigned_intern] = []
            
            st.session_state.tasks[assigned_intern].append({
                'id': task_id,
                'title': task_title,
                'description': task_description,
                'priority': task_priority,
                'deadline': task_deadline.strftime("%Y-%m-%d"),
                'status': 'Assigned',
                'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'created_by': st.session_state.current_user
            })
            
            # Add to intern's assigned tasks
            st.session_state.interns[assigned_intern]['assigned_tasks'].append(task_id)
            
            # Save to database
            save_database()
            
            st.success(f"Task '{task_title}' assigned to {assigned_intern}")
    
    # View and manage tasks for a specific intern
    st.subheader("Manage Intern Tasks")
    intern_to_manage = st.selectbox("Select Intern", [""] + list(st.session_state.interns.keys()))
    
    if intern_to_manage and intern_to_manage in st.session_state.tasks:
        tasks = st.session_state.tasks[intern_to_manage]
        
        for task in tasks:
            with st.expander(f"{task['title']} - {task['status']}"):
                st.write(f"**Description:** {task['description']}")
                st.write(f"**Priority:** {task['priority']}")
                st.write(f"**Deadline:** {task['deadline']}")
                st.write(f"**Assigned by:** {task['created_by']}")
                
                # Update task status
                new_status = st.selectbox("Status", ["Assigned", "In Progress", "Completed", "Reviewed"], 
                                        key=f"status_{task['id']}",
                                        index=["Assigned", "In Progress", "Completed", "Reviewed"].index(task['status']))
                
                if new_status != task['status']:
                    if st.button("Update Status", key=f"update_{task['id']}"):
                        task['status'] = new_status
                        if new_status == "Completed":
                            # Update intern's completed tasks count
                            st.session_state.interns[intern_to_manage]['completed_tasks'] = \
                                st.session_state.interns[intern_to_manage].get('completed_tasks', 0) + 1
                        
                        # Save to database
                        save_database()
                        
                        st.success("Task status updated")
                        st.rerun()
                
                # Add feedback/notes
                feedback = st.text_area("Add feedback/notes", key=f"feedback_{task['id']}")
                if st.button("Save Feedback", key=f"save_feedback_{task['id']}") and feedback:
                    if 'feedback' not in task:
                        task['feedback'] = []
                    task['feedback'].append({
                        'by': st.session_state.current_user,
                        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'text': feedback
                    })
                    
                    # Save to database
                    save_database()
                    
                    st.success("Feedback added")
    
    if st.button("Back to Admin Panel", use_container_width=True):
        st.session_state.show_intern_management = False
        st.rerun()

def render_id_card():
    if st.session_state.current_user in st.session_state.id_cards:
        st.markdown("### 🪪 Your ID Card")
        id_card_data = st.session_state.id_cards[st.session_state.current_user]
        st.image(BytesIO(base64.b64decode(id_card_data)), use_column_width=True)
        
        # Download button
        buf = BytesIO(base64.b64decode(id_card_data))
        st.download_button(
            label="Download ID Card",
            data=buf,
            file_name=f"{st.session_state.current_user}_id_card.png",
            mime="image/png",
            use_container_width=True
        )
    else:
        st.info("ID card not available. Please contact administrator to generate one.")
    
    if st.button("Back to Chat", use_container_width=True):
        st.session_state.show_id_card = False
        st.rerun()

def main():
    # Initialize admin user if not exists
    if "admin" not in st.session_state.users:
        st.session_state.users["admin"] = {
            'password': st.session_state.admin_password,
            'full_name': "System Administrator",
            'specialty': "System Administration",
            'role': "Administrator",
            'department': "IT",
            'staff_id': "ADMIN-001",
            'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'qr_code': generate_qr_code("ADMIN-001"),
            'access_level': "Administrator",
            'status': 'active',
            'is_intern': False
        }
        
        # Save to database
        save_database()

    if st.session_state.current_user is None:
        render_login()
    elif st.session_state.current_user == "admin" and st.session_state.get('show_admin_panel', False):
        render_admin_panel()
    elif st.session_state.get('show_intern_management', False):
        render_intern_management()
    elif st.session_state.get('show_id_card', False):
        render_id_card()
    elif not st.session_state.qr_verified and st.session_state.show_qr_scanner:
        render_qr_verification()
    else:
        render_sidebar()
        render_chat_interface()

if __name__ == "__main__":
    main()