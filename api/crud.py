from api.database import init_db
from api.database import db_session
from api.models import Info


def show_all_infos():
    queries = db_session.query(Info)
    infos = [dict(id=q.id, email=q.email, blog=q.blog) for q in queries]
    print(entires)
    db_session.close()


def get_all_infos_dict():
    queries = db_session.query(Info)

    infos_model = []
    for q in queries:
        infos_model.append(q)

    db_session.close()
    return infos_model


def print(infos_dic):
    list = infos_dic.values()
    for i in list:
        print(i.count())


def add_info(email, blog, blog_type):
    info = Info(email, blog, blog_type)
    db_session.add(info)
    db_session.commit()
    db_session.close()


def delete_info(email, blog, blog_type):
    db_session.query(Info).filter(Info.email == email, Info.blog == blog, Info.blog_type == blog_type).delete()
    db_session.commit()
    db_session.close()


def main():
    add_info("test1", "test1", "NAVER")


if __name__ == "__main__":
    init_db()
    main()
