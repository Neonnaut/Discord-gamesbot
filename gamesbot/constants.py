import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DISCORD_CLIENT = os.getenv('DISCORD_CLIENT')
PREFIX = '!!'
ACTIVITY = f'Waiting for {PREFIX} commands'
DESCRIPTION = 'A bot with commands for games, querying Google Sheets, and other utilities.'
TESTING = True if os.getenv('TESTING') == 'True' else False

DBFILE = 'bot.sqlite'

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
CHECK = '✅>'
ERR = '❌'
WARN = '⚠️'
DIAMOND = '🔸'

#POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')

"""
class Colour(Enum):
    default = 0XA69F9C
    red = 0xBA0202
    dark_red = 0x9E0F00
    orange = 0xD96D0D
    dark_orange = 0xAB4100
    brown = 0x523110
    yellow = 0xFFD414
    green = 0X45C33A
    dark_green = 0x116E06
    blue = 0x137AD4
    dark_blue = 0x145499
    teal = 0x18AB8E
    purple = 0xA30DE0
    dark_purple = 0x5C1C78
    blurple = 0x5865F2
    magenta = 0x990066
    pink = 0xf03799
    grey = 0x858588
    dark_grey = 0x3D3F45
    gray = grey
    dark_gray = dark_grey
    @classmethod
    def random(cls):
        return random.choice(list(cls.__members__.values()))
"""