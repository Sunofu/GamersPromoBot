import asyncio
from bot import bot_app

if __name__ == "__main__":
    asyncio.run(bot_app.run_polling())