def hellp(update: Update, context: CallbackContext) -> None:
    return update.message.reply_text(f'Вот команды доступные команды бота:\n /help - список существующих команд \n/start - команда для начала работы с ботом \n/recipe_of_the_day -выдает рандомный рецепт для опытных поворят \n/save_favorite (имя рецепта) - сохроняет ваш любимый рецепт')


dispatcher.add_handler(CommandHandler("help", hellp))