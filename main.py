import os
import json
import requests
import re

from downloader import download_file
from analyzer import load_dataset
from logger import log_event
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


def ask_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    return response.json()["response"]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    url_match = re.search(r'https?://\S+', user_message)

    dataset_info = ""

    if url_match:
        try:
            file_path = download_file(url_match.group())
            df = load_dataset(file_path)

            dataset_info = f"""
    Dataset columns:
    {list(df.columns)}

    First 5 rows:
    {df.head().to_string()}
    """
        except Exception as e:
          dataset_info = f"Could not read dataset: {e}"
    prompt = f"""
You are a data analyst.

User question:
{user_message}

{dataset_info}

Answer only the user's question.
Do not explain.
"""

    try:
        answer = ask_ollama(prompt).strip()

    except Exception as e:
        answer = f"Error: {e}"

    log_file = log_event({
        "question": user_message,
        "answer": answer
        })
    final_json = {
        "answer": answer,
        "log_url": log_file
    }

    await update.message.reply_text(json.dumps(final_json))


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot Running...")

app.run_polling()