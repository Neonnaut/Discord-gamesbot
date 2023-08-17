import asyncio
from random import SystemRandom

from bs4 import BeautifulSoup
from io import BytesIO
import base64
import praw
import discord
from craiyon import Craiyon, craiyon_utils
from discord.ext import commands
from typing import Optional

from constants import REDDIT_CLIENT

class Fun(commands.Cog, name='fun'):
    """Random and fun commands."""
    COG_EMOJI = '🎏'

    def __init__(self, bot):
        self.bot:discord.Client = bot

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cat(self, ctx:commands.Context):
        """Shows a picture of a cat."""
        try:
            response = await self.bot.session.get('https://cataas.com/cat?json=true')
        except:
            return await self.bot.send_error(ctx, 'Request took too long')
        data = await response.json()

        embed = discord.Embed(title='A Picture of a Cat')
        embed.set_image(url='https://cataas.com/' + data['url'])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dog(self, ctx:commands.Context):
        """Shows a picture of a dog."""
        try:
            response = await self.bot.session.get('https://dog.ceo/api/breeds/image/random')
        except:
            return await self.bot.send_error(ctx, 'Request took too long')
        data = await response.json()

        embed = discord.Embed(title='A Picture of a Dog')
        embed.set_image(url=data['message'])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def fox(self, ctx:commands.Context):
        """Shows a picture of a fox."""
        try:
            response = await self.bot.session.get('https://randomfox.ca/floof/?ref=apilist.fun')
        except:
            return await self.bot.send_error(ctx, 'Request took too long')
        data = await response.json()

        embed = discord.Embed(title='A Picture of a Fox')
        embed.set_image(url=data['image'])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def frog(self, ctx:commands.Context):
        """Shows a picture of a frog."""
        choice = f'00{SystemRandom().randrange(1, 54)}'
        embed = discord.Embed(title='Image of a frog')
        embed.set_image(url=f'http://www.allaboutfrogs.org/funstuff/random/{choice}.jpg')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 62, commands.BucketType.default)
    async def imagine(self, ctx:commands.Context, *, prompt):
        """Generates some images based on your text prompt using Craiyon.com"""
        craiyon_generator = Craiyon() # Initialize Craiyon() class

        msg = await ctx.reply(f'Generating prompt "{prompt}". ETA of 1 minute...', mention_author=False)
    
        generated_images = await craiyon_generator.async_generate(prompt) # Generate images
        b64_list = await craiyon_utils.async_encode_base64(generated_images.images) # Download images from https://img.craiyon.com and store them as b64 bytestring object
        
        images = []
        for index, image in enumerate(b64_list): # Loop through b64_list, keeping track of the index
            img_bytes = BytesIO(base64.b64decode(image)) # Decode the image and store it as a bytes object
            image = discord.File(img_bytes)
            image.filename = f'result{index}.webp'
            images.append(image) # Add the image to the images1 list
            
        await msg.edit(content='"prompt". Generated by Craiyon.com', attachments=images, allowed_mentions=None)

        del craiyon_generator

    @commands.command(name='8ball')
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def magic_ball(self, ctx:commands.Context, *, question:str):
        """Asks the 8ball a question."""
        answers = ['It is certain.', 'It is decidedly so.', 'Without a doubt.',
                   'Yes – definitely.', 'You may rely on it.', 'As I see it, yes.',
                   'Most likely.', 'Outlook good.', 'Yes.',
                   'Ask again later.', 'Better not tell you now.',
                   'My sources say no.', 'Very doubtful.', 'No, absolutely not.']
        await ctx.send(f'{answers[SystemRandom().randrange(0, len(answers))]}',mention_author=False)
    
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def reddit(self, ctx:commands.Context, *, sub:str):
        """Gets the five hot posts from a subreddit."""

        try:
            r = praw.Reddit(client_id=REDDIT_CLIENT[0],
                client_secret=REDDIT_CLIENT[1],
                user_agent=REDDIT_CLIENT[2]
                )
                    
            subreddit = r.subreddit(sub)
            subposts = []
            for post in subreddit.hot(limit=5):
                if post.over_18:
                    return await self.bot.send_error(ctx, 'Nope')
                else:
                    subposts.append(str('{DIAMOND}[' + post.title +
                                        '](https://www.reddit.com' + post.permalink + ')'))

            subposts = '\n'.join(subposts) or 'None'

        except Exception as e:
            return await self.bot.send_error(ctx, f'Could not find "{sub}", {e}')

        embed = discord.Embed(
            title=f'r/{sub}'
        )
        embed.set_thumbnail(
            url=subreddit.community_icon or subreddit.icon_img)
        embed.add_field(
            inline=True,
            name=f'**Five of the hottest posts:**',
            value=f'{subposts}'
        )

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def speak(self, ctx:commands.Context):
        """Makes the bot say something."""
        choice = SystemRandom().choice(['Good day, pal.', 'You\'re adopted.', 'Woof!',
            'You and me, we\'re the only people around who aren\'t complete fools.'])
        await ctx.send(choice)

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def xkcd(self, ctx:commands.Context, *, option: Optional[str]):
        """Shows an xkcd comic, gets a random comic by default.
        Use `|p|xkcd latest` to get the latest comic, `|p|xkcd <number> for a specific"""

        if not option: option = 'random/comic'
        url = f'https://c.xkcd.com/{option}/'
        response = await self.bot.session.get(url=url)
        if response.status == 404:
            return print('that does not exist')
        elif response.status != 200:
            return print(':(')
        
        response = await response.read()
        loop = asyncio.get_event_loop()
        soup = await loop.run_in_executor(None,
            BeautifulSoup, response.decode('utf-8'), 'html.parser'
        ) # lxml is faster, but needs install

        try:
            comic = soup.find('div', {'id': 'comic'})
            img = f'https:{comic.find("img")["src"]}'

            title = soup.find('div', {'id': 'ctitle'}).text
        except:
            return None
        
        embed = discord.Embed(
            title=title
        )
        embed.set_image(url=img)
        
        await ctx.send(embed=embed)
    
async def setup(bot: commands.bot):
    await bot.add_cog(Fun(bot))