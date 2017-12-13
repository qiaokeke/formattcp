# coding:utf-8
import sys, struct

MODBUS_CMD_LIST = [
    '\x12\x03\x00\x38\x00\x34\xc7\x73', \
    '\x12\x03\x07\xcf\x00\x78\x76\x00', \
 \
    '\x13\x03\x00\x38\x00\x34\xc6\xa2', \
    '\x13\x03\x07\xcf\x00\x78\x77\xD1', \
 \
    '\x14\x03\x00\x38\x00\x34\xc7\x15', \
    '\x14\x03\x07\xcf\x00\x78\x76\x66', \
 \
    '\x15\x03\x00\x38\x00\x34\xc6\xc4', \
    '\x15\x03\x07\xcf\x00\x78\x77\xB7', \
 \
    '\x17\x03\x00\x38\x00\x34\xc7\x26', \
    '\x17\x03\x07\xcf\x00\x78\x76\x55', \
 \
    '\x18\x03\x00\x38\x00\x34\xc7\xd9', \
    '\x18\x03\x07\xcf\x00\x78\x76\xAA', \
 \
    '\x19\x03\x00\x38\x00\x34\xc6\x08', \
    '\x19\x03\x07\xcf\x00\x78\x77\x7B', \
 \
    '\x1A\x03\x00\x38\x00\x34\xc6\x3b', \
    '\x1A\x03\x07\xcf\x00\x78\x77\x48', \
 \
    '\x1B\x03\x00\x38\x00\x34\xc7\xea', \
    '\x1B\x03\x07\xcf\x00\x78\x76\x99'
]

CMD_LIST = [0, 2, 4, 6, 8, 10, 12, 14, 16]
import socketserver, time
from socketserver import StreamRequestHandler as SRH
from time import ctime

host = ''
port = 6100
addr = (host, port)
data_no_per_dianbiao = [52 * 2, 120 * 2]


class Servers(SRH):
    def handle(self):
        print( 'got connection from ', self.client_address)
        #self.wfile.write('connection %s:%s at %s succeed!' % (host, port, ctime()))
        for i in CMD_LIST:
            self.request.send(MODBUS_CMD_LIST[i])
            list_per_count = []
            print
            'send', i
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

                if ('\x03\x68' in data):
                    print("RECV from ", self.client_address[0])

                    'this is %s recv' % (i), data.encode('hex'), len(data)
                    '''新添加的(2017-09-02)插入数据库'''
                    index = data.index('\x03\x68')

                    dian_hex = data[index + 2:index + 2 + data_no_per_dianbiao[0]]

                    for j in range(len(dian_hex)):
                        if (j % 4 == 0):
                            dian_hex_temp = dian_hex[j + 2] + dian_hex[j + 3] + dian_hex[j] + dian_hex[j + 1]
                            # print 'dian_hex'
                            # print len(dian_hex_temp),'dian_hex'
                            dian_decimal = struct.unpack('!f', dian_hex_temp)[0]
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

                        if ('\x03\xf0' in data):
                            print
                            "RECV from ", self.client_address[0]
                            print
                            'this is %s recv' % (i + 1), data.encode('hex'), len(data)
                            '''新添加的(2017-09-02)插入数据库'''
                            index_2 = data.index('\x03\xf0')
                            dianbiao_no_hex = data[index_2 - 1] + '\x00'
                            dianbiao_no_decimal = struct.unpack('h', dianbiao_no_hex)[0]
                            dian_hex_2 = data[index_2 + 2:index_2 + 2 + data_no_per_dianbiao[1]]
                            for j in range(len(dian_hex_2)):
                                if (j % 4 == 0):
                                    dian_hex_temp = dian_hex_2[j + 2] + dian_hex_2[j + 3] + dian_hex_2[j] + dian_hex_2[
                                        j + 1]
                                    # print 'dian_hex'
                                    # print len(dian_hex_temp),'dian_hex'
                                    dian_decimal_2 = struct.unpack('!f', dian_hex_temp)[0]
                                    # print dian_decimal,'dian_decimal DY'

                                    list_per_count.append(float(dian_decimal_2))
                            dianbiao_t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                            # print 'shijian',dianbiao_t
                            list_per_count.append(dianbiao_t)
                            list_per_count.append(int(dianbiao_no_decimal))
                            print
                            "+++++++"
                            # print len(list_per_count),list_per_count
                            saveData(list_per_count)
                            break
                    break

