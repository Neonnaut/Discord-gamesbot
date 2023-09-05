from random import SystemRandom
from typing import Optional

import discord
import sympy
from constants import CHECK
from discord.ext import commands

from .chess.lobby import Chess_Lobby
from .flag_guesser import check_flag_guess, get_flag
from .minesweeper import print_minesweeper
from .place import Matrix
from .wordle import (
    daily_puzzle_id, generate_info_embed, generate_puzzle_embed,
    process_message_as_guess, random_puzzle_id
)


class Games(commands.Cog, name='games'):
    """Games like Chess, Wordle or a flag guessing game."""
    COG_EMOJI = '🕹️'

    def __init__(self, bot: discord.Client):
        self.bot:discord.Client = bot

        self.chess_lobby = Chess_Lobby(max_matches=3)

    @commands.hybrid_command(description='Plays chess : @<challengee> | <move> | concede | help.')
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    @discord.app_commands.describe(action='@<challengee>, <move>, concede, or help')
    async def chess(self, ctx:commands.Context, *, action):
        """
        Play a standard game of Chess with the bot or another user.
        Use `|h|chess info` for more information.
        """
        async with ctx.typing():
            ## Send help embed
            if action in ['info','help','?',None,'']:
                return await ctx.reply(embed=await self.chess_lobby.show_info_embed(ctx.clean_prefix),
                                    mention_author=False, ephemeral=False)
            ## List running chess matches
            if action in ['list matches','list']:
                return await ctx.reply(await self.chess_lobby.list_matches(),
                                    mention_author=False, ephemeral=False)            
            ## Concede
            elif action in ['concede','forfeit','quit','end']:
                myMatch, message = await self.chess_lobby.concede_match(ctx.message.author.id)
                if myMatch:
                    return await ctx.send(f'{CHECK} {message}')
                return await self.bot.send_error(ctx, message)

            ## Challenge another user
            elif action.startswith('<@') and not ' ' in action and action.endswith('>'):
                challenger = ctx.message.author
                try:
                    challengee = await commands.MemberConverter().convert(ctx, action)
                except Exception as e:
                    return await self.bot.send_error(ctx, f'{e}\nI could not challenge that user.')
                
                validate, black_robot, message = await self.chess_lobby.validate_new_match(
                    challenger, challengee, self.bot.user)
                if not validate:
                    return await self.bot.send_error(ctx, message)
                if not black_robot:
                    reacted, rotate, message = await self.chess_lobby.get_reaction(
                        ctx, challenger, challengee)
                    if not reacted:
                        return await ctx.reply(message)
                else:
                    rotate = False

                board, message = await self.chess_lobby.create_match(
                    challenger_id=challenger.id, challenger_name=challenger.display_name,
                    challengee_id=challengee.id, challengee_name=challengee.display_name,
                    black_robot=black_robot, do_rotating=rotate)
                if not board:
                    return await self.bot.send_error(ctx, message)
                return await ctx.send(message, file=board)

            ## Interpret action as a chess move
            else:
                board, message = await self.chess_lobby.make_move(
                    move=action, player_id=ctx.message.author.id)
                if not board:
                    return await self.bot.send_error(ctx, message)
                return await ctx.send(message, file=board)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def choose(self, ctx:commands.Context, first:str, second:str, third:Optional[str]):
        """Chooses a random option from two to three options.
        Example: `|p|choose "Helena Rubinstein" Cher "Margot Robbie"`"""
        choice = SystemRandom().choice([first, second, third])
        await ctx.reply(choice, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coinflip(self, ctx:commands.Context, coin: Optional[str]):
        """Flips a coin and returns heads or tails."""
        result = SystemRandom().choice(['heads', 'tails'])
        if coin:
            mess=f'{"You chose "+coin.casefold()} {"but"if coin.casefold()!=result else"and"} the'
        else:
            mess='The'
        await ctx.reply(f'{mess} result was {result}', mention_author=False) 

    @commands.hybrid_command(aliases=['flag','flagguess'],description='Guess a random country flag.')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def flag_guesser(
        self, ctx:commands.Context
    ):
        """Guess a random country flag."""
        embed = await get_flag()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def minesweeper(self, ctx:commands.Context):
        """Plays Minesweeper."""
        await ctx.reply(embed=print_minesweeper(), mention_author=False, ephemeral=False)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def place(
        self, ctx:commands.Context,
        colour:str,
        x:int, y:int
    ):
        """Like r/place."""

        colour = colour.casefold()
        my_matrix = Matrix(
            background=r'cogs/chess/place.png',
        )

        try:
            my_matrix.add(colour=colour, x=x, y=y)
        except Exception as e:
            return await self.bot.send_error(ctx, str(e))
        my_matrix.save()
        my_file = my_matrix.show()
        await ctx.send(file=my_file)

    @commands.hybrid_command(aliases=['r','dice','rol','rll'],
        description='Rolls dice in the format <№_dice>d<№_sides>, in the range <1-10>d<2-100>.')
    @discord.app_commands.describe(dice='A number of sides, or NdN, in the range <1-10>d<2-100>',
        modifier='A number to add or subtract from the total')
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def roll(self, ctx:commands.Context, dice:str, *, modifier:Optional[str]):
        """
        Rolls dice in the format <№_of_dice>d<№_of_sides>, in the range <1-10>d<2-100>.
        You can optionally add a + or - modifier to the result.
        Example: `|h|roll 2d100 -3`

        You can also specify a single dice with just it's number of faces.
        Example: `|h|roll 3`
        """
        amount = 0
        die = 0
        rolls = []
        total = 0
        myModifier = modifier
        if not modifier:
            modifier = ''

        errorMessage = []
        goodMessage = []

        if 'd' in dice:
            amount, die = dice.split('d')
            if die.isdigit() and amount.isdigit():
                die = int(die)
                amount = int(amount)
                if 1 <= amount <= 100:
                    if 2 <= die <= 100:
                        for _ in range(amount):
                            roll = SystemRandom().randrange(1, die+1)
                            rolls.append(roll)
                        if len(rolls) == 1:
                            goodMessage.append(f'Result: **{rolls[0]}**')
                        else:
                            strRolls = ''
                            for roll in rolls:
                                strRolls += f'**{roll}**, '
                            strRolls = strRolls[:-2]
                            strRolls = f'{strRolls}'
                            goodMessage.append(f'Result: {strRolls}')
                    else:
                        errorMessage.append('The die must be in the range 2 to 100')
                else:
                    errorMessage.append('The amount of dice must be in the range 1 to 100')
            else:
                errorMessage.append('The requested dice roll was not in the format NdN')
        elif dice.isdigit():
            die = int(dice)
            dice = f'1d{dice}'
            if 2 <= die <= 100:
                roll = SystemRandom().randrange(1, die+1)
                rolls.append(roll)
                goodMessage.append(f'Result:** {roll}**')
            else:
                errorMessage.append('The amount of dice must be in the range 1 to 10')
        else:
            errorMessage.append('The requested dice roll was not in the format NdN')

        # Modifier
        if myModifier != None:
            if len(myModifier) < 6:
                try:
                    myModifier = myModifier.replace('**', '')
                    myModifier = myModifier.replace('*', '')
                    myModifier = myModifier.replace('/', '')
                    myModifier = sympy.sympify(myModifier)
                    myModifier = f'{myModifier}'

                    myModifier = int(myModifier)
                    if myModifier < 0:
                        modifier = f'- {str(myModifier).replace("-", "")}'
                    else:
                        modifier = f'+ {myModifier}'
                    goodMessage.append(f'Modifier: **{modifier}**')
                except:
                    myModifier = 0
                    errorMessage.append('Modifiers should look like `+ 300` or `- 20`')
            else:
                myModifier = 0
                errorMessage.append('Modifiers cannot exceed 5 digits')
        else:
            myModifier = 0

        # Total
        for roll in rolls:
            total += roll
        total += myModifier
        if myModifier == 0 and len(rolls) == 1:
            pass
        else:
            goodMessage.append(f'Total: **{total}**')

        # Send
        if len(errorMessage) == 0:
            first = str(total)[0]
            last = str(total)[-1]
            if first == '-':
                colour = 0x000000 # black
            elif last == '1':
                colour = 0x523110 # brown
            elif last == '2':
                colour = 0xBA0202 # red
            elif last == '3':
                colour = 0xFE7000 # orange
            elif last == '4':
                colour = 0xDBA800 # yellow
            elif last == '5':
                colour = 0x07B307 # green
            elif last == '6':
                colour = 0x0067C4 # blue
            elif last == '7':
                colour = 0x7F40BF # purple
            elif last == '8':
                colour = 0x696969 # grey
            elif last == '9':
                colour = 0xf2efed # white
            else:
                colour = 0x000000 # black

            embed = discord.Embed(
                title=f'Roll {dice} {modifier}',
                description=f', '.join(goodMessage),
                colour=colour
            )
            await ctx.reply(embed=embed, mention_author=False)
        else:
            return await self.bot.send_error(ctx, '. '.join(errorMessage))

    @commands.hybrid_command(name='wordle', description='Plays a game of Wordle : <wordle_id> | daily | random | help.')
    @commands.cooldown(1, 5, commands.BucketType.user)
    @discord.app_commands.describe(puzzle='<wordle_id>, daily, random, or help')
    @commands.guild_only()
    async def wordle(
        self,
        ctx: commands.Context,
        puzzle: str
    ):
        """
        Plays a game of Wordle.

        **You can start a game with:**
        :key: `|h|wordle <puzzle_id>` - Play a puzzle by it's ID
        :sunny: `|h|wordle daily` - Play the puzzle of the day
        :game_die: `|h|wordle random` - Play a random puzzle
        
        Use `|h|wordle help` for info on how to play.
        """
        if puzzle in ['random','r','rand',None]:
            await ctx.reply(embed=generate_puzzle_embed(ctx.author, random_puzzle_id()), mention_author=False)
        elif puzzle in ['daily','d','today','todays']:
            await ctx.reply(embed=generate_puzzle_embed(ctx.author, daily_puzzle_id()), mention_author=False)
        elif puzzle in ['info','help','?']:
            await ctx.reply(embed=generate_info_embed(ctx.clean_prefix), mention_author=False, ephemeral=False)
        elif puzzle.isdigit():
            await ctx.reply(embed=generate_puzzle_embed(ctx.author, puzzle), mention_author=False)
        else:
            await ctx.reply(embed=generate_info_embed(ctx.clean_prefix), ephemeral=True)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(
        self,
        message: discord.Message
    ):
        """
        When a message is sent, process it as a wordle guess.
        """
        # Don't look at messages by bots
        if message.author.bot:
            return False
        
        # get the message replied to
        ref = message.reference
        if not ref or not isinstance(ref.resolved, discord.Message):
            return False
        parent = ref.resolved

        # if the parent message is not the bot's message, ignore it
        if parent.author.id != self.bot.user.id:
            return False

        # if the parent message is not from a bot, ignore it
        if not parent.author.bot:
            return False

        # check that the message has embeds
        if not parent.embeds:
            return False

        embed = parent.embeds[0]
        if not embed.title:
            return False
        if not embed.footer:
            return False
    
        wordle = await process_message_as_guess(self.bot, message, parent, embed)

        if not wordle:
            await check_flag_guess(message, parent, embed)

async def setup(bot: commands.bot):
    await bot.add_cog(Games(bot))