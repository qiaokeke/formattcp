# coding:utf-8
import sys, struct

MODBUS_CMD_LIST = [
    b'\x12\x03\x00\x38\x00\x34\xc7\x73', \
    b'\x12\x03\x07\xcf\x00\x78\x76\x00', \
    b'\x12\x03\x01\x0f\x00\x08\x77\x50', \
 \
    b'\x13\x03\x00\x38\x00\x34\xc6\xa2', \
    b'\x13\x03\x07\xcf\x00\x78\x77\xD1', \
    b'\x13\x03\x01\x0f\x00\x08\x76\x81', \
 \
    b'\x14\x03\x00\x38\x00\x34\xc7\x15', \
    b'\x14\x03\x07\xcf\x00\x78\x76\x66', \
    b'\x14\x03\x01\x0f\x00\x08\x77\x36', \
 \
    b'\x15\x03\x00\x38\x00\x34\xc6\xc4', \
    b'\x15\x03\x07\xcf\x00\x78\x77\xB7', \
    b'\x15\x03\x01\x0f\x00\x08\x76\xe7', \
 \
    b'\x17\x03\x00\x38\x00\x34\xc7\x26', \
    b'\x17\x03\x07\xcf\x00\x78\x76\x55', \
    b'\x17\x03\x01\x0f\x00\x08\x77\x05', \
 \
    b'\x18\x03\x00\x38\x00\x34\xc7\xd9', \
    b'\x18\x03\x07\xcf\x00\x78\x76\xAA', \
    b'\x18\x03\x01\x0f\x00\x08\x77\xfa', \
 \
    b'\x19\x03\x00\x38\x00\x34\xc6\x08', \
    b'\x19\x03\x07\xcf\x00\x78\x77\x7B', \
    b'\x19\x03\x01\x0f\x00\x08\x76\x2b', \
 \
    b'\x1A\x03\x00\x38\x00\x34\xc6\x3b', \
    b'\x1A\x03\x07\xcf\x00\x78\x77\x48', \
    b'\x1A\x03\x01\x0f\x00\x08\x76\x18', \
 \
    b'\x1B\x03\x00\x38\x00\x34\xc7\xea', \
    b'\x1B\x03\x07\xcf\x00\x78\x76\x99',\
    b'\x13\x03\x01\x0f\x00\x08\x77\xc9', \
]

CMD_LIST = [0, 3, 6, 9, 12, 15, 18, 21,24]
import socketserver, time
from socketserver import StreamRequestHandler as SRH
from time import ctime

host = ''
port = 6002
addr = (host, port)
data_no_per_dianbiao = [52 * 2, 120 * 2,8*2]

class myServerHandler(SRH):
    def handle(self):
        print( 'got connection from ', self.client_address)
        #self.wfile.write('connection %s:%s at %s succeed!' % (host, port, ctime()))
        for i in CMD_LIST:
            self.request.send(MODBUS_CMD_LIST[i])
            list_per_count = []
            print ('send', i)
            time.sleep(0.2)
            while True:
                data = self.request.recv(1024)
                time.sleep(0.1)
                while len(data) < data_no_per_dianbiao[0]:

                    tmp = self.request.recv(1024)

                    if not tmp:
                        break
                    data = data + tmp
                if not data:
                    break

                if (b'\x03\x68' in data):
                    print("RECV from ", self.client_address)
                    print(data.hex())
                   # 'this is %s recv' % (i), data.encode('hex'), len(data)
                    '''新添加的(2017-09-02)插入数据库'''
                    index = data.index(b'\x03\x68')
                    print(index)
                    dian_hex = data[index + 4:index + 4 + data_no_per_dianbiao[0]]
                    print(dian_hex.hex())
                    for j in range(len(dian_hex)):
                        if (j % 4 == 0):
                            #dian_hex_temp = dian_hex[j + 2] + dian_hex[j + 3] + dian_hex[j] + dian_hex[j + 1]
                            # print 'dian_hex'
                            # print len(dian_hex_temp),'dian_hex'
                            #print(dian_hex[j:j+4].hex())
                            dian_decimal = struct.unpack('!f', dian_hex[j:j+4])[0]
                            #print(dian_decimal)
                            # print dian_decimal,'dian_decimal DY'
                            list_per_count.append(float(dian_decimal))

                    # saveData(list_per_count)
                    '''   新添加的(2017-09-02)插入数据库代码到这里'''
                    self.request.send(MODBUS_CMD_LIST[i + 1])
                    while True:
                        data = self.request.recv(1024)
                        time.sleep(0.1)
                        while len(data) < data_no_per_dianbiao[1]:

                            tmp = self.request.recv(1024)

                            if not tmp:
                                break
                            data = data + tmp
                        if not data:
                            break

                        if (b'\x03\xf0' in data):
                            print("recv from:",self.client_address)
                            print(data.hex())

                            '''新添加的(2017-09-02)插入数据库'''
                            index_2 = data.index(b'\x03\xf0')
                            dianbiao_no_hex = data[index_2-1]
                            #dianbiao_no_decimal = struct.unpack('h', dianbiao_no_hex)[0]
                            dian_hex_2 = data[index_2 + 4:index_2 + 4 + data_no_per_dianbiao[1]]
                            print(dian_hex_2.hex())
                            for j in range(len(dian_hex_2)):
                                if (j % 4 == 0):

                                    # print 'dian_hex'
                                    # print len(dian_hex_temp),'dian_hex'
                                    dian_decimal_2 = struct.unpack('!f', dian_hex_2[j:j+4])[0]
                                    # print dian_decimal,'dian_decimal DY'
                                    #print(dian_decimal_2)
                                    list_per_count.append(float(dian_decimal_2))
                            dianbiao_t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                            # print 'shijian',dianbiao_t
                            list_per_count.append(dianbiao_t)
                            list_per_count.append(int(dianbiao_no_hex))

                            # print len(list_per_count),list_per_count
                            self.request.send(MODBUS_CMD_LIST[i + 2])
                            while True:
                                data = self.request.recv(1024)
                                time.sleep(0.1)
                                while len(data) < data_no_per_dianbiao[2]:
                                    tmp = self.request.recv(1024)
                                    if not tmp:
                                        break
                                    data = data + tmp
                                if not data:
                                    break
                                if (b'\x03\x10' in data):
                                    print("recv from:", self.client_address)
                                    print(data.hex())
                                    index_3 = data.index(b'\x03\x10')
                                    dian_hex_3 = data[index_3 + 4:index_3 + 4 + data_no_per_dianbiao[2]]
                                    print(dian_hex_3)
                                    for j in range(len(dian_hex_3)):
                                        if (j % 4 == 0):
                                            # print 'dian_hex'
                                            # print len(dian_hex_temp),'dian_hex'
                                            dian_decimal_3 = struct.unpack('!l', dian_hex_3[j:j + 4])[0]
                                            # print dian_decimal,'dian_decimal DY'
                                            #print(dian_decimal_3)
                                            list_per_count.append(float(dian_decimal_3)/1000.0)
                                    print(list_per_count)
                                    import dabase
                                    dabase.saveData(list_per_count)
                                    break
                            break
                    break

server = socketserver.ThreadingTCPServer(addr, myServerHandler)
server.serve_forever(10)
