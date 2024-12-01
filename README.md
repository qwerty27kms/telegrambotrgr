Описание
Этот бот предназначен для управления складом и взаимодействия между менеджерами и работниками через Telegram. Менеджер может добавлять товары, просматривать склад, историю заказов и получать уведомления о проблемах. Работники могут проверять поступления, уведомлять о несоответствиях и выполнять другие действия.

Функционал
Для менеджера:
Добавление товаров на склад:

Формат ввода: Название товара, количество.
Пример: Карандаши, 50.
Просмотр истории заказов:

Отображает все добавленные товары.
Просмотр текущего остатка на складе:

Список всех товаров и их количества.
Диаграмма наличия товаров:

Отправляет диаграмму текущего состояния склада.
Назад:

Возвращает в главное меню выбора роли.
Для работника:
Просмотр поступлений:

Отображает текущий список товаров на складе.
Уведомление о несоответствии:

Уведомляет менеджера о проблеме с товаром.
Последний добавленный товар автоматически удаляется из списка и со склада.
Назад:

Возвращает в главное меню выбора роли.
Установка и запуск
Убедитесь, что у вас установлен Python (рекомендуемая версия: 3.10+).
Установите необходимые библиотеки:
bash
Копировать код
pip install python-telegram-bot matplotlib
Вставьте токен вашего бота в функцию main() вместо "ВАШ_ТОКЕН_ТЕЛЕГРАМ_БОТА".
Запустите файл:
bash
Копировать код
python bot.py
Используемые библиотеки
python-telegram-bot: для работы с Telegram API.
matplotlib: для создания диаграмм.
io: для работы с буфером изображений.
Структура кода
Основные состояния
CHOOSING_ROLE: выбор роли (менеджер или работник).
MANAGER_MENU: меню менеджера.
WORKER_MENU: меню работника.
Основные переменные
stock: словарь для хранения текущих товаров на складе.
orders: список для записи истории заказов.
manager_chat_id: идентификатор чата менеджера.
Пример работы
Пользователь запускает команду /start.
Выбирает свою роль: "Менеджер" или "Работник".
В зависимости от роли получает доступ к соответствующим функциям:
Менеджер добавляет товар, просматривает склад или получает уведомления.
Работник уведомляет о проблемах или проверяет поступления.
Примечания
Уведомления о несоответствии отправляются менеджеру в реальном времени.
Последний добавленный товар удаляется из склада при уведомлении о несоответствии.
Диаграммы создаются автоматически на основе текущего состояния склада.
