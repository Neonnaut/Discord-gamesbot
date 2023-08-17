import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DISCORD_CLIENT = os.getenv('DISCORD_CLIENT')
PREFIX = '!!'
ACTIVITY = f'Waiting for {PREFIX} commands'
DESCRIPTION = 'A bot with commands for games, querying Google Sheets, and other utilities.'
DBFILE = 'bot.sqlite'
TESTING = True if os.getenv('TESTING') == 'True' else False

# Gsheets
GSHEETS_CLIENT = {
    'client_email': os.getenv('GSHEETS_EMAIL'),
    'private_key': os.getenv('GSHEETS_KEY'),
    'token_uri': 'https://oauth2.googleapis.com/token'
}
MOD_ROLE = 'Data Frogling'
ACTION_CATEGORY_NAME = '🎲 game'
SPECIAL_SHEETS = ['nations', 'cultures', 'nationsdata', 'culturesdata']
if TESTING:
    WORKBOOK_KEY = '1Fm4EgslzB3MKZR-5SX-KKYfmgVaDmzKfaBUp50oUJlw'
else:
    WORKBOOK_KEY = '13e43oDnum0HA6vE1XxsEuRY6MjVM28OQnrH2N18hZkU'

WEATHER_CLIENT = os.getenv('WEATHER_CLIENT')
REDDIT_CLIENT = os.getenv('REDDIT_CLIENT').split(',')
WORDLE_SORT_KEY = os.getenv('WORDLE_SORT_KEY')

# Stuff for the About command
STARTTIME = datetime.utcnow()
PROJECTSTART = datetime.strptime('2022, 10, 24', '%Y, %m, %d')
SKIPPEDWEEKS = int(1)

# Emojis
CHECK = '<:check:1001706162665832448>'
ERR = '<:err:1001706158786101269>'
WARN = '<:warn:1001706160438657109>'
INFO = '<:info:1003510951515005008>'
DIAMOND = '<:sgd:1135150741120622622>'

#POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')