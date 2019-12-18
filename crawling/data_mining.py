from collections import Counter
from operator import itemgetter
import nltk
from nltk.corpus import stopwords
from konlpy.tag import Okt
import csv

# import plt
# from wordcloud import WordCloud

OUTPUT_FILE_DIRECTORY = "C:/Users/LG/Desktop/크롤링 텀프로젝트/"


def get_korean_noun(text, ntags=20):
    stop_words = read_ko_stopwords()  # 불용어 목록
    okt = Okt()
    nouns = okt.nouns(text)
    count = Counter(nouns)

    return_list = []
    for word, count in count.most_common(ntags):
        if len(word) <= 1 or word in stop_words or count == 1:  # 길이가 1인것, 불용어, count가 1인것
            continue

        temp = {'tag': word, 'count': count}
        return_list.append(temp)

    return return_list


def read_ko_stopwords():
    ko_stopwords = []
    f = open(OUTPUT_FILE_DIRECTORY + 'ko_stopwords.csv', 'r')
    rdr = csv.reader(f)

    for line in rdr:
        ko_stopwords.append(line[0])

    f.close()
    return ko_stopwords


def get_english_noun(text, ntags=20):
    stop_words = set(stopwords.words('english'))  # 불용어 리스트
    tokens = nltk.word_tokenize(text)  # 토큰화
    tagged_tokens = nltk.pos_tag(tokens)  # 단어, 품사종류 형태
    nouns_and_verbs = [token[0] for token in tagged_tokens if token[1] in ['NN']]  # 명사 추출
    frequency = nltk.FreqDist(nouns_and_verbs)  # 빈도수 계산

    key_list = list(frequency.keys())
    return_list = []
    for key in key_list:
        if len(key) <= 1 or key in stop_words or frequency.get(key) == 1:  # 길이가 1인것, 불용어, count가 1인것
            continue

        temp = {'tag': key, 'count': frequency.get(key)}
        return_list.append(temp)

    return return_list


def get_all_noun(korean_noun_list, english_noun_list):
    korean_noun_list.extend(english_noun_list)  # list 합치기
    sort_noun_list = sorted(korean_noun_list, key=itemgetter('count'), reverse=True)  # 정렬

    if len(sort_noun_list) <= 20:
        return sort_noun_list
    else:
        return sort_noun_list[:20]  # 최대 20개만 출력


def save_word_count(all_noun_list, output_file_name):
    open_output_file = open(OUTPUT_FILE_DIRECTORY + output_file_name, 'w', -1, "utf-8")

    for tag in all_noun_list:
        noun = tag['tag']
        count = tag['count']
        open_output_file.write('{} {}\n'.format(noun, count))  # 파일에 저장

    open_output_file.close()


# def save_word_cloud(all_noun_list):
#     all_noun_dic = {}
#     for noun in all_noun_list:
#         all_noun_dic[noun.get('tag')] = noun.get('count')
#
#     word_cloud = WordCloud(font_path='C:/Windows/Fonts/Arial.ttf', background_color='white',
#                            width=1500, height=1000).generate_from_frequencies(all_noun_dic)
#
#     word_cloud.to_file('test.png') # ***********에러***********


def text_mining(contents_list, str_date, email, blog):
    contents_str = ' '.join(contents_list)  # to String
    blog_str = blog.replace("https://", "")

    noun_count = 20  # 최대 많은 빈도수부터 추출할 명사의 개수
    korean_noun_list = get_korean_noun(contents_str, noun_count)  # konlpy를 이용해 한글 추출
    english_noun_list = get_english_noun(contents_str, noun_count)  # nltk를 이용해 영어 추출
    all_noun_list = get_all_noun(korean_noun_list, english_noun_list)  # 한글 + 영어 명사 최대 20개 추출

    output_file_name = str_date + '_' + '_' + email + '_' + blog_str + '_' + "count.txt"
    save_word_count(all_noun_list, output_file_name)  # 빈도수 파일 저장
    # save_word_cloud(all_noun_list)  # 워드 클라우드 파일 저장

    return output_file_name


def main():
    test_list = ["우리의 아버지", "최고의 선생님", "book 좋다", "java 프로그램", "적", "i your am a man", 'i like java', 'java 자바']
    text_mining(test_list, "test", "test", "test")


if __name__ == '__main__':
    main()

