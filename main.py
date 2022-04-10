
import telebot 

from telebot import types
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage


import DataBase
import conf

state_storage = StateMemoryStorage()

bot = telebot.TeleBot(conf.configure["token"],
state_storage= state_storage)

d_r = DataBase.delete_orders_0()
for i in d_r:
    bot.send_message(i, conf.botMessage['delete_order'])

class MyStates(StatesGroup):
    main_menu = State()
    account = State()
    buy = State()
    buy_ = State()
    new_num_name = State()
    commentariy = State()
    com_ch = State()
    info_order = State()
    buy_product = State()
    add_cart = State()
    choice_ = State()

class adminStates(StatesGroup):
    admin = State()
    admin_menu = State()
    admin_choice = State()
    
    prod_ad = State()
    prod_ad_category = State()
    add_prod = State()
    prod_upcount = State()
    prod_upcost = State()
    prod_delete = State()
    prod_add_new_category = State()

    order_menu = State()
    order_info = State()
    order_cancel = State()
    order_complete = State()
    order_bonus = State()

    report_ = State()
    raffle_menu = State()
    loc_num = State()

    date = State()
    spam = State()

@bot.message_handler(commands=['start'])
def start_user(message):
    id_user = message.from_user.id
    if (message.from_user.username is None):
        bot.send_message(message.from_user.id, conf.botMessage['error_start'])
    else:
        if (DataBase.new_user(id_user)):
            DataBase.add_new_Client(id_user, message.from_user.username)
        DataBase.delete_location_user(message.from_user.id)
        photo = open("media/intro.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=conf.botMessage['welcome'])
        select_location(message)
    

@bot.message_handler(commands='admin')
def admin_enter(message):
    bot.send_message(message.chat.id, conf.admin['entry'])
    bot.set_state(message.from_user.id, adminStates.admin)

@bot.message_handler(commands='test')
def test(message):
    bot.send_message(message.chat.id, str(message.from_user.id) + " " + str(message.chat.id))

@bot.message_handler(state="*", commands='cancel')
def any_state(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, conf.botMessage['cancel'])

@bot.message_handler(state = MyStates.main_menu)
def menu(message):

    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
    if (message.text != conf.buttons['menu']):
        if (DataBase.check_location_user(message.from_user.id)):
            DataBase.set_location_user(message.from_user.id, message.text)

    with bot.retrieve_data(message.chat.id) as data:
        data['order'] = None
    
    markup_reply.add(conf.buttons['products'], conf.buttons['buy'], conf.buttons['account'], row_width = 2)

    if (DataBase.check_raffle()):
        if (message.from_user.username is None):
            bot.send_message(message.chat.id, conf.botMessage['raffle_error'])
        elif (DataBase.check_ticket(message.from_user.username)):
            markup_reply.add(conf.buttons['raffle_join'])

    bot.send_message(message.chat.id, conf.botMessage['menu'], reply_markup = markup_reply)
    bot.set_state(message.from_user.id, state=MyStates.choice_)

@bot.message_handler(state = MyStates.account)
def account_menu(message):
    info_user = DataBase.get_info_client(message.from_user.id)
    msg = ""
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    markup.add(conf.buttons['order_info'], conf.buttons['menu'], row_width=2)
    for row in info_user:
        msg = conf.botMessage['account'] % (row[0], row[1])
    if (not DataBase.check_ticket(message.from_user.username)):
        msg += conf.botMessage['raffle_ticket'] % (DataBase.get_ticket(message.from_user.username))
    orders_user = DataBase.get_bot_complete(message.from_user.id)
    for row in orders_user:
        if row[0] is not None and row[1] is not None:
            msg += conf.botMessage['active_order'] % (row[0], row[1])
            markup.add(conf.buttons['call'], conf.buttons['cancel_order'], row_width=2)
        else:
            msg += conf.botMessage['not_active_order']
    markup.add(conf.buttons['select_location'])
    bot.send_message(message.from_user.id, msg, reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.choice_)

@bot.message_handler(state = MyStates.info_order)
def order_info_client(message):
    info_ = DataBase.get_orders(message.from_user.id)
    msg = ""
    if (info_ is None):
        bot.send_message(message.from_user.id, conf.botMessage['not_info_orders'])
    else:
        for row in info_:
            if (row[3] is None and row[1] is None and row[2] is None):
                break
            else:
                msg += conf.botMessage['info_order'] % (row[3], row[1], row[2]) 
                msg += "\n"
        if (msg == ""):
            msg = conf.botMessage['empty_orders']
        bot.send_message(message.from_user.id, msg)
    bot.set_state(message.from_user.id, state=MyStates.choice_)

@bot.message_handler(state=MyStates.buy)
def buy_menu(message):
    location = DataBase.get_location_user(message.chat.id)
    list_category = DataBase.get_positive_category_in_location(location)

    markup=types.ReplyKeyboardMarkup(one_time_keyboard= True,resize_keyboard=True)
    with bot.retrieve_data(message.chat.id) as data:
        if (data['order'] is not None):
            markup.add(conf.buttons['end_buy'])
        else:
            markup.add(conf.buttons['back'])
    if (list_category is None):
        bot.send_message(message.chat.id, conf.botMessage['failed_location'])
    else:
        temp = [None,None]
        for row in enumerate(list_category):
            if (row[0]%3 == 2):
                markup.add(temp[0], temp[1], row[1][0], row_width=3)
                temp[0] = None
                temp[1] = None
            else:
                temp[row[0]%3] = row[1][0]
        if (temp[1] is not None):
            markup.add(temp[0], temp[1], row_width=2)
        elif (temp[0] is not None):
            markup.add(temp[0])
    bot.send_message(message.chat.id,conf.botMessage['category'],reply_markup=markup)
    bot.set_state(message.from_user.id, state=MyStates.buy_)

@bot.message_handler(state=MyStates.buy_)
def buy_menu_(message):
    if (message.text == conf.buttons['back']):
        bot.set_state(message.chat.id, state=MyStates.main_menu)
        menu(message)
    elif (message.text == conf.buttons['end_buy']):
        bot.set_state(message.chat.id, state= MyStates.new_num_name)
        num_name(message)
    else:
        location = DataBase.get_location_user(message.chat.id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard= True,resize_keyboard=True)
        list_products = DataBase.get_products_category_location(message.text, location)
        with bot.retrieve_data(message.chat.id) as data:
            if (data['order'] is not None):
                markup.add(conf.buttons['back'], conf.buttons['end_buy'], row_width=2)
            else:
                markup.add(conf.buttons['back'], conf.buttons['menu'], row_width=2)
        with bot.retrieve_data(message.chat.id) as data:
            data['category'] = message.text
        for row in list_products:
            markup.add(conf.buttons['prod'] % (row[1], row[5], row[0]))
        bot.send_message(message.chat.id, conf.botMessage['product'], reply_markup= markup)
        bot.set_state(message.from_user.id, MyStates.buy_product)

@bot.message_handler(state=MyStates.buy_product)
def buy_product(message):
    if (message.text == conf.buttons['menu']):
        get_text(message)
    elif(message.text == conf.buttons['back']):
        with bot.retrieve_data(message.chat.id) as data:
            message.text = data['category']
            bot.set_state(message.from_user.id, state=MyStates.buy)
            buy_menu(message)
    elif(message.text == conf.buttons['end_buy']):
        bot.set_state(message.chat.id, state= MyStates.new_num_name)
        num_name(message)
    else:
        id_product = ""
        temp = False
        for char in message.text:
            if (char == '[' or char == ']'):
                temp = not temp
            elif (temp):
                id_product += char
            

        markup = types.ReplyKeyboardMarkup(one_time_keyboard= True,resize_keyboard=True)

        markup.add(conf.buttons['back'])

        product = DataBase.get_product(int(id_product))
        list_count = []
        product_ = product[2]
        if (product_ > 5):
            product_ = 5
        i = 0
        while (product_ > i):
            i+=1
            list_count.append(str(i) + " шт.")
            
        if (len(list_count) == 5):
            markup.add(list_count[0], list_count[1], list_count[2], list_count[3], list_count[4], row_width=5)
        elif (len(list_count) == 4):
            markup.add(list_count[0], list_count[1], list_count[2], list_count[3], row_width=4)
        elif (len(list_count) == 3):
            markup.add(list_count[0], list_count[1], list_count[2], row_width=3)
        elif (len(list_count) == 2):
            markup.add(list_count[0], list_count[1], row_width=2)
        elif (len(list_count) == 1):
            markup.add(list_count[0])
        
        with bot.retrieve_data(message.chat.id) as data:
            data['id_prod'] = product[0]
            data['counts'] = product[2]
            data['cost'] = product[5]
        
        bot.send_message(message.chat.id, conf.botMessage['count'], reply_markup=markup)
        bot.set_state(message.from_user.id, state=MyStates.add_cart)

@bot.message_handler(state=MyStates.add_cart)
def add_new_order(message):
    if (message.text == conf.buttons['back']):
        with bot.retrieve_data(message.chat.id) as data:
            message.text = data['category']
            bot.set_state(message.from_user.id, state=MyStates.buy_)
            buy_menu_(message)
    else:
        count_ = ""
        for char in message.text:
                if (char == ' '):
                    break
                else:
                    count_ += char
            
        with bot.retrieve_data(message.chat.id) as data:
            temp = True
            try:
                count_ = int(count_)
                if (count_ > data['counts']):
                    a = int('s')
            except ValueError:
                bot.send_message(message.chat.id, conf.botMessage['error'])
                message.text = data['id_order'] + ':'
                bot.set_state(message.chat.id, state=MyStates.buy_product)
                buy_product(message)
                temp = False
            if (temp):
                if (data['order'] is None):
                    data['id_order'] = DataBase.add_new_Order(
                        data['id_prod'], 
                        message.from_user.id,
                        int(data['cost']) * count_, 
                        DataBase.get_location_user(message.from_user.id), 
                        count_)
                    data['order'] = data['id_order']
                else:
                    DataBase.add_plus_Order(
                        data['order'], 
                        message.from_user.id,
                        data['id_prod'],
                        int(data['cost']) * count_,
                        DataBase.get_location_user(message.from_user.id),
                        count_)
                DataBase.update_count_product(data['id_prod'], -1 * count_)
        
        markup = types.ReplyKeyboardMarkup(one_time_keyboard= True,resize_keyboard=True)
        markup.add(conf.buttons['continue'], conf.buttons['end_buy'], row_width=2)
        bot.send_message(message.chat.id, conf.botMessage['accept_order'], reply_markup=markup)
        bot.set_state(message.chat.id, state=MyStates.choice_)
    
    
    
@bot.message_handler(state = MyStates.new_num_name)
def num_name(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard= True)
    if (DataBase.check_num(message.from_user.id)):
        markup.add(conf.buttons['no'])
    else:
        markup.add(conf.buttons['yes'])
    bot.send_message(message.chat.id, conf.botMessage['num_name'], reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.commentariy)

@bot.message_handler(state = MyStates.commentariy)
def comm(message):
    if (message.text != conf.buttons['no'] or message.text != conf.buttons['yes']):
        DataBase.update_num_and_name(message.chat.id, message.text)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard= True,resize_keyboard=True)
    markup.add(conf.buttons['no'])
    bot.send_message(message.chat.id, conf.botMessage['comm'], reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.com_ch)

