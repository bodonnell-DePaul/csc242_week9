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


afile = open('links.html')
contents = afile.read()
afile.close()

lp = LinkParser()
lp.feed(contents)