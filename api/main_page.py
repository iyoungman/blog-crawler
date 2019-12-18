from flask import Flask, render_template, request, redirect, url_for
from api.database_query import add_info, init_db, get_blog_by_email

app = Flask(__name__)


@app.route("/")
def init():
    return render_template('main.html')


@app.route("/", methods=['POST'])
def post():  # 이메일과 블로그 주소로 DB에 저장
    if request.method == 'POST':
        email = request.form['email']
        blog = request.form['blog']
        blog_type = ("NAVER" if request.form.get("blogType") == "네이버" else "TISTORY")
        save(email, blog, blog_type)

    return render_template('main.html')


def save(email, blog, blog_type):
    print("email : " + email + "   blog : " + blog + "   blog_type : " + blog_type)
    add_info(email, blog, blog_type)


@app.route("/list", methods=['POST'])
def confirm_blog_list():  # 나의 블로그 목록 확인
    email = request.form['confirm_email']
    str_blog_list = get_blog_by_email(email)

    return render_template('main.html', blog_list=str_blog_list)


if __name__ == '__main__':
    app.run()
