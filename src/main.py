import asyncio

from bot.bot import KarbanBot
from logger import logger


async def run_bot():
    logger.info(f'KarbanBot started')
    bot = KarbanBot()
    await bot.run()


if __name__ == "__main__":
    asyncio.run(run_bot())