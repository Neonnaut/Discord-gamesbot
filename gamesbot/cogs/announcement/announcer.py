from datetime import datetime, timedelta, time as other_time
import time as tea_time
import time
from typing import List
# import asyncpg
import aiosqlite
from discord import Embed

from constants import SKIPPEDWEEKS, PROJECTSTART, DIAMOND, DBFILE  # ,POSTGRES_KEY


class Announcer:
    def __init__(self):
        self.RECORDS: List = []

    async def get_record_from_cache(self, guildID):
        for record in self.RECORDS:
            my_record = record.get('server_id')
            if my_record == guildID:
                return record
        return None

    async def display_record(self, record, bot, guild_name):
        """
        We want to display a human-readable record with all our ID things as names
        and create an embed out of it.
        """
        stuff = []
        mockup = ''
        now = datetime.utcnow()
        for key, value in record.items():
            if key == 'repeat_every':
                value = f'{value.capitalize()} UTC'
            if key == 'channel_id':
                if value.isdigit():
                    value = bot.get_channel(int(value)).name.capitalize()
                key = 'channel name'
            elif key == 'next_announcement_date':
                date_announcement_date = datetime.strptime(
                    value, '%Y-%b-%d, %H:%M')
                value = f'<t:{int((time.mktime(date_announcement_date.timetuple())))}:F> ({value} UTC)'
                annoncementDate = value
            if key != 'server_id':
                stuff.append(f'{DIAMOND}**{key.capitalize().replace("_"," ")}**: '
                             + f'{value}')

        my_message = record.get('message')
        repeat_every = record.get('repeat_every')
        mockup = await self.format_message(
            my_message, guild_name, now, repeat_every, annoncementDate, date_announcement_date)

        embed = Embed(
            title=f'{guild_name} Announcement Settings',
            description='\n'.join(stuff),
            colour=0Xa69f9c
        )
        embed.add_field(name='Mockup Announcement', value=mockup)
        return embed

    async def format_message(
            self, message, guild_name,
            now, repeatEvery, announcementDate='N/A', myDelta='N/A'
    ):
        """
        We want to replace things enclosed in curly brackets in our message with
        a list of variables, where the thing and variable match, and return the message.
        """
        total_days = abs(PROJECTSTART - datetime.utcnow()).days
        day = total_days % 7 + 1
        week = total_days // 7 - SKIPPEDWEEKS + 1

        ingameyear = (week-1)*50 + ((day-1) * 7.142857142857143)

        weekpercent = ''

        day_percent_of_fifty = now - datetime.combine(now.date(), other_time())
        day_percent_of_fifty = day_percent_of_fifty.total_seconds() / 86400.0
        day_percent_of_fifty = day_percent_of_fifty * 100

        vars = {
            'repeatevery': f'{repeatEvery} UTC',
            'announcementdate': announcementDate,
            'server': guild_name,
            'week': week,
            'weekpercent': f'{weekpercent}%',
            'day': day,
            'ingameyears': f'{(week-1)*50} - {week*50} AS (weeks * 50)',
            'ingameyear': f'Circa {ingameyear} AS',
            'projectstart': f'<t:{int(tea_time.mktime(now.timetuple()))}:F> ({PROJECTSTART.strftime("%Y-%b-%d")} UTC)',
            'skippedweeks': str(SKIPPEDWEEKS),
            'timenow': f'<t:{int(tea_time.mktime(now.timetuple()))}:F> ({now.strftime("%Y-%b-%d, %H:%M")} UTC)',
            'timedelta': f'<t:{int(tea_time.mktime(myDelta.timetuple()))}:R>'
        }
        message = message.replace('\\n', '\n')
        for key, value in vars.items():
            message = message.replace('{'+key+'}', str(value))
        return message

    async def next_weekday(self, d: datetime, weekday, time_set=None):
        """
        We want to use a utcnow datetime and increase the date to the next weekday 
        from the weekday variable, and replace our datetime's
        hours and minutes with our time_set variable's hours and minutes.
        """
        myDate = d
        if time_set:
            divisions = time_set.split(':')
            if len(divisions) == 2:
                # removing the trailing zero of hours and minutes
                hour = int(divisions[0])
                minute = int(divisions[1])

                myDate = myDate.replace(hour=hour, minute=minute, second=0)

        if weekday == 'monday':
            weekday = 0
        elif weekday == 'tuesday':
            weekday = 1
        elif weekday == 'wednesday':
            weekday = 2
        elif weekday == 'thursday':
            weekday = 3
        elif weekday == 'friday':
            weekday = 4
        elif weekday == 'saturday':
            weekday = 5
        else:
            weekday = 6

        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            if myDate <= d:  # new date time has already happened this day
                days_ahead += 7

        myDate = myDate + timedelta(days_ahead)

        return myDate.strftime('%Y-%b-%d, %H:%M')

    async def update_cache_and_db(self, record: dict):
        """
        We want to update a record with an entirtely new record in the cache and db
        where the record's server_id matches the record's, else append as a new record
        """
        myServerId = record.get('server_id')

        updated = False
        # Update the cache with our new or updated record
        for i in range(0, len(self.RECORDS)):
            if self.RECORDS[i].get('server_id') == myServerId:
                # Update the record as it exists already
                self.RECORDS[i] = record
                updated = True
        if not updated:
            # The record does not exist yet
            self.RECORDS.append(record)

        conn = await aiosqlite.connect(DBFILE)
        await conn.execute('''
            INSERT OR REPLACE INTO Announcer
                (server_id, channel_id, message,
                next_announcement_date, repeat_every)
            VALUES
                ($1, $2, $3, $4, $5);''',
                           (record.get('server_id'), record.get('channel_id'),
                            record.get('message'), record.get(
                                'next_announcement_date'),
                               record.get('repeat_every'))
                           )
        await conn.commit()
        await conn.close()

        """
        conn = await asyncpg.connect(POSTGRES_KEY)
        await conn.execute('''
            INSERT INTO Announcer
                (server_id, channel_id, message, next_announcement_date, repeat_every)
            VALUES
                ($1, $2, $3, $4, $5)
            ON CONFLICT (server_id) DO UPDATE
                SET server_id = $1, channel_id = $2,
                message = $3, next_announcement_date = $4,
                repeat_every = $5;''',
            record.get('server_id'), record.get('channel_id'),
            record.get('message'), record.get('next_announcement_date'),
            record.get('repeat_every')
        )
        await conn.close()
        """

    async def get_db_and_set_cache(self):
        """Get records from database."""

        conn = await aiosqlite.connect(DBFILE)
        conn.row_factory = aiosqlite.Row
        # Create table if not exists
        await conn.execute('''CREATE TABLE IF NOT EXISTS Announcer
                (server_id  TEXT  PRIMARY KEY  NOT NULL,
                channel_id TEXT NOT NULL,
                message  TEXT  NOT NULL,
                next_announcement_date TEXT NOT NULL,          
                repeat_every TEXT  NOT NULL);''')
        await conn.commit()
        # Fetch our records with announcement data
        cur = await conn.execute('''SELECT
                server_id, channel_id, message, next_announcement_date, repeat_every
                FROM Announcer''')
        myRecords = await cur.fetchall()
        await cur.close()
        await conn.close()

        if myRecords == None:
            return None

        for record in myRecords:
            self.RECORDS.append(dict(record))

    async def delete_from_db(self, server_id: str):
        """Delete a rcord form our db and cache where the record's server_id matches."""

        conn = await aiosqlite.connect(DBFILE)
        cur = await conn.cursor()
        await cur.execute('''DELETE FROM Announcer
                WHERE server_id = $1''', (server_id,))
        await conn.commit()
        await cur.close()
        await conn.close()

        for record in self.RECORDS:
            if record.get('server_id') == server_id:
                self.RECORDS.remove(record)
                return None
