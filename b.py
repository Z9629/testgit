def reverse(text):
    return text[::-1]
    


def is_p(text):
    return text==reverse(text)
    
s=input('enter text:')
i=0

while i<len(s):
    if s[i]==' 'or','or'.'or'!'or'?':
        s[i]==''
    i=i+1
if is_p(s):
    print('yes ,it is a p')
else:
    print('no,it is not')
