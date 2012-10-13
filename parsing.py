import urllib
from HTMLParser import HTMLParser


def loadPage(url):
    try:
        f = urllib.urlopen(url)
    except (UnicodeError, IOError):
        return None
    encoding = f.headers.getparam('charset')
    if not encoding:
        encoding = 'utf-8'
    s = f.read()
    f.close()
    try:
        s = s.decode(encoding)
    except UnicodeDecodeError:
        pass
    return s

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        try:
            if tag == 'a':
                for attr in attrs:
                    if attr[0] == 'href':
                        self.urls.append(attr[1])
        except UnicodeDecodeError:
            print "OVER HEREAAAa"
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        pass


parser = MyHTMLParser()

def getLinks(website):
    url = website[1]
    s = loadPage(url)
    if not s:
        return []
    parser.urls = []
    parser.feed(s)
    return parser.urls
