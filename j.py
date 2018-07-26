sum=1;
a=int(input(':'))
i=1
while(i<=a):
    if(a==1):
        print(1) 
        break
    sum=sum*i
    i=i+1

print('%e' % sum)