import urllib.request

# t = urllib.request.urlopen('https://www.w3.org/')
# t.geturl()

def news(url, topics):
    resp = urllib.request.urlopen(url)
    content = resp.read()
    text = content.decode().lower()
    for topic in topics:
        count = text.count(topic)
        print("{} has been found {} times".format(topic, count))


#news('https://bbc.co.uk', ['news', 'business', 'travel'])

from html.parser import HTMLParser
class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        'print value of href attribute if any'
        if tag == 'a':
            # search for href attribute and print its value
            for attr in attrs:
                if attr[0] == 'href':
                    print(attr[1])


def linkParser():
    afile = open('links.html')
    contents = afile.read()
    afile.close()

    lp = LinkParser()
    lp.feed(contents)


class MyHTMLParser(HTMLParser):

    def __init__(self, url):
        super().__init__()
        if 'http' in url or 'https' in url:
            resp = urllib.request.urlopen(url)
            content = resp.read()
            html = content.decode().lower() 
            self.feed(html)
        else:
            afile = open('links.html')
            file_contents = afile.read()
            afile.close()
            self.feed(file_contents)

    def handle_starttag(self, tag, attrs):
        
        if tag == 'html':
            print('{} start'.format(tag))
        elif tag == 'head' or tag == 'body':
            print ('\t{} start'.format(tag))
        elif tag == 'title' or tag == 'h1' or tag == 'h2' or tag == 'a' or tag == 'ol':
            print('\t\t{} start'.format(tag))
        elif tag == 'li':
            print('\t\t\t{} start'.format(tag))
        
    def handle_endtag(self, tag):
        if tag == 'html':
            print('{} end'.format(tag))
        elif tag == 'head' or tag == 'body':
            print ('\t{} end'.format(tag))
        elif tag == 'title' or tag == 'h1' or tag == 'h2' or tag == 'a' or tag == 'ol':
            print('\t\t{} end'.format(tag))
        elif tag == 'li':
            print('\t\t\t{} end'.format(tag))
    

# def myParser():
#     afile = open('index.html')
#     contents = afile.read()
#     afile.close()

#     mp = MyHTMLParser()
#     mp.feed(contents)

mp = MyHTMLParser('https://w3.org')