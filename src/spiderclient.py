import asyncore
import socket
import spider
import json
import logging
import logging.handlers
import time
import traceback
import exceptions
import datetime

SEND_INTERVAL = 0.1
class SpiderClient(asyncore.dispatcher):
    def __init__(self,host,port):
        asyncore.dispatcher.__init__(self)
        self.interval = SEND_INTERVAL
        self.recvbuffsize = 10240

        self.log_file = 'spider.log'
        handler = logging.handlers.RotatingFileHandler(self.log_file, maxBytes = 1024*1024, backupCount = 5)
        fmt = '[%(asctime)s][%(levelname)s]%(filename)s:%(lineno)s - %(message)s'  
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        self.logger = logging.getLogger('spider')
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

        self.spider = spider.Spider(self.logger)
        self.messages=[{'layer':0,'url':'http://www.baike.com/wiki/%E6%A2%85%E8%A5%BFk'}]
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connect((host,port))
    def handle_connect(self):
        pass
    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(self.recvbuffsize)
        if data:
            try:
                urls = json.loads(data)
            except exceptions.ValueError as e:
                self.logger.error('json_decode parser info fail. info='+data) 
                return
            else:
                self.messages.extend(urls)

    def writable(self):
        return (len(self.messages) > 0)

    def handle_write(self):
            t1 = datetime.datetime.now()
            tmp = self.messages.pop(0)
            res = self.spider.get_html(tmp['layer'],tmp['url'])
            data = {} 
            data['layer'] = res[0]
            data['filename'] = res[1]
            self.send(json.dumps(data))
            t2 = datetime.datetime.now()
            interval = (t2-t1).microseconds*1.0/1000
            self.logger.info('Download {} to {}. cost=[{}]ms'.format(tmp['url']
                            ,data['filename']
                            ,str(interval))
                        )
            #time.sleep(self.interval)


client = SpiderClient('localhost',9999)
try:
    asyncore.loop(timeout=5)
except:
    print 'Spider Close'



