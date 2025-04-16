from flask import Flask, render_template_string, jsonify
import logging
import os
import threading
import time
from telegram_bot import send_notification

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# HTML template for the status page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tipsport Bot Status</title>
    <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .status-card {
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .status-online {
            background-color: var(--bs-success-bg-subtle);
            border: 1px solid var(--bs-success-border-subtle);
        }
        .info-section {
            margin-top: 30px;
        }
        .criteria-box {
            background-color: var(--bs-dark-bg-subtle);
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
        }
        .footer {
            margin-top: 40px;
            font-size: 0.9em;
            text-align: center;
            color: var(--bs-secondary-color);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="mt-4 mb-4">Tipsport Monitoring Bot</h1>
        
        <div class="status-card status-online">
            <h3 class="mb-3">Bot Status: <span class="text-success">Online</span></h3>
            <p>The Tipsport monitoring bot is currently running and checking for matches.</p>
            <p>Last checked: <span id="lastChecked">{{ current_time }}</span></p>
        </div>
        
        <div class="info-section">
            <h3>What This Bot Does</h3>
            <p>This bot monitors Tipsport for hockey and football matches where a team is winning by 2+ goals with odds of 1.5 or higher. When it finds matches meeting these criteria, it sends notifications to your Telegram.</p>
            
            <div class="criteria-box">
                <h4>Monitoring Criteria:</h4>
                <ul>
                    <li>Sports: Hockey and Football</li>
                    <li>Goal difference: 2 or more goals</li>
                    <li>Odds: 1.5 or higher</li>
                </ul>
            </div>
        </div>
        
        <div class="info-section">
            <h3>Bot Commands</h3>
            <p>You can interact with the bot on Telegram using these commands:</p>
            <ul>
                <li><strong>/start</strong> - Start the bot and get a welcome message</li>
                <li><strong>/help</strong> - Get help information</li>
                <li><strong>/status</strong> - Check if the bot is running</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>Tipsport Monitoring Bot &copy; {{ current_year }}</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Home page with bot status"""
    from datetime import datetime
    return render_template_string(
        HTML_TEMPLATE, 
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        current_year=datetime.now().year
    )

@app.route('/api/status')
def api_status():
    """API endpoint for bot status"""
    return jsonify({
        'status': 'online',
        'monitoring': True,
        'timestamp': int(time.time())
    })

@app.route('/api/send-test')
def send_test_message():
    """Send a test message via Telegram"""
    try:
        # Create a thread to send the notification (to avoid blocking)
        thread = threading.Thread(
            target=send_notification,
            args=("🧪 *Test Message*\n\nThis is a test notification from the Tipsport Monitoring Bot. " 
                  "If you're seeing this, the bot is working correctly!",)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Test message sent'
        })
    except Exception as e:
        logger.error(f"Error sending test message: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


create root app.py
