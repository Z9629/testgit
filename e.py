import sys
import time

f=None
try:
    f=open('poem.txt')
    while True:
        line=f.readline()
        if len(line)==0:
            break
            
        print(line,end='')
       
        sys.stdout.flush()
        print('press ctrl+c now')
        time.sleep(2)
except IOError:
    print('could not')
except KeyboardInterrupt:
    print('!!you can')
finally:
    if f:
        f.close()
    print('clean up')