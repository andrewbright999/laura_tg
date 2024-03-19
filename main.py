import asyncio, logging, sys
from aiogram import Bot, Dispatcher
from handlers import questions, visit, admins, chat
from forwarding import forward

TG_TOKEN =  '6440298772:AAGL48-IZCl5D2Lxcn_VHAfAfKnk8GN3_hI' #Laura GPT

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TG_TOKEN, parse_mode="HTML")
dp = Dispatcher()


async def main() -> None:
    dp.include_routers(admins.router, questions.router, visit.router, chat.router, forward.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
