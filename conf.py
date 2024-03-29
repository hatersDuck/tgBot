persent_bonus = 0.02

configure = {
    'token': '5284765764:AAFsASMMUfq-4HwXFfFuaQKtXZa5ZVWVZyU', #5179373973:AAEt5nTmx8K0I9-JAjKTvZ-XOgKcF_ZBeNM
    'adminKey': "39020ae13d2b79ce6489477436a6e472d713b35da8d0643015659245c0d35c0da4c49279d501b1e3249d070c7f198334842c30cab76c6586af21132d987e9f46"
}

botMessage = {
    'welcome': "Добро пожаловать!",
    'location': "Выберите удобную вам локацию",
    'category': "Выберите категорию товара",
    'product': "Выберите товар",
    'count': "Выберите количество товара",
    'empty': "Категории которые сейчас недоступны в данной локации:",
    'failed_category': "Выбрана неверная категория!",
    'failed_location': "Данной локации либо нету товара, либо мы там не работаем!",
    'cancel': "Вы очистили свои данные!\nНапишите или нажмите /start ",
    'menu': "Главное меню",
    'accept_order': "Ваш заказ принят, желаете продолжить покупки?",
    'accept_cart': "Ваш заказ сформирован",
    'num_name': 'Введите номер телефона и как к вам обращаться.',
    'comm': 'Укажите адрес доставки',
    'error': 'Данные введены неверно',
    'er' : "В данный момент не указан",
    'account': "Информация о вас:\nБонусы: %d\nВсего сделанных закaзов: %d",
    'active_order': "\n\nАктивный заказ: %d на сумму %d руб.\nПродавец свяжется в скором времени",
    'not_active_order': "\n\nАктивных заказов нету.",
    'not_info_orders': "У вас ещё нету заказов",
    'info_order': "%s: Стоимость заказа %d rub. - %s",
    'raffle_join': "Теперь вы участвуете в розыгрыше под номером %d",
    'raffle_ticket': "\nВаш билет в розыгрыше: %d",
    'prod_list': "%s - %d руб/шт",
    'one_active_order': "У вас уже есть активный заказ!",
    'empty_products': "Товаров нет в наличие",
    'raffle_error': "Для того, чтобы участвовать в розыгрыше, выставите в настройках телеграма 'Имя пользователя'",
    'empty_orders': "Вы ещё не совершили заказ",

    'order_date': "Доставка производится с ",
    'complete_order' : "Заказ выполнен! Вам начисленно %d бонусов",
    'cancel_order': "Ваш заказ отменён по причине: ",

    'error_start': "Для продолжения работы укажите в настройках телеграма 'Имя пользователя'\nИ напишите снова /start", 
    'error_state': "Извините случились неполадки, мы это исправим в скором времени.\n",
    'delete_order': "Ваш незаконченный заказ удалён. Простите за неудобства"
}

buttons = {
    'products': "💵Товары",
    'buy': "🛒Купить",
    'account': "🗂Личный кабинет",
    'menu': "Главная",
    'select_location': "🌏Сменить локацию",
    'call': "📞Связь с продавцом",
    'back': "Назад",
    'continue': "Продолжить покупки",
    'end_buy': "Закончить покупку",
    'no': "Не указывать",
    'yes': "Уже указано",
    #1 - id, 2 - name 3 - count 4-cost
    #Если захотие, удалить одну из %s то надо залезать в код
    'prod': "%s %d руб./шт. [%d]",
    'order_info': "🗃История заказов",
    'cancel_order': "🚫Отменить заказ",
    'raffle_join': "🎟Участвовать в розыгрыше"
}

admin = {
    'entry': "Введите пароль для входа",
    'admin_menu': "Админ меню",
    'prod_add': "Название-Количество-Стоимость\nВсё через тире, а не отдельными сообщениями",
    'prod_update_count': "id-Новое количество",
    'prod_update_cost': "id-Новая цена",
    'accept': "Принято",

    'id_order': "Введите id заказа",
    'id_prod': "Введите id продукта",
    'active_order': "%d: Сумма заказа - %d"

    
}

admin_button = {
    'menu': "Меню",

    'prod': "🍍Продукты",
    'prod_add': "Добавить продукт",
    'prod_update_count': "Изменить количество",
    'prod_update_cost': "Изменить цену",
    'prod_delete': "Удалить",
    'prod_add_new_category':"Добавить новую категорию",

    'order': "Заказы",
    'active_order': "Подробности заказа",
    'cancel_order': "Отменить заказ",
    'complete_order': "Выполнить заказ",

    'raffle': "Розыгрыш",
    'raffle_start': 'Начать розыгрыш',
    'raffle_info': "Информация об участниках",
    'raffle_end': "Закончить розыгрыш",
    'raffle_delete': "Очистить розыгрыш",

    'loc_num': "📞Изменить номер телефона локации",

    'report': "💼Отчёт",
    'report_moth': "За месяц",
    'report_all': "За всё время",
    'report_all_moth': "За всё время по месяцам",

    'date': "Изменить время доставки",
    'spam': "Рассылка"
}

#не редактировать
id_cancel_order = 0
id_client = 0
