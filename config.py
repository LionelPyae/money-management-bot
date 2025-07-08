import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8114777947:AAF49VRSOGr6xT_EhQ3LrmAf1m8utdak2Qs")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-4642426494")
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./money_bot.db")
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    # Webhook Configuration (for production)
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-app-name.onrender.com/telegram") 