@bot.message_handler(state = MyStates.com_ch)
def last_comm(message):
    with bot.retrieve_data(message.chat.id) as data:
        if (message.text != conf.buttons['no']):
            DataBase.add_comm(data['order'], message.text)

        temp = data['order']
        msg = conf.botMessage['accept_cart'] + "\n" + conf.botMessage['order_date'] + DataBase.get_time_loc(DataBase.get_location_user(message.chat.id))
        bot.send_message(message.from_user.id, msg)
        DataBase.bot_complete_order(data['order'])
        for i in data:
            data[i] = None
        data['order_process'] = temp
    bot.set_state(message.chat.id, MyStates.main_menu)
    DataBase.increase_order(message.from_user.id)
    temp = DataBase.get_id_admins(DataBase.get_location_user(message.from_user.id))
    for i in temp:
        send_message_user(i, "Появился новый заказ")
    menu(message)

from pygost import gost34112012512
@bot.message_handler(state = adminStates.admin)
def admin_check(password):
    password.text = gost34112012512.new(password.text.encode("utf-8")).hexdigest()
    if (password.text == conf.configure['adminKey']):
        DataBase.set_state_user(password.from_user.id, "admin")
        bot.set_state(password.from_user.id, adminStates.admin_menu)
        admin_menu(password)
    else:
        bot.send_message(password.chat.id, conf.botMessage['error'])
        bot.set_state(password.from_user.id, MyStates.choice_)
        menu(password)

