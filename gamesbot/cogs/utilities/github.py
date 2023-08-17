from discord import Embed


async def get_github(arg, session) -> Embed:
    """Fetch repository info"""

    try:
        req = await session.get(f'https://api.github.com/repos/{arg}')
    except:
        return 'An error occured'

    if req.status == 200:

        apijson = await req.json()

        embed = Embed(
            title = apijson['name'],
            url = apijson['html_url'],
            description = apijson['description'],
            colour=0x0,
        )
        
        embed.set_author(
            name=apijson['owner']['login'],
            icon_url=apijson['owner']['avatar_url'],
            url=apijson['owner']['html_url']
        )
        
        embed.add_field(
            name='Repository:',
            value=f'[{apijson["name"]}]({apijson["html_url"]})',
            inline=True
        )

        embed.add_field(
            name='Language:',
            value=apijson['language'],
            inline=True
        )

        if apijson['stargazers_count'] != 0:
            embed.add_field(
                name='Stars:',
                value=apijson['stargazers_count'],
                inline=True
            )
        if apijson['forks_count'] != 0:
            embed.add_field(
                name='Forks:',
                value=apijson['forks_count'],
                inline=True
            )
        if apijson['open_issues'] != 0:
            embed.add_field(
                name='Issues:',
                value=apijson['open_issues'],
                inline=True
            )

        return embed, 'success'
    
    elif req.status_code == 404:
        return 'Could not find that repository'
    elif req.status_code == 503:
        """GithubAPI down"""
        return 'GithubAPI down'
    else:
        return 'some error occurred while fetching repository info'