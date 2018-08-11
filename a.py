# def reverse(text):
    # return text[::-1]
# def is_p(text):
    # return text==reverse(text)
    
# s=input('enter text:')
# if is_p(s):
    # print('yes ,it is a p')
# else:
    # print('no,it is not')

    #------------------------------------
    
# # 
# # a='a.txt'
# # print(open(a).readline())
# import json
# a='a.txt'
# records=[json.loads(line) for line in open(a)]
# # print(records[0])
# print(records[0]['tz'])



# time_zones = [rec ['tz'] for rec in records if 'tz' in rec]
# time_zones[:10]

#------------------------------------
import numpy as np
print(np.random.rand(2,4))
list=np.arange(1,11).reshape([2,-3])

print(np.exp(list))













