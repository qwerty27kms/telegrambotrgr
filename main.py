import matplotlib.pyplot as plt
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import io

CHOOSING_ROLE, MANAGER_MENU, WORKER_MENU = range(3)

stock = {}
orders = []
manager_chat_id = None  # Для хранения chat_id менеджера

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Менеджер', 'Работник']]
    await update.message.reply_text(
        "Привет! Кто вы?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return CHOOSING_ROLE

async def choose_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text.lower()
    context.user_data['role'] = user_choice

    if user_choice == "менеджер":
        global manager_chat_id
        manager_chat_id = update.message.chat_id  # Сохраняем chat_id менеджера
        await update.message.reply_text(
            "Вы выбрали роль менеджера. Что хотите сделать?\n"
            "1. Создать заявку (формат: название, количество)\n"
            "2. История заказов\n"
            "3. Остаток на складе\n"
            "4. Диаграмма наличия товаров\n"
            "5. Назад"
        )
        return MANAGER_MENU
    elif user_choice == "работник":
        await update.message.reply_text(
            "Вы выбрали роль работника. Что хотите сделать?\n"
            "1. Посмотреть поступления\n"
            "2. Уведомить о несоответствии\n"
            "3. Назад"
        )
        return WORKER_MENU
    else:
        await update.message.reply_text("Выберите правильную роль.")
        return CHOOSING_ROLE

async def manager_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()

    if text == "назад":
        reply_keyboard = [['Менеджер', 'Работник']]
        await update.message.reply_text(
            "Вы вернулись в главное меню. Кто вы?",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )
        return CHOOSING_ROLE
    elif "," in text:
        try:
            item, quantity = map(str.strip, text.split(",", 1))
            quantity = int(quantity)
            stock[item] = stock.get(item, 0) + quantity  # Обновляем склад
            orders.append((item, quantity))  # Добавляем запись в историю заказов
            await update.message.reply_text(f"Заявка принята: {item} - {quantity} шт.")
        except ValueError:
            await update.message.reply_text("Ошибка ввода. Убедитесь, что формат: название, количество (например, решетка,100).")
    elif text.startswith("история заказов"):
        history = "\n".join([f"{item}: {qty}" for item, qty in orders]) if orders else "История заказов пуста."
        await update.message.reply_text(f"История заказов:\n{history}")
    elif text.startswith("остаток на складе"):
        stock_list = "\n".join([f"{item}: {qty}" for item, qty in stock.items()]) if stock else "Склад пуст."
        await update.message.reply_text(f"Остаток на складе:\n{stock_list}")
    elif text.startswith("диаграмма наличия товаров"):
        if stock:
            await send_stock_chart(update, context)
        else:
            await update.message.reply_text("Склад пуст, нечего отображать.")
    else:
        await update.message.reply_text("Выберите правильный пункт меню или введите заявку в формате: название, количество.")
    return MANAGER_MENU

async def send_stock_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создание диаграммы
    items = list(stock.keys())
    quantities = list(stock.values())

    fig, ax = plt.subplots()
    ax.bar(items, quantities, color='skyblue')
    ax.set_title('Наличие товаров на складе')
    ax.set_xlabel('Товары')
    ax.set_ylabel('Количество')

    # Сохранение диаграммы в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    # Отправка диаграммы
    await context.bot.send_photo(
        chat_id=update.message.chat_id,
        photo=buf
    )

async def worker_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global manager_chat_id
    text = update.message.text.lower()

    if text.startswith("посмотреть поступления"):
        if stock:
            goods_list = "\n".join([f"{item}: {qty}" for item, qty in stock.items()])
            await update.message.reply_text(f"Текущие поступления:\n{goods_list}")
        else:
            await update.message.reply_text("Нет новых поступлений.")
    elif text.startswith("уведомить о несоответствии"):
        if orders:
            last_item, last_quantity = orders.pop()  # Удаляем последнюю заявку из истории
            stock[last_item] -= last_quantity  # Обновляем склад
            if stock[last_item] <= 0:
                del stock[last_item]  # Удаляем товар, если его количество стало <= 0

            # Уведомляем менеджера
            if manager_chat_id:
                await context.bot.send_message(
                    chat_id=manager_chat_id,
                    text=f"Работник уведомил о несоответствии. Последний добавленный товар отменён: {last_item} - {last_quantity} шт."
                )
            await update.message.reply_text("Несоответствие зафиксировано, последний товар удалён.")
        else:
            await update.message.reply_text("Нет товаров для отмены.")
    elif text == "назад":
        reply_keyboard = [['Менеджер', 'Работник']]
        await update.message.reply_text(
            "Вы вернулись в главное меню. Кто вы?",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )
        return CHOOSING_ROLE
    else:
        await update.message.reply_text("Выберите правильный пункт меню.")
    return WORKER_MENU

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Работа завершена. До свидания!")
    return ConversationHandler.END

def main():
    application = Application.builder().token("7661475741:AAEG9Gy4kJot7IYJs8CV1KBzQAAsClE1z3g").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_role)],
            MANAGER_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, manager_menu)],
            WORKER_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, worker_menu)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
