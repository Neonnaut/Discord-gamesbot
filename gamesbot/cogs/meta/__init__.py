from typing import List, Optional
import time as tea_time

import discord
from discord import app_commands
from discord.ext import commands

from .help import MyHelpCommand
from .about import get_bot, get_project, get_system

from constants import DIAMOND, DESCRIPTION


class Meta(commands.Cog, name='meta'):
    """Meta commands."""
    COG_EMOJI = '🏛'

    def __init__(self, bot: discord.Client):
        self.bot:discord.Client = bot

        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    @app_commands.command()
    async def help(self, interaction: discord.Interaction, command: Optional[str]):
        """Shows help on a command or category of commands."""

        ctx = await self.bot.get_context(interaction, cls=commands.Context)
        #await ctx.reply(f'{INFO} Help on prefix commands', mention_author=False, delete_after=3)
        if command is not None and command != 'all':
            await ctx.send_help(command)
        else:
            await ctx.send_help()

    @help.autocomplete('command')
    async def command_autocomplete(self, interaction: discord.Interaction, needle: str) -> List[app_commands.Choice[str]]:
        assert self.bot.help_command
        ctx = await self.bot.get_context(interaction, cls=commands.Context)
        help_command = self.bot.help_command.copy()
        help_command.context = ctx
        """
        if not needle:
            return [
                app_commands.Choice(name=f'{getattr(cog, 'COG_EMOJI', None)} {cog_name}', value=cog_name)
                for cog_name, cog in self.bot.cogs.items()
                if await help_command.filter_commands(cog.get_commands())
            ][:25]
        """
        if needle:
            needle = needle.lower()

            return_commands = []
            for command in await help_command.filter_commands(self.bot.walk_commands(), sort=True):
                if needle in command.qualified_name:
                    return_commands.append(app_commands.Choice(name=command.qualified_name, value=command.qualified_name))

            for cog_name, cog in self.bot.cogs.items():
                if needle in cog_name.casefold():
                    return_commands.append(app_commands.Choice(name=f'{getattr(cog, "COG_EMOJI", None)} {cog_name}', value=cog_name))

            return_commands = return_commands[:10]

            return return_commands
        else:
            return [app_commands.Choice(name='Type a command or category...', value='all')]

    @commands.hybrid_command(aliases=['uptime', 'botInfo', 'status','info'])
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def about(self, ctx:commands.Context):
        """Shows info about this bot and the project."""
        async with ctx.typing():
            embed = discord.Embed(
                title=f'About {self.bot.user.name}',
                description=f'{DESCRIPTION if DESCRIPTION!=""else"..."}\n'\
                    +f'Use `{ctx.clean_prefix}help` for a list of commands.\n',
                colour=0Xa69f9c
            )
            embed.set_author(name=f'{self.bot.user.name}',icon_url=self.bot.user.avatar.url)
            embed.add_field(name='Bot', inline=False, value=await get_bot(self.bot))
            embed.add_field(name='System', inline=False, value=await get_system())
            embed.add_field(name='Project', inline=False, value=await get_project())

            await ctx.send(embed=embed)

    @commands.command(aliases=['roleinfo'])
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def role_info(self, ctx:commands.Context, *, role: discord.Role):
        """Shows information about a server role."""
        try:
            name = role.name

            members = []
            for index, member in enumerate(role.members):
                myName = member.nick or member
                members.append(str(myName))

            if len(members) == 0 or len(members) > 6:
                members = str(len(members))
            else:
                members = ', '.join(members)

            mentionable = role.mentionable
            position = role.position
            colour = role.colour
            created = role.created_at.strftime('%Y %b %d')

            permissions = []
            for index, permission in enumerate(role.permissions):
                if permission[1] == True:

                    permissions.append(
                        permission[0].upper().replace('_', ' '))
            if len(permissions) == 0:
                permissions = 'None'
            else:
                permissions = ', '.join(permissions)

        except:
            return await self.bot.send_error(ctx, f'{role} not found.')

        embed = discord.Embed(
            colour=colour,
            title=f'Information about this role:'
        )
        embed.set_author(
            name=f'{ctx.guild.name}',
            icon_url=ctx.guild.icon
        )
        embed.add_field(
            inline=True,
            name=f'**Name**: {name}',
            value=f'▫{DIAMOND}**Created**: {created}\n'
            + f'{DIAMOND}**Position**: {position}\n'
            + f'{DIAMOND}**Mentionable**: {mentionable}\n'
            + f'{DIAMOND}**Members**: {members}\n'
            + f'{DIAMOND}**Permissions**: {permissions}\n'
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['serverinfo'])
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def server_info(self, ctx:commands.Context):
        """Shows information about this server."""

        onlineCount = await self.bot.fetch_guild(ctx.guild.id, with_counts=True)
        onlineCount = onlineCount.approximate_presence_count
        server: discord.Guild = ctx.guild
        try:
            numberofbots = 0
            for member in ctx.guild.members:
                if member.bot:
                    numberofbots += 1
            name = server.name
            members = f'{str(server.member_count)} ({numberofbots} Bots), {onlineCount} Online'
            icon = server.icon
            verification = str(server.verification_level).capitalize()
            created = f'<t:{int(tea_time.mktime(server.created_at.timetuple()))}:D>, '\
                f'<t:{int(tea_time.mktime(server.created_at.timetuple()))}:R>'
            owner = server.owner.nick
            channels = f'{len(server.text_channels)} Text, {len(server.voice_channels)} Voice, {len(server.categories)} Categories'
            features = ', '.join([
                str(feature).capitalize()
                for feature in server.features
            ]) or 'None'

            banner = server.banner

        except Exception as e:
            await ctx.send(f'{e} {str(server)} not found.')
            return

        embed = discord.Embed(
            title=f'Information About This Server', colour=0Xa69f9c
        )
        embed.add_field(
            inline=True,
            name=f'**Name**: {name}',
            value=f'{DIAMOND}**Owner**: {owner}\n'
            + f'{DIAMOND}**Members**: {members}\n'
            + f'{DIAMOND}**Channels**: {channels}\n'
            + f'{DIAMOND}**Created**: {created}\n'
            + f'{DIAMOND}**Features**: {features}\n'
            + f'{DIAMOND}**Verification Level**: {verification}\n'
        )

        if icon:
            embed.set_thumbnail(url=icon)
        if banner:
            embed.set_image(url=banner)
        await ctx.send(embed=embed)

    @commands.hybrid_command(aliases=['joined','userinfo'])
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def user_info(self, ctx:commands.Context, *, member: Optional[discord.Member]):
        """Shows information about a member.
        Or shows information about yourself if none specified."""

        if ctx.current_argument == None:
            member = ctx.message.author
        elif member == None:
            return await self.bot.send_error(ctx, f'"{ctx.current_argument}" not found.')
        try:
            roles = []
            if member.top_role.name != '@everyone':
                roles.append(f'<@&{str(member.top_role.id)}>')
            for role in member.roles:
                if str(role.name) == '@everyone':
                    roles.append('@everyone')
                elif str(role.id) != str(member.top_role.id):
                    roles.append(f'<@&{str(role.id)}>')
            roles = '**Roles**: ' + ' '.join(roles) or ''

            status = str(member.status).capitalize() if not str(member.status) == 'dnd' else 'Do not disturb'
            is_bot = member.bot
            activity = member.activity

            try:
                if activity:
                    if activity.type == discord.ActivityType.listening:
                        if activity.name.casefold() == 'spotify':
                            activity = f'**Listening To**: [{activity.title}]({activity.track_url}), by {activity.artist}'
                        else:
                            activity = f'**Listening To**: {activity.name}'

                    elif activity.type == discord.ActivityType.playing:
                        activity = f'**Playing**: {activity.name}'

                    elif activity.type == discord.ActivityType.competing:
                        activity = f'**Competing In**: {activity.name}'

                    elif activity.type == discord.ActivityType.streaming:
                        activity = f'**Streaming**: [{activity.name}]({activity.url}) -- {activity.game}'

                    else:
                        activity = f'**Activity**: {activity.name}'

                    activity += '\n'
                else:
                    activity = ''
            except:
                activity = ''

            colour = member.colour
            created = f'<t:{int(tea_time.mktime(member.created_at.timetuple()))}:D>, '\
                f'<t:{int(tea_time.mktime(member.created_at.timetuple()))}:R>'
            joined = f'<t:{int(tea_time.mktime(member.joined_at.timetuple()))}:D>, '\
                f'<t:{int(tea_time.mktime(member.joined_at.timetuple()))}:R>'
            avatar = member.avatar
        except:
            return await self.bot.send_error(ctx, f'{member} not found.')

        embed = discord.Embed(
            colour=colour,
            title=f'Information About {"Bot" if is_bot else "User"}: **{member.display_name}**',
            description=f'{DIAMOND}**Global Display Name**: {member.global_name if member.global_name else member}\n'\
            f'{DIAMOND}**Status**: {status}\n'\
            f'{DIAMOND + activity if activity else ""}'\
            f'{DIAMOND}**Account Creation**: {created}\n'\
            f'{DIAMOND}**Joined Server**: {joined}\n'\
            f'{DIAMOND + roles if roles else ""}\n'
        )

        ua=await self.bot.fetch_user(member.id)
        if ua.banner:
            embed.set_image(url=ua.banner.url)
        embed.set_thumbnail(url=avatar)

        await ctx.send(embed=embed)

async def setup(bot: commands.bot):
    await bot.add_cog(Meta(bot))
