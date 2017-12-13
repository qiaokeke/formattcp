# coding:utf-8
import sys, struct

MODBUS_CMD_LIST = [

    b'\x22\x03\x00\x38\x00\x34\xc2\x83',
    b'\x22\x03\x07\xcf\x00\x78\x73\xf0',
    b'\x22\x03\x01\x0f\x00\x08\x72\xa0',

    b'\x23\x03\x00\x38\x00\x34\xc3\x52',
    b'\x23\x03\x07\xcf\x00\x78\x72\x21',
    b'\x23\x03\x01\x0f\x00\x08\x73\x71',

    b'\x24\x03\x00\x38\x00\x34\xc2\xe5',
    b'\x24\x03\x07\xcf\x00\x78\x73\x96',
    b'\x24\x03\x01\x0f\x00\x08\x72\xc6',

    b'\x25\x03\x00\x38\x00\x34\xc3\x34',
    b'\x25\x03\x07\xcf\x00\x78\x72\x47',
    b'\x25\x03\x01\x0f\x00\x08\x73\x17',

    b'\x26\x03\x00\x38\x00\x34\xc3\x07',
    b'\x26\x03\x07\xcf\x00\x78\x72\x74',
    b'\x26\x03\x01\x0f\x00\x08\x73\x24',

    b'\x27\x03\x00\x38\x00\x34\xc2\xd6',
    b'\x27\x03\x07\xcf\x00\x78\x73\xa5',
    b'\x27\x03\x01\x0f\x00\x08\x72\xf5',

    b'\x28\x03\x00\x38\x00\x34\xc2\x29',
    b'\x28\x03\x07\xcf\x00\x78\x73\x5a',
    b'\x28\x03\x01\x0f\x00\x08\x72\x0a',

    b'\x29\x03\x00\x38\x00\x34\xc3\xf8',
    b'\x29\x03\x07\xcf\x00\x78\x72\x8b',
    b'\x29\x03\x01\x0f\x00\x08\x73\xdb',

    b'\x2A\x03\x00\x38\x00\x34\xc3\xcb',
    b'\x2A\x03\x07\xcf\x00\x78\x72\xb8',
    b'\x2A\x03\x01\x0f\x00\x08\x73\xe8',

    b'\x2B\x03\x00\x38\x00\x34\xc2\x1a',
    b'\x2B\x03\x07\xcf\x00\x78\x73\x69',
    b'\x2B\x03\x01\x0f\x00\x08\x72\x39',

    b'\x2C\x03\x00\x38\x00\x34\xc3\xad',
    b'\x2C\x03\x07\xcf\x00\x78\x72\xde',
    b'\x2C\x03\x01\x0f\x00\x08\x73\x8e',

    b'\x2D\x03\x00\x38\x00\x34\xc2\x7c',
    b'\x2D\x03\x07\xcf\x00\x78\x73\x0f',
    b'\x2D\x03\x01\x0f\x00\x08\x72\x5f',

    b'\x2E\x03\x00\x38\x00\x34\xc2\x4f',
    b'\x2E\x03\x07\xcf\x00\x78\x73\x3c',
    b'\x2E\x03\x01\x0f\x00\x08\x72\x6c',

    b'\x2F\x03\x00\x38\x00\x34\xc3\x9e',
    b'\x2F\x03\x07\xcf\x00\x78\x72\xed',
    b'\x2F\x03\x01\x0f\x00\x08\x73\xbd',

    b'\x30\x03\x00\x38\x00\x34\xc1\xf1',
    b'\x30\x03\x07\xcf\x00\x78\x70\x82',
    b'\x30\x03\x01\x0f\x00\x08\x71\xd2',

    b'\x31\x03\x00\x38\x00\x34\xc0\x20',
    b'\x31\x03\x07\xcf\x00\x78\x71\x53',
    b'\x31\x03\x01\x0f\x00\x08\x70\x03'
]

CMD_LIST = [0, 3, 6, 9, 12, 15,18,21,24,27,30,33]
import socketserver, time
from socketserver import StreamRequestHandler as SRH
from time import ctime

host = ''
port = 6003
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
print("run:"+port)
server.serve_forever(10)
