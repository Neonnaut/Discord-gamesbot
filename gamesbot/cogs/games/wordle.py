import datetime
import random
import re
from typing import List, Optional

from constants import WARN

import discord
from constants import WORDLE_SORT_KEY

popular_words = open('cogs/games/dict-popular.txt').read().splitlines()
random.Random(WORDLE_SORT_KEY).shuffle(popular_words)
all_words = set(word.strip() for word in open('cogs/games/dict-sowpods.txt'))

EMOJI_CODES = {
    'green': {
        'a': '[2;32m[2;47m A ',
        'b': '[2;32m[2;47m B ',
        'c': '[2;32m[2;47m C ',
        'd': '[2;32m[2;47m D ',
        'e': '[2;32m[2;47m E ',
        'f': '[2;32m[2;47m F ',
        'g': '[2;32m[2;47m G ',
        'h': '[2;32m[2;47m H ',
        'i': '[2;32m[2;47m I ',
        'j': '[2;32m[2;47m J ',
        'k': '[2;32m[2;47m K ',
        'l': '[2;32m[2;47m L ',
        'm': '[2;32m[2;47m M ',
        'n': '[2;32m[2;47m N ',
        'o': '[2;32m[2;47m O ',
        'p': '[2;32m[2;47m P ',
        'q': '[2;32m[2;47m Q ',
        'r': '[2;32m[2;47m R ',
        's': '[2;32m[2;47m S ',
        't': '[2;32m[2;47m T ',
        'u': '[2;32m[2;47m U ',
        'v': '[2;32m[2;47m V ',
        'w': '[2;32m[2;47m W ',
        'x': '[2;32m[2;47m X ',
        'y': '[2;32m[2;47m Y ',
        'z': '[2;32m[2;47m Z ',
    },
    'yellow': {
        'a': '[2;41m[2;37m A̰ ',
        'b': '[2;41m[2;37m B̰ ',
        'c': '[2;41m[2;37m C̰ ',
        'd': '[2;41m[2;37m D̰ ',
        'e': '[2;41m[2;37m Ḛ ',
        'f': '[2;41m[2;37m F̰ ',
        'g': '[2;41m[2;37m G̰ ',
        'h': '[2;41m[2;37m H̰ ',
        'i': '[2;41m[2;37m Ḭ ',
        'j': '[2;41m[2;37m J̰ ',
        'k': '[2;41m[2;37m K̰ ',
        'l': '[2;41m[2;37m L̰ ',
        'm': '[2;41m[2;37m M̰ ',
        'n': '[2;41m[2;37m N̰ ',
        'o': '[2;41m[2;37m O̰ ',
        'p': '[2;41m[2;37m P̰ ',
        'q': '[2;41m[2;37m Q̰ ',
        'r': '[2;41m[2;37m R̰ ',
        's': '[2;41m[2;37m S̰ ',
        't': '[2;41m[2;37m T̰ ',
        'u': '[2;41m[2;37m Ṵ ',
        'v': '[2;41m[2;37m V̰ ',
        'w': '[2;41m[2;37m W̰ ',
        'x': '[2;41m[2;37m X̰ ',
        'y': '[2;41m[2;37m Y̰ ',
        'z': '[2;41m[2;37m Z̰ ',
    },
    'grey': {
        'a': '[2;42m[2;37m A͓ ',
        'b': '[2;42m[2;37m ͓B ',
        'c': '[2;42m[2;37m ͓C ',
        'd': '[2;42m[2;37m D͓ ',
        'e': '[2;42m[2;37m E͓ ',
        'f': '[2;42m[2;37m F͓ ',
        'g': '[2;42m[2;37m G͓ ',
        'h': '[2;42m[2;37m H͓ ',
        'i': '[2;42m[2;37m I͓ ',
        'j': '[2;42m[2;37m J͓ ',
        'k': '[2;42m[2;37m K͓ ',
        'l': '[2;42m[2;37m L͓ ',
        'm': '[2;42m[2;37m M͓ ',
        'n': '[2;42m[2;37m N͓ ',
        'o': '[2;42m[2;37m O͓ ',
        'p': '[2;42m[2;37m ͓P ',
        'q': '[2;42m[2;37m Q͓ ',
        'r': '[2;42m[2;37m R͓ ',
        's': '[2;42m[2;37m S͓ ',
        't': '[2;42m[2;37m T͓ ',
        'u': '[2;42m[2;37m U͓ ',
        'v': '[2;42m[2;37m V͓ ',
        'w': '[2;42m[2;37m W͓ ',
        'x': '[2;42m[2;37m X͓ ',
        'y': '[2;42m[2;37m Y͓ ',
        'z': '[2;42m[2;37m Z͓ ',
    },
}

