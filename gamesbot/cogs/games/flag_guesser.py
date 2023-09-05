import random
import json
from discord import Embed, Message

from constants import ERR, CHECK

already_countries = []

async def check_flag_guess(message: Message, parent, embed: Embed) -> None:
    """Check if guess is right"""

    if embed.title != 'Which country is this? Reply to me.':
        return None
    if '#' not in embed.footer.text:
        return None
    try:
        country_id = embed.footer.text.replace('#', '')
    except:
        return None
    
    f = open('cogs/games/countries.json', encoding="utf8")
    countries = json.load(f)

    country = countries.get(country_id)
    countrys_names = country['names']

    answered = False
    for name in countrys_names:
        if name.casefold() == message.content.casefold():
            answered = True
    
    if answered:
        await message.add_reaction(CHECK)
        await message.channel.send(content=f'You\'re right, {message.author.nick}! It\'s {countrys_names[0]}.')
        embed.remove_footer()
        embed.set_footer(text=f'It was {countrys_names[0]}, answered by {message.author.nick}!')
        await parent.edit(embed=embed)
    else:
        answered = False
        await message.add_reaction(ERR)

    return countrys_names[0], answered

async def get_flag() -> Embed:
    # Get random country

    the_limit = 0

    f = open('cogs/games/countries.json', encoding="utf8")
    countries = json.load(f)

    while the_limit < 40:
        country_id = str(random.randint(0,len(countries)) + 1)

        if country_id in already_countries:
            the_limit += 1
        else:
            the_limit += 42

        country = countries.get(country_id)

    country_flag_url = country['flag']

    already_countries.append(country_id)

    embed = Embed(
        title='Which country is this? Reply to me.',
        colour = 0x45c33a,
    )
    embed.set_image(url=country_flag_url)
    embed.set_footer(text=f'#{country_id}')

    return embed

