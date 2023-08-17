
def number_to_letter(number: int) -> str:
    if number <= 9:
        return str(number)
    letter = chr(number + 55)
    return letter

def letter_to_number(letter: str) -> int:
    try:
        num_letter = int(letter)
        return num_letter
    except:
        if letter.isalpha() and len(letter) == 1:
            return int(ord(letter.capitalize()) - 64) + 9
        else:
            return 0

def custom_base_to_ten(num, base):
    position = len(num) - 1
    output = 0

    for i in range(0, len(num)):
        decipher_num = letter_to_number(num[i])

        if position != 0:
            mult = base ** position
            decipher_num = decipher_num * mult
            position = position - 1

        output += decipher_num
    return output

def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        x = int(n % b)
        digits.append(number_to_letter(x))
        n //= b
    return digits[::-1]

async def converter(number, from_base, to_base):
    b = custom_base_to_ten(number,from_base)
    c = numberToBase(b,to_base)
    return ''.join(c)


