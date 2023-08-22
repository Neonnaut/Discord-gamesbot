import os
import aiosqlite
import discord
import logging
from typing import Optional
from discord.ext import commands
from constants import DBFILE, CHECK, PREFIX, DIAMOND

logger = logging.getLogger('logger')

COGSFILE = 'cogs.'

class Admin(commands.Cog, name='admin'):
    """For administrators only."""
    COG_EMOJI = '⚙️'

    def __init__(self, bot:commands.Bot):
        self.bot:discord.Client = bot

    @commands.command()
    @commands.is_owner()
    async def load_cog(self, ctx:commands.Context, *, cog:str):
        """Command which loads a cog.
        Example: `|p|load misc`"""
        cog = cog.casefold()
        try:
            await self.bot.load_extension(f'{COGSFILE}{cog}')
            #importlib.reload(module)
            await ctx.send(f'{CHECK} Successfully loaded: {cog}')
        except commands.ExtensionError as e:
            logger.exception(str(e))
            return await self.bot.send_error(ctx, e)

    @commands.command()
    @commands.is_owner()
    async def reload_cog(self, ctx:commands.Context, *, cog:str):
        """Command which reloads a cog.
        Example: `|p|reloadCog misc`"""
        cog = cog.casefold()
        try:
            await self.bot.unload_extension(f'{COGSFILE}{cog}')
            await self.bot.load_extension(f'{COGSFILE}{cog}')
        except commands.ExtensionError as e:
            logger.exception(str(e))
            return await self.bot.send_error(ctx, e)
        await ctx.send(f'{CHECK} Successfully reloaded: {cog}')

    @commands.command()
    @commands.is_owner()
    async def reload_cogs(self, ctx:commands.Context):
        """Command which reloads all cogs."""
        for cog in self.bot.cogs.keys():
            await self.bot.load_extension(f'{COGSFILE}{cog}')
            await self.bot.unload_extension(f'{COGSFILE}{cog}')
            try:
                await self.bot.load_extension(f'{COGSFILE}{cog}')
                await ctx.send(f'{CHECK} Reloaded {cog}')
            except commands.ExtensionError as e:
                logger.exception(str(e))
                await self.bot.send_error(ctx, f'Failed to reload. {cog}.')
        await ctx.send('Done.')

    @commands.command()
    @commands.is_owner()
    async def unload_cog(self, ctx:commands.Context, *, cog:str):
        """Command which unloads a cog.
        Example: `|p|unloadCog misc`"""
        cog = cog.casefold()
        if cog == 'admin':
            return await self.bot.send_error(ctx, 'The admin cog cannot be unloaded.')
        try:
            await self.bot.unload_extension(f'{COGSFILE}{cog}')
            await ctx.send(f'{CHECK} Successfully unloaded: {cog}')
        except commands.ExtensionError as e:
            logger.exception(str(e))
            return await self.bot.send_error(ctx, e)
        
    @commands.command()
    @commands.is_owner()
    async def list_cogs(self, ctx:commands.Context):
        """Lists all cogs."""
        cogs = [
            cog[:-3] if cog.endswith('.py') else cog
            for cog in sorted(os.listdir('./cogs'))
            if not cog.startswith('__') #and not os.path.isdir(f'./cogs/{cog}')
        ]
        embed = discord.Embed(
            title='Bot\'s Cogs',
            description='\n'.join([
                f'{"`✅`"if cog in self.bot.cogs.keys() else"`❌`"} {cog.capitalize()}'
                for cog in cogs
            ]) or 'None',
            colour=0Xa69f9c
        )
        embed.set_author(name=f'{self.bot.user.name}',icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def list_logs(self, ctx:commands.Context):
        """Lists last 12 logs in the log file."""
        try:
            logs = open('bot.log').read().splitlines()
        except:
            logs = '`None`'
        else:
            logs='\n\n'.join([
                log
                for log in logs
                if log != ''
            ])
            logs = logs[-4000:]

        embed = discord.Embed(
            title='Bot\'s Logs',
            description = f'```ansi\n{logs}```' if len(logs) > 0 else '`None`',
            colour=0Xa69f9c
        )
        embed.set_author(name=f'{self.bot.user.name}',icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def list_permissions(self, ctx:commands.Context):
        """Lists the bot's permissions."""
        embed = discord.Embed(title='Bot\'s Permissions', colour=0Xa69f9c)
        embed.add_field(
            name=f'{ctx.guild.name} Permissions',
            value='\n'.join([
                f'{"`❌`" if not value else "`✅`"} {name.lower().replace("_", " ").title()}'
                for name, value in ctx.guild.me.guild_permissions
            ]) or 'None'
        )
        embed.add_field(
            name='Intents',
            value='\n'.join([
                f'{"`❌`" if not value else "`✅`"} {name.lower().replace("_", " ").title()}'
                for name, value in discord.Intents.all()
            ]) or 'None'
        )
        embed.set_author(name=f'{self.bot.user.name}',icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def list_servers(self, ctx:commands.Context):
        """Lists all the servers the bot is in."""
        embed = discord.Embed(
            title='Servers Bot Is In',
            description='\n'.join([
                f'{DIAMOND} {guild}'
                for guild in self.bot.guilds
            ]) or 'None',
            colour=0Xa69f9c
        )
        embed.set_author(name=f'{self.bot.user.name}',icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def list_tables(self, ctx:commands.Context):
        """Lists all tables in bot's database."""
        output = []

        conn = await aiosqlite.connect(DBFILE)
        conn.text_factory = str
        cur = await conn.cursor()

        result = await cur.execute('SELECT name FROM sqlite_master WHERE type="table";')
        result = await result.fetchall()
        table_names = result

        for table_name in table_names:
            column_names = await cur.execute('PRAGMA table_info("%s")' % table_name)
            column_names = await column_names.fetchall()
            col_names = ', '.join(
                col_name[1]
                for col_name in column_names
            )
            output.append(f'{DIAMOND}**{table_name[0]}**: {col_names}')
        await conn.close()

        embed = discord.Embed(
            title='Tables in Bot\'s Database',
            description='\n'.join(output) or 'None',
            colour=0Xa69f9c
        )
        embed.set_author(name=f'{self.bot.user.name}',icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def change_nickname(self, ctx:commands.Context, *, name:str):
        """Changes the bot's nickname. Up to 20 characters only.
        Example: `|p|changeNickname Betty`"""
        if len(name) > 20:
            return await self.bot.send_error(ctx, 'The name is over 20 characters!')
        try:
            await ctx.guild.get_member(self.bot.user.id).edit(nick=name)
        except Exception as e:
            logger.exception(str(e))
            return await self.bot.send_error(ctx, e)
        await ctx.send(f"{CHECK} Bot's nickname has been changed to {name}!")

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def change_presence(self, ctx:commands.Context, activity:str, status:Optional[discord.Status]):
        """Changes the bot's nickname. Up to 20 characters only.
        Example: `|p|changeNickname Betty`"""
        try:
            await self.bot.change_presence(
                activity=discord.CustomActivity(name = activity),
                status=status
            )
        except Exception as e:
            logger.exception(str(e))
            return await self.bot.send_error(ctx, e)
        await ctx.send(f'{CHECK} Bot presence changed to activity: {activity}, status: {status}')

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def change_prefix(self, ctx:commands.Context, prefix:str):
        """Sets a custom prefix. Prefix must be ASCII and be no more than 3 characters."""
        if len(prefix) > 3:
            return await self.bot.send_error(ctx, 'The custom prefix is over 3 characters!')
        elif not prefix.isascii():
            return await self.bot.send_error(ctx, 'The custom prefix is not ASCI2!')
        try:
            self.bot.command_prefix = commands.when_mentioned_or(*[PREFIX, prefix])
        except Exception as e:
            logger.exception(str(e))
            return await self.bot.send_error(ctx, 'An error occured. Nothing happened')
        await ctx.send(f'{CHECK} The custom prefix has been succesfully changed.')

    @commands.command()
    @commands.is_owner()
    async def disable_command(self, ctx:commands.Context, command):
        """Disables a command."""
        command = self.bot.get_command(command)
        if not command:
            return await self.bot.send_error(ctx, f'Could not find command "{command}"')
        if not command.enabled:
            return await self.bot.send_error(ctx, 'This command is already disabled')
        command.update(enabled=False)
        await ctx.reply(f'{CHECK} {command.name.capitalize()} disabled.',mention_author=False)

    @commands.command()
    @commands.is_owner()
    async def enable_command(self, ctx:commands.Context, command):
        """(Re)Enables a command."""
        command = self.bot.get_command(command)
        if not command:
            return await self.bot.send_error(ctx, f'Could not find command "{command}"')
        if command.enabled:
            return await self.bot.send_error(ctx, 'This command is already enabled')
        command.update(enabled=True)
        await ctx.reply(f'{CHECK} {command.name.capitalize()} enabled.',mention_author=False)

    @commands.command()
    @commands.is_owner()
    async def leave_guild(self, ctx:commands.Context, *, guild_name):
        """Leaves a guild the bot is in."""
        guild = discord.utils.get(self.bot.guilds, name=guild_name)
        if guild is None:
            return await self.bot.send_error(ctx, 'No guild with that name found.')
        try:
            await guild.leave() # Guild found
            await ctx.send(f'I left {guild.name}!')
        except Exception as e:
            logger.exception(str(e))
            await self.bot.send_error(ctx, 'Not able to leave this guild.')

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def sleep(self, ctx:commands.Context):
        """This disconnects the bot."""
        for cog in sorted(os.listdir('./cogs')):
            if os.path.isdir(f'./cogs/{cog}') and not cog.startswith('__'):
                try:
                    await self.bot.unload_extension(f'cogs.{cog}._{cog}')
                except:
                    pass
        await ctx.send('Closing the connection.')
        logger.info('Closing the connection.')
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def sync_commands(self, ctx:commands.Context):
        """Syncs slash commands globaly."""
        try:
            commands = await self.bot.tree.sync(guild=None)
            await ctx.send(f'{CHECK} {len(commands)} slash commands synced!')
        except Exception as e:
            logger.exception(str(e))
            await self.bot.send_error(ctx, 'Slash commands were not synced!')

async def setup(bot: commands.bot):
    await bot.add_cog(Admin(bot))
