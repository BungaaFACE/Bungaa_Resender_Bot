from os.path import dirname, abspath, join
import os

ACCOUNTS_FOLDER = join(
    dirname(dirname(abspath(__file__))), 'accounts') + os.sep

# Параметры для пользовательского аккаунта
API_ID = ''
API_HASH = ''
REAL_ACCOUNT_ID = []
# Параметры для бота рассылки пользователям
RESENDER_API_KEY = ''
RESENDER_BOT_KEY = 
# Токен для оплаты
PROVIDER_TOKEN = ''
# DB file
SQLITE3_FILENAME = 'BungaaResenderDB.db'

# Prices
CURRENCY = 'RUB'
ONE_MONTH_PRICE = 300
