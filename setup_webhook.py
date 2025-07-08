#!/usr/bin/env python3
"""
Utility script to set up Telegram webhook for the money management bot.
"""

import requests
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def set_webhook(bot_token, webhook_url):
    """Set the webhook URL for the Telegram bot"""
    url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    data = {"url": webhook_url}
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            print(f"✅ Webhook set successfully!")
            print(f"📡 Webhook URL: {webhook_url}")
            return True
        else:
            print(f"❌ Failed to set webhook: {result.get('description')}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error setting webhook: {e}")
        return False

def get_webhook_info(bot_token):
    """Get current webhook information"""
    url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            webhook_info = result.get("result", {})
            print("📡 Current webhook information:")
            print(f"   URL: {webhook_info.get('url', 'Not set')}")
            print(f"   Has custom certificate: {webhook_info.get('has_custom_certificate', False)}")
            print(f"   Pending update count: {webhook_info.get('pending_update_count', 0)}")
            print(f"   Last error date: {webhook_info.get('last_error_date')}")
            print(f"   Last error message: {webhook_info.get('last_error_message')}")
            return webhook_info
        else:
            print(f"❌ Failed to get webhook info: {result.get('description')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting webhook info: {e}")
        return None

def delete_webhook(bot_token):
    """Delete the current webhook"""
    url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
    
    try:
        response = requests.post(url)
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            print("✅ Webhook deleted successfully!")
            return True
        else:
            print(f"❌ Failed to delete webhook: {result.get('description')}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error deleting webhook: {e}")
        return False

def main():
    """Main function"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "8114777947:AAF49VRSOGr6xT_EhQ3LrmAf1m8utdak2Qs")
    
    if not bot_token:
        print("❌ Please set your TELEGRAM_BOT_TOKEN in the .env file")
        print("   Get your token from @BotFather on Telegram")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python setup_webhook.py set <webhook_url>")
        print("  python setup_webhook.py info")
        print("  python setup_webhook.py delete")
        print("\nExamples:")
        print("  python setup_webhook.py set https://your-app.onrender.com/telegram")
        print("  python setup_webhook.py info")
        print("  python setup_webhook.py delete")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "set":
        if len(sys.argv) < 3:
            print("❌ Please provide the webhook URL")
            print("   Example: python setup_webhook.py set https://your-app.onrender.com/telegram")
            sys.exit(1)
        
        webhook_url = sys.argv[2]
        print(f"🔧 Setting webhook to: {webhook_url}")
        set_webhook(bot_token, webhook_url)
        
    elif command == "info":
        print("🔍 Getting webhook information...")
        get_webhook_info(bot_token)
        
    elif command == "delete":
        print("🗑️ Deleting webhook...")
        delete_webhook(bot_token)
        
    else:
        print(f"❌ Unknown command: {command}")
        print("   Available commands: set, info, delete")
        sys.exit(1)

if __name__ == "__main__":
    main() 