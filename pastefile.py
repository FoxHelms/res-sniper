penis = {'k1':'v1','k2':'v2','k3':'v3'}
u = 'username'
p = '123123123'

def printer(req1, req2, *args, **kwargs):
    print('Hello' + req1)
    print('\nLets see ur tits' + req2)
    u = args[0]
    p = args[1]
    print(f'U: {u}\npass: {p}\n\n')
    print(kwargs)


printer('Fox', 'Mom', u, p, **penis)

