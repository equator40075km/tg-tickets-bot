from datetime import date


MONTHS = {
    1: 'январь ❄️',
    2: 'февраль ❄️',
    3: 'март 🌥',
    4: 'апрель ⛅️',
    5: 'май 🌤',
    6: 'июнь ☀️',
    7: 'июль ☀️',
    8: 'август ☀️',
    9: 'сентябрь ⛅️',
    10: 'октябрь 🌦',
    11: 'ноябрь 🌨',
    12: 'декабрь ❄️'
}


def get_month_name(month: int) -> str:
    return MONTHS.get(month, 'ERROR')


def get_month_last_day(_date: date) -> int:
    tmp_date = _date
    while True:
        try:
            tmp_date = tmp_date.replace(day=tmp_date.day + 1)
        except ValueError:
            break

    return tmp_date.day


def get_future_month(offset: int) -> date:
    _date: date = date.today()

    if offset < 1:
        return _date

    if _date.month + offset > 12:
        return _date.replace(year=_date.year + 1,
                             month=_date.month + offset - 12,
                             day=1)

    return _date.replace(month=_date.month + offset,
                         day=1)
