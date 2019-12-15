import urllib.request
from datetime import date, timedelta

from bs4 import BeautifulSoup
from dateutil.parser import parse

from api.crud import get_all_infos_dict
from crawling.dtos import Response


def crawling():
    infos_model = get_all_infos_dict()
    result_dict = {}

    for model in infos_model:
        email = model.get_email
        blog = model.get_blog
        blog_type = model.get_blog_type

        rcv_data = get_request_url(blog_type, blog)
        soup_data = BeautifulSoup(rcv_data, 'html.parser')

        for index_data in soup_data.find_all("item"):
            put_data = index_data.find("pubdate").text
            dt_put_data = parse(put_data).date()
            # str_put_data = parse(put_data).strftime('%Y-%m-%d')
            sub_date = (dt_put_data - get_yesterday()).days

            if not sub_date >= 0:  # Sat, 14 Dec 2019 23:43:56 +0900
                break
            title = index_data.find("title").text
            link = index_data.find("guid").text
            if email in result_dict:  # 존재하면
                result_dict[email].append(Response(blog, title, link, None))
            else:
                dto_list = []
                dto_list.append(Response(blog, title, link, None))
                result_dict[email] = dto_list

    print("END")


def get_request_url(blog_type, blog_url, enc='utf-8'):
    if blog_type == "NAVER":
        splits = blog_url.split('.')
        splits.insert(1, "rss.")
        blog_url = blog_url + "".join(splits)
    else:  # 티스토리
        blog_url = blog_url + "/rss"

    req = urllib.request.Request(blog_url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            try:
                rcv = response.read()
                ret = rcv.decode(enc)
            except UnicodeDecodeError:
                ret = rcv.decode(enc, 'replace')
            return ret
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (date.today(), blog_url))
        return None


def get_yesterday():
    BEFORE_DAY = 20
    yesterday = date.today() - timedelta(BEFORE_DAY)
    return yesterday


if __name__ == '__main__':
    crawling()

# import urllib.request
# from bs4 import BeautifulSoup
# import pandas as pd
# import datetime
# from itertools import count
#
# def get_request_url(url, enc='utf-8'):
#     req = urllib.request.Request(url)
#     try:
#         response = urllib.request.urlopen(req)
#         if response.getcode() == 200:
#             try:
#                 rcv = response.read()
#                 ret = rcv.decode(enc)
#             except UnicodeDecodeError:
#                 ret = rcv.decode(enc, 'replace')
#             return ret
#     except Exception as e:
#         print(e)
#         print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
#         return None
#
# def getPelicanaAddress(result):
#
#     for page_idx in count():
#
#         Pelicana_URL = 'http://www.pelicana.co.kr/store/stroe_search.html?&branch_name=&gu=&si=&page=%s' \
#                        % str(page_idx + 1)
#         print ("[Pericana Page] : [%s]" % (str(page_idx + 1)))
#
#         rcv_data = get_request_url(Pelicana_URL)
#         soupData = BeautifulSoup(rcv_data, 'html.parser')
#
#         store_table = soupData.find('table', attrs={'class':'table mt20'})
#         tbody = store_table.find('tbody')
#         bEnd = True
#         for store_tr in tbody.findAll('tr'):
#             bEnd = False
#             tr_tag = list(store_tr.strings)
#             store_name = tr_tag[1]
#             store_address = tr_tag[3]
#             store_sido_gu = store_address.split()[:2]
#
#             result.append([store_name] + store_sido_gu + [store_address])
#
#         if (bEnd == True):
#             print(result[0]) #확인용으로 출력
#             print("== 데이터 수 : %d" %len(result))
#             return
#
#     return
#
# def cswin_pericana():
#
#     result = []
#     print('PERICANA ADDRESS CRAWLING START')
#     getPelicanaAddress(result)
#     pericana_table = pd.DataFrame(result, columns=('store', 'sido', 'gungu', 'store_address'))
#     pericana_table.to_csv("./pericana.csv", encoding="cp949", mode='w', index=True)
#     del result[:]
#     print('FINISHED')
#
# if __name__ == '__main__':
#     cswin_pericana()
#
#
#
#
