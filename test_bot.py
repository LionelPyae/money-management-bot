#!/usr/bin/env python3
"""
Test script to verify Telegram bot token and send a test message.
"""

import asyncio
import sys
from telegram import Bot
from config import Config

async def test_bot():
    """Test the bot token and send a test message"""
    try:
        # Initialize bot
        bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        
        # Get bot info
        bot_info = await bot.get_me()
        print(f"✅ Bot connected successfully!")
        print(f"🤖 Bot name: {bot_info.first_name}")
        print(f"📝 Bot username: @{bot_info.username}")
        print(f"🆔 Bot ID: {bot_info.id}")
        
        # Send test message to admin chat
        test_message = "🧪 Test message from Money Management Bot!\n\n✅ Bot is working correctly and ready to track your finances!"
        
        await bot.send_message(
            chat_id=Config.TELEGRAM_CHAT_ID,
            text=test_message
        )
        
        print(f"✅ Test message sent to chat ID: {Config.TELEGRAM_CHAT_ID}")
        print("\n🎉 Bot is ready to use!")
        
    except Exception as e:
        print(f"❌ Error testing bot: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check if the bot token is correct")
        print("2. Make sure the bot is added to the chat/group")
        print("3. Verify the chat ID is correct")
        return False
    
    return True

async def main():
    """Main function"""
    print("🧪 Testing Telegram Bot Configuration...")
    print(f"🔑 Bot Token: {Config.TELEGRAM_BOT_TOKEN[:10]}...")
    print(f"💬 Chat ID: {Config.TELEGRAM_CHAT_ID}")
    print("-" * 50)
    
    success = await test_bot()
    
    if success:
        print("\n🚀 Next steps:")
        print("1. Deploy to Render or run locally")
        print("2. Set up webhook for production")
        print("3. Start tracking your money!")
    else:
        print("\n❌ Please fix the issues above before proceeding")

if __name__ == "__main__":
    asyncio.run(main()) 