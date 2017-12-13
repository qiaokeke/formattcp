import sys,struct
import socketserver, time
from socketserver import StreamRequestHandler as SRH
from time import ctime

MODUS_CMD_LIST =[]


class myServerHandler(SRH):
    def handle(self):
        print ('got connection from',self.client_address)
