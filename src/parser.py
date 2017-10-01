import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import DataStore

title = []
links = []
infos = []
tagstack = []

def judgelink(url):
    if url.find('http')>=0 and url.find('baike.com')>=0:
        if url.find('jpg')>=0 or url.find('tupian')>=0 or url.find('help')>=0 or url.find('passport')>=0 or url.find('zhaopin')>=0:
            return False
        return True
    else:
        return False 

def eat_attrs(atts,outputlist,attname,judge=None):
    for a in atts:
        if a[0].lower() == attname:
            if judge:
                if judge(a[1]):
                    outputlist.append(a[1])
            else:
                outputlist.append(a[1])
                

class ParseHTMLStructure(HTMLParser.HTMLParser):
    def handle_starttag(self,tag,attrs):
        if len(tagstack) and tag.lower()=='a':
            eat_attrs(attrs,infos,'title')
            eat_attrs(attrs,links,'href')
            tagstack.append(tag)
        elif tag.lower()=='p' and len(tagstack)==0: 
            for att in attrs: 
                if att[0].lower()=='id' and att[1]=='openCatp':
                    tagstack.append(tag)
        elif tag.lower() == 'a':
            eat_attrs(attrs,links,'href',judgelink)
        elif tag.lower() == 'title':
            tagstack.append(tag)
           
    def handle_endtag(self,tag):
        if len(tagstack) > 0:
            tagstack.pop()
    def handle_data(self,data):
        if len(tagstack)>0 and tagstack[-1:][0]=='title':
            title.append(data.split('_')[0])

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
        response = []
        for lk in links:
            if not DataStore.isDuplicate(self.logger,lk): 
                response.append(lk)

        if len(title)>0 and len(infos)>0:
            DataStore.save(self.logger,title[0],infos)

        del infos[:]
        del links[:]
        del title[:]
        if len(response) == 0:
            self.logger.info('no urls found')
            return None

        layer = str(no+1)
        msg = ''
        for url in response:
            msg = msg+layer+','+url+'|'
        msg = msg[:-1]
        return msg
