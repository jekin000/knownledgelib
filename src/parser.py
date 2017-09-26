import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ParseHTMLStucture
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
		
