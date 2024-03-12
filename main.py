import asyncio, logging, sys
from aiogram import Bot, Dispatcher
# from aiogram.client.session.aiohttp import AiohttpSession
from handlers import questions, visit, admins, chat
# TG_TOKEN = '6953464010:AAGrYWjXK5uohJ7qJ3NqXD_lm7KRJWDoScM'#JPTBotrm -r .venv
TG_TOKEN =  '6440298772:AAGL48-IZCl5D2Lxcn_VHAfAfKnk8GN3_hI' #Laura GPT

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TG_TOKEN, parse_mode="HTML")
dp = Dispatcher()
# dp.message.filter(lambda message: message.from_user.is_bot == True)

async def main() -> None:
    dp.include_routers(admins.router, questions.router, visit.router, chat.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

# try:
#     session = AiohttpSession(proxy='http://proxy.server:3128')
#     bot = Bot(token=TG_TOKEN, session=session)
# except:
#     bot = Bot(token=TG_TOKEN)
