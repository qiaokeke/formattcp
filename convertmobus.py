import modbus



if __name__ == '__main__':
    print('[',end='')
    for cmd in modbus.MODBUS_CMD_LIST:
        print('[',end='')
        for c in cmd:
            print("%d"%c,end=',')
        print('\b],')
    print('\b\b]')