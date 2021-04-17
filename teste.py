x = '010201110003782962'
y = '2104168040085 5036'
x = y

if len(x) == 18 and x.isnumeric():
    if x[0] == '0':
        print('produto: ', x[4:8])
    else:
        print('produto: ', x[6:9])
elif len(x) == 20 and x.isnumeric():
    print('produto: ', x[4:10])
else:
    print('codigo invalido!')