@bot.message_handler(state = adminStates.admin_menu)
def admin_menu(message):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
    markup_reply.add(conf.admin_button['prod'], conf.admin_button['order'], conf.admin_button['raffle'], conf.admin_button['loc_num'],conf.admin_button['report'],
                    conf.admin_button['date'], conf.admin_button['spam'], row_width=2)
    bot.send_message(message.chat.id, conf.admin['admin_menu'], reply_markup=markup_reply)
    bot.set_state(message.from_user.id, adminStates.admin_choice)

@bot.message_handler(state = adminStates.prod_ad)
def prod_menu(msg):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
    location = DataBase.get_location_user(msg.from_user.id)
    list_products = DataBase.get_all_location_products(location)
    markup_reply.add(conf.admin_button['prod_add'],conf.admin_button['prod_delete'], conf.admin_button['prod_add_new_category'],
                    conf.admin_button['prod_update_count'], conf.admin_button['prod_update_cost'], conf.admin_button['menu'], row_width=2)

    message_bot = ""
    for row in list_products:
        message_bot += str(row) + "\n"
    bot.send_message(msg.chat.id, message_bot, reply_markup = markup_reply)
    bot.set_state(msg.from_user.id, adminStates.admin_choice)

@bot.message_handler(state = adminStates.prod_ad_category)
def prod_ad_category(message):
    if (message.text == conf.buttons['back']):
        bot.set_state(message.from_user.id, adminStates.admin_menu)
        admin_menu(message)
    else:
        with bot.retrieve_data(message.chat.id) as data:
            data['cat'] = message.text
        bot.send_message(message.chat.id, conf.admin['prod_add'])
        bot.set_state(message.from_user.id, adminStates.add_prod)


