## api 패키지
### database_create.py
* ORM을 통해 DB 테이블 생성

### database_model.py
* DB 테이블의 모델

### database_query.py
* DB 쿼리 목록

### main_page.py
* Flask를 통한 API 클래스

### templates 패키지의 main.html
* 메인 페이지

***  

## crawling 패키지
### blog_crawling.py
* 블로그 목록 크롤링
    - 크롤링한 정보를 파일 저장

### data_mining.py
* 데이터 마이닝을 하는 모듈
    - 빈도수 추출후 파일 저장

### dtos.py
* 이메일로 전송할 정보를 저장할 모듈

### send_email.py
* 결과를 이메일로 전송하는 모듈
    - 위에서 저장한 파일 전송