def generate_coloured_word(guess: str, answer: str) -> (tuple[str, list, list, list]):
    """
    Builds a string of emoji codes where each letter is
    coloured based on the key:
    - Same letter, same place: Green
    - Same letter, different place: Yellow
    - Different letter: Grey
    Args:
        word (str): The word to be coloured
        answer (str): The answer to the word
    Returns:
        str: A string of emoji codes
    """
    coloured_word = [EMOJI_CODES['grey'][letter] for letter in guess]
    guess_letters: List[Optional[str]] = list(guess)
    answer_letters: List[Optional[str]] = list(answer)

    absent_letters = list(guess.upper())
    missplaced_letters = []
    placed_letters = []

    # change colours to green if same letter and same place
    for i in range(len(guess_letters)):
        if guess_letters[i] == answer_letters[i]:
            my_letter = guess_letters[i].upper()
            coloured_word[i] = EMOJI_CODES['green'][guess_letters[i]]
            answer_letters[i] = None
            guess_letters[i] = None
            placed_letters.append(my_letter)
            absent_letters.remove(my_letter)
    # change colours to yellow if same letter and not the same place
    for i in range(len(guess_letters)):
        if guess_letters[i] is not None and guess_letters[i] in answer_letters:
            my_letter = guess_letters[i].upper()
            coloured_word[i] = EMOJI_CODES['yellow'][guess_letters[i]]
            answer_letters[answer_letters.index(guess_letters[i])] = None
            missplaced_letters.append(my_letter)
            absent_letters.remove(my_letter)

    for char in absent_letters:
        if char in missplaced_letters:
            absent_letters.remove(char)
        elif char in placed_letters:
            absent_letters.remove(char)

    return ''.join(coloured_word), missplaced_letters, placed_letters, absent_letters

def generate_puzzle_embed(user: discord.User, puzzle_id: int) -> discord.Embed:
    """
    Generate an embed for a new puzzle given the puzzle id and user
    Args:
        user (discord.User): The user who submitted the puzzle
        puzzle_id (int): The puzzle ID
    Returns:
        discord.Embed: The embed to be sent
    """
    embed = discord.Embed(
        title=f'Discord Wordle #{puzzle_id} 0/6 guesses',
        colour=0X45c33a
    )

    embed.add_field(value='**Correct**:\n**Missplaced**:\n**Total Absent**:',name='\u200b')

    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
    embed.set_footer(
        text='To guess, reply to this message with a word'
    )
    return embed

def update_embed(embed: discord.Embed, guess: str) -> discord.Embed:
    """
    Updates the embed with the new guesses
    Args:
        embed (discord.Embed): The embed to be updated
        puzzle_id (int): The puzzle ID
        guess (str): The guess made by the user
    Returns:
        discord.Embed: The updated embed
    """
    title = embed.title.replace('Discord Wordle ', '')

    puzzle_id = title.split()[0]
    puzzle_id = int(puzzle_id.replace('#', ''))

    no_of_guesses = title.split()[1].split('/')[0]
    no_of_guesses = int(no_of_guesses) + 1
    embed.title = f"Discord Wordle #{puzzle_id} {no_of_guesses}/6 guesses"

    answer = popular_words[puzzle_id]

    # Add answer to embed description
    coloured_word, missplaced, correct, absent = generate_coloured_word(guess, answer)
    old_description = embed.description[:-3] if embed.description else '```ansi\n'
    new_description = f'{old_description}\n{coloured_word}```'
    embed.description = new_description

    myLines = embed._fields[0].get('value').split('\n')
    correct = sorted(correct)

    missplaced = sorted(missplaced)

    old_absent = myLines[2].split(':')[1].split(' ')
    absent = sorted(list(dict.fromkeys(old_absent + absent)))

    embed.clear_fields()

    embed.add_field(
        value=f'**Correct**: {" ".join(correct).strip()}'
        f'\n**Missplaced**: {" ".join(missplaced).strip()}'
        f'\n**Total Absent**: {" ".join(absent).strip()}',
        name='\u200b')

    # check for game over
    if guess == answer:
        if no_of_guesses == 6:
            embed.set_footer(text='Phew!')
        if no_of_guesses == 5:
            embed.set_footer(text='Great!')
        if no_of_guesses == 4:
            embed.set_footer(text='Splendid!')
        if no_of_guesses == 3:
            embed.set_footer(text='Impressive!')
        if no_of_guesses == 2:
            embed.set_footer(text='Magnificent!')
        if no_of_guesses == 1:
            embed.set_footer(text='Genius!')
    elif no_of_guesses == 6:
        embed.set_footer(text=f'The answer was {answer}!')
    return embed

