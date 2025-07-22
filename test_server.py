#!/usr/bin/env python3
"""
Simple test server for CareerGuideAI
"""

from flask import Flask, render_template_string
import webbrowser
import threading
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CareerGuideAI Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 800px; margin: 0 auto; text-align: center; }
            .card { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; margin: 20px 0; }
            .btn { background: #6366f1; color: white; padding: 12px 24px; border: none; border-radius: 8px; text-decoration: none; display: inline-block; margin: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1>🚀 CareerGuideAI Test Server</h1>
                <p>If you can see this page, the Flask server is working correctly!</p>
                <p>Server is running on: <strong>http://127.0.0.1:8080</strong></p>
            </div>
            
            <div class="card">
                <h2>✅ Server Status: RUNNING</h2>
                <p>Flask application is successfully serving content.</p>
                <a href="http://127.0.0.1:5000" class="btn">Try Main App (Port 5000)</a>
                <a href="http://localhost:5000" class="btn">Try Localhost (Port 5000)</a>
            </div>
            
            <div class="card">
                <h3>🔧 Troubleshooting</h3>
                <p>If the main app isn't working, try these URLs:</p>
                <ul style="text-align: left; display: inline-block;">
                    <li>http://127.0.0.1:5000</li>
                    <li>http://localhost:5000</li>
                    <li>http://10.58.30.179:5000</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    ''')

def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:8080')

if __name__ == '__main__':
    print("🚀 Starting CareerGuideAI Test Server...")
    print("📱 Server will be available at: http://127.0.0.1:8080")
    print("🌐 Opening browser automatically...")
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run the server
    app.run(debug=False, host='127.0.0.1', port=8080) 