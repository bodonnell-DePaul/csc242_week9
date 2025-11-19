import urllib.request
from html.parser import HTMLParser

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

class MLBGameList(HTMLParser):
    def __init__(self,url):
        super().__init__()
        self.url = url[8:]
        self.url = self.url.split('/')[0]
        self.links = []
        self.isLink = False
        self.lastLink = ''
        if 'http' in url or 'https' in url:
            resp = urllib.request.urlopen(url)
            content = resp.read()
            html = content.decode()
            self.feed(html)
        pass

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    #a trigger for our handle_data function
                    self.isLink = True
                    #gathering the address and storing it in a variable
                    self.lastLink = attr[1]



    def handle_data(self, data):
        super().handle_data(data)
        if self.isLink is True:
            #detecting if we want to add the url to our list
            if data.lower() == 'boxscore':
                self.links.append('https://'+self.url+self.lastLink)



    def handle_endtag(self, tag):
        return super().handle_endtag(tag)
    

class DataGather(HTMLParser):
    def __init__(self, url):
        super().__init__()
        self.boxScore = []
        self.tableHeader = []
        self.teamOneTable = []
        self.teamTwoTable = []
        self.gatherData = False
        self.gatherHeader = False
        self.gatherTeamOne = False
        self.gatherTeamTwo = False
        if 'http' in url or 'https' in url:
            resp = urllib.request.urlopen(url)
            content = resp.read()
            html = content.decode()
            self.feed(html)
        pass

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'linescore_wrap':
                    self.gatherData = True
        if tag == 'thead':
            self.gatherHeader = True
        if tag == 'tbody':
            self.gatherTeamOne = True
            #self.gatherTeamTwo = True



    def handle_data(self, data):
        super().handle_data(data)
        if self.gatherData is True:
            if self.gatherHeader is True and data.find('\n') == -1:
                self.tableHeader.append(data)
            elif self.gatherTeamOne is True and data.find('\n') == -1:
                self.teamOneTable.append(data)
            elif self.gatherTeamTwo is True and data.find('\n') == -1:
                self.teamTwoTable.append(data)




    def handle_endtag(self, tag):
        super().handle_endtag(tag)
        if tag == 'thead':
            if self.gatherHeader is True:
                self.gatherHeader = False
                print(self.tableHeader)
        if tag == 'tr':
            if self.gatherTeamOne is True:
                self.gatherTeamOne = False
                self.gatherTeamTwo = True
                while len(self.teamOneTable) > len(self.tableHeader):
                    self.teamOneTable.pop(0)
                
                self.teamOneTable[0] = '\xa0'
                self.teamOneTable[1] = '\xa0'

                print(self.teamOneTable)

            elif self.gatherTeamTwo is True:
                self.gatherTeamTwo = False
                while len(self.teamTwoTable) > len(self.tableHeader):
                    self.teamTwoTable.pop(0)
                
                self.teamTwoTable[0] = '\xa0'
                self.teamTwoTable[1] = '\xa0'

                print(self.teamTwoTable)

            if self.gatherTeamOne is False and self.gatherTeamTwo is False:
                self.boxScore.append(self.tableHeader)
                self.boxScore.append(self.teamOneTable)
                self.boxScore.append(self.teamTwoTable)

                print(self.boxScore)



baseballSchedule = "https://www.baseball-reference.com/leagues/majors/2025-schedule.shtml"
baseballLinks = MLBGameList(baseballSchedule)
gameData = DataGather(baseballLinks.links[0])
