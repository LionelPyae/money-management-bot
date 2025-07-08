import logging
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import re
from typing import Dict, Any
from types import SimpleNamespace

from .database import get_db, create_tables
from . import crud, schemas
from config import Config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Money Management Bot", version="1.0.0")

# Initialize bot
bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)

# Admin notification function
async def send_admin_notification(message: str):
    """Send notification to admin chat"""
    try:
        await bot.send_message(chat_id=Config.TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        logger.error(f"Failed to send admin notification: {e}")

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Starting up Money Management Bot...")
        logger.info(f"TELEGRAM_BOT_TOKEN: {Config.TELEGRAM_BOT_TOKEN[:8]}... (hidden) ")
        logger.info(f"DATABASE_URL: {Config.DATABASE_URL}")
        create_tables()
        logger.info("Database tables created")
        # Send startup notification to admin
        startup_message = "🚀 Money Management Bot is now online and ready to track your finances!"
        await send_admin_notification(startup_message)
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_message = """
💰 Welcome to your Personal Money Management Bot!

Here are the available commands:

📝 Add transactions:
• +100 salary (add income)
• -50 food (add expense)
• +2000 bonus work bonus (add income with description)

📊 View summaries:
• /summary - Last 30 days summary
• /summary 7 - Last 7 days summary
• /summary 90 - Last 90 days summary

📋 View recent transactions:
• /transactions - Last 10 transactions
• /transactions 5 - Last 5 transactions

🗑️ Delete transaction:
• /delete <transaction_id>

💡 Examples:
• +1000 salary
• -25 coffee
• -150 groceries food shopping
• +5000 bonus year end bonus

Start tracking your money now! 💸
    """
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_message = """
🤖 Money Management Bot Help

📝 Adding Transactions:
• Use + for income: +100 salary
• Use - for expenses: -50 food
• Add description: +2000 bonus work bonus

📊 Commands:
• /start - Welcome message
• /help - This help message
• /summary [days] - Financial summary
• /transactions [count] - Recent transactions
• /delete <id> - Delete transaction

💡 Tips:
• Categories help organize expenses
• Descriptions provide context
• Use /summary to track your progress
    """
    await update.message.reply_text(help_message)

async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /summary command"""
    user_id = update.effective_user.id
    days = 30  # default
    
    if context.args:
        try:
            days = int(context.args[0])
            if days <= 0 or days > 365:
                await update.message.reply_text("Please specify days between 1 and 365.")
                return
        except ValueError:
            await update.message.reply_text("Please provide a valid number of days.")
            return
    
    # Get database session
    db = next(get_db())
    try:
        summary = crud.get_user_summary(db, user_id, days)
        category_summary = crud.get_category_summary(db, user_id, days)
        
        message = f"""
📊 Financial Summary (Last {days} days)

💰 Income: ${summary.total_income:.2f}
💸 Expenses: ${summary.total_expenses:.2f}
💵 Balance: ${summary.balance:.2f}
📈 Total Transactions: {summary.transaction_count}
        """
        
        if category_summary:
            message += "\n📋 Expenses by Category:\n"
            for category, amount in sorted(category_summary.items(), key=lambda x: x[1], reverse=True):
                message += f"• {category}: ${amount:.2f}\n"
        
        await update.message.reply_text(message)
    finally:
        db.close()

async def transactions_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /transactions command"""
    user_id = update.effective_user.id
    limit = 10  # default
    
    if context.args:
        try:
            limit = int(context.args[0])
            if limit <= 0 or limit > 50:
                await update.message.reply_text("Please specify limit between 1 and 50.")
                return
        except ValueError:
            await update.message.reply_text("Please provide a valid number.")
            return
    
    # Get database session
    db = next(get_db())
    try:
        transactions = crud.get_transactions_by_user(db, user_id, limit)
        
        if not transactions:
            await update.message.reply_text("No transactions found.")
            return
        
        message = f"📋 Recent Transactions (Last {limit}):\n\n"
        for t in transactions:
            emoji = "💰" if t.transaction_type == "income" else "💸"
            date_str = t.created_at.strftime("%Y-%m-%d %H:%M")
            message += f"{emoji} ${t.amount:.2f} - {t.category or 'No category'}\n"
            if t.description:
                message += f"   📝 {t.description}\n"
            message += f"   📅 {date_str} (ID: {t.id})\n\n"
        
        await update.message.reply_text(message)
    finally:
        db.close()

async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /delete command"""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text("Please provide a transaction ID to delete.\nUsage: /delete <transaction_id>")
        return
    
    try:
        transaction_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Please provide a valid transaction ID.")
        return
    
    # Get database session
    db = next(get_db())
    try:
        success = crud.delete_transaction(db, transaction_id, user_id)
        if success:
            await update.message.reply_text(f"✅ Transaction {transaction_id} deleted successfully.")
        else:
            await update.message.reply_text("❌ Transaction not found or you don't have permission to delete it.")
    finally:
        db.close()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages for adding transactions"""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    logger.info(f"Received message from user {user_id}: {text}")
    
    # Parse transaction from message
    # Format: +100 salary or -50 food or +2000 bonus work bonus
    pattern = r'^([+-])(\d+(?:\.\d{1,2})?)\s+(\w+)(?:\s+(.+))?$'
    match = re.match(pattern, text)
    
    if not match:
        await update.message.reply_text(
            "❌ Invalid format. Use:\n"
            "• +100 salary (income)\n"
            "• -50 food (expense)\n"
            "• +2000 bonus work bonus (with description)"
        )
        return
    
    sign, amount_str, category, description = match.groups()
    amount = float(amount_str)
    transaction_type = "income" if sign == "+" else "expense"
    
    # Create transaction
    db = next(get_db())
    try:
        transaction_data = schemas.TransactionCreate(
            user_id=user_id,
            amount=amount,
            transaction_type=transaction_type,
            category=category,
            description=description
        )
        
        transaction = crud.create_transaction(db, transaction_data)
        
        emoji = "💰" if transaction_type == "income" else "💸"
        message = f"{emoji} Transaction added successfully!\n\n"
        message += f"Amount: ${amount:.2f}\n"
        message += f"Type: {transaction_type.title()}\n"
        message += f"Category: {category}\n"
        if description:
            message += f"Description: {description}\n"
        message += f"ID: {transaction.id}"
        
        await update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error creating transaction: {e}")
        await update.message.reply_text("❌ Error creating transaction. Please try again.")
    finally:
        db.close()

# Webhook endpoint for Telegram
@app.post("/telegram")
async def telegram_webhook(request: Request):
    try:
        update_data = await request.json()
        update = Update.de_json(update_data, bot)

        # Dummy context with args
        class DummyContext:
            def __init__(self, args=None):
                self.args = args or []

        if update.message:
            if update.message.text:
                text = update.message.text
                if text.startswith('/'):
                    split_text = text.split()
                    command = split_text[0]
                    args = split_text[1:]
                    context = DummyContext(args)
                    if command == '/start':
                        await start_command(update, context)
                    elif command == '/help':
                        await help_command(update, context)
                    elif command == '/summary':
                        await summary_command(update, context)
                    elif command == '/transactions':
                        await transactions_command(update, context)
                    elif command == '/delete':
                        await delete_command(update, context)
                    else:
                        await update.message.reply_text("Unknown command. Use /help for available commands.")
                else:
                    context = DummyContext()
                    await handle_message(update, context)

        return JSONResponse(content={"status": "ok"})
    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        return JSONResponse(content={"status": "error"}, status_code=500)

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Money Management Bot is running!", "status": "healthy"}

# Health check for Render
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "money-management-bot"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT) 