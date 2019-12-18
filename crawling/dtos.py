class Response:

    def __init__(self, blog, title, link, contents, text_mining_file):
        self.blog = blog
        self.title = title
        self.link = link
        self.contents = contents
        self.text_mining_file = text_mining_file

    @property
    def get_blog(self):
        return self.blog

    @property
    def get_title(self):
        return self.title

    @property
    def get_link(self):
        return self.link

    @property
    def get_text_mining_file(self):
        return self.text_mining_file


