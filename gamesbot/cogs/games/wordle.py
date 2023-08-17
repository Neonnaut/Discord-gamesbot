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
        'a': '<:green_a:1036629308262858894>',
        'b': '<:green_b:1036629310456475688>',
        'c': '<:green_c:1036629312209702942>',
        'd': '<:green_d:1036629313891610674>',
        'e': '<:green_e:1036629315699355678>',
        'f': '<:green_f:1036629317481930813>',
        'g': '<:green_g:1036629319625228308>',
        'h': '<:green_h:1036629321588154408>',
        'i': '<:green_i:1036629323291045909>',
        'j': '<:green_j:1036629325228810303>',
        'k': '<:green_k:1036629327028162581>',
        'l': '<:green_l:1036629329293103104>',
        'm': '<:green_m:1036629331004379197>',
        'n': '<:green_n:1036629333290262588>',
        'o': '<:green_o:1036629334921846916>',
        'p': '<:green_p:1036629337350348830>',
        'q': '<:green_q:1036629339162300436>',
        'r': '<:green_r:1036629341125234778>',
        's': '<:green_s:1036629342895218768>',
        't': '<:green_t:1036629344614879283>',
        'u': '<:green_u:1036629346393260064>',
        'v': '<:green_v:1036629348171653130>',
        'w': '<:green_w:1036629349799047218>',
        'x': '<:green_x:1036629351380303943>',
        'y': '<:green_y:1036629353557143632>',
        'z': '<:green_z:1036629355482320906>',
    },
    'yellow': {
        'a': '<:yellow_a:1038074301699600385>',
        'b': '<:yellow_b:1038074303687688262>',
        'c': '<:yellow_c:1038074305780646019>',
        'd': '<:yellow_d:1038074307823284254>',
        'e': '<:yellow_e:1038074309656190977>',
        'f': '<:yellow_f:1038074311753334804>',
        'g': '<:yellow_g:1038074313649172480>',
        'h': '<:yellow_h:1038074315301715999>',
        'i': '<:yellow_i:1038074317033975868>',
        'j': '<:yellow_j:1038074318745247774>',
        'k': '<:yellow_k:1038074320485875814>',
        'l': '<:yellow_l:1038074322486566942>',
        'm': '<:yellow_m:1038074323958775910>',
        'n': '<:yellow_n:1038074325464514631>',
        'o': '<:yellow_o:1038074327565881414>',
        'p': '<:yellow_p:1038074329398771763>',
        'q': '<:yellow_q:1038074330757734411>',
        'r': '<:yellow_r:1038074332846510130>',
        's': '<:yellow_s:1038074334591328277>',
        't': '<:yellow_t:1038074336285835354>',
        'u': '<:yellow_u:1038074337959350362>',
        'v': '<:yellow_v:1038074339553189999>',
        'w': '<:yellow_w:1038074341646147584>',
        'x': '<:yellow_x:1038074343227396107>',
        'y': '<:yellow_y:1038074347715309668>',
        'z': '<:yellow_z:1038074349451743273>',
    },
    'grey': {
        'a': '<:grey_a:1036628776676765746>',
        'b': '<:grey_b:1036628778887163955>',
        'c': '<:grey_c:1036628780510347334>',
        'd': '<:grey_d:1036628782183895100>',
        'e': '<:grey_e:1036628784163586149>',
        'f': '<:grey_f:1036628785799368714>',
        'g': '<:grey_g:1036628787443544074>',
        'h': '<:grey_h:1036628789121265714>',
        'i': '<:grey_i:1036628791017091112>',
        'j': '<:grey_j:1036628792791269508>',
        'k': '<:grey_k:1036628794745819186>',
        'l': '<:grey_l:1036628796767486002>',
        'm': '<:grey_m:1036628798860431391>',
        'n': '<:grey_n:1036628800475234304>',
        'o': '<:grey_o:1036628802505277491>',
        'p': '<:grey_p:1036628804606623754>',
        'q': '<:grey_q:1036628806506655774>',
        'r': '<:grey_r:1036628808528302161>',
        's': '<:grey_s:1036628810587701310>',
        't': '<:grey_t:1036628812902965268>',
        'u': '<:grey_u:1036628814740074648>',
        'v': '<:grey_v:1036628816719794257>',
        'w': '<:grey_w:1036628818435244114>',
        'x': '<:grey_x:1036628820486266970>',
        'y': '<:grey_y:1036628822474367036>',
        'z': '<:grey_z:1036628824286298152>',
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
        title=f'Discord Wordle #{puzzle_id}',
        color=0X45c33a,
        description = '\n'.join([generate_blanks()] * 6)
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
    puzzle_id = embed.title.split()[-1]
    puzzle_id = int(puzzle_id.replace('#', ''))
    answer = popular_words[puzzle_id]
    colored_word = generate_colored_word(guess, answer)
    empty_slot = generate_blanks()
    # replace the first blank with the colored word
    embed.description = embed.description.replace(empty_slot, colored_word, 1)
    # check for game over
    num_empty_slots = embed.description.count(empty_slot)
    if guess == answer:
        if num_empty_slots == 0:
            embed.description += '\n\nPhew!'
        if num_empty_slots == 1:
            embed.description += '\n\nGreat!'
        if num_empty_slots == 2:
            embed.description += '\n\nSplendid!'
        if num_empty_slots == 3:
            embed.description += '\n\nImpressive!'
        if num_empty_slots == 4:
            embed.description += '\n\nMagnificent!'
        if num_empty_slots == 5:
            embed.description += '\n\nGenius!'
        embed.set_footer(text='')
    elif num_empty_slots == 0:
        embed.description += f'\n\nThe answer was {answer}!'
        embed.set_footer(text='')
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
    return '\n\n' in embed.description


def generate_info_embed(prefix) -> discord.Embed:
    """
    Generates an embed with information about the bot
    Returns:
        discord.Embed: The embed to be sent
    """

    # Username
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
            f'{EMOJI_CODES["green"]["w"]}{EMOJI_CODES["yellow"]["e"]}{EMOJI_CODES["grey"]["a"]}{EMOJI_CODES["grey"]["r"]}{EMOJI_CODES["grey"]["y"]}\n'
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
        message.delete()
    except:
        pass