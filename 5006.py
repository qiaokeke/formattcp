# coding:utf-8
import sys, struct

MODBUS_CMD_LIST = [

    b'\x01\x03\x00\x38\x00\x34\xc5\xd0',
    b'\x01\x03\x07\xcf\x00\x78\x74\xa3',
    b'\x01\x03\x01\x0f\x00\x08\x75\xf3',

    b'\x02\x03\x00\x38\x00\x34\xc5\xe3',
    b'\x02\x03\x07\xcf\x00\x78\x74\x90',
    b'\x02\x03\x01\x0f\x00\x08\x75\xc0',

    b'\x03\x03\x00\x38\x00\x34\xc4\x32',
    b'\x03\x03\x07\xcf\x00\x78\x75\x41',
    b'\x03\x03\x01\x0f\x00\x08\x74\x11',

    b'\x04\x03\x00\x38\x00\x34\xc5\x85',
    b'\x04\x03\x07\xcf\x00\x78\x74\xf6',
    b'\x04\x03\x01\x0f\x00\x08\x75\xa6',

    b'\x05\x03\x00\x38\x00\x34\xc4\x54',
    b'\x05\x03\x07\xcf\x00\x78\x75\x27',
    b'\x05\x03\x01\x0f\x00\x08\x74\x77',

    b'\x06\x03\x00\x38\x00\x34\xc4\x67',
    b'\x06\x03\x07\xcf\x00\x78\x75\x14',
    b'\x06\x03\x01\x0f\x00\x08\x74\x44',

    b'\x07\x03\x00\x38\x00\x34\xc5\xb6',
    b'\x07\x03\x07\xcf\x00\x78\x74\xc5',
    b'\x07\x03\x01\x0f\x00\x08\x75\x95',

    b'\x08\x03\x00\x38\x00\x34\xc5\x49',
    b'\x08\x03\x07\xcf\x00\x78\x74\x3a',
    b'\x08\x03\x01\x0f\x00\x08\x75\x6a',

    b'\x09\x03\x00\x38\x00\x34\xc4\x98',
    b'\x09\x03\x07\xcf\x00\x78\x75\xeb',
    b'\x09\x03\x01\x0f\x00\x08\x74\xbb'

]

CMD_LIST = [0, 3, 6, 9, 12, 15,18,21,24]
import socketserver, time
from socketserver import StreamRequestHandler as SRH
from time import ctime

host = ''
port = 6005
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
