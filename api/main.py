from flask import Flask, render_template, request
from api.crud import add_info, init_db

app = Flask(__name__)


@app.route("/")
def init():
    return render_template('main.html')


@app.route("/", methods=['POST'])
def post():
    if request.method == 'POST':
        email = request.form['email']
        blog = request.form['blog']
        blog_type = ("NAVER" if request.form.get("blogType") == "네이버" else "TISTORY")
        save(email, blog, blog_type)

    return render_template('main.html')


def save(email, blog, blog_type):
    print("email : " + email + "   blog" + blog)
    print(blog_type)
    add_info(email, blog, blog_type)


if __name__ == '__main__':
    app.run()
