from random import randint
from math import floor
from discord import Embed

width = 9
height = 9
nBombs = 20
board = [[0 for i in range(width)] for j in range(height)]
bombs = [[0, 0]] * nBombs
emojis = [':blue_square:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:']
emojiBomb = ':boom:'


def genBomb(bombs):
    x = randint(0, width - 1)
    y = randint(0, height - 1)
    if [x, y] in bombs:
        return genBomb(bombs)
    return [x, y]


def genBoard():
    newBoard = [[0 for i in range(width)] for j in range(height)]
    bombs = [[0, 0]] * nBombs
    for i in range(nBombs):
        b = genBomb(bombs)
        bombs[i] = b
        newBoard[b[1]][b[0]] = 10
        for y in range(-1, 2):
            for x in range(-1, 2):
                yc = b[1] + y
                xc = b[0] + x
                if 0 <= xc < width and 0 <= yc < height:
                    newBoard[yc][xc] += 1
    placeVoid = True
    i = 0
    while placeVoid and i < 200:
        x = randint(0, width - 1)
        y = randint(0, height - 1)
        if newBoard[y][x] == 0:
            newBoard[y][x] = -10
            placeVoid = False
        i += 1
    return (newBoard)


def print_minesweeper():
    board = genBoard()

    embed = Embed(
        title='Minesweeper',
        colour = 0x4C4E52
    )

    output = ''
    for i in board:
        for j in i:
            if j < 0:
                output += emojis[0]
            elif j < 9:
                output += '{1}{0}{1}'.format(emojis[j], '||')
            else:
                output += '{1}{0}{1}'.format(emojiBomb, '||')
        output += '\n'
    
    embed.add_field(
        inline=False,
        name=
            '**Size:** {0}x{1} · '.format(width, height)
            +'**Mines:** {0} ({1}%)\n'.format(nBombs, floor(nBombs / (height * width) * 100)),
        value=output
    )

    return embed