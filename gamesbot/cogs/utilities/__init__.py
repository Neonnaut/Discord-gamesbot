import asyncio
import json
import random
import time as t
from datetime import datetime
from typing import Optional

import discord
import emoji
import pytz
import regex
import sympy
from bs4 import BeautifulSoup
from discord import Embed
from discord.ext import commands

from .bases import converter
from .codetest import CodeBlock
from .github import get_github
from .kon import do_block, generate_word
from .translator import translate
from .unit_converter import get_units, money_convert, unit_convert

from constants import CHECK, DIAMOND, REDDIT_CLIENT, WEATHER_CLIENT


class Utilities(commands.Cog, name='utilities'):
    """Useful commands."""
    COG_EMOJI = '🔖'

    def __init__(self, bot: discord.Client):
        self.bot:discord.Client = bot
        self.stopwatch_date = None

    @commands.command(aliases=['bc'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def base_converter(
        self, ctx:commands.Context,
        number: str, from_base: int, to_base: int
    ):
        """
        Converts a number from a base to another base.
        Don't try converting above base 36.
        """
        if len(str(number)) > 4 or len(str(from_base)) > 4 or len(str(to_base)) > 4:
            return await self.bot.send_error(ctx, f'At least one of your inputs was over 4') 
        output = await converter(number, from_base, to_base)
        await ctx.send(output)

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def calc(self, ctx:commands.Context, *, equation):
        """Returns the result of a calculation.
        Example: |p|calc (a + b) - 2 + 2 ^ 5`"""

        calc = equation
        if len(equation) >= 60:
            return await self.bot.send_error(ctx, 'That calculation is too large.')
        calc = calc.replace('^', '**')
        calc = calc.replace('x', '*')
        try:
            calc = str(sympy.sympify(calc))
            calc = calc.replace('**', '^')
            calc = calc.replace('*', 'x')
            if '.' in calc:
                calc = calc.rstrip('0')
            if len(calc) > 900:
                return await self.bot.send_error(ctx, 'The result of that calculation was over 900 characters in length.')
            await ctx.reply(calc, mention_author=False)
        except:
            return await self.bot.send_error(ctx, 'There was something wrong with the input')

    @commands.guild_only()
    @commands.command(aliases=['compile','coliru'])
    async def compile_code(self, ctx:commands.Context, *, code: CodeBlock):
        """Compiles code via Coliru.

        You have to pass in a code block with the language syntax
        either set to one of these: CPP, C, Python, & Haskell

        Anything else isn't supported. The C++ compiler uses g++ -std=c++14. The python support is now 3.5.2.

        Please don't spam this for Stacked's sake.
        """
        payload = {
            'cmd': code.command,
            'src': code.source,
        }

        data = json.dumps(payload)

        async with ctx.typing():
            async with self.bot.session.post('http://coliru.stacked-crooked.com/compile', data=data) as resp:
                if resp.status != 200:
                    return await ctx.send('Coliru did not respond in time.')
                output = await resp.text(encoding='utf-8')

                if len(output) < 1992:
                    return await ctx.send(f'```\n{output}\n```')

                return await ctx.send('output is too big')
                    

    @commands.command(aliases=['cc'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def currency_converter(
        self, ctx:commands.Context, * text: str
    ):
        """
        Converts currencies in the format `<ammount> <currency> to <currency>`
        """
        text = ' '.join(text)
        mess, preNum, preUnit, postUnit = await get_units(text)
        if not preNum:
            return await self.bot.send_error(ctx, mess)
        mess, output = await money_convert(preNum, preUnit, postUnit)
        if not output:
            return await self.bot.send_error(ctx, mess)
        await ctx.reply(output, mention_author=False)

    @commands.command(aliases=['gh'])
    @commands.guild_only()
    async def github(self, ctx:commands.Context, repo):
        """Fetches repository info from Github."""

        github = await get_github(repo, self.bot.session)
        if isinstance(github, str):
            return await self.bot.send_error(ctx, github)
        await ctx.send(embed=github)

    @commands.hybrid_command(description='Basic emoji based poll creator')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def poll(self, ctx:commands.Context,
        title, option1, option2,
        option3: Optional[str], option4: Optional[str], option5: Optional[str], option6: Optional[str],
        option7: Optional[str], option8: Optional[str], option9: Optional[str], option10: Optional[str]
    ):
        """
        Creates a poll for users to vote on using emoji.
        Remember to enclose options that have spaces in them with quotes, e.g:
        `|h|poll "My Title" apple "dragon fruit" banana`
        or put them on seperate lines:
        `|h|poll My Title
        🍏 apple
        dragon fruit
        🍌 banana`
        If you give an emoji for an option, the vote option will be that emoji.
        """

        output = []
        options = [
            option1, option2, option3, option4, option5, option6, option7, option8, option9, option10
        ]

        things = []
        message = ctx.message.content
        message = message[len(ctx.prefix):]
        if '\n' in message:
            things = message.split('\n')
            title = things[0]
            title = title.split()
            title = title[1:]
            title = ' '.join(title)

            things = things[1:]

            if len(things) >= 10:
                things = things[:10]

            for i in range(0, len(options)):
                if i > len(things) - 1:
                    options[i] = None
                else:
                    options[i] = things[i]

        keycap = '\N{variation selector-16}\N{combining enclosing keycap}'
        numbers = ['1'+keycap, '2'+keycap, '3'+keycap, '4'+keycap, '5'+keycap, '6'+keycap, '7'+keycap, '8'+keycap, '9'+keycap, '\N{keycap ten}']
        reactions = []
        for i in range(0, len(options)):
            if options[i] != None:

                foundEmoji = None
                data = regex.match(r'<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>', options[i])
                if data == None:
                    if options[i][0] in emoji.EMOJI_DATA:
                        data = regex.findall(r'\X', options[i])
                        for word in data:
                            if any(char in emoji.EMOJI_DATA for char in word):
                                foundEmoji = word
                                break
                else:
                    foundEmoji = data.group()
                if foundEmoji == None:
                    reactions.append(numbers[i])
                else:
                    options[i] = options[i].replace(foundEmoji, '')
                    reactions.append(foundEmoji)

                output.append(f'{reactions[i]} {options[i].strip()}')

        output = '\n'.join(output)

        embed = discord.Embed(
            title=f'Poll: {title.casefold().capitalize()}',
            description=output
        )
        embed.set_author(
            name=f'{ctx.author.display_name}',
            icon_url=ctx.author.avatar
        )

        msg = await ctx.reply(embed=embed)

        try:
            await ctx.message.delete(delay=2)
        except:
            pass

        for i in range(0, len(reactions)):
            try:
                await msg.add_reaction(reactions[i])
            except:
                await msg.add_reaction(numbers[i])

    @commands.command()
    @commands.guild_only()
    async def stopwatch(self, ctx):
        """Starts or stops a stopwatch."""

        if not self.stopwatch_date:
            self.stopwatch_date = datetime.utcnow()
            await ctx.send(f'Stopwatch started')
        else:
            myTime = datetime.utcnow() - self.stopwatch_date

            total_seconds = int(myTime.total_seconds())
            hours, remainder = divmod(total_seconds,60*60)
            minutes, seconds = divmod(remainder,60)

            if hours == 0:
                hours = ''
            elif hours == 1:
                hours = f'{hours} hour '
            else:
                hours = f'{hours} hours '

            if minutes == 0:
                minutes = ''
            elif minutes == 1:
                minutes = f'{minutes} minute '
            else:
                minutes = f'{minutes} minutes '

            if seconds == 1:
                seconds = f'{seconds} second'
            else:
                seconds = f'{seconds} seconds'

            await ctx.send(f'Stopwatch stopped at {hours}{minutes}{seconds}')
            self.stopwatch_date = None

    @commands.command(aliases=['timeat'])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def time_at(self, ctx:commands.Context, *, zone: str):
        """Gets the current time of a timezone.

        Examples: `|p|timeat Asia/Tokyo`, `|p|timeat GMT+1`, `|p|timeat US/Eastern`"""

        try:
            vzone = zone
            if 'GMT+' in zone:
                v = zone.split('+')
                if len(v) == 2:
                    vzone = 'GMT-'+v[1]
            elif 'GMT-' in zone:
                v = zone.split('-')
                if len(v) == 2:
                    vzone = 'GMT+'+v[1]

            myZone = pytz.timezone(f'Etc/{vzone}')
        except:
            try:
                myZone = pytz.timezone(f'{zone}')
            except:
                return await self.bot.send_error(ctx, f'Could not find "{zone}".\nRemeber to put region before the locale e.g: `{ctx.clean_prefix}timeat US/Eastern`')

        myTime = datetime.now(myZone)

        await ctx.send(f'Current time in {zone}: **{myTime.strftime("%H:%M:%S")}**')

    @commands.guild_only()
    @commands.command()
    async def translate(self, ctx:commands.Context, *, message):
        """Translates a message to English using Google translate."""
        try:
            result = await translate(message, session=self.bot.session)
        except Exception as e:
            return await ctx.send(f'An error occurred: {e}')

        embed = discord.Embed(title='Translated', colour = 0x4284F3)
        embed.add_field(name=f'From {result.source_language}', value=result.original, inline=False)
        embed.add_field(name=f'To {result.target_language}', value=result.translated, inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['uc'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unit_converter(
        self, ctx:commands.Context, * text: str
    ):
        """
        Converts a unit of measurement to another in the format `<number> <unit_type> to <unit_type>`. e.g:
        `50 km/hr to miles/hr`
        """
        text = ' '.join(text)
        mess, preNum, preUnit, postUnit = await get_units(text)
        if not preNum:
            return await self.bot.send_error(ctx, mess)
        mess, output = await unit_convert(preNum, preUnit, postUnit)
        if not output:
            return await self.bot.send_error(ctx, mess)
        await ctx.reply(output, mention_author=False)

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def weather(self, ctx:commands.Context, location):
        """Shows the weather of a city or locale."""
        m_location = ctx.message.content.replace(ctx.prefix,'').split(' ')
        m_location = ' '.join(m_location[1:]).strip()
        location = m_location if m_location else location

        lx=location.casefold()
        if lx == 'melbourne':
            location = 'Melbourne, AU'
        elif lx == 'sydney':
            location = 'Sydney, AU'
        elif lx == 'brisbane':
            location = 'Brisbane, AU'
        elif lx == 'gold coast':
            location = 'Gold Coast, AU'
        elif lx == 'newcastle':
            location = 'Newcastle, AU'
        elif lx == 'canberra':
            location = 'Canberra, AU'
        elif lx == 'sunshine coast':
            location = 'Sunshine Coast, AU'
        elif lx == 'wollongong':
            location = 'Wollongong, AU'
        elif lx == 'geelong':
            location = 'Geelong, AU'
        elif lx == 'hobart':
            location = 'Hobart, AU'
        elif lx == 'townsville':
            location = 'Townsville, AU'
        elif lx == 'cairns':
            location = 'Cairns, AU'
        elif lx == 'toowoomba':
            location = 'Toowoomba, AU'
        elif lx == 'darwin':
            location = 'Darwin, AU'

        output = ''

        request = await self.bot.session.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&APPID={WEATHER_CLIENT}'
        )
        data = await request.json()

        if data.get('cod') != '200':
            output += f'{location} not found.'
            return await self.bot.send_error(ctx, output)
        try:
            myLocation = f'{data.get("name")}, {data.get("sys").get("country")}'
            myMain = data.get('main')
            myWeather = data.get('weather')
            icon = data.get('weather')[0].get('icon')
            myWind = data.get('wind')['speed']
            timenow = int(datetime.utcnow().timestamp())
            time = datetime.fromtimestamp((data.get(
                'timezone') + timenow)).strftime('%H:%M %a %d %b')

            embed = discord.Embed()
            embed.add_field(
                inline=True,
                name=f'Weather results for {myLocation} @ {time}',
                value=f'\n{DIAMOND}**Temperature**: {myMain["temp"]}°C'
                + f' (Min–max: {myMain["temp_min"]}–{myMain["temp_max"]}°C)'
                + f'\n{DIAMOND}**Weather**: {myWeather[0].get("main")}'
                + f'\n{DIAMOND}**Humidity**: {myMain["humidity"]}%'
                + f'\n{DIAMOND}**Wind**: {myWind} km/h'
            )
            try:
                embed.set_thumbnail(url=f'https://openweathermap.org/img/wn/{icon}@2x.png')
            except:
                pass
        except Exception as e:
            output += f'{e}'
            return await self.bot.send_error(ctx, output)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wikipedia(
        self, ctx:commands.Context, * query: str
    ):
        """Shows a summary of a wikipedia article"""
        query = ' '.join(query)
        query = query.replace("'",'%27').replace(' ','_')

        url = f'https://en.wikipedia.org/wiki/{query}'
        response = await self.bot.session.get(url=url)
        if response.status == 404:
            return await self.bot.send_error(ctx, f'"{query}" not found.')
        elif response.status != 200:
            return await self.bot.send_error(ctx, f'Wikipedia did not respond.')
        
        response = await response.read()
        loop = asyncio.get_event_loop()
        soup = await loop.run_in_executor(None,
            BeautifulSoup, response.decode('utf-8'), 'html.parser'
        ) # lxml is faster, but needs install

        title = soup.find('h1', {'id': 'firstHeading'}).text


        my_p = soup.select_one('p', {'class': 'mw-empty-elt'})
        text = ''
        done_ps = 0
        do_continue = True
        while done_ps < 2 and do_continue:
            if my_p.name == 'p':
                text+= my_p.text
                done_ps += 1
            try:
                my_p = my_p.find_next_sibling()
            except:
                do_continue = False
            if not my_p:
                do_continue = False

        if len(text) > 697:
            text = text.rstrip()[:600]
            if text[-1] in ['.','!','?']:
                pass
            elif text[-1] in [' ', ',']:
                text = f'{text[:-1]}...'
            else:
                text = f'{text}...'
        text = regex.sub('\[[0-9]+\]', '', text)
        
        embed = Embed(
            description=text,
            title=title,
            url=url,
            colour = 0Xe30b5c
        )

        try:
            side = soup.find('table', {'class': 'infobox'})
            try:
                img = side.find('img')['src']
                embed.set_thumbnail(url=f'https:{img}')
            except:
                pass
        except:
            pass

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def gloss(self, ctx:commands.Context, *, text):
        """Format lingustic gloss into columns. Last line should be a translation."""
        text = text.split('\n')
        last_line = ''
        if len(text) == 1:
            return await self.bot.send_error(ctx, 'You must provide at least 2 lines')
        elif len(text) > 2:
            last_line = text.pop()
        text = '\n'.join(text)


        blocks = text.split('\n\n')

        output = []
        for block in blocks:
            output.append(do_block(block))
        output = '\n\n'.join(output)
        await ctx.send(f'```\n{output}```{last_line}')

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ipa(self, ctx:commands.Context):
        """Shows information on IPA symbols."""
        text = """```
CONSONANTS
          bl ld dn al rf pa ap pl vl uv ph gl
   nasal  m  ɱ  n̪  n  ɳ        ɲ  ŋ  ɴ
 vl stop  p     t̪  t  ʈ        c  k  q  ʡ  ʔ
  v stop  b     d̪  d  ɖ        ɟ  g  ɢ
 ej stop  pʼ    t̪ʼ tʼ ʈʼ       cʼ kʼ qʼ
 implosv  ɓ	    ɗ  ᶑ        ʄ  ɠ  ʛ
 vl fric  ɸ  f  θ  s  ʂ  ʃ  ɕ  ç  x  χ  ħ  h
  v fric  β  v  ð  z  ʐ  ʒ  ʑ  ʝ  ɣ  ʁ  ʕ  ɦ
vl afrct  p͡ɸ p͡f    t͡s t͡ʂ t͡ʃ t͡ɕ c͡ç k͡x q͡χ
 v afrct  b͡β p͡v    d͡z d͡ʐ d͡ʒ d͡ʑ ɟ͡ʝ ɡ͡ɣ ɢ͡ʁ
  approx     ʋ     ɹ  ɻ        j  ɰ
   trill  ʙ        r  ɽ͡r             ʀ
    flap     ⱱ     ɾ  ɽ
   click  ʘ     ǀ  !           ǂ

Lateral Consonants:
         al     rf     pl     vl
   fric  ɬ  ɮ   ꞎ 
  afrct  t͡ɬ d͡ɮ  t͡ꞎ
 approx  l      ɭ      ʎ      ʟ
    tap  ɺ
  click  ǁ  

Co-articulated Consonants:
 ŋ͡m k͡p ɡ͡b ʍ w  labial-velars     
 ɫ ɥ ɧ         others

Secondary articulation:
  ʰ  aspirated      ʱ  breathy-voiced
  ʲ  palatalized    ˤ  pharyngealized
  ʷ  labialized     ˠ  velarized
 ˀ ʼ glottalized    ⁿ  nasal release

  c̊  voiceless      c̩  syllabic
  c̬  voiced         c̚ unreleased
``````
VOWELS
 i y   ɨ ʉ   ɯ u
 ɪ ʏ           ʊ
 e ø   ɘ ɵ   ɤ o
       ə
 ɛ œ   ɜ ɞ   ʌ ɔ
 æ ɶ a ɐ     ɑ ɒ

 aː  long           ä  centralized
 aˑ  half-long      a̟  advanced
 ă   extra-short    a̠  retracted
 ã   nasalised      a̝  raised   
 a̰   creaky-voice   a̞  lowered
``````
TONES
 ȁ ˩  extra low     ǎ ˩˥  rising
 à ˨  low           a᷄ ˦˥  high rising
 ā ˧  mid           a᷅ ˩˨  low falling
 á ˦  high          â ˥˩  falling
 a̋ ˥  extra high    a᷈ ˧˦˨  rising-falling
 a᷅ ˩˨  low rising
``````
SUPRASEGMENTALS
 ˈ   primary stress
 ˌ   secondary stress
 ↓   downstep
```"""
        embed = discord.Embed(
            #title=title,
            description=text
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(aliases=['rw'])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def random_word(self, ctx:commands.Context, *, text):
        """
        Generates a random phonological word with the following abbreviations:
        **A**: africate, **C**: consonant, **E**: ejective, **F**: fricative,
        **I**: implosive, **J**: palatal, **K**: click, **L**: lateral,
        **N**: nasal, **P**: plosive, **R**: rhotic, **S**: sibilant,
        **T**: tap, **U**: simple-vowel, **V**: any-vowel, **W**: approximate, **X**: trill,
        *****: any phoneme, **+**: repeats the previous character.
        """

        if len(text) > 200 and ctx.message.author.id == 871760081593696338:
            return await self.bot.send_error(ctx, 'Fuck off Atsu 🤣')
        if len(text) > 100:
            return await self.bot.send_error(ctx, 'No. That is too long an input')
        output = generate_word(text)
        await ctx.send(output)

    @commands.command(aliases=['syntax'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def syntax_test(self, ctx:commands.Context):
        """Displays a random sentence for you to test a language's syntax."""
        sentences = open('cogs/utilities/syntax_list.txt').read().splitlines()
        rando = random.randint(0, len(sentences))
        mySentence = sentences[rando]

        await ctx.send(f'**Syntax Test Sentence #{rando}**\n`{mySentence}`')

    @commands.command(aliases=['newwiki','wikinew', 'wikianew', 'createwiki', 'wikicreate', 'newwikia'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def new_wiki(self, ctx:commands.Context, *, query):
        """Creates a new wiki page on the TC Wiki with the title you give it, if it doesn't exist yet."""

        new_query = query
        if "'" in query:
            new_query = new_query.replace("'",'%27')
        if ' ' in query:
            new_query = new_query.replace(' ','_')

        url = f'https://thousand-crowns-worldbuilding.fandom.com/wiki/{new_query}'
        response = await self.bot.session.get(url=url)

        if response.status == 200:
            return await self.bot.send_error(ctx, f'"{query}" already exists.')
        await ctx.send(f'{CHECK} {url}?veaction=edit can be created.')

    @commands.command(aliases=['wikia'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wiki(self, ctx:commands.Context, *, query):
        """Displays some information found on the TW Wiki or the TC Wiki."""

        old_query = query

        myPageNum = 1
        if ' | ' in query:
            query_check = query.split(' | ')
            if len(query_check) == 2:
                if query_check[1].strip().isdigit():
                    query = query_check[0].strip()
                    myPageNum = int(query_check[1].strip())

        if "'" in query:
            query = query.replace("'",'%27')
        if " " in query:
            query = query.replace(' ','_')

        Eurl = f'https://thousand-crowns-worldbuilding.fandom.com/wiki/{query}'
        response = await self.bot.session.get(url=Eurl)

        if response.status != 200:
            Eurl = f'https://thousand-crowns-worldbuilding.fandom.com/wiki/Category:{query}'
            response = await self.bot.session.get(url=Eurl)
            if response.status != 200:
                Eurl = f'https://the-two-constructed-continents.fandom.com/wiki/{query}'
                response = await self.bot.session.get(url=Eurl)
                if response.status != 200:
                    return await self.bot.send_error(ctx, f'Could not find \'{old_query}\'.')

        text = await response.read()
        loop = asyncio.get_event_loop()
        soup = await loop.run_in_executor(None,
            BeautifulSoup, text.decode('utf-8'), 'html.parser'
        )

        title = soup.find('h1', {'class': 'page-header__title'}).text
        title = str(title).strip().capitalize()
        embed = discord.Embed(
            title=title,
            url=Eurl
        )

        # Aside details
        if myPageNum == 1:
            try:
                side = soup.find('div', {'class': 'mw-parser-output'}).find('aside')
                try:
                    img = side.find('a').find('img')['src']
                    embed.set_thumbnail(url=img)
                except:
                    pass
            except:
                pass
            else:
                try: 
                    labels = side.find_all( class_ = 'pi-data-label' )
                    values = side.find_all( class_ = 'pi-data-value' )
                    details = ''
                    for i in range(0, len(labels)):
                        if i < 8:
                            details += f'**{DIAMOND}{labels[i].text}**: {values[i].text}\n'
                    embed.add_field(
                        inline=False,
                        name=f'**Details:**',
                        value=f'{details}'
                    )
                except:
                    pass
            
        try:
            ourcontent = description = soup.find('div', {'class': 'mw-parser-output'})

            # Iterate each line
            for x in ourcontent.find_all():
            
                # fetching text from tag and remove whitespaces
                if len(x.get_text(strip=True)) == 0 or len(x.get_text()) == 0:
                    
                    # Remove empty tag
                    x.decompose()

            description = ourcontent.select(':is(h1:has(.mw-headline), h2:has(.mw-headline), h3:has(.mw-headline), h4:has(.mw-headline), h5:has(.mw-headline), h6:has(.mw-headline))')
            for little in description:
                siblings = little.find_next_siblings()
                found_a_p = False
                for j in range(0, len(siblings)):
                    if siblings[j].name in ['p','pre']:
                        found_a_p = True
                    elif siblings[j].name in ['h1','h2','h3','h4','h5','h6']:
                            break
                    
                if not found_a_p:
                    description.remove(little)
                if len(little.get_text(strip=True)) == 0 or len(little.get_text()) == 0:
                    description.remove(little)

            num_of_pages = len(description)

            ###HERE

            description = description[myPageNum - 1]

            get_second_header = description.text.replace('[]','')

            description = description.find_next_siblings()

            myPage = []
            for i in range(0, len(description)):
                if description[i].name in ['p','pre','div']:
                    myPage.append(description[i].text)
                elif description[i].name in ['h1','h2','h3','h4','h5','h6']:
                    break
            if len(myPage) == 0:
                myPage.append('...')

            myPage = ' \n'.join(myPage)

            description = myPage

            if myPageNum == 1:
                description = (description[:301] + '...') if len(description) > 301 else description
                description = description.replace('\n\n', ' ')
                embed.description=description
            else:
                description = (description[:990] + '...') if len(description) > 993 else description
                description = description.replace('\n\n', ' ')
                embed.add_field(name=get_second_header, value=description)

            embed.set_footer(text = f'Section {myPageNum} of {num_of_pages}')
        except:
            pass

        await ctx.send(embed=embed)

    @commands.command(aliases=['sampa'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def xsampa(self, ctx:commands.Context):
        """Shows X-sampa notation help."""
        text = """```
CONSONANTS
           bl ld dn al rf pa ap pl vl uv ph gl
    nasal  m  F     n  n`       J  N  N/
  vl stop  p        t  t`       c  k  q  >/  ?
   v stop  b        d  d`       J/ g  G/
  vl fric  p/ f  T  s  s` S  s/ C  x  X  X/  h
   v fric  B  v  D  z  z` Z  z/ j/ G  R  ?/  h/
   approx     v/    r/ r/`      j  M/
    trill  B/ r     r`                R/
     flap  v/       4
    click  O/    |/ !           =/

  y/ w   rounded semivowels
  H/ Q/  epiglottal trills
  K  K/  lateral fricatives
     4/  lateral flap
   |/|/  lateral click
     L   velarized l
     w;  voiceless w
     x;  swedish sj-sound

  ejectives and implosives are
  made by sufixing:
    _>  _<
       
  affricates and coarticulations may be
  joined by a tiebar:
    ts} tS}   kp} gb}
``````
VOWELS
  i y    1  W    M u
  I Y    I; U;     U
  e 0    e; o;   7 o
           @
  E 9    3  O;   2 O
  &        6
  a 9;           A 8
``````
DIACRITICS
  a:  long              t+?  unreleased
  a~  nasal             s-a  apical
  d{  dental            s-l  laminal
  k"  ejective          e-r  raised
  b<  implosive         e-T  lowered
  m>  voiceless         e+"  centralized
  r=  syllabic          e-^  non-syllabic
 
 superscripts are written with ^
  ^h  aspirated          ^H  breathy-voiced
  ^j  palatalized        ^Q  pharyngealized
  ^w  labialized         ^G  velarized
  ^?  glottalized
``````
SUPRASEGMENTALS
  '   primary stress
  ,   secondary stress
  ,;  downstep
  |   minor pause
  ||  major pause
``````
TONES
  #1  extra low          #8  high rising
  #2  low                #9  low falling
  #3  mid                #A  falling
  #4  high               #B  high falling
  #5  extra high         #C  peaking
  #6  low rising         #D  dipping
  #7  rising
 
 contour tones can also be written as
 sequences of level tones in parentheses:
  #(214) #(51)
 
 tone diacritics are notated with + instead of #
```"""
        text = text.replace('/', '\\')
        embed = discord.Embed(
            #title=title,
            description=text
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def xti(self, ctx:commands.Context, *, input):
        """Converts X-SAMPA to IPA. Maximum of 200 characters."""

        if len(input) > 200:
            return await self.bot.send_error(ctx, 'Your input was more than 200 characters!')

        output = ''

        words = input.split()

        x = ['S\\', 'z\\','_R_F', 'J\\_<', '_H_T', 'G\\_<', '_B_L', '\|\\\|\\', 'r\\`', '<R>', 'g_<', '<F>', 'd_<', 'b_<', '_\?\\', 'z\\', 'z`', 'X\\', 'x\\', '_x', '_X', '_w', 'v\\', '_v', 'U\\', 't`', '_t', '_T', 's\\', 's`', 'r\\', 'r`', '_r', 'R\\', '_R', '_q', 'p\\', '_o', 'O\\', '_O', 'n`', '_n', 'N\\', '_N', '_m', 'M\\', '_M', 'l\\', 'l`', '_l', 'L\\', '_L', '_k', 'K\\', 'j\\', '_j', 'J\\', 'I\\', 'h\\', '_h', 'H\\', '_H', 'G\\', '_G', '_F', '_e', 'd`', '_d', '_c', 'B\\', '_B', '_a', '_A', '3\\', '_0', '@\\', '\?\\', '\!\\',
             ':\\', '\-\\', '_\+', '_\\', '_\}', '_"', '_/', '_\-', '_>', '_=', '_~', '_\^', '\|\\', '\|\|', '>\\', '=\\', '<\\', 'Z', 'z', 'y', 'Y', 'X', 'x', 'w', 'W', 'v', 'V', 'u', 'U', 'T', 't', 's', 'S', 'r', 'R', 'q', 'Q', 'p', 'P', 'O', 'o', 'N', 'n', 'm', 'M', 'l', 'L', 'k', 'K', 'j', 'J', 'i', 'I', 'h', 'H', 'g', 'G', 'f', 'F', 'E', 'e', '@', 'D', 'd', 'C', 'c', 'B', 'b', '{', 'a', 'A', '9', '8', '7', '6', '5', '4', '3', '2', '1', '%', '&', '\}', '"', '\'', '\.', '\?', '\!', ':', '\|', '=', '~', '\^', '`', 't_s', 'd_z',
             ]
        p = ['ɕ', 'ʑ','\u1DC8', 'ʄ', '\u1DC4', 'ʛ', '\u1DC5', 'ǁ', 'ɻ', '↗', 'ɠ', '↘', 'ɗ', 'ɓ', 'ˤ', 'ʑ', 'ʐ', 'ħ', 'ɧ', '\u033D', '\u0306̆', 'ʷ', 'ʋ', '\u032C', 'ᵿ', 'ʈ', '\u0324', '	\u02DD', 'ɕ', 'ʂ', 'ɹ', 'ɽ', '\u031D', 'ʀ', '\u02C7', '\u0319', 'ɸ', '\u031E', 'ʘ', '\u0339', 'ɳ', 'ⁿ', 'ɴ', '\u033C', '\u033B', 'ɰ', '\u0304', 'ɺ', 'ɭ', 'ˡ', 'ʟ', '\u0300', '\u0330', 'ɮ', 'ʝ', 'ʲ', 'ɟ', 'ᵻ', 'ɦ', 'ʰ', 'ʜ', '\u0301', 'ɢ', 'ˠ', '\u0302', '\u0334', 'ɖ', '\u032A', '\u031C', 'ʙ', '\u030F', '\u033A', '\u0318', 'ɞ', '\u0325', 'ɘ', 'ʕ', 'ǃ', 'ˑ', '‿', '\u031F', '\u0302',
             '\u031A', '\u00A8', '\u030C', '\u0320', 'ʼ', '\u0329', '\u0303', '\u032F', 'ǀ', '‖', 'ʡ', 'ǂ', 'ʢ', 'ʒ', 'z', 'y', 'ʏ', 'χ', 'x', 'w', 'ʍ', 'v', 'ʌ', 'u', 'ʊ', 'θ', 't', 's', 'ʃ', 'r', 'ʁ', 'q', 'ɒ', 'p', 'ʋ', 'ɔ', 'o', 'ŋ', 'n', 'm', 'ɯ', 'l', 'ʎ', 'k', 'ɬ', 'j', 'ɲ', 'i', 'ɪ', 'h', 'ɥ', 'ɡ', 'ɣ', 'f', 'ɱ', 'ɛ', 'e', 'ə', 'ð', 'd', 'ç', 'c', 'β', 'b', 'æ', 'a', 'ɑ', 'œ', 'ɵ', 'ɤ', 'ɐ', 'ɫ', 'ɾ', 'ɜ', 'ø', 'ɨ', 'ˌ', 'ɶ', 'ʉ', '\ˈ', 'ʲ', '.', 'ʔ', 'ꜜ', 'ː', '|', '\u0329', '\u0303', 'ꜛ', '˞ ', 't͡s', 'd͡z',
             ]

        for word in words:
            for i in range(1, len(x)):
                word = word.replace(x[i], p[i])

            output += word + ' '

        await ctx.send(output)

async def setup(bot: commands.bot):
    await bot.add_cog(Utilities(bot))
