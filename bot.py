import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import requests

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Напиши /steam или /epic, чтобы узнать текущие скидки на игры!"
    )

async def steam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = 'https://store.steampowered.com/api/featuredcategories?cc=us&l=en'
    response = requests.get(url).json()
    specials = response.get("specials", {}).get("items", [])[:5]
    if not specials:
        await update.message.reply_text("Не удалось получить данные со Steam 😢")
        return
    text = "🔥 Скидки в Steam:\n\n"
    for item in specials:
        name = item.get("name")
        discount = item.get("discount_percent", 0)
        price = item.get("final_price", 0) / 100
        link = f"https://store.steampowered.com/app/{item.get('id')}/"
        text += f"{name}\n -{discount}% | ${price:.2f}\n🔗 {link}\n\n"
    await update.message.reply_text(text)

async def epic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=ru-RU"
    response = requests.get(url).json()
    games = response["data"]["Catalog"]["searchStore"]["elements"]
    discounted = [g for g in games if g["price"]["totalPrice"]["discountPrice"] < g["price"]["totalPrice"]["originalPrice"]][:5]
    if not discounted:
        await update.message.reply_text("Не удалось получить данные с Epic Games 😢")
        return
    text = "🤑 Скидки в Epic Games:\n\n"
    for game in discounted:
        title = game["title"]
        discount = 100 - int(game["price"]["totalPrice"]["discountPrice"] / game["price"]["totalPrice"]["originalPrice"] * 100)
        link = f"https://store.epicgames.com/ru/p/{game['productSlug']}"
        text += f"{title}\n -{discount}%\n🔗 {link}\n\n"
    await update.message.reply_text(text)

bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("steam", steam))
bot_app.add_handler(CommandHandler("epic", epic))

