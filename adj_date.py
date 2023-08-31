import datetime as DT


def adjust_date(time_delta: int) -> str:
    '''adjust date by factor time delta'''
    today: DT.date = DT.date.today()
    nextweek: DT.date = today + DT.timedelta(days=7)
    adjusted_date: DT.date = nextweek + DT.timedelta(time_delta)
    return adjusted_date.strftime('%Y-%m-%d') # '2023-08-22'
