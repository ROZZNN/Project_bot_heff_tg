def hellp(update: Update, context: CallbackContext) -> None:
    return update.message.reply_text(f'Вот команды доступные команды бота:\n /help - список существующих команд \n/start - команда для начала работы с ботом \n/recipe_of_the_day -выдает рандомный рецепт для опытных поворят \n/save_favorite (имя рецепта) - сохроняет ваш любимый рецепт')


dispatcher.add_handler(CommandHandler("help", hellp))

# Функция для сохранения любимого рецепта
def save_favorite(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    recipe_name = " ".join(context.args)  # Получаем название рецепта из аргументов команды
    if user_id not in favorite_recipes:
        favorite_recipes[user_id] = []
        favorite_recipes[user_id].append(recipe_name)
        update.message.reply_text(f'Рецепт "{recipe_name}" добавлен в Ваши любимые рецепты!')
    else 
        update.message.reply_text(f'Данный рецепт уже добавлен в избранное')
