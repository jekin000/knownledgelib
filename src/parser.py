import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


links = []
infos = []
tagstack = []

def eat_attrs(atts,outputlist,attname):
    for a in atts:
        if a[0].lower() == attname:
            outputlist.append(a[0])

class ParseHTMLStructure(HTMLParser.HTMLParser):
    def handle_starttag(self,tag,attrs):
        if len(tagstack) and tag.lower()=='a':
            eat_attrs(attrs,infos,'title')
            eat_attrs(attrs,links,'href')
            tagstack.append(tag)
        elif tag.lower()=='p' and len(tagstack)==0: 
            for att in attrs: 
                print att
                if att[0].lower()=='id' and att[1]=='openCatp':
                    print 'get it==================>'
                    tagstack.append(tag)
           
    def handle_endtag(self,tag):
        if len(tagstack) > 0:
            tagstack.pop()
    def handle_data(self,data): pass

class Parser:
    def __init__(self,logger):
        self.logger = logger
    def read_file(self,filename):
        html = ''
        try:
            with open(filename,'r') as f:
                html = f.read() 
        except:
            return  None

        return html
            
    def parse_html(self,no,filename):
        html = self.read_file(filename)
        if html:
            return self.do_parse(no,html)
        else:
            return None

    def do_parse(self,no,html):
        ParseHTMLStructure().feed(html) 
        print 'parse end'
        for i in infos:
            print i
	    
