from datetime import datetime, time
import time as tea_time
import os
import platform
import re
import subprocess
import psutil
from pathlib import Path
from discord import __version__ as dpy_version, Client

from constants import DESCRIPTION, PROJECTSTART, SKIPPEDWEEKS, STARTTIME, DIAMOND

async def get_bot(bot:Client):
    # what this is doing is subtracting the date from the bot initialised date
    # and displaying it as the uptime in days.
    unformatted_uptime = abs(datetime.utcnow() - STARTTIME)
    days = unformatted_uptime.days
    hours = unformatted_uptime.seconds//3600
    days = f'{days} day{"" if days == 1 else "s"}'
    hours = f'{hours} hour{"" if hours == 1 else "s"}'

    try:
        bmem = f'{psutil.Process().memory_info().rss/1000000:.2f}'
        bstore = f'{sum(f.stat().st_size for f in Path(".").glob("**/*") if f.is_file())/1024/1024:.2f}'
    except Exception as e:
        bmem = '?'
        bstore = '?'
    
    format=\
    f'{DIAMOND} Uptime: `{days}`, `{hours}`'\
    f'\n{DIAMOND} No̱ of Guilds In: `{len(bot.guilds)}`'\
    f'\n{DIAMOND} No̱ of Commands: `{len(bot.commands)}`'\
    f'\n{DIAMOND} Bot Storage Size: `{bstore} MB`'\
    f'\n{DIAMOND} Bot Memory: `{bmem} MB`'\
    f'\n{DIAMOND} Latency: `{round(bot.latency * 1000, 2)} ms`'\
    f'\n{DIAMOND} Owner: {f"<@{bot.owner_id}>" if bot.owner_id else "?"}'\
    f'\n{DIAMOND} Python Version: `{platform.python_version()}`'\
    f'\n{DIAMOND} Discord.py Version: `{dpy_version}`'
    return format

async def get_system():
    uname = platform.uname()
    mem = psutil.virtual_memory()
    sto = psutil.disk_usage('/')
    try:
        format =\
        f'{DIAMOND} OS: `{uname.system} {uname.machine}`'\
        f'\n{DIAMOND} HDD: `{sto.percent}%` of `{sto.total/1024/1024:.2f} MB`'\
        f'\n{DIAMOND} RAM: `{mem.percent}%` of `{mem.total/1000000:.2f} MB`'\
        f'\n{DIAMOND} CPU: `{psutil.cpu_percent(interval=0.5)}%`'\
        f'\n{DIAMOND} CPU Model: `{get_processor_name().strip()}`'
        return format
    except Exception as e:
        return f'{e}'

async def get_project():
    now = datetime.utcnow()

    total_days = abs(PROJECTSTART - now).days
    day = total_days % 7 + 1
    week = total_days // 7 - SKIPPEDWEEKS + 1

    ingameyear = (week-1)*50 + ((day-1) * 7.142857142857143)

    day_percent_of_fifty = now - datetime.combine(now.date(), time())
    day_percent_of_fifty =  day_percent_of_fifty.total_seconds() / 86400.0

    ingameyear = int(ingameyear + day_percent_of_fifty)
    
    format=\
    f'{DIAMOND} Week: `{week}`, day: `{day}`'\
    f'\n{DIAMOND} Skipped Weeks: `{SKIPPEDWEEKS}`'\
    f'\n{DIAMOND} First day of Project Timeline: {PROJECTSTART.strftime("%Y-%b-%d")} UTC, <t:{int(tea_time.mktime(PROJECTSTART.timetuple()))}:R>'\
    f'\n{DIAMOND} Time now: {now.strftime("%Y-%b-%d, %H:%M")} UTC, <t:{int(tea_time.mktime(now.timetuple()))}:R>'
    return format

def get_processor_name():
    if platform.system() == 'Windows':
        return platform.processor()
    elif platform.system() == 'Darwin':
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command ='sysctl -n machdep.cpu.brand_string'
        return subprocess.check_output(command).strip()
    elif platform.system() == 'Linux':
        command = 'cat /proc/cpuinfo'
        all_info = subprocess.check_output(command, shell=True).decode().strip()
        for line in all_info.split('\n'):
            if 'model name' in line:
                return re.sub( '.*model name.*:', '', line,1)
    return '?'