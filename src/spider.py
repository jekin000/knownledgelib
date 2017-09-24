import urllib2 
import traceback

class Spider:
    def __init__(self,logger):
        self.logger = logger
        self.fileno = 0

    def write_file(self,data):
        filename = str(self.fileno)+'.html' 
        self.fileno += 1
        try:
            with open(filename,'w') as f:
                f.write(data)
        except:
            traceback.print_exc()
            self.fileno -= 1
            return None
        return filename
        
	
    def get_html(self,layer,url):
        req = urllib2.Request(url)
        resp = urllib2.urlopen(req)
        html = resp.read()
        filename = self.write_file(html)
        return (layer,filename)


