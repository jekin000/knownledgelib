
class Parser:
    def __init__(self,logger):
        self.logger = logger
    def parse_html(self,no,filename):
        print 'parse '+filename
        if filename == '0.html':
            return (no+1,['http://www.baidu.com'
                            ,'http://www.sina.com'
                            ,'http://www.youku.com'
                        ])

		
