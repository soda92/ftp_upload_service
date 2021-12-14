import datetime
from model import Config


def check_time(config: Config, time: datetime.datetime, check_period: datetime.timedelta):
    time_array = config.schedules.split(',')
    runs = []
    for i in time_array:
        hour, minutes = map(int, i.split(':'))
        time_for_check = datetime.datetime(
            year=time.year, month=time.month,
            day=time.day, hour=hour, minute=minutes)
        runs.append(time_for_check)

    for i in runs:
        if i <= time < i+check_period:
            return True
    return False
