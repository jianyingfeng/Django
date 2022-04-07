a = {'name':'zs','age':18}

def fun_a():
    return False


if __name__ == '__main__':
    a.pop('name')
    fun_a()
    print(a)