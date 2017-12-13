import dataformat.cmdlis as list

if __name__ == '__main__':
    print('[',end='\n')
    for cmd in list.CMD_LIST:
        print('[',end='')
        for c in cmd:
            print("%d"%c,end=',')
        print('\b],')
    print('\b\b]')