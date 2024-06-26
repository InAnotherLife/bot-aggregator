import asyncio
import json
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from dotenv import load_dotenv

from aggregation import Aggregation

load_dotenv()


async def get_result(message: types.Message, aggregation: Aggregation) -> None:
    """
    Получение сообщения от пользователя, вызов метода для получения результата
    агрегации данных и отправка результата вычисления пользователю.
    """
    try:
        result = await aggregation.get_result(json.loads(message.text))
        await message.answer(str(result), parse_mode=ParseMode.MARKDOWN)
    except Exception:
        await message.answer('Невалидный запрос. Пример запроса:\n{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}')  # noqa: E501


async def start_bot(token: str, aggregation: Aggregation) -> None:
    """
    Запуск телеграм бота, установка обработчика handle_all_messages для всех
    входящих сообщений.
    """
    bot = Bot(token=token)
    dp = Dispatcher(bot)
    dp.middleware.setup(LoggingMiddleware())

    @dp.message_handler()
    async def handle_all_messages(message: types.Message):
        await get_result(message, aggregation)

    await dp.start_polling()

if __name__ == '__main__':
    aggregation = Aggregation()
    asyncio.run(start_bot(os.getenv('TOKEN'), aggregation))
