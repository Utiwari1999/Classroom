# script to strip given text from HTML tags
# usecase: Content from webpages recovered may have stray HTML tags, like <b> or <i>

from html.parser import HTMLParser
from io import StringIO

#Simple class to encapsulate the stripping of html tags.
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

#module to strip tags.
#uses the MLStripper class
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    # print(s.get_data())
    return s.get_data()
