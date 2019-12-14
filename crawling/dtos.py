

class Response:

    def __init__(self, blog, title, link, contents):
        self.blog = blog
        self.title = title
        self.link = link
        self.contents = contents

    @property
    def get_blog(self):
        return self.blog