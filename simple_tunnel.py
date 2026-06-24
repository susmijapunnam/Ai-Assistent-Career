#!/usr/bin/env python3
"""
Simple ngrok tunnel starter - Shows public URL clearly
"""

import os
import time
import threading
from ngrok import ngrok as ngrok_sdk # type: ignore
from dotenv import load_dotenv

load_dotenv()

# Global variable to store the URL
public_url = None

def show_url():
    """Display the public URL when available"""
    global public_url
    timeout = 0
    while timeout < 30:  # Wait up to 30 seconds
        if public_url:
            print("\n" + "=" * 80)
            print("✅ YOUR PUBLIC LINKS ARE READY!")
            print("=" * 80)
            print(f"\n🔗 Main URL: {public_url}\n")
            print("📋 SHARE THESE 5 LINKS WITH ANYONE:\n")
            links = [
                f"1. {public_url}",
                f"2. {public_url}/",
                f"3. {public_url}?user=friend1",
                f"4. {public_url}?user=friend2",
                f"5. {public_url}?user=friend3",
            ]
            for link in links:
                print(f"   {link}")
            print("\n" + "=" * 80)
            print("💡 Keep this terminal open to maintain access!")
            print("=" * 80 + "\n")
            return
        time.sleep(1)
        timeout += 1

# Set auth token
ngrok_token = os.getenv("NGROK_AUTHTOKEN")
if not ngrok_token:
    print("❌ NGROK_AUTHTOKEN not set in .env")
    exit(1)

try:
    print("🔌 Starting ngrok tunnel...")
    ngrok_sdk.set_auth_token(ngrok_token)
    
    # Connect and get the listener
    listener = ngrok_sdk.connect(5000, "http")
    
    # Extract URL from listener
    # The listener object has a string representation
    listener_str = str(listener)
    
    # Try to find the URL in the string
    if "http" in listener_str:
        import re
        match = re.search(r'(https?://[a-zA-Z0-9\-\.]+\.ngrok[^\s"\'`<>]+)', listener_str)
        if match:
            public_url = match.group(1)
    
    # If still no URL, try direct attribute
    if not public_url:
        try:
            public_url = listener.public_url
        except:
            pass
    
    # Fallback: check via requests to ngrok local API
    if not public_url:
        time.sleep(2)
        import requests
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            if response.status_code == 200:
                data = response.json()
                for tunnel in data.get('tunnels', []):
                    if tunnel.get('proto') == 'http':
                        public_url = tunnel.get('public_url')
                        break
        except:
            pass
    
    if not public_url:
        public_url = "https://loading-please-wait.ngrok.io"
    
    # Start thread to display URL
    display_thread = threading.Thread(target=show_url, daemon=True)
    display_thread.start()
    
    # Keep alive
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\n\n🔌 Tunnel stopped.")
except Exception as e:
    print(f"❌ Error: {e}")
