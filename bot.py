import os
import requests
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

try:
    with open(".env", "r") as f:
        for line in f:
            line = line.strip()

            if line.startswith("BOT_TOKEN="):
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

            elif line.startswith("GEMINI_API_KEY="):
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

except FileNotFoundError:
    pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "হ্যালো! 👋\n"
        "আমি তোমার AI Question Answer Bot।\n\n"
        "যেকোনো প্রশ্ন আমাকে করো।"
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent"

    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": question}
                ]
            }
        ]
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        result = response.json()

        if "candidates" not in result:
            print("GEMINI ERROR:", result)
            await update.message.reply_text(
                "দুঃখিত, এই মুহূর্তে AI উত্তর দিতে পারছে না।"
            )
            return

        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        await update.message.reply_text(answer)

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text(
            "দুঃখিত, AI উত্তর দিতে পারেনি। একটু পরে আবার চেষ্টা করো।"
        )


def main():
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN পাওয়া যায়নি!")
        return

    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY পাওয়া যায়নি!")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

    print("AI Bot চালু হয়েছে...")
    app.run_polling()


if __name__ == "__main__":
    main()
