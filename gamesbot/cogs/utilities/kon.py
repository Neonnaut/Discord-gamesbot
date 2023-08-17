import random

fricatives = ['ɸ','β','f','v','θ','ð'
             ,'s','z','ʃ','ʒ','ɕ','ʑ','ʂ','ʐ'
             ,'ç','ʝ','x','ɣ','χ','ʁ','ħ','ʕ','h','ɦ','ɬ','ɮ']
palatals = ['c','ɟ','ɲ','ç','ʝ','j','ʎ','ɕ','ʑ']
laterlas = ['ʟ','ʎ','l','ɬ','ɮ','ɭ','ɺ']
nasals = ['m','n','ɳ','ɲ','ŋ','ɴ']
plosives = ['p','b','t','d','ʈ','ɖ','c','ɟ','k','g','q','ɢ','ʔ']
rhotics = ['r','ɾ','ɹ','ɻ','ʀ','ʁ','ɽ','ɺ']
sibilants = ['s','z','ʃ','ʒ','ʂ','ʐ','ɕ','ʑ']
taps = ['ⱱ','ɾ','ɽ','ɺ']
approx = ['ʋ','ɹ','ɻ','j','ɰ','l','ɭ','ʎ','ʟ','w','ɥ']
trills = ['ʙ','r','ɽr','ʀ']
click = ['k͡ʘ','q͡ʘ','ɡ͡ʘ','ɢ͡ʘ','ŋ͡ʘ','ɴ͡ʘ'
         ,'k͡ǀ','q͡ǀ','ɡ͡ǀ','ɢ͡ǀ','ŋ͡ǀ','ɴ͡ǀ'
         ,'k͡ǂ','q͡ǂ','ɡ͡ǂ','ɢ͡ǂ','ŋ͡ǂ','ɴ͡ǂ'
         ,'k͡ǁ','q͡ǁ','ɡ͡ǁ','ɢ͡ǁ','ŋ͡ǁ','ɴ͡ǁ']
implosives = ['ɓ','ɗ','ᶑ','ʄ','ɠ','ʛ']
ejectives = ['pʼ','tʼ','ʈʼ','cʼ','kʼ','qʼ','t͡sʼ','t̠͡ʃʼ','t͡ʂʼ','k͡xʼ','q͡χʼ']
africates = ['t͡s','d͡z','t͡ʃ','d͡ʒ','t͡ʂ','d͡ʐ','t͡ɕ','d͡ʑ'
             ,'p͡ɸ','b͡β ','c͡ç','ɟ͡ʝ','k͡x','ɡ͡ɣ','q͡χ','ɢ͡ʁ','t͡ɬ','d͡ɮ']

consonants = plosives + nasals + fricatives + approx + taps + trills\
           + implosives + ejectives + africates

vowelw = ['i','y','ɨ','ʉ','ɯ','u'
        ,'ɪ','ʏ','ʊ','e','ø','ɘ','ɵ','ɤ','o'
        ,'ə','ɛ','œ','ɜ','ɞ','ʌ','ɔ'
        ,'æ','ɐ','a','ɶ','ɑ','ɒ']

vowel = ['i','y','ɨ','ɯ','u'
        ,'ɪ','ʏ','ʊ','e','ø','ɤ','o'
        ,'ə','ɛ','œ','ʌ','ɔ'
        ,'æ','a']

allletters = consonants + vowelw + click



def generate_word(text):
    prevchar = ''
    spatout = ''
    for char in text:
        if char == 'A':
            prevchar = random.choice(africates)
            spatout += prevchar
        elif char == 'C': #consonants
            prevchar = random.choice(consonants)
            spatout += prevchar
        elif char == 'E': #consonants
            prevchar = random.choice(ejectives)
            spatout += prevchar
        elif char == 'F':
            prevchar = random.choice(fricatives)
            spatout += prevchar
        elif char == 'I':
            prevchar = random.choice(implosives)
            spatout += prevchar
        elif char == 'J':
            prevchar = random.choice(palatals)
            spatout += prevchar
        elif char == 'K':
            prevchar = random.choice(click)
            spatout += prevchar
        elif char == 'L':
            prevchar = random.choice(laterlas)
            spatout += prevchar
        elif char == 'N':
            prevchar = random.choice(nasals)
            spatout += prevchar
        elif char == 'P':
            prevchar = random.choice(plosives)
            spatout += prevchar
        elif char == 'R':
            prevchar = random.choice(rhotics)
            spatout += prevchar
        elif char == 'S':
            prevchar = random.choice(sibilants)
            spatout += prevchar
        elif char == 'T':
            prevchar = random.choice(taps)
            spatout += prevchar
        elif char == 'U':
            prevchar = random.choice(vowelw)
            spatout += prevchar
        elif char == 'V':
            prevchar = random.choice(vowel)
            spatout += prevchar
        elif char == 'W':
            prevchar = random.choice(approx)
            spatout += prevchar
        elif char == 'X':
            prevchar = random.choice(trills)
            spatout += prevchar
        elif char == '*':
            prevchar = random.choice(allletters)
            spatout += prevchar
        elif char == '+':
            prevchar if prevchar != '' else '?'
            spatout += prevchar
        else:
            spatout += char
    return spatout

def do_block(block):
    lines = block.split('\n')
    MY_LINES_LIST = []
    for i in range(0, len(lines)):
        if lines[i] == '':
            pass #Line is null
        else:
            words = lines[i].split(' ')
            for i in range(len(words)):
                pass
            MY_LINES_LIST.append(words)

    longest_line = 0
    for line in MY_LINES_LIST:
        if longest_line <= len(line):
            longest_line = len(line)

    for i in range(0, len(MY_LINES_LIST)):
        while len(MY_LINES_LIST[i]) != longest_line:
            MY_LINES_LIST[i].append('')

    max_columns = []
    for i in range(0, longest_line):
        max_columns.append(0)

    for l in range(0, len(MY_LINES_LIST)): # For line in line
        for w in range(0, len(MY_LINES_LIST[l])): # For word in line
            if max_columns[w] < len(MY_LINES_LIST[l][w]):
                max_columns[w] = len(MY_LINES_LIST[l][w])

    return_lines = []

    for l in range(0, len(MY_LINES_LIST)): # For line in line
        for w in range(0, len(MY_LINES_LIST[l])): # For word in line
            while  len(MY_LINES_LIST[l][w]) < max_columns[w]:
                MY_LINES_LIST[l][w] += ' '
        return_lines.append(' '.join(MY_LINES_LIST[l]))

    return '\n'.join(return_lines)