@bot.message_handler(state = adminStates.add_prod)
def add_new_prod(message):
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup_reply.add(conf.buttons['back'])
    location = DataBase.get_location_user(message.from_user.id)
    if (message.text == conf.buttons['back']):
        bot.set_state(message.from_user.id, adminStates.admin_menu)
        admin_menu(message)
    else:
        row = tranc(message.text)
        try:
            with bot.retrieve_data(message.chat.id) as data:
                DataBase.add_new_Product(row[0], int(row[1]), data['cat'], location, int(row[2]))
            bot.send_message(message.from_user.id, conf.admin['accept'], reply_markup=markup_reply)
        except ValueError:
            bot.send_message(message.from_user.id, conf.botMessage['error'], reply_markup=markup_reply)

@bot.message_handler(state = adminStates.prod_upcount)
def update_count(message):
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup_reply.add(conf.buttons['back'])
    if (message.text == conf.buttons['back']):
        bot.set_state(message.from_user.id, adminStates.admin_menu)
        admin_menu(message)
    else:
        row = tranc(message.text)
        DataBase.set_count_product(int(row[0]),int(row[1]))
        bot.send_message(message.from_user.id, conf.admin['accept'], reply_markup=markup_reply)

@bot.message_handler(state = adminStates.prod_upcost)
def update_cost(message):
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup_reply.add(conf.buttons['back'])
    if (message.text == conf.buttons['back']):
        bot.set_state(message.from_user.id, adminStates.admin_menu)
        admin_menu(message)
    else:
        row = tranc(message.text)
        DataBase.set_cost_product(int(row[0]), int(row[1]))
        bot.send_message(message.from_user.id, conf.admin['accept'], reply_markup=markup_reply)

