import os
import telebot
import sqlite3
import random

# Mengambil token dari variabel environment Railway
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN tidak ditemukan!")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)

# --- Database ---
def init_db():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, name TEXT, level INTEGER, exp INTEGER, gold INTEGER)''')
    conn.commit()
    conn.close()

def get_user(user_id, name):
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = c.fetchone()
    if not user:
        c.execute("INSERT INTO users VALUES (?, ?, 1, 0, 0)", (user_id, name))
        conn.commit()
        user = (user_id, name, 1, 0, 0)
    conn.close()
    return user

def update_user(user_id, exp, gold):
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute("UPDATE users SET exp = exp + ?, gold = gold + ? WHERE user_id=?", (exp, gold, user_id))
    conn.commit()
    conn.close()

init_db()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    get_user(user_id, name)
    bot.reply_to(message, f"Halo {name}! Gunakan /hunt untuk bermain.")

@bot.message_handler(commands=['hunt'])
def hunt(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    exp, gold = random.randint(10, 20), random.randint(5, 15)
    update_user(user_id, exp, gold)
    bot.reply_to(message, f"🎯 Berhasil berburu!\n+ {exp} EXP\n+ {gold} Gold")

print("Bot Jalan...")
bot.infinity_polling()
