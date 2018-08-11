def num(x):
    if x==1:
        return 1;
    return x*num(x-1)
        
    
s=int(input(':'))
print('%e' % num(s))