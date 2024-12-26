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

# Словарь для хранения любимых рецептов пользователей
favorite_recipes = {}

# Функция для старта
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Напиши мне продукты, которые у тебя есть, или используй команду /recipe_of_the_day для получения рецепта дня.')

# Функция для обработки сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    recipes = find_recipes(user_input)  # Функция для поиска рецептов
    if recipes:
        update.message.reply_text(f'Вот рецепты, которые Вы можете приготовить:\n{recipes}')
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
        update.message.reply_text(f'Рецепт дня: {recipe["title"]}\nИнструкция: {recipe["instructions"]}')
    else:
        update.message.reply_text("Ошибка: не удалось получить рецепт дня.")

# Функция для сохранения любимого рецепта
def save_favorite(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    recipe_name = " ".join(context.args)  # Получаем название рецепта из аргументов команды
    if user_id not in favorite_recipes:
        favorite_recipes[user_id] = []
    favorite_recipes[user_id].append(recipe_name)
    update.message.reply_text(f'Рецепт "{recipe_name}" добавлен в Ваши любимые!')

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("recipe_of_the_day", recipe_of_the_day))  # Добавлена команда для рецепта дня
    dispatcher.add_handler(CommandHandler("save_favorite", save_favorite))  # Добавлена команда для сохранения любимого рецепта
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
