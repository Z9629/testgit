'''
a=open('a.txt','w')
a.write('nihaoma')
a.close()
a=open('a.txt','r')
print(a.read(20))
a.seek(0)       #游标置零，重新读取
print(a.read(200))
'''
'''
d=a=[11,33,44,22,55]
b=a.sort()
print(b)
print(a)

c=d.reverse()
print(c)
print(d)
'''
'''
a=(1,2,3)
print(id(a))
print(a)
b=list(a)
print(id(b))
print(b)
c=[4,5,6]
print(id(c))
print(c)
d=tuple(c)
print(id(d))
print(d)
'''
'''
a=[1,13,14,15,16]
print({m for m in a if  m%2==1})
'''

'''print ('6' if True else 3)'''

'''for x in 'i am li lei'.split(' '):
    print (x)'''
'''print(True and False or True and False)'''

#encoding=utf-8
#coding=utf-8
'''def a():
    #print('abc')
    '哈哈哈'
    return 'abc'
print(a())
print(a.__doc__)
'''

'''
def num(a,b):
    return a+b
print(num(1,2))
'''
a='abc'

for i,ch in enumerate(a):
    print(ch,'(%d)' % i)
















