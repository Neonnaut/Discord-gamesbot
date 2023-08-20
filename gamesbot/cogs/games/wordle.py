import datetime
import random
import re
from typing import List, Optional

from constants import ERR, WARN

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
        'a': '[2;47m[2;33m A᷈ ',
        'b': '[2;47m[2;33m B᷈ ',
        'c': '[2;47m[2;33m C᷈ ',
        'd': '[2;47m[2;33m D᷈ ',
        'e': '[2;47m[2;33m E᷈ ',
        'f': '[2;47m[2;33m F᷈ ',
        'g': '[2;47m[2;33m G᷈ ',
        'h': '[2;47m[2;33m H᷈ ',
        'i': '[2;47m[2;33m I᷈ ',
        'j': '[2;47m[2;33m J᷈ ',
        'k': '[2;47m[2;33m K᷈ ',
        'l': '[2;47m[2;33m L᷈ ',
        'm': '[2;47m[2;33m M᷈ ',
        'n': '[2;47m[2;33m N᷈ ',
        'o': '[2;47m[2;33m O᷈ ',
        'p': '[2;47m[2;33m P᷈ ',
        'q': '[2;47m[2;33m Q᷈ ',
        'r': '[2;47m[2;33m R᷈ ',
        's': '[2;47m[2;33m S᷈ ',
        't': '[2;47m[2;33m T᷈ ',
        'u': '[2;47m[2;33m U᷈ ',
        'v': '[2;47m[2;33m V᷈ ',
        'w': '[2;47m[2;33m W᷈ ',
        'x': '[2;47m[2;33m X᷈ ',
        'y': '[2;47m[2;33m Y᷈ ',
        'z': '[2;47m[2;33m Z᷈ ',
    },
    'grey': {
        'a': '[2;42m[2;37m A̽ ',
        'b': '[2;42m[2;37m B̽ ',
        'c': '[2;42m[2;37m C̽ ',
        'd': '[2;42m[2;37m D̽ ',
        'e': '[2;42m[2;37m E̽ ',
        'f': '[2;42m[2;37m F̽ ',
        'g': '[2;42m[2;37m G̽ ',
        'h': '[2;42m[2;37m H̽ ',
        'i': '[2;42m[2;37m I̽ ',
        'j': '[2;42m[2;37m J̽ ',
        'k': '[2;42m[2;37m K̽ ',
        'l': '[2;42m[2;37m L̽ ',
        'm': '[2;42m[2;37m M̽ ',
        'n': '[2;42m[2;37m N̽ ',
        'o': '[2;42m[2;37m O̽ ',
        'p': '[2;42m[2;37m P̽ ',
        'q': '[2;42m[2;37m Q̽ ',
        'r': '[2;42m[2;37m R̽ ',
        's': '[2;42m[2;37m S̽ ',
        't': '[2;42m[2;37m T̽ ',
        'u': '[2;42m[2;37m U̽ ',
        'v': '[2;42m[2;37m V̽ ',
        'w': '[2;42m[2;37m W̽ ',
        'x': '[2;42m[2;37m X̽ ',
        'y': '[2;42m[2;37m Y̽ ',
        'z': '[2;42m[2;37m Z̽ ',
    },
}


def generate_colored_word(guess: str, answer: str) -> str:
    """
    Builds a string of emoji codes where each letter is
    colored based on the key:
    - Same letter, same place: Green
    - Same letter, different place: Yellow
    - Different letter: Gray
    Args:
        word (str): The word to be colored
        answer (str): The answer to the word
    Returns:
        str: A string of emoji codes
    """
    colored_word = [EMOJI_CODES['grey'][letter] for letter in guess]
    guess_letters: List[Optional[str]] = list(guess)
    answer_letters: List[Optional[str]] = list(answer)
    # change colors to green if same letter and same place
    for i in range(len(guess_letters)):
        if guess_letters[i] == answer_letters[i]:
            colored_word[i] = EMOJI_CODES['green'][guess_letters[i]]
            answer_letters[i] = None
            guess_letters[i] = None
    # change colors to yellow if same letter and not the same place
    for i in range(len(guess_letters)):
        if guess_letters[i] is not None and guess_letters[i] in answer_letters:
            colored_word[i] = EMOJI_CODES['yellow'][guess_letters[i]]
            answer_letters[answer_letters.index(guess_letters[i])] = None
    return ''.join(colored_word)


def generate_blanks() -> str:
    """
    Generate a string of 5 blank white square emoji characters
    Returns:
        str: A string of white square emojis
    """
    return '◻️' * 5


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
        title=f'Discord Wordle #{puzzle_id} 0/6',
        color=0X45c33a
    )

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
    embed.title = f"Discord Wordle #{puzzle_id} {no_of_guesses}/6"

    answer = popular_words[puzzle_id]

    # Add answer to embed description
    colored_word = generate_colored_word(guess, answer)
    old_description = embed.description[:-3] if embed.description else '```ansi\n'
    new_description = f'{old_description}\n{colored_word}```'
    embed.description = new_description

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
        color=0X45c33a
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