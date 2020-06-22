
a = 10

def f():
    global a
    global b
    print(a,b)
    print(__name__)

if __name__ == '__main__':
    b = 11
    f()
    