@bot.message_handler(state = adminStates.prod_delete)
def delete_prod(message):
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup_reply.add(conf.buttons['back'])
    if (message.text == conf.buttons['back']):
        bot.set_state(message.from_user.id, adminStates.admin_menu)
        admin_menu(message)
    else:
        row = int(message.text)
        DataBase.delete_prod(row)
        bot.send_message(message.from_user.id, conf.admin['accept'], reply_markup=markup_reply)

@bot.message_handler(state = adminStates.prod_add_new_category)
def add_new_cat(message):
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup_reply.add(conf.buttons['back'])
    if(message.text == conf.buttons['back']):
        bot.set_state(message.from_user.id, adminStates.admin_menu)
        admin_menu(message)
    else:
        DataBase.add_new_category(DataBase.get_location_user(message.chat.id), message.text)
        bot.send_message(message.chat.id, "Принято", reply_markup=markup_reply)



@bot.message_handler(state = adminStates.order_menu)
def order_menu(message):
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    list_active_orders = DataBase.get_active_orders(DataBase.get_location_user(message.from_user.id))
    msg = ""
    for row in list_active_orders:
        if (row[0] is None and row[1] is None):
            msg += conf.botMessage['not_active_order']
            break
        msg += conf.admin['active_order']%(row[0], row[1]) + "\n"
    if (msg == ""):
        msg = "Зачилься, заказов нету!"
    markup_reply.add(conf.admin_button['active_order'], conf.admin_button['menu'], conf.admin_button['cancel_order'], conf.admin_button['complete_order'], row_width=2)
    bot.send_message(message.from_user.id, msg, reply_markup=markup_reply)
    bot.set_state(message.from_user.id, adminStates.admin_choice)

@bot.message_handler(state = adminStates.order_info)
def order_info(message):
    id_order = int(message.text)
    id_client = DataBase.get_id_user(id_order)
    msg = "Номер телефона и имя: "
    temp = DataBase.get_num_name(id_client)
    if (temp is None):
        msg+= "Не указан"
    else:
        msg += temp
    msg += "\nНикнейм: " + DataBase.get_username_client(int(id_client))
    msg += "\nРепутация: "
    temp = DataBase.get_count_orders_client(id_client)
    for row in temp:
        msg += str(row[0]) + "/" + str(row[1])
    msg += "\nКоличество бонусов: "
    temp = DataBase.get_info_client(id_client)
    for row in temp:
        msg += str(row[0])
    msg += "\n\nСписок продуктов:\n"
    for row in DataBase.get_active_product_order(id_order):
        msg += str(row[0]) + " " + str(row[1]) + "шт.\n"
    msg += "\nКомментарий - "
    temp = DataBase.get_comm_order(id_order)
    if (temp is None):
        msg+= "Не указан"
    else:
        msg += temp
    bot.set_state(message.from_user.id, adminStates.admin_menu)
    bot.send_message(message.chat.id, msg)
    admin_menu(message)


@bot.message_handler(state = adminStates.order_cancel)
def order_cancel(message):
    try:
        id_order = int(message.text)
        DataBase.cancel_order(id_order)
        DataBase.increase_cancel_order(DataBase.get_id_user(id_order))
        bot.send_message(message.chat.id, "Укажите причину отмены")
        if (conf.id_cancel_order == 0):
            conf.id_cancel_order = id_order
    except ValueError:
        id_client = DataBase.get_id_user(conf.id_cancel_order)
        send_message_user(id_client, conf.botMessage['cancel_order'] + message.text)
        bot.set_state(message.from_user.id, adminStates.admin_menu)
        conf.id_cancel_order = 0
        admin_menu(message)
        
    

@bot.message_handler(state=adminStates.order_complete)
def order_complere(message):
    temp = DataBase.client_add_bonusese(int(message.text))
    send_message_user(temp[0], conf.botMessage['complete_order']%(temp[1]))
    DataBase.complete_order(int(message.text))
    conf.id_client = temp[0]
    bot.set_state(message.from_user.id, adminStates.order_bonus)
    bot.send_message(message.chat.id, "Сколько бонусов потратил клиент?")

