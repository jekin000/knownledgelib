import urllib2 
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Spider:
    def __init__(self,logger):
        self.logger = logger
        self.fileno = 0
        self.maxfileno = 200

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
        if self.fileno >= self.maxfileno:
            self.logger.info('Spider exceed maxfileno, stop get html')
            return None    
        req = urllib2.Request(url)
        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            self.logger.error('Can not get {}'.format(url),exc_info=True)
            return None
        except:
            traceback.print_exc()
            return None

        html = resp.read()
        filename = self.write_file(html)
        return (layer,filename)


