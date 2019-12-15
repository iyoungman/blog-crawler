from dateutil.parser import parse
from datetime import date, timedelta


def test():
    raw = 'Thu, 12 Oct 2017 07:41:16 +0000'
    str_dt = parse(raw).strftime('%Y-%m-%d') # to String
    dt = parse(raw).date()

    print(str_dt)
    print(dt)


def test2():
    today = date.today()
    yesterday = date.today() - timedelta(20)
    print(yesterday)


def test3():
    time1 = date(2019, 12, 12)
    time2 = date.today()
    print((time1 - time2).days)


if __name__ == '__main__':
    # test3()
    test()
    # test2()
