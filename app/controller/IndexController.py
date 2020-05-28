from BaseController import BaseController


class IndexController(BaseController):

    def index(self):
        return self.render('index')
