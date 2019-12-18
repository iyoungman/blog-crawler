import urllib.request
from datetime import date, timedelta, datetime

from bs4 import BeautifulSoup
from dateutil.parser import parse

from api.database_query import get_all_infos_dict
from crawling.dtos import Response
from crawling.data_mining import text_mining
from crawling.send_email import send_email
import ssl
import re


def crawling():
    infos_model = get_all_infos_dict()  # DB에서 사용자 이메일, 블로그 조회
    result_dict = {}  # 결과를 담을 딕셔너리

    for model in infos_model:
        email = model.get_email  # 이메일
        blog = model.get_blog  # 블로그
        blog_type = model.get_blog_type  # 블로그 타입

        rcv_data = get_request_url(blog_type, blog)
        soup_data = BeautifulSoup(rcv_data, 'html.parser')

        for index_data in soup_data.findAll("item"):
            put_data = index_data.find("pubdate").text  # 블로그 글 날짜
            dt_put_data = parse(put_data).date()
            sub_date = (dt_put_data - get_yesterday()).days  # 블로그 글 날짜 - 어제 날짜의 차이
            if not sub_date >= 0:  # 어제 쓰여진 글이 아니면
                break

            link = index_data.find("guid").get_text()  # 글 링크
            contents_list = []
            if blog_type == "NAVER":  # 네이버 본문 내용
                title = index_data.find('title').get_text().replace('[CCIE] ', "")  # 글 제목
                title = re.sub('[-=.#/?:$}]', '', title)  # 특수문자 제거
                contents_tag_str = index_data.find('description').get_text()
                contents_list = [contents_tag_str]
            else:  # 티스토리 본문 내용
                title = index_data.find('title').get_text()  # 글 제목
                contents_tag_str = index_data.find('description').contents[0]  # tag가 들어간 문자열
                contents_list = get_tistory_contents_list(contents_tag_str)

            # 텍스트 마이닝 후 저장된 파일 경로 반환
            text_mining_file = text_mining(contents_list, datetime.today().strftime('%Y-%m-%d'), email, title)

            if email in result_dict:  # 존재하면
                result_dict[email].append(Response(blog, title, link, contents_list, text_mining_file))
            else:
                dto_list = [Response(blog, title, link, contents_list, text_mining_file)]
                result_dict[email] = dto_list

    save_blog_update_info(result_dict)

    print("===================CRAWLING END===================")


def get_request_url(blog_type, blog_url, enc='utf-8'):
    if blog_type == "NAVER":
        splits = blog_url.split('.')
        splits.insert(1, "rss")
        blog_url = ".".join(splits)
    else:  # 티스토리
        blog_url = blog_url + "/rss"

    req = urllib.request.Request(blog_url)
    try:
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(req, context=context)
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


def get_tistory_contents_list(contents_tag_str):
    contents_tag = BeautifulSoup(contents_tag_str)  # str to tag

    contents_list = []
    for contents_p in contents_tag.findAll('p'):
        if contents_p.text == '\xa0':  # 공백인 p 태그 패스
            continue
        contents_list.append(contents_p.text + " ")  # 블로그 글 본문 내용 추출

    return contents_list


def save_blog_update_info(result_dict=dict):
    output_file_directory = "C:/Users/LG/Desktop/크롤링 텀프로젝트/"

    for key in result_dict.keys():  # key = email
        dto_list = result_dict.get(key)
        open_output_file = open(output_file_directory + "BlogUpdate.txt", 'w', -1, "utf-8")
        text_mining_dic = {}

        for dto in dto_list:
            blog = dto.get_blog
            title = dto.get_title
            link = dto.get_link
            text_mining_file = dto.get_text_mining_file

            open_output_file.write(blog + '\n')
            open_output_file.write(title + '\n')
            open_output_file.write(link + '\n\n')
            text_mining_dic[title + '.txt'] = output_file_directory + text_mining_file

        open_output_file.close()

        text_mining_dic['BlogUpdate.txt'] = output_file_directory + "BlogUpdate.txt"
        send_email([key], text_mining_dic)  # 이메일 전송


def get_yesterday():
    BEFORE_DAY = 20  # 원래는 1이지만(하루전 블로그 글 크롤링) 실험을 위해 20일로 설정
    yesterday = date.today() - timedelta(BEFORE_DAY)
    return yesterday


if __name__ == '__main__':
    crawling()
