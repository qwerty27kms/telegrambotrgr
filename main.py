from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Ваш API токен
TOKEN = '7661475741:AAEG9Gy4kJot7IYJs8CV1KBzQAAsClE1z3g'

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я твой Telegram-бот.')

# Основная функция для запуска бота
def main():
    # Создаем приложение с токеном
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler('start', start))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()