@bot.message_handler(state = adminStates.order_bonus)
def minus_bonus(message):
    sign = -1 * int(message.text)
    DataBase.increase_bonuses(conf.id_client, sign)
    bot.send_message(message.chat.id, "Заказ выполнен")
    bot.set_state(message.chat.id, adminStates.admin_menu)
    admin_menu(message)

@bot.message_handler(state = adminStates.raffle_menu)
def raffle_menu(message):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
    markup_reply.add(conf.admin_button['raffle_info'], conf.admin_button['raffle_delete'], row_width=2)
    if (not DataBase.check_raffle()):
        markup_reply.add(conf.admin_button['raffle_start'])
    else:
        markup_reply.add(conf.admin_button['raffle_end'])
    markup_reply.add(conf.admin_button['menu'])
    bot.send_message(message.chat.id,conf.admin_button['raffle'], reply_markup=markup_reply)

@bot.message_handler(state = adminStates.loc_num)
def set_num_loc(message):
    DataBase.set_loc_num(message.text, DataBase.get_location_user(message.from_user.id))
    bot.send_message(message.chat.id, "Добавлен")
    bot.set_state(message.from_user.id, adminStates.admin_choice)
    
@bot.message_handler(state = adminStates.report_)
def report_call(message):
    if (message.text == conf.admin_button['report_moth']):
        bot.send_message(message.chat.id, "Напишите полный месяц (01-12)")
    elif (message.text == conf.admin_button['report_all']):
        temp = DataBase.report_all(DataBase.get_location_user(message.from_user.id))
        msg = "Количество заказов: " + str(temp[0])
        msg += "\nСумма: " + str(temp[1])
        msg += "\nСредний чек: " + str(temp[2])
        bot.send_message(message.chat.id, msg)

    elif (message.text == conf.admin_button['menu']):
        admin_menu(message)
    else:
        temp = DataBase.report_moth(message.text, DataBase.get_location_user(message.chat.id))
        msg = "Количество заказов: " + str(temp[0][0])
        msg += "\nСумма: " + str(temp[0][1])
        msg += "\nСредний чек: " + str(temp[0][2])
        msg += "\n\nТоп-5 продуктов:\n"
        for i in enumerate(temp[1]):
            if (i[0] == 5):
                break
            msg += str(i[0] + 1) + "." + str(i[1][0]) + " " + str(i[1][1]) + " шт.\n"

        bot.send_message(message.chat.id, msg)


@bot.message_handler(state = adminStates.date)
def set_new_date(message):
    DataBase.set_time_loc(DataBase.get_location_user(message.chat.id), message.text)
    bot.send_message(message.chat.id, "okok")
    bot.set_state(message.chat.id, adminStates.admin_menu)

@bot.message_handler(state = adminStates.spam)
def spam_all(message):
    if (message.text == conf.admin_button['menu']):
        bot.set_state(id, adminStates.admin_menu)
        admin_menu(message)
    else:
        temp = DataBase.get_all_id_clients()
        for i in temp:
            send_message_user(i, message.text)
        bot.set_state(message.chat.id, adminStates.admin_menu)
        admin_menu(message)

