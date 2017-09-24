import logging
import logging.handlers
import asyncore
import socket
import parser
import json

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        logger = logging.getLogger('parser')
        data = self.recv(1024)
        if data:
            msg = json.loads(data)
            p = parser.Parser(logger) 
            res = p.parse_html(msg['layer'],msg['filename'])
            l = []
            if res:
                msg = {}
                layer = res[0]
                urls  = res[1]
                for u in urls:
                    msg['layer'] = layer
                    msg['url']   = u
                    l.append(msg)
                self.send(json.dumps(l))
            else:
                logger.info('No expected url')
            

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

