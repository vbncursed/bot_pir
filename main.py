import os
from aiogram import Bot, Dispatcher
from bot import cmd_start, handle_rar_file
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

# Инициализация бота
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Команда /start
dp.register_message_handler(cmd_start, commands="start")

# Обработчик документов
dp.register_message_handler(handle_rar_file, content_types="document")


if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