@bot.message_handler(state = adminStates.admin_choice)
def get_admin(message):
    id = message.from_user.id
    if (message.text == conf.admin_button['menu']):
        bot.set_state(id, adminStates.admin_menu)
        admin_menu(message)

    elif (message.text == conf.admin_button['prod']):
        bot.set_state(id, adminStates.prod_ad)
        prod_menu(message)
    elif (message.text == conf.admin_button['prod_add']):
        #Меня заставили!! Это стыдно НЕ ЧИТАЙТЕ
        temp = [None,None]
        list_category = DataBase.get_category_in_location(DataBase.get_location_user(message.from_user.id))
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        markup.add(conf.buttons['back'])
        for row in enumerate(list_category):
                if (row[0]%3 == 2):
                    markup.add(temp[0], temp[1], row[1][0], row_width=3)
                    temp[0] = None
                    temp[1] = None
                else:
                    temp[row[0]%3] = row[1][0]
        if (temp[1] is not None):
            markup.add(temp[0], temp[1], row_width=2)
        elif (temp[0] is not None):
            markup.add(temp[0])

        bot.send_message(id, "Выберите категорию", reply_markup= markup)
        bot.set_state(id, adminStates.prod_ad_category)
    elif (message.text == conf.admin_button['prod_update_count']):
        bot.send_message(id, conf.admin['prod_update_count'])
        bot.set_state(id, adminStates.prod_upcount)
    elif (message.text == conf.admin_button['prod_update_cost']):
        bot.send_message(id, conf.admin['prod_update_cost'])
        bot.set_state(id, adminStates.prod_upcost)
    elif (message.text == conf.admin_button['prod_delete']):
        id_prod_print(message)
        bot.set_state(id, adminStates.prod_delete)

    elif (message.text == conf.admin_button['prod_add_new_category']):
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        markup.add(conf.buttons['back'])
        bot.send_message(id, "Введите новую категорию", reply_markup= markup)
        bot.set_state(message.chat.id, adminStates.prod_add_new_category)

    elif (message.text == conf.admin_button['order']):
        bot.set_state(id, adminStates.order_menu)
        order_menu(message)
    elif (message.text == conf.admin_button['active_order']):
        id_order_print(message)
        bot.set_state(id, adminStates.order_info)
    elif (message.text == conf.admin_button['cancel_order']):
        id_order_print(message)
        bot.set_state(id, adminStates.order_cancel)
    elif (message.text == conf.admin_button['complete_order']):
        id_order_print(message)
        bot.set_state(id, adminStates.order_complete)

    elif (message.text == conf.admin_button['raffle']):
        raffle_menu(message)
    elif (message.text == conf.admin_button['raffle_start']):
        DataBase.new_raffle()
        bot.send_message(id, conf.admin_button['raffle_start'])
        raffle_menu(message)
    elif (message.text == conf.admin_button['raffle_info']):
        temp = DataBase.get_all_ticket()
        msg = ""
        for row in temp:
            msg += "@" + row[0] + " - " + str(row[1]) + "\n"
        if (msg == ""):
            msg = "Участников нету"
        bot.send_message(id, msg)
    elif (message.text == conf.admin_button['raffle_end']):
        DataBase.close_raffle()
        bot.send_message(id, conf.admin_button['raffle_end'])
        raffle_menu(message)
    elif (message.text == conf.admin_button['raffle_delete']):
        DataBase.delete_raffle()
        bot.send_message(id, conf.admin_button['raffle_delete'])
        

    elif(message.text == conf.admin_button['loc_num']):
        bot.send_message(message.chat.id, "Введите новый телефон для локации")
        bot.set_state(id, adminStates.loc_num)

    elif (message.text == conf.admin_button['report']):
        report_menu(message)

    elif (message.text == conf.admin_button['date']):
        bot.send_message(message.from_user.id, "Введите новое время доставки в формате 00-00")
        bot.set_state(message.from_user.id, adminStates.date)
    elif (message.text == conf.admin_button['spam']):
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
        markup_reply.add(conf.admin_button['menu'])
        bot.send_message(message.chat.id, "Введите текст рассылки", reply_markup=markup_reply)
        bot.set_state(message.chat.id, adminStates.spam)

