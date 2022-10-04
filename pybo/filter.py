import locale
locale.setlocale(locale.LC_ALL, '')
def format_datetime(value, fmt='%Y년 %m월 %d일'):
    return value.strftime(fmt)