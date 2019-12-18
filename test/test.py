from operator import itemgetter

from dateutil.parser import parse
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup

def test():
    raw = 'Thu, 12 Oct 2017 07:41:16 +0000'

    str_dt = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    # str_dt = parse(date.today()).strftime('%Y-%m-%d')  # to String
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


def test4():
    test = [{'tag': "test", 'count': 5}, {'tag': "test2", 'count': 6}]
    test2 = [{'tag': "test3", 'count': 2}, {'tag': "test4", 'count': 10}]
    test.extend(test2)

    sort_test = sorted(test, key=itemgetter('count'), reverse=True)
    print(sort_test)


if __name__ == '__main__':
    test()
    # test2()
    # test3()

    # test4()