def is_valid_word(word: str) -> bool:
    """
    Validates a word
    Args:
        word (str): The word to validate
    Returns:
        bool: Whether the word is valid
    """
    return word in all_words

def random_puzzle_id() -> int:
    """
    Generates a random puzzle ID
    Returns:
        int: A random puzzle ID
    """
    return random.randint(0, len(popular_words) - 1)

def daily_puzzle_id() -> int:
    """
    Calculates the puzzle ID for the daily puzzle
    Returns:
        int: The puzzle ID for the daily puzzle
    """
    # calculate days since 1/1/2022 and mod by the number of puzzles
    num_words = len(popular_words)
    time_diff = datetime.datetime.now().date() - datetime.date(2022, 1, 1)
    return time_diff.days % num_words

def is_game_over(embed: discord.Embed) -> bool:
    """
    Checks if the game is over in the embed
    Args:
        embed (discord.Embed): The embed to check
    Returns:
        bool: Whether the game is over
    """
    if embed.footer.text == 'To guess, reply to this message with a word':
        return False
    else:
        return True

def generate_info_embed(prefix) -> discord.Embed:
    """
    Generates an embed with information about the bot
    Returns:
        discord.Embed: The embed to be sent
    """
    embed = discord.Embed(
        title='Guess the Wordle in 6 tries',
        description=
            'Each guess must be a valid 5 letter word by replying to the bot message.\n'
            'The colours of the tiles change to show how close the guess is to the word.\n',
        colour=0X45c33a
    )
    
    embed.add_field(
        inline=False,
        name=f'**Example**',
        value=
            f'```ansi\n{EMOJI_CODES["green"]["w"]}{EMOJI_CODES["yellow"]["e"]}{EMOJI_CODES["grey"]["a"]}{EMOJI_CODES["grey"]["r"]}{EMOJI_CODES["grey"]["y"]}```'
            '__W__ is in the word and in the correct spot\n'
            '__E__ is in the word but in the wrong spot\n'
            '__A__ is not in the word in any spot\n'
    )
    embed.add_field(
        inline=False,
        name=f'**You can start a game with**',
        value=
            f':key: `{prefix}wordle <puzzle_id>` - Play a puzzle by ID\n'
            f':sunny: `{prefix}wordle daily` - Play the puzzle of the day\n'
            f':game_die: `{prefix}wordle random` - Play a random puzzle\n'
    )
    return embed

async def process_message_as_guess(
    bot: discord.Client, message: discord.Message,
    parent, embed: discord.Embed
) -> bool:
    """
    Check if a new message is a reply to a Wordle game.
    If so, validate the guess and update the bot's message.
    Args:
        bot (discord.Client): The bot
        message (discord.Message): The new message to process
    Returns:
        bool: True if the message was processed as a guess, False otherwise
    """

    if 'Discord Wordle #' not in embed.title:
        return False

    guess = message.content.lower()

    # check that the user is the one playing
    if (
        embed.author.name != message.author.name
        or embed.author.icon_url != message.author.display_avatar.url
    ):
        reply = 'Start a new game with /wordle'
        if embed.author:
            reply = f'{WARN} This game was started by {embed.author.name}. {reply}'
        await send_wordle_error(message, reply)
        return True
    # check that the game is not over
    if is_game_over(embed):
        await send_wordle_error(message, 'The game is already over. Start a new game with /wordle')
        return True

    # strip mentions from the guess
    guess = re.sub(r'<@!?\d+>', '', guess).strip()

    if len(guess) == 0:
        await send_wordle_error(message,
            'I am unable to see what you are trying to guess.\n'
            'Please try mentioning me in your reply before the word you want to guess.\n\n'
            f'**For example:**\n{bot.user.mention} crate\n\n'            
        )
        return True

    # check that a single word is in the message
    if len(guess.split()) > 1:
        await send_wordle_error(message, f'{guess} is not a 5-letter word')
        return True

    # check that the word is valid
    if not is_valid_word(guess):
        await send_wordle_error(message, f'{guess} is not a valid word')
        return True

    # update the embed
    embed = update_embed(embed, guess)
    await parent.edit(embed=embed)

    # attempt to delete the message
    try:
        await message.delete()
    except Exception:
        pass
    return True

async def send_wordle_error(message, error):
    """Send error reply and delete message"""
    await message.reply(f'{WARN} {error}', delete_after=5)
    try:
        await message.delete()
    except:
        pass