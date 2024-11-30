from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler


# Функция для отправки начального меню
async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Кнопка 1", callback_data='1')],
        [InlineKeyboardButton("Кнопка 2", callback_data='2')],
        [InlineKeyboardButton("Кнопка 3", callback_data='3')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Удаление старого сообщения, если вызов идет из callback
    if update.callback_query:
        await update.callback_query.message.delete()
        await update.callback_query.answer()  # Подтверждение callback
        await update.callback_query.message.reply_text('Выберите одну из кнопок:', reply_markup=reply_markup)
    elif update.message:  # Если это команда /start
        await update.message.reply_text('Выберите одну из кнопок:', reply_markup=reply_markup)


# Функция для обработки выбора пользователя
async def button(update, context):
    query = update.callback_query
    choice = query.data

    # Логируем значение callback_data для отладки
    print(f"Выбор пользователя: {choice}")

    # Определяем текст в зависимости от выбора
    if choice == '1':
        response_text = "Вы выбрали кнопку 1."
    elif choice == '2':
        response_text = "Вы выбрали кнопку 2."
    elif choice == '3':
        response_text = "Вы выбрали кнопку 3."
    elif choice == 'back':  # Обработка нажатия на кнопку "Назад"
        # Переходим в начальное меню
        await start(update, context)
        return  # Завершаем выполнение функции, чтобы не происходило дальнейшей обработки
    else:
        response_text = "Неверный выбор."

    # Удаление старого сообщения
    await query.message.delete()

    # Кнопка "Назад"
    back_button = InlineKeyboardButton("Назад", callback_data='back')
    keyboard = [[back_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем новое сообщение с результатом выбора и кнопкой "Назад"
    await query.message.reply_text(response_text, reply_markup=reply_markup)


# Основная функция для запуска бота
def main():
    # Токен бота, полученный от BotFather
    token = '7661475741:AAEG9Gy4kJot7IYJs8CV1KBzQAAsClE1z3g'

    # Создаем приложение с токеном
    application = Application.builder().token(token).build()

    # Обработчики команд и нажатий кнопок
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()
