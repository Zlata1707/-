import csv
import random
import requests
from PIL import Image
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

# Пути к файлам с датасетами
dialogs_dataset_path = "dialogs.csv"
images_dataset_path = "images.csv"

# Загрузка датасетов
def load_dialogs(dataset_path):
    dialogs = {}
    with open(dataset_path, encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:
                q_id = row[0]
                question = row[1].lower()
                answer = row[2]
                if question not in dialogs:
                    dialogs[question] = []
                dialogs[question].append(answer)
    return dialogs

def load_images_dataset(images_dataset_path):
    images = []
    with open(images_dataset_path, encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            image_context = row[0].lower()
            image_url = row[1]
            images.append((image_url, image_context))
    return images

# Загрузка датасетов
dialogs = load_dialogs(dialogs_dataset_path)
images = load_images_dataset(images_dataset_path)

# Отправка ответа на текстовый запрос
def send_response(update: Update, context: CallbackContext):
    user_input = update.message.text.lower()
    if user_input in dialogs:
        response = random.choice(dialogs[user_input])
    else:
        response = "Не могу найти подходящий ответ на ваш запрос."
    update.message.reply_text(response)

# Отправка случайной картинки
def send_random_photo(update: Update, context: CallbackContext):
    image_url, image_context = random.choice(images)
    image_data = requests.get(image_url).content
    image = Image.open(BytesIO(image_data))
    image.save("temp.jpg")
    bot = Bot(token="YOUR_BOT_TOKEN")
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=open("temp.jpg", "rb"))
    os.remove("temp.jpg")

# Обработка входящего сообщения
def handle_message(update: Update, context: CallbackContext):
    user_input = update.message.text.lower()

    if user_input == "[share the photo]":
        send_random_photo(update, context)
    else:
        send_response(update, context)

# Настройка телеграм-бота
updater = Updater(token="YOUR_BOT_TOKEN", use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler("start", handle_message)
dispatcher.add_handler(start_handler)

# Запуск телеграм-бота
updater.start_polling()