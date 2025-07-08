# 💸 Personal Money Management Telegram Bot

A Python-based Telegram bot that helps you track and manage your personal income and expenses. Built with FastAPI, SQLAlchemy, and python-telegram-bot.

## 🚀 Features

- **Easy Transaction Logging**: Add income and expenses with simple text commands
- **Financial Summaries**: Get detailed summaries of your spending and income
- **Category Tracking**: Organize transactions by categories
- **Transaction History**: View recent transactions with full details
- **Secure**: Each user's data is isolated and secure
- **Cloud Ready**: Deploy easily on Render or other cloud platforms

## 📋 Commands

### Adding Transactions
- `+100 salary` - Add $100 income with category "salary"
- `-50 food` - Add $50 expense with category "food"
- `+2000 bonus work bonus` - Add income with description
- `-150 groceries food shopping` - Add expense with description

### Viewing Data
- `/start` - Welcome message and command overview
- `/help` - Detailed help and examples
- `/summary` - Last 30 days financial summary
- `/summary 7` - Last 7 days summary
- `/summary 90` - Last 90 days summary
- `/transactions` - Last 10 transactions
- `/transactions 5` - Last 5 transactions

### Managing Data
- `/delete <transaction_id>` - Delete a specific transaction

## 🛠️ Technology Stack

- **Backend**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Telegram Integration**: python-telegram-bot
- **Deployment**: Render (Free tier)
- **Environment**: python-dotenv

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd money_bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   cp config.py .env  # Or create manually
   ```
   
   Edit `.env` file:
   ```
   TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
   DATABASE_URL=sqlite:///./money_bot.db
   HOST=0.0.0.0
   PORT=8000
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Set up webhook** (for production)
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
        -H "Content-Type: application/json" \
        -d '{"url": "https://your-app-name.onrender.com/telegram"}'
   ```

## 🚀 Deployment on Render

### Option 1: Using render.yaml (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Set Environment Variables**
   - In your Render service dashboard
   - Go to "Environment" tab
   - Add `TELEGRAM_BOT_TOKEN` with your actual bot token

4. **Deploy**
   - Render will automatically build and deploy your app
   - Your app will be available at `https://your-app-name.onrender.com`

### Option 2: Manual Setup

1. **Create a new Web Service on Render**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Set Environment Variables**
   - `TELEGRAM_BOT_TOKEN`: Your bot token
   - `DATABASE_URL`: `sqlite:///./money_bot.db`
   - `HOST`: `0.0.0.0`
   - `PORT`: `8000`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | Required |
| `DATABASE_URL` | Database connection string | `sqlite:///./money_bot.db` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `WEBHOOK_URL` | Webhook URL for production | Auto-generated |

### Database Schema

The bot uses a single `transactions` table:

```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    transaction_type VARCHAR(10) NOT NULL,
    category VARCHAR(50),
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

## 📊 Usage Examples

### Adding Transactions
```
+1000 salary
-25 coffee
-150 groceries food shopping
+5000 bonus year end bonus
-75 gas transportation
```

### Viewing Summaries
```
/summary          # Last 30 days
/summary 7        # Last week
/summary 90       # Last 3 months
```

### Managing Transactions
```
/transactions     # Last 10 transactions
/transactions 5   # Last 5 transactions
/delete 123       # Delete transaction with ID 123
```

## 🔒 Security Features

- **User Isolation**: Each user can only access their own transactions
- **Input Validation**: All inputs are validated and sanitized
- **Error Handling**: Comprehensive error handling prevents crashes
- **Environment Variables**: Sensitive data stored in environment variables

## 🐛 Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check if webhook is set correctly
   - Verify bot token in environment variables
   - Check Render logs for errors

2. **Database errors**
   - Ensure database file is writable
   - Check if tables are created (should happen automatically)

3. **Deployment issues**
   - Verify all environment variables are set
   - Check build logs in Render dashboard
   - Ensure requirements.txt is up to date

### Logs

Check logs in Render dashboard or locally:
```bash
# Local logs
uvicorn app.main:app --log-level debug

# Render logs
# Available in Render dashboard under "Logs" tab
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [python-telegram-bot](https://python-telegram-bot.org/) for Telegram integration
- [SQLAlchemy](https://www.sqlalchemy.org/) for database ORM
- [Render](https://render.com/) for free hosting

---

**Happy Money Management! 💰** 