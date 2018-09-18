try:
    text=input('enter something-->')
except EOFError:
    print('why did you do an EOF on me?')
except KeyboardInterrupt:
    print('you are wrong')
else:
    print('you entered {}'.format(text))