@bot.message_handler(state = MyStates.choice_)
def get_text(message):
    if (message.text == conf.buttons['products']):
        show_products(message)

    elif (message.text == conf.buttons['buy']):
        orders_user = DataBase.get_bot_complete(message.from_user.id)
        for row in orders_user:
            if row[0] is not None:
                bot.send_message(message.chat.id, conf.botMessage['one_active_order'])
            else:
                bot.set_state(message.chat.id, MyStates.buy)
                buy_menu(message)
        

    elif (message.text == conf.buttons['account']):
        bot.set_state(message.chat.id, MyStates.account)
        account_menu(message)
    elif (message.text == conf.buttons['menu']):
        bot.set_state(message.chat.id, state = MyStates.main_menu)
        menu(message)

    elif (message.text == conf.buttons['select_location']):
        DataBase.delete_location_user(message.from_user.id)
        select_location(message)

    elif (message.text == conf.buttons['continue']):
        bot.set_state(message.chat.id, state=MyStates.buy)
        buy_menu(message)

    elif (message.text == conf.buttons['end_buy']):
        bot.set_state(message.chat.id, state= MyStates.new_num_name)
        num_name(message)

    elif (message.text == conf.buttons['order_info']):
        order_info_client(message)

    elif (message.text == conf.buttons['call']):
        temp = DataBase.get_num_loc(DataBase.get_location_user(message.from_user.id))
        if (temp is None):
            bot.send_message(message.chat.id, conf.botMessage['er'])
        else:
            bot.send_message(message.chat.id, temp)

    elif (message.text == conf.buttons['cancel_order']):
        temp = DataBase.get_bot_complete(message.from_user.id)
        for row in temp:
            DataBase.client_cancel_odrer(row[0])
            DataBase.cancel_order(row[0])        

        DataBase.increase_cancel_order(message.from_user.id)
        account_menu(message)

    elif (message.text == conf.buttons['raffle_join'] and DataBase.check_ticket(message.from_user.username)):
        if (DataBase.check_ticket(message.from_user.username)):
            DataBase.add_new_ticket(message.from_user.username)
            bot.send_message(message.chat.id, conf.botMessage['raffle_join']%(DataBase.get_ticket(message.from_user.username)))
    
    else:
        bot.send_message(message.chat.id, conf.botMessage['error'])

@bot.message_handler(content_types=['text'])
def get_state(message):
    if (message.text == conf.buttons['products']):
        show_products(message)
    elif (message.text == conf.buttons['account']):
        bot.set_state(message.chat.id, MyStates.account)
        account_menu(message)
    else: 
        bot.send_message(message.chat.id, conf.botMessage['error_state'])
        start_user(message)


def select_location(msg):
    markup=types.ReplyKeyboardMarkup(one_time_keyboard= True,resize_keyboard=True)
    list_location = DataBase.get_all_location()
    for row in list_location:
        if (not(row[0] is None)):
            markup.add(row[0])

    bot.send_message(msg.chat.id,conf.botMessage['location'],reply_markup=markup)
    bot.set_state(msg.from_user.id, MyStates.main_menu)

def report_menu(msg):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(conf.admin_button['report_moth'], conf.admin_button['report_all'], conf.admin_button['menu'], row_width=2)
    bot.send_message(msg.chat.id, "Выберите отчёт", reply_markup=markup)
    bot.set_state(msg.from_user.id, adminStates.report_)

def show_products(msg):
    location = DataBase.get_location_user(msg.from_user.id)
    list_products = DataBase.get_location_products(location)

    message_bot = ""
    #[0]-id,[1]-name,[2]-count,[3]-type,[4]-loc, [5]-cost
    temp = ""
    for row in list_products:
        temp = row[3].title()
        message_bot += temp + ":\n"
        break
    for row in list_products:
        if (temp != row[3].title()):
            message_bot += "\n" + row[3].title() + ":\n"
            temp = row[3].title()
        message_bot += conf.botMessage['prod_list']%(row[1], row[5]) + "\n"
    if (message_bot == ""):
        message_bot = conf.botMessage['empty_products']
    bot.send_message(msg.chat.id, message_bot)

def tranc(text):
    i = 0
    row = []
    row.append("")
    for c in text:
        if (c == '-'):
            i += 1
            row.append("")
        else:
            row[i] += c
    return row

def send_message_user(id, msg):
    bot.send_message(id, msg)

def id_order_print(message):
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    list_active_orders = DataBase.get_active_orders(DataBase.get_location_user(message.from_user.id))
    for row in list_active_orders:
        if (row[0] is None and row[1] is None):
            break
        markup_reply.add(str(row[0]))
    
    bot.send_message(message.from_user.id, conf.admin['id_order'], reply_markup=markup_reply)

def id_prod_print(message):
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    list_active_prod = DataBase.get_all_location_products(DataBase.get_location_user(message.from_user.id))
    markup_reply.add(conf.buttons['back'])

    for row in list_active_prod:
        if (row[0] is None and row[1] is None):
            break
        markup_reply.add(str(row[0]))
    
    bot.send_message(message.from_user.id, conf.admin['id_prod'], reply_markup=markup_reply)

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

bot.infinity_polling(skip_pending=True)

