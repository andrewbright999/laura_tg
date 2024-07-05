import asyncio, logging, sys
from aiogram import Bot, Dispatcher
from handlers import flight_handler, questions, visit, admins, chat, personal_questions, wine_questions
from forwarding import forward, expedition_forward
from config import TG_TOKEN


logging.basicConfig(level=logging.INFO)


bot = Bot(token=TG_TOKEN, parse_mode="markdown")
dp = Dispatcher()


async def main() -> None:
    dp.include_routers(forward.router, admins.router, questions.router, visit.router, chat.router, personal_questions.router, wine_questions.router, flight_handler.router, expedition_forward.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
