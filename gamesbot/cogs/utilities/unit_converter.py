from pint import UnitRegistry
import re
from currency_converter import CurrencyConverter

def get_money_name(text):
    output = ''
    text = text.casefold().strip()
    if text in ['€','euro']:
        output = 'EUR'
    elif text in ['$','us','american']:
        output = 'USD'
    elif text in ['¥','yen','japanese','japan']:
        output = 'JPY'
    elif text in ['lev','bulgarian','bulgaria']:
        output = 'BGN'
    elif text in ['kč','czech','czechia','koruna','crown']:
        output = 'CZK'	
    elif text in ['danish','denmark','krone']:
        output = 'DKK'
    elif text in ['pound','sterling','pound sterling','quid','£','uk','ukd']:
        output = 'GBP'
    elif text in ['hungarian','hungaria','forint']:
        output = 'HUF'
    elif text in ['polish','poland','zloty']:
        output = 'PLN'
    elif text in ['lei','leu','romanian','romania']:
        output = 'RON'
    elif text in ['sweden','swedish','Krona']:
        output = 'SEK'
    elif text in ['swiss franc','swiss','switzerland']:
        output = 'CHF'
    elif text in ['iceland','icelandish']:
        output = 'ISK'
    elif text in ['krone','norway','norwegian']:
        output = 'NOK' 
    elif text in ['₺','lira','turkey','turkish']:
        output = 'TRY'
    elif text in ['a$','australia','australian','aussie']:
        output = 'AUD'
    elif text in ['real','brazil','brazilian']:
        output = 'BRL'
    elif text in ['c$','canada','canadian']:
        output = 'CAD'
    elif text in ['chinese','china']:
        output = 'CNY'
    elif text in ['hk$','hk','hong kong']:
        output = 'HKD'
    elif text in ['rupiah','indonesian','indonesia','indo']:
        output = 'IDR'
    elif text in ['shekel','israel','israeli']:
        output = 'ILS'
    elif text in ['rupee','india','indian']:
        output = 'INR'
    elif text in ['korea','south korea','won','south korean','korean']:
        output = 'KRW'
    elif text in ['mexican peso','mexican','mexico']:
        output = 'MXN'
    elif text in ['ringgit','malaysia','malaysian']:
        output = 'MYR'
    elif text in ['new zealand','newzealand','nz','aotearaoa']:
        output = 'NZD'
    elif text in ['piso','philippine peso','philippines','philippine']:
        output = 'PHP'
    elif text in ['singapore','singaporean']:
        output = 'SGD'
    elif text in ['r','rand','south african','south africa']:
        output = 'ZAR'
    else:
        output = text.upper()
    return output

async def money_convert(number: float, from_currency: str, to_currency: str):
    cc = CurrencyConverter()

    from_currency = get_money_name(from_currency)
    to_currency = get_money_name(to_currency)

    try:
        a = cc.convert(number, from_currency.upper(), to_currency.upper())
        output = 'yes', f'{round(a,3)} {to_currency}'
    except Exception as e:
        output = e, None
    del cc
    return output

async def unit_convert(number: float, from_unit:str, to_unit:str) -> str:
    ur = UnitRegistry()
    try:
        a = number * ur.parse_expression(from_unit)
    except:
        del ur
        return f'{from_unit} wasn not found', None
    try:
        output = str(a.to(to_unit))
        if output[:3] == '1.0':
            output = True, output
        elif output[:2] == '0.':
            output = output.split(' ')
            num = output.pop(0)
            art = 'an' if output[0][0] in ['a','e','i','o','u'] else 'a'
            output = True, f'{num} of {art} {" ".join(output)}'
        else:
            if output[len(output) - 2:] in ['ch','sh']:
                output = True, f'{output}es'
            elif output[-1] in ['s','x','z']:
                output = True, f'{output}es'
            else:
                output = True, f'{output}s'
    except:
        output = f'{to_unit} wasn not found', None
    del ur
    return output

async def get_units(text):
    preNum = ''
    preUnit = ''
    postUnit = ''

    if ' to ' not in text:
        return 'Input wasn\'t in the format <number> <unit_type> to <unit_type>', None, None, None
    myList = text.split(' to ')
    if len(myList) != 2:
        return 'Input wasn\'t in the format <number> <unit_type> to <unit_type>', None, None, None
    
    try:
        preUnit = re.sub(r'[0-9\.]+', '', myList[0])
        if preUnit == '':
            return 'Input wasn\'t in the format <number> <unit_type> to <unit_type>', None, None, None
        preNum = re.sub('[^0-9\.]', '', myList[0])
        preNum = re.sub(r'\s]+', '', preNum)
        preNum = float(preNum)
    except:
        return 'Input wasn\'t in the format <number> <unit_type> to <unit_type>', None, None, None
    
    try:
        postUnit = re.sub(r'[0-9\.]+', '', myList[1])
        if postUnit == '':
            return 'Input wasn\'t in the format <number> <unit_type> to <unit_type>', None, None, None
    except:
        return 'Input wasn\'t in the format <number> <unit_type> to <unit_type>', None, None, None
    
    return 'yes', preNum, preUnit, postUnit
