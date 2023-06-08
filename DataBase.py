import sqlite3
import conf

db = sqlite3.connect('DataBase.db', check_same_thread=False)
sql = db.cursor()

status = {
    0 : "Обрабатывается",
    1 : "Обработан",
    2 : "Принят",
    3 : "Выполнен",
    4 : "Отклонён",
    5 : "Отменён",
    'not_like': "Обр%" # = 1-3 буквам 0-1 статусу
}


# add
def add_new_Client(id:int, username:str):
    if username is None:
        username = "Empty"
    username = "@"+username
    sql.execute("INSERT INTO clients(id, username) VALUES (?, ?)", (id, username))
    db.commit()

def add_new_Order(id_product,id_client:int, cost:int, location:str, counts:int): 
    max_id = sql.execute("SELECT MAX(id_order) FROM orders").fetchone()
    for row in max_id:
        if (not(row is None)):
            TEMP = row
    max_id = TEMP + 1

    sql.execute("INSERT INTO orders(id_order, id_client, id_product, cost, location, date, counts) VALUES(?, ?, ?, ?, ?, date('now'), ?)", 
    (max_id, id_client, id_product, cost, location, counts))
    db.commit()
    return max_id

def add_plus_Order(id_order, id_client, id_prod, cost,location, counts):
    sql.execute("INSERT INTO orders(id_order, id_client, id_product, cost, location, date, counts) VALUES(?, ?, ?, ?, ?, date('now'), ?)", 
    (id_order, id_client, id_prod, cost*counts, location, counts))
    db.commit()

def add_new_Product(name:str, count:int, type_prod:str, location:str, cost:int): 
    max_id = sql.execute("SELECT MAX(id) FROM products").fetchone()
    max_id = int(max_id[0]) + 1

    sql.execute("INSERT INTO products VALUES(?, ?, ?, ?, ?, ?)", (max_id, name, count, type_prod, location, cost))
    db.commit()

def add_new_category(location, category):
    add_new_Product("Новая категория", 0, category, location, 0)

def add_comm(id, comm):
    sql.execute("INSERT INTO order_comm VALUES(?, ?)", (id, comm))
    db.commit()

# set
def increase_order(id:int):
    sql.execute("UPDATE clients SET count_orders = count_orders + 1 WHERE id = ?", (id,))
    db.commit()

def increase_cancel_order(id:int):
    sql.execute("UPDATE clients SET count_cancel_orders = count_cancel_orders + 1 WHERE id = ?", (id,))
    db.commit()

def update_count_product(id:int, sign:int):
    sql.execute("UPDATE products SET count = count + ? WHERE id = ?", (sign, id))
    db.commit()

def set_count_product(id,sign):
    sql.execute("UPDATE products SET count = ? WHERE id = ?", (sign, id))
    db.commit()

def set_cost_product(id,sign):
    sql.execute("UPDATE products SET cost = ? WHERE id = ?", (sign, id))
    db.commit()

def set_location_user(id:int, location:str):
    sql.execute("UPDATE clients SET location = ? WHERE id = ?", (location,id,))
    db.commit()

def update_num_and_name(id:int, num_name:str):
    sql.execute("UPDATE clients SET num_name = ? WHERE id = ?", (num_name,id,))
    db.commit()

def set_loc_num(numberPhone, location):
    temp = sql.execute("SELECT * FROM loc_num WHERE loc LIKE ?", (location,)).fetchone()
    if (temp is None):
        sql.execute("INSERT INTO loc_num(loc) VALUES (?)", (location,))
        db.commit
    sql.execute("UPDATE loc_num SET num = ? WHERE loc LIKE ?", (numberPhone, location))
    db.commit()

#update
def bot_complete_order(id:int):
    sql.execute("UPDATE orders SET status = ? WHERE id_order = ?", (status[1], id))
    db.commit()

def accept_order(id:int):
    sql.execute("UPDATE orders SET status = ? WHERE id_order = ?", (status[2], id))
    db.commit()

def complete_order(id:int):
    sql.execute("UPDATE orders SET status = ? WHERE id_order = ?", (status[3], id))
    db.commit()

def cancel_order(id:int):
    sql.execute("UPDATE orders SET status = ? WHERE id_order = ?", (status[4], id))
    db.commit()
    temp = get_id_product_in_order(id)
    for row in temp:
        if (not row[0] is None):
            update_count_product(row[0], row[1])

def client_cancel_odrer(id:int):
    sql.execute("UPDATE orders SET status = ? WHERE id_order = ?", (status[5], id))
    db.commit()

def client_add_bonusese(id:int):
    temp = get_order_(id)
    id_client = 0
    bonuses = 0
    for row in temp:
        if (not(row[0] is None and row[1] is None)):
            id_client = row[1]
            bonuses = row[0] * conf.persent_bonus
    sql.execute("UPDATE clients SET bonuses = bonuses + ? WHERE id = ?", (bonuses, id_client))
    db.commit()
    return id_client, bonuses

