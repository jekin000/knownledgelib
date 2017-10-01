import logging
import logging.handlers
import asyncore
import socket
import parser
import json
import datetime
import exceptions
import time


SEND_INTERVAL = 1

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        logger = logging.getLogger('parser')
        data = self.recv(1024)
        if data:
            try:
                msg = json.loads(data)
            except exceptions.ValueError as e:
                logger.error('Unexpected file {}'.format(data),exc_info=True)
            else:
                p = parser.Parser(logger) 
                t1 = datetime.datetime.now()
                res = p.parse_html(msg['layer'],msg['filename'])
                t2 = datetime.datetime.now()
                interval = (t2-t1).microseconds*1.0/1000
                logger.info('parse {} finish. cost=[{}]ms'.format(msg['filename']
                            ,str(interval))
                        )
                if res:
                    self.send(res)
                else:
                    logger.info('Can not get url from {}'.format(msg['filename']))
            

class ParserServer(asyncore.dispatcher):
    def __init__(self,host,port):
        asyncore.dispatcher.__init__(self)

        self.log_file = 'parser.log'
        handler = logging.handlers.RotatingFileHandler(self.log_file, maxBytes = 1024*1024, backupCount = 5)
        fmt = '[%(asctime)s][%(levelname)s]%(filename)s:%(lineno)s - %(message)s'  
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        self.logger = logging.getLogger('parser')
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host,port))
        self.listen(5)
    def handle_accept(self):
        conn,addr = self.accept()
        self.logger.info('Incoming connection from %s' % repr(addr))
        self.handler = EchoHandler(conn)

server = ParserServer('localhost',9999)
try:
    asyncore.loop()
except:
    print 'Server terminal.'

