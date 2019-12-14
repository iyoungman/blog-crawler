from dateutil.parser import parse
from datetime import date, timedelta


def test():
    raw = 'Thu, 12 Oct 2017 07:41:16 +0000'
    dt = parse(raw).strftime('%Y-%m-%d')
    print(dt)


def test2():
    today = date.today()
    yesterday = date.today() - timedelta(20)
    print(yesterday)


if __name__ == '__main__':
    test()
    test2()
