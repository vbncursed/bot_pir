import os
import paramiko
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor
from ssh import upload_file_to_server, unpack_rar_file, run_qgis_script, download_file_from_server, delete_file_on_server

# Инициализация бота
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Параметры подключения к удаленному серверу
HOST_NAME = os.getenv('HOST_NAME')
USER_NAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')

# Команда /start
@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply("Отправьте ваш архив с картой. Название карты в архиве должно быть строго: srtm_25_23.tif")


# Обработчик документов
@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def handle_rar_file(message: types.Message):
    await message.answer("Начинаю обработку файла...")

    # Получаем информацию о файле
    file_info = message.document
    file_id = file_info.file_id
    file_name = file_info.file_name

    # Отправляем сообщение о получении информации о файле
    await message.answer("Получена информация о файле. Начинаю загрузку...")

    # Скачиваем файл
    file_path = await bot.get_file(file_id)
    downloaded_file = await bot.download_file(file_path.file_path)

    # Отправляем сообщение о завершении загрузки файла
    await message.answer("Файл успешно скачан. Начинаю загрузку на сервер...")

    # Загружаем файл на сервер
    with open(file_name, 'wb') as f:
        f.write(downloaded_file.read())

    # Отправляем сообщение о завершении загрузки на сервер
    await message.answer("Файл успешно загружен на сервер. Подключаюсь к удаленному серверу...")

    try:
        # Подключаемся к удаленному серверу по SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=HOST_NAME, username=USER_NAME, password=PASSWORD)

        # Загружаем файл на удаленный сервер
        upload_file_to_server(ssh, file_name, '/root/qgis_script/' + file_name)
        await message.answer("Файл успешно загружен на удаленный сервер.")

        # Распаковываем файл на удаленном сервере
        unpack_rar_file(ssh, '/root/qgis_script/' + file_name, '/root/qgis_script/tif_files')
        await message.answer("Файл успешно распакован на удаленном сервере.")

        # Запуск скрипта QGIS для создания файла export.csv
        run_qgis_script(ssh, '/root/qgis_script/tif_files/qgis1.py')
        await message.answer("Скрипт QGIS успешно выполнен.")

    finally:
        # Закрываем SSH-соединение
        ssh.close()

        # Подключаемся к удаленному серверу по SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=HOST_NAME, username=USER_NAME, password=PASSWORD)

        # Скачиваем файл с удаленного сервера
        download_file_from_server(ssh, '/root/qgis_script/tif_files/export.csv', 'export.csv')
        await message.answer("Файл успешно скачан с удаленного сервера.")

        # Отправка файла пользователю
        with open('export.csv', 'rb') as f:
            await bot.send_document(message.chat.id, f)

        # Удаляем файлы с удаленного сервера
        delete_file_on_server(ssh, '/root/qgis_script/' + file_name)
        delete_file_on_server(ssh, '/root/qgis_script/tif_files/export.csv')
        delete_file_on_server(ssh, '/root/qgis_script/tif_files/srtm_25_23.tif')

        # Закрываем SSH-соединение
        ssh.close()

        # Удаляем файл с локального сервера
        os.remove('export.csv')
        os.remove(file_name)

        await message.answer("Файлы успешно удалены с удаленного и локального серверов.")


if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
