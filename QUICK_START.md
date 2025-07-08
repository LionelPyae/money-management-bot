# 🚀 Quick Start Guide - Money Management Bot

## ✅ Your Bot Credentials
- **Bot Token**: `8114777947:AAF49VRSOGr6xT_EhQ3LrmAf1m8utdak2Qs`
- **Chat ID**: `-4642426494`

## 📋 Setup Steps

### 1. Create Environment File
Create a `.env` file in your project root with this content:
```env
TELEGRAM_BOT_TOKEN=8114777947:AAF49VRSOGr6xT_EhQ3LrmAf1m8utdak2Qs
TELEGRAM_CHAT_ID=-4642426494
DATABASE_URL=sqlite:///./money_bot.db
HOST=0.0.0.0
PORT=8000
```

### 2. Test Your Bot (Optional)
```bash
python test_bot.py
```
This will send a test message to your chat to verify everything works.

### 3. Deploy to Render

#### Option A: GitHub + Render Blueprint (Recommended)
1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Set environment variable: `TELEGRAM_BOT_TOKEN=8114777947:AAF49VRSOGr6xT_EhQ3LrmAf1m8utdak2Qs`
   - Deploy!

#### Option B: Manual Render Setup
1. Create new Web Service on Render
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set environment variable: `TELEGRAM_BOT_TOKEN=8114777947:AAF49VRSOGr6xT_EhQ3LrmAf1m8utdak2Qs`

### 4. Set Up Webhook
After deployment, your app will be at `https://your-app-name.onrender.com`

Set the webhook:
```bash
python setup_webhook.py set https://your-app-name.onrender.com/telegram
```

### 5. Start Using Your Bot!
Send `/start` to your bot to see all available commands.

## 🎯 Bot Commands
- `+1000 salary` - Add income
- `-50 food` - Add expense
- `/summary` - View financial summary
- `/transactions` - View recent transactions
- `/help` - Get help

## 🔧 Troubleshooting

### Bot not responding?
1. Check webhook status: `python setup_webhook.py info`
2. Verify bot token in Render environment variables
3. Check Render logs for errors

### Test locally first:
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📞 Support
If you encounter issues:
1. Check the logs in Render dashboard
2. Verify your bot token is correct
3. Make sure the bot is added to your chat/group

---

**Your bot is ready to track your money! 💰** 