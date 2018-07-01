from werkzeug.routing import BaseConverter


class Regex_url(BaseConverter):
    def __init__(self,url_map,*args):
        super(Regex_url, self).__init__(url_map)
        self.regex = args[0]



