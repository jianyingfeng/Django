class A:
    def __call__(self, *args, **kwargs):
        print('call')


A()()