def increase_bonuses(id_client:int, sign:int):
    sql.execute("UPDATE clients SET bonuses = bonuses + ? WHERE id = ?", (sign, id_client))
    db.commit()

def update_product(id:int, count:int):
    sql.execute("UPDATE products SET count = ? WHERE id = ?", (count, id))
    db.commit()

def delete_prod (id:int):
    sql.execute("DELETE FROM products WHERE id = ?", (id,))
    db.commit()

def delete_location_user(id:int):
    sql.execute("UPDATE clients SET location = NULL WHERE id = ?", (id,))
    db.commit()

def delete_orders_0():
    list_id_orders = sql.execute("SELECT id_order FROM orders WHERE status like ?", (status[0],)).fetchall()
    rtn = []
    for id in list_id_orders:
        rtn.append(get_id_user(id[0]))
        temp = get_id_product_in_order(id[0])
        for row in temp:
            if (not row[0] is None):
                update_count_product(row[0], row[1])
        sql.execute("DELETE FROM orders WHERE status LIKE ?", (status[0],))
    db.commit()
    return rtn

def set_state_user(id, state):
    sql.execute("UPDATE clients SET state = ? WHERE id = ?", (state, id))
    db.commit()

def set_time_loc(location, times):
    sql.execute("UPDATE loc_num SET time = ? WHERE loc like ?", (times, location))
    db.commit()

#Геттеры
def get_username_client(id:int):
    temp = sql.execute("SELECT username FROM clients WHERE id = (?)", (id,)).fetchone()
    if (temp is None):
        return None
    for row in temp:
        return row

def get_location_user(id:int):
    temp = sql.execute("SELECT location FROM clients WHERE id = (?)", (id,)).fetchone()
    if (temp is None):
        return None
    for row in temp:
        return row
    
def get_all_products():
    return sql.execute("SELECT * FROM products").fetchall()

def get_location_products(location):
    return sql.execute("SELECT * FROM products WHERE location LIKE ? AND count > 0 ORDER BY type", (location,)).fetchall()

def get_all_location_products(location):
    return sql.execute("SELECT * FROM products WHERE location LIKE ?", (location,)).fetchall()

def get_count_orders_client(id:int):
    return sql.execute("SELECT count_orders, count_cancel_orders FROM clients WHERE id = ?", (id,))

def get_product(id:int):
    return sql.execute("SELECT * FROM products WHERE id = ?", (id,)).fetchone()

def get_products_category_location(category, location):
    return sql.execute("SELECT * FROM products WHERE type LIKE ? AND location LIKE ? AND count>0", (category, location)).fetchall()

def get_positive_category_in_location(location):
    return sql.execute("SELECT DISTINCT type FROM products WHERE location LIKE '" + location + "' AND count > 0").fetchall()

def get_category_in_location(location):
    return sql.execute("SELECT DISTINCT type FROM products WHERE location LIKE '" + location + "'").fetchall()

def get_empty_category_in_location(location):
    return sql.execute("SELECT type FROM products WHERE count = 0 AND type != (SELECT type FROM products WHERE location LIKE '" + location + "' AND count > 0);")

def get_orders(id:int):
    return sql.execute("SELECT id_order, SUM(cost),status , date FROM orders WHERE id_client = ? AND status NOT LIKE ? GROUP BY id_order", (id, status['not_like'])).fetchall()


def get_active_orders(location):
    return sql.execute("SELECT id_order, SUM(cost) FROM orders WHERE location LIKE ? and status LIKE ? GROUP BY id_order", (location, status[1])).fetchall()

def get_order_(id:int):
    return sql.execute("SELECT SUM(cost), id_client FROM orders WHERE id_order = ?", (id,))

def get_all_location():
    return sql.execute("SELECT DISTINCT location FROM products").fetchall()

def get_id_admins(location):
    temp = sql.execute("SELECT id FROM clients WHERE state LIKE 'admin' and location LIKE ?", (location,)).fetchall()
    rtn = []
    for row in temp:
        rtn.append(row[0])
    return rtn

def get_comm_order(id:int):
    temp = sql.execute("SELECT comm FROM order_comm WHERE id_order = ?", (id,)).fetchone()
    if (temp is None):
        return None
    for row in temp:
        return row

def get_active_product_order(id:int):
    return sql.execute("SELECT name, counts FROM orders, products WHERE id = id_product and id_order = ?", (id,)).fetchall()

def get_num_name(id:int):
    sql.execute("SELECT num_name FROM clients WHERE id = ?", (str(id),))
    temp = sql.fetchone()
    if (temp is None):
        return None
    for row in temp:
        return row


def get_id_user(id):
    temp = sql.execute("SELECT id_client FROM orders WHERE id_order = ?", (id,)).fetchone()
    if (temp is None):
        return None
    for row in temp:
        return row

def get_info_client(id:int):
    return sql.execute("SELECT bonuses, count_orders FROM clients WHERE id = (?)", (id,)).fetchall()

def get_bot_complete(id:int):
    return sql.execute("SELECT id_order, SUM(cost) FROM orders WHERE id_client = ? AND status = ?", (id, status[1])).fetchall()

def get_num_loc(location:str):
    temp =  sql.execute("SELECT num FROM loc_num WHERE loc LIKE ?", (location,))
    temp = sql.fetchone()
    if (temp is None):
        return None
    for row in temp:
        return row
    
def get_time_loc(location):
    temp = sql.execute("SELECT time FROM loc_num WHERE loc like ?", (location,)).fetchone()
    return temp[0]

def get_id_product_in_order(id:int):
    return sql.execute("SELECT id_product, counts FROM orders WHERE id_order = ?", (id,)).fetchall()

def get_all_id_clients():
    temp = sql.execute("SELECT id FROM clients").fetchall()
    rtn = []
    for i in temp:
        rtn.append(i[0])
    return rtn
   
#bool
def new_user(id:int):
    temp = sql.execute("SELECT id FROM clients WHERE id = " + str(id)).fetchone()
    if temp is None:
        return True
    else:
        return False

def check_location_user(id:int):
    temp  = get_location_user(id)
    if (temp is None):
        return True
    return False

def check_order(id:int):
    temp = sql.execute("SELECT id_order FROM orders WHERE id_order = (?)", (id,)).fetchone()
    if (temp is None):
        return True
    return False

def check_num(id:int):
    temp = sql.execute("SELECT num_name FROM clients WHERE id = (?)", (id,)).fetchone()
    for row in temp:
        if row is None:
            return True
        else:
            return False



#raffle

def get_ticket(first_name):
    temp = sql.execute("SELECT ticket FROM raffle WHERE user LIKE ?", (first_name,))
    for c in temp:
        return int(c[0])
def add_new_ticket(last_name):
    temp = 0
    max_id = sql.execute("SELECT MAX(ticket) FROM raffle").fetchone()
    for row in max_id:
        if (not(row is None)):
            temp = row
    max_id = temp + 1

    sql.execute("INSERT INTO raffle VALUES(?, ?)", (last_name, max_id))
    db.commit()




def check_ticket(last_name):
    temp = sql.execute("SELECT ticket FROM raffle WHERE user = ?", (last_name,)).fetchone()
    if (temp is None):
        return True
    else:
        return False

def get_all_ticket():
    return sql.execute("SELECT * FROM raffle").fetchall()

def new_raffle():
    sql.execute("UPDATE booling SET raffle = 1")
    db.commit()

def close_raffle():
    sql.execute("UPDATE booling SET raffle = 0")
    db.commit()

def delete_raffle():
    sql.execute("DELETE FROM raffle")
    db.commit()

def check_raffle():
    temp = sql.execute("SELECT raffle FROM booling").fetchone()
    for i in temp:
        if (temp[0]):
            return True
        else:
            return False

def report_moth(date, location):
    date = "2022-" + date + "%"
    rtn = [sql.execute("SELECT SUM(cnt), SUM(pr), AVG(vg) FROM (SELECT COUNT(DISTINCT id_order) as cnt, SUM(cost) as pr, AVG(cost) as vg FROM orders WHERE date LIKE ? and status LIKE ? and location LIKE ? GROUP BY date ) as a",
            (date, status[3], location)).fetchone()] 
    rtn.append(sql.execute("SELECT name, SUM(counts) as top FROM orders, products WHERE id = id_product and date like ? and orders.location like ? and status like ? GROUP BY id_product ORDER BY top DESC",
            (date, location, status[3])))
    return rtn

def report_all(location):
    return sql.execute("SELECT SUM(cnt), SUM(pr), AVG(vg) FROM (SELECT COUNT(DISTINCT id_order) as cnt, SUM(cost) as pr, AVG(cost) as vg FROM orders WHERE status LIKE ? and location LIKE ? GROUP BY date ) as a",
            (status[3], location)).fetchone()

#Tests
id_cl = 470070588
id_pr = 4
cnt = 100
num = 540
long_str = "Juja, Puja, Check"
one_str = ["One", "Two", "Three"]




        # if row is not None:
        #     print(conf.botMessage['active_order'] % (row[0], row[1]))
#add_new_Client(id_cl)
#add_new_Order(long_str, id_cl, num, one_str[0])
#add_new_Product(one_str[0], cnt, one_str[1], one_str[2], num)

# increase_order(id_cl)
# increase_cancel_order(id_cl)
# update_count_product(id_pr, -7)

# accept_order(1)
# cancel_order(2)
# complete_order(3)
# update_product(3, 228)