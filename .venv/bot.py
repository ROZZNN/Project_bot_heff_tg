import logging
from telegram import Update
from telegram.ext import Filters
import requests 
from googletrans import Translator
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
import random

# Вставьте Ваш токен
TOKEN = '7616264600:AAETYkgioF5ruz83npkJVN-yTHb78V6RDN8'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Инициализация переводчика
translator = Translator()

# Функция для старта
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Напиши мне продукты, которые у тебя есть, или используй команду /recipe_of_the_day для получения рецепта дня.')

# Функция для обработки сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    # Переводим входное сообщение на английский
    translated_input = translator.translate(user_input, dest='en').text
    recipes = find_recipes(translated_input)  # Функция для поиска рецептов
    if recipes:
        # Переводим ответ на русский
        translated_recipes = translator.translate(f'Вот рецепты, которые Вы можете приготовить:\n{recipes}', dest='ru').text
        update.message.reply_text(translated_recipes)
    else:
        update.message.reply_text('Извини, я не нашел рецептов с этими продуктами.')

# Функция для поиска рецептов
def find_recipes(ingredients):
    api_key = 'f9c90cf8e3554ae7b2b54f64742c579a'
    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={",".join(ingredients.split())}&apiKey={api_key}'
    
    response = requests.get(url)  # Отправляем GET-запрос к API
    if response.status_code == 200:
        recipes = response.json()  # Получаем данные в формате JSON
        if recipes:
            # Формируем список рецептов
            recipe_list = [recipe['title'] for recipe in recipes]
            return ", ".join(recipe_list)  # Возвращаем список рецептов
        else:
            return "Нет рецептов, соответствующих вашим ингредиентам."
    else:
        return "Ошибка:001; напишите в поддержку"

# Функция для получения рецепта дня
def recipe_of_the_day(update: Update, context: CallbackContext) -> None:
    api_key = 'f9c90cf8e3554ae7b2b54f64742c579a'
    url = f'https://api.spoonacular.com/recipes/random?apiKey={api_key}'
    
    response = requests.get(url)  # Отправляем GET-запрос к API
    if response.status_code == 200:
        recipe = response.json()['recipes'][0]  # Получаем случайный рецепт
        # Переводим ответ на русский
        translated_recipe = translator.translate(f'Рецепт дня: {recipe["title"]}\nИнструкция: {recipe["instructions"]}', dest='ru').text
        update.message.reply_text(translated_recipe)
    else:
        update.message.reply_text("Ошибка: не удалось получить рецепт дня.")

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("recipe_of_the_day", recipe_of_the_day))  # Добавлена команда для рецепта дня
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
