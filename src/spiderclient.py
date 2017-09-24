import asyncore
import socket
import spider
import json
import logging
import logging.handlers

class SpiderClient(asyncore.dispatcher):
    def __init__(self,host,port):
        asyncore.dispatcher.__init__(self)

        self.log_file = 'spider.log'
        handler = logging.handlers.RotatingFileHandler(self.log_file, maxBytes = 1024*1024, backupCount = 5)
        fmt = '[%(asctime)s][%(levelname)s]%(filename)s:%(lineno)s - %(message)s'  
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        self.logger = logging.getLogger('spider')
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

        self.spider = spider.Spider(self.logger)

        self.messages=['{"url": "http://www.baike.com/wiki/%E6%A2%85%E8%A5%BFk", "layer": 3}']
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connect((host,port))
    def handle_connect(self):
        pass
    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(1024)
        print data

    def writable(self):
        return (len(self.messages) > 0)

    def handle_write(self):
        msg = json.loads(self.messages.pop(0))
        res = self.spider.get_html(msg['layer'],msg['url'])
        data = {} 
        data['layer'] = res[0]
        data['filename'] = res[1]
        self.send(json.dumps(data))


client = SpiderClient('localhost',9999)
try:
    asyncore.loop(timeout=5)
except:
    print 'Spider Close'