def saveData(list_):
    sq_command = "insert into tbl_power_info_v2(P_A_DIANYA,P_B_DIANYA,P_C_DIANYA,P_UAB_XIANDIANYA,P_UBC_XIANDIANYA,\
                                        P_UCA_XIANDIANYA,P_A_DIANLIU,P_B_DIANLIU,P_C_DIANLIU,P_A_YGGL,\
					P_B_YGGL,P_C_YGGL,P_HXYGGL,P_A_WGGL,P_B_WGGL,\
					P_C_WGGL,P_HXWGGL,P_A_SZGL,P_B_SZGL,P_C_SZGL,\
					P_HXSZGL,P_A_GLYS,P_B_GLYS,P_C_GLYS,P_HXGLYS,\
					P_DWPL,\
					P_BY_KwhZ,P_BY_KwhJ,P_BY_KwhF,P_BY_KwhP,P_BY_KwhG,\
					P_BY_HKwhZ,P_BY_HKwhJ,P_BY_HKwhF,P_BY_HKwhP,P_BY_HKwhG,\
					P_BY_KvarhZ,P_BY_KvarhJ,P_BY_KvarhF,P_BY_KvarhP,P_BY_KvarhG,\
					P_BY_HKvarhZ,P_BY_HKvarhJ,P_BY_HKvarhF,P_BY_HKvarhP,P_BY_HKvarhG,\
					P_SY_KwhZ,P_SY_KwhJ,P_SY_KwhF,P_SY_KwhP,P_SY_KwhG,\
					P_SY_HKwhZ,P_SY_HKwhJ,P_SY_HKwhF,P_SY_HKwhP,P_SY_HKwhG,\
					P_SY_KvarhZ,P_SY_KvarhJ,P_SY_KvarhF,P_SY_KvarhP,P_SY_KvarhG,\
					P_SY_HKvarhZ,P_SY_HKvarhJ,P_SY_HKvarhF,P_SY_HKvarhP,P_SY_HKvarhG,\
					P_SSY_KwhZ,P_SSY_KwhJ,P_SSY_KwhF,P_SSY_KwhP,P_SSY_KwhG,\
					P_SSY_HKwhZ,P_SSY_HKwhJ,P_SSY_HKwhF,P_SSY_HKwhP,P_SSY_HKwhG,\
					P_SSY_KvarhZ,P_SSY_KvarhJ,P_SSY_KvarhF,P_SSY_KvarhP,P_SSY_KvarhG,\
					P_SSY_HKvarhZ,P_SSY_HKvarhJ,P_SSY_HKvarhF,P_SSY_HKvarhP,P_SSY_HKvarhG,\
                                        P_TIME,P_CODE)values(%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,\
                                                            %s, %s,%s, %s,%s,%s, %s,%s, %s,%s,\
                                                            %s, %s,%s, %s,%s,%s, %s,%s, %s,%s,\
                                                            %s, %s,%s, %s,%s,%s, %s,%s, %s,%s,\
                                                            %s, %s,%s, %s,%s,%s, %s,%s, %s,%s,\
                                                            %s, %s,%s, %s,%s,%s, %s,%s, %s,%s,\
                                                            %s, %s,%s, %s,%s,%s, %s,%s, %s,%s,\
                                                            %s, %s,%s, %s,%s,%s, %s,%s, %s,%s,\
                                                            %s, %s,%s, %s,%s,%s, %s,%s)"
    print
    'insert success!!'


print
'server is running....'
server = socketserver.ThreadingTCPServer(addr, Servers)
server.serve_forever(10)
