import asyncio

from bot.bot import KarbanBot
from posiflora.client import PosifloraClient
from logger import logger


# async def run_posiflora():
#     logger.info(f'Requesting data from Posiflora')
#     posiflora = PosifloraClient()
#     await posiflora.run()

async def run_bot():
    logger.info(f'KarbanBot started')
    bot = KarbanBot()
    await bot.run()

async def main():
    #posiflora = asyncio.create_task(run_posiflora())
    bot = asyncio.create_task(run_bot())
    await asyncio.gather(bot)


if __name__ == "__main__":
    asyncio.run(main())