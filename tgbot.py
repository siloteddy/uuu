
import sqlite3
import telebot
from  telebot import types


bot = telebot.TeleBot('6775955619:AAHnwgn7iy9ZSpOOj_GPGaCB4QxKXqpUxSU')

def executeAll(request):
    connection = sqlite3.connect(('shilorya.db'))
    cursor = connection.cursor()
    cursor.execute(request)
    data = cursor.fetchall()
    connection.close()
    return data

def executeOne(request):
    connection = sqlite3.connect('shilorya.db')
    cursor = connection.cursor()
    cursor.execute(request)
    data = cursor.fetchone()
    connection.close()
    return data

print('работает но я не уверена')

@bot.message_handler(commands=['start'])
def qwezxc(message):
    user_id = message.from_user.id
    balance = 0
    connection = sqlite3.connect('shilorya.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_exists = cursor.fetchone()

    if not user_exists:
        cursor.execute('INSERT INTO users (id, balance) VALUES (?, ?)', (user_id, balance))
    connection.commit()
    connection.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Мейн мейн меню', callback_data='menu'))
    markup.add(types.InlineKeyboardButton('История покупок', callback_data='history'))
    markup.add(types.InlineKeyboardButton('Узнать баланс', callback_data='balance'))
    markup.add(types.InlineKeyboardButton('Пополнить баланс', callback_data='addbal'))
    bot.send_photo(message.chat.id, photo=open("./qwe.jpg",  "rb"), caption=f"Привет, {message.chat.first_name}. Я бот-навигатор пользователя shilorya, где вы можете купить шмот из игры Dota 2!",reply_markup=markup)

# на рандомный текст ответ
@bot.message_handler()
def send_text(message):
    bot.send_message(message.chat.id, "Че ты ввел?")

# мейн мейн меню
@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def zxcqwe(call):
    if call.data == 'menu':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Dota 2', callback_data='dota'))
        markup.add(types.InlineKeyboardButton('Назад', callback_data='vozvrashenie'))
        bot.send_message(call.message.chat.id,  text='Давайте признаем, что игры лучше чем дота - не существует',reply_markup=markup)

#деняк на балансе
@bot.callback_query_handler(func=lambda call: call.data == 'balance')
def zxxxqwe(call):
   if call.data == 'balance':
        result = executeAll(f'SELECT balance FROM users WHERE id = {call.message.chat.id}')
        if result:
            balance = result[0]
            bot.send_message(call.message.chat.id, f'Текущий баланс:  {balance}')

#пополняем деньки
@bot.callback_query_handler(func=lambda call: call.data == 'addbal')
def qwzx(call):
   if call.data == 'addbal':
        connection = sqlite3.connect('shilorya.db')
        cursor = connection.cursor()
        user_id = call.from_user.id

        cursor.execute(f'SELECT balance FROM users WHERE id = {user_id}')
        result = cursor.fetchone()
        if result:
            balance = result[0]
            bot.send_message(call.message.chat.id, f'Текущий баланс: {balance}')
            bot.send_message(call.message.chat.id, 'Для пополнения баланса переведите деньги по номеру 4279 3806 5187 5702:')
            bot.register_next_step_handler(call.message, ewqzzx)

def ewqzzx(message):
        cash = int(message.text)
        user_id = message.from_user.id
        connection = sqlite3.connect('shilorya.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT balance FROM users WHERE id = {user_id}')
        result = cursor.fetchone()
        if result:
            balance = result[0]
            if cash > 0:
                qwiii = balance + cash
                cursor.execute(f'UPDATE users SET balance = {qwiii} WHERE id = {user_id}')
                connection.commit()
                connection.close()

# история
@bot.callback_query_handler(func=lambda call: call.data == 'history')
def qwzxqweqw(call):
    if call.data == 'history':
        user_id = call.from_user.id
        connection = sqlite3.connect('shilorya.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT * from bills WHERE user_id={user_id}')
        bills = cursor.fetchall()
        qwe = 'Приобретено:'
        for bill in bills:
            qwe += " {item_name}, {date}\n".format(item_name=bill[1], date=bill[2])
        cursor.close()
        connection.close()
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Бекаем', callback_data="vozvrashenie6")
        markup.add(btn1)
        bot.send_message(call.message.chat.id, qwe, reply_markup=markup)

# назад пиздуем(меню)
@bot.callback_query_handler(func=lambda call: call.data == 'vozvrashenie6')
def zwzwzaq(call):
    if call.data == 'vozvrashenie6':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Мейн мейн меню', callback_data='menu'))
        markup.add(types.InlineKeyboardButton('История покупок', callback_data='history'))
        markup.add(types.InlineKeyboardButton('Узнать баланс', callback_data='balance'))
        markup.add(types.InlineKeyboardButton('Пополнить баланс', callback_data='addbal'))
        bot.send_photo(call.message.chat.id, photo=open("./qwe.jpg",  "rb"), caption=f"Привет, {call.message.chat.first_name}. Я бот-навигатор пользователя shilorya, где вы можете купить шмот из игры Dota 2!",reply_markup=markup)


# из меню в товары

@bot.callback_query_handler(func=lambda call: call.data == 'dota')
def zxqweqeqww(call):
    connection = sqlite3.connect('shilorya.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM categories")
    data = cursor.fetchall()
    connection.close()
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Мой папа', url='https://clck.ru/37ACu7'))
    markup.add(types.InlineKeyboardButton('Назад', callback_data='vozvrashenie4'))
    for item in data:
        id, type = item
        markup.add(types.InlineKeyboardButton(type, callback_data=f'category_{id}'))

    bot.send_message(call.message.chat.id, parse_mode = "html", text="Выберите категорию товаров:", reply_markup=markup)
    

# в категорию какую-то
@bot.callback_query_handler(func=lambda call: call.data.startswith("category_"))
def qwxcweeq(call):
        category_id = call.data.split("_")[1] 
        connection = sqlite3.connect('shilorya.db')
        cursor = connection.cursor()
        zxc = f'''
               SELECT items.id, items.name
               FROM items
               INNER JOIN categories ON items.category_id = categories.id
               WHERE categories.id = {category_id}
               '''
        cursor.execute(zxc)
        data = cursor.fetchall()
        connection.close()

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Бекаем', callback_data='vozvrashenie5'))
        for item in data:
            item_id, item_name = item
            markup.add(types.InlineKeyboardButton(item_name, callback_data=f'item_{item_id}'))
        bot.send_message(call.message.chat.id, text = "Выбрал?", reply_markup=markup)


# из списка товаров в товары
@bot.callback_query_handler(func=lambda call: call.data.startswith("item_"))
def qwezxqawz(call):
    connection = sqlite3.connect('shilorya.db')
    cursor = connection.cursor()
    item_id = call.data.split("_")[1] 
    query = f'''
            SELECT name, price
            FROM items
            WHERE id = {item_id}
            '''
    cursor.execute(query)
    data = cursor.fetchone()
    item_name, item_price = data
    bot.send_message(call.message.chat.id, text=f"Название: {item_name}\nЦена: {item_price}")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Бекаем', callback_data='vozvrashenie6'))
    markup.add(types.InlineKeyboardButton('Купить', callback_data=f'buy_{item_id}'))
    bot.send_message(call.message.chat.id, "Для покупки сюдаа:", reply_markup=markup)

# покупаем
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def weqzxcq(call):
    connection = sqlite3.connect('shilorya.db')
    cursor = connection.cursor()
    user_id = call.from_user.id
    item_id = call.data.split("_")[1]
    
    item_query  = """
            SELECT name, price
            FROM items
            WHERE id = ?"""
    cursor.execute(item_query, (item_id,))
    item_data = cursor.fetchone()
    item_name, item_price_str = item_data
    item_price = int(item_price_str)
    
    balance_query = """
            SELECT balance
            FROM users
            WHERE id = ?"""
    cursor.execute(balance_query, (user_id,))
    user_balance = cursor.fetchone()[0]
    
    if user_balance >= item_price:
        new_balance = user_balance - item_price
        update_query = """
                   UPDATE users
                   SET balance = ?
                   WHERE id = ?"""
        cursor.execute(update_query, (new_balance, user_id))

        insert_query = """
                   INSERT INTO bills (user_id, item_id, date)
                   VALUES (?, ?, CURRENT_TIMESTAMP)"""
        cursor.execute(insert_query, (user_id, item_id))

        connection.commit()

        bot.send_message(call.message.chat.id, "Деньки есть")
    else:
        bot.send_message(call.message.chat.id, "Деняк нет")

# из выбранной в категории

@bot.callback_query_handler(func=lambda call: call.data == 'vozvrashenie5')
def qqqwzx(call):
    connection = sqlite3.connect('shilorya.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM categories")
    data = cursor.fetchall()
    connection.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Dota 2', callback_data='dota'))
    markup.add(types.InlineKeyboardButton('Назад', callback_data='vozvrashenie3'))
    for item in data:
        id, type = item
        markup.add(types.InlineKeyboardButton(type, callback_data=f'category_{id}'))
    bot.send_photo(call.message.chat.id,parse_mode= 'html',  photo=open('photo2.png',  'rb'), caption=f'Давайте признаем, что игры лучше чем дота - не существует',reply_markup=markup)

# из доты в меню
@bot.callback_query_handler(func=lambda call: call.data == "vozvrashenie4")
def sasaa(call):
   if call.data == "vozvrashenie4":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Dota 2', callback_data='dota'))
        markup.add(types.InlineKeyboardButton('Назад', callback_data='vozvrashenie2'))
        bot.send_photo(call.message.chat.id,parse_mode= 'html',  photo=open('photo2.png',  'rb'), caption=f'Давайте признаем, что игры лучше чем дота - не существует',reply_markup=markup)



# с мейн мейн в туда

@bot.callback_query_handler(func=lambda call: call.data == 'vozvrashenie2')
def callback_menu(call):
   if call.data == 'vozvrashenie2':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Мейн мейн меню', callback_data='menu'))
        markup.add(types.InlineKeyboardButton('История покупок', callback_data='history'))
        markup.add(types.InlineKeyboardButton('Узнать баланс', callback_data='balance'))
        markup.add(types.InlineKeyboardButton('Пополнить баланс', callback_data='addbal'))
        bot.send_photo(call.message.chat.id, photo=open("./qwe.jpg",  "rb"), caption=f"Привет, {call.message.chat.first_name}. Я бот-навигатор пользователя shilorya, где вы можете купить шмот из игры Dota 2!",reply_markup=markup)

# наааададвад

@bot.callback_query_handler(func=lambda call: call.data == "menu")
def zxcmama(call):
    if call.data == 'menu':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Мейн мейн меню', callback_data='menu'))
        markup.add(types.InlineKeyboardButton('История покупок', callback_data='history'))
        markup.add(types.InlineKeyboardButton('Узнать баланс', callback_data='balance'))
        markup.add(types.InlineKeyboardButton('Пополнить баланс', callback_data='addbal'))
        bot.send_photo(call.message.chat.id, photo=open("./qwe.jpg",  "rb"), caption=f"Привет, {call.message.chat.first_name}. Я бот-навигатор пользователя shilorya, где вы можете купить шмот из игры Dota 2!",reply_markup=markup)


bot.polling(none_stop=True, interval=0)












