import asyncio
from datetime import datetime
import logging
import re
import discord

from discord.ext import commands, tasks

from .announcer import Announcer

from constants import CHECK, TESTING

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class Announcement(commands.Cog, name='announcement'):
    """A group of commands to setup a weekly announcement."""
    COG_EMOJI = '📯'

    def __init__(self, bot):
        self.bot:discord.Client = bot
        self.announcer = Announcer() # To store announcements and do queries on them
        #if not TESTING:
        self.do_announce.start() # Start task
    def cog_unload(self):
        self.do_announce.cancel()

    async def cog_load(self):
        #if not TESTING:
        await self.announcer.get_db_and_set_cache()

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    @commands.guild_only()
    async def announcement(self, ctx:commands.Context) -> None:
        """A group of commands to setup a weekly announcement."""
        # Command group. Nothing to see here
        await ctx.send_help(ctx.command)
        
    @tasks.loop(minutes=20.0)
    async def do_announce(self):
        """
        In this task we are getting an array of announcement dicts and seeing which ones
        have a next_announcement_date that is equal to or earlier than utcnow().
        For these announcements, we get the server, channel, and message -
        and send the message. We then  increase the next_announcement_date to next week
        in the local cache and in the postgres database.
        """
        now = datetime.utcnow()

        # Go through the dict of dicts
        for record in self.announcer.RECORDS:
            next_announcement_date = record.get('next_announcement_date')
            next_announcement_date = datetime.strptime(next_announcement_date, '%Y-%b-%d, %H:%M')
            if next_announcement_date > now:
                await asyncio.sleep(1) # This guild is not announcing on this task loop
            else:
                try:
                    guild_id = record.get('server_id')
                    channel_id = record.get('channel_id')
                    
                    got_guild:discord.Guild = self.bot.get_guild(int(guild_id))
                    got_channel:discord.TextChannel = await got_guild.fetch_channel(int(channel_id))

                    myDelta = next_announcement_date

                    message = record.get('message')
                    message = await self.announcer.format_message(
                        message, got_guild.name, now, record.get('repeat_every'), record.get('next_announcement_date'), myDelta
                    )

                    await got_channel.send(message)
                    logger.info(f'Sent announcement from {got_guild.name}')

                except Exception as e:
                    logger.error(f'{e}\nDeleting announcement from db')
                    await self.announcer.delete_from_db(str(got_guild.id))

                repeat_every = record.get('repeat_every').split(' ')

                next_announcement_date = await self.announcer.next_weekday(
                    d=next_announcement_date, weekday=repeat_every[1])
                record.update({'next_announcement_date':next_announcement_date})

                # Update the cache and db with updated record
                await self.announcer.update_cache_and_db(record)

    @announcement.command(aliases=['create','make'])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def set(self, ctx:commands.Context, *, settings:str) -> None:
        """Sets what the message will be. Must format it like this:
        ```|p|announcement show
        message = <message>
        channel = <channel name>
        repeat every = <weekday> <HH>:<MM>```
        Message can have the following variables using curly brackets:
        {timedelta}, {timenow}, {repeatevery}, {announcementdate}, {server}, {week}, {day}, {ingameyear}, {ingameyears}, {projectstart}, {skippedweeks}"""
        if not await self.check_perms(ctx):
            return await self.bot.send_error(ctx, 'Permission denied')        
        
        now = datetime.utcnow()

        myRecord = await self.announcer.get_record_from_cache(str(ctx.guild.id))
        if myRecord is None:
            myRecord = {}

        myRecord.update({'server_id':str(ctx.guild.id)})

        settings = settings.replace(' | ', '\n')
        myLines = settings.split('\n')
        for line in myLines:
            things = line.split('=')
            if len(things) != 2:
                return await self.bot.send_error(ctx, f'Settings "{things}" not in format: message/channel/repeat every = <value>')
            things[0]=things[0].strip()
            things[1]=things[1].strip()

            if things[0] == 'channel':
                myChannel = discord.utils.get(ctx.guild.channels, name=things[1])
                if not myChannel:
                    return await self.bot.send_error(ctx, f'{things[0]} isn\'t a channel')
                myRecord.update({'channel_id':str(myChannel.id)})

            if things[0] == 'message':
                myRecord.update({'message':things[1]})

            if things[0] == 'repeat every':
                date = things[1].split(' ')
                if len(date) != 2:
                    return await self.bot.send_error(ctx, f'Settings was not in format: <##>:<##> <weekday>')
                date[1] = date[1].casefold()
                if date[1] not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                    return await self.bot.send_error(ctx, f'{date[1]} was not a day of the week')
                timeMatch = re.match('(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]', date[0])
                if not timeMatch:
                    return await self.bot.send_error(ctx, f'{date[0]} was not a 24 hour time in the format: ##:##')
                myRecord.update({'repeat_every':things[1]})

                next_announcement_date = await self.announcer.next_weekday(
                    d=now,
                    weekday=date[1],
                    time_set=date[0])
                myRecord.update({'next_announcement_date':next_announcement_date})

        if len(myRecord) != 5:
            return await self.bot.send_error(ctx, f'The announcement setting for this server does not yet have <message>, <channel> and/or a <repeat every> property yet.')
        
        # Update the cache and db with updated record
        await self.announcer.update_cache_and_db(myRecord)

        embed = await self.announcer.display_record(myRecord, self.bot, ctx.guild.name)
        await ctx.send(content=f'{CHECK} Announcement settings updated.', embed=embed)

    @announcement.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def delete(self, ctx:commands.Context):
        """Deletes announcement settings for this server."""
        if not await self.check_perms(ctx):
            return await self.bot.send_error(ctx, 'Permission denied')
        
        myRecord = await self.announcer.get_record_from_cache(str(ctx.guild.id))
        if myRecord == None:
            return await self.bot.send_error(ctx, 'No announcement set in this server')
        await self.announcer.delete_from_db(str(ctx.guild.id))
        await ctx.send(f'{CHECK} Announcement settings deleted.')

    @announcement.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def show(self, ctx:commands.Context):
        """Shows the announcement settings for this server."""
        myRecord = await self.announcer.get_record_from_cache(str(ctx.guild.id))
        if myRecord == None:
            return await self.bot.send_error(ctx, 'No announcement set in this server')
        embed = await self.announcer.display_record(myRecord, self.bot, ctx.guild.name)
        await ctx.send(embed=embed)

    async def check_perms(self, ctx:commands.Context) -> None:
        is_owner = await self.bot.is_owner(ctx.message.author)
        manage_messages = ctx.message.author.guild_permissions.manage_messages
        if is_owner == True or manage_messages == True:
            return True
        return False

    @do_announce.before_loop
    async def before_do_announcement(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.bot):
    await bot.add_cog(Announcement(bot))