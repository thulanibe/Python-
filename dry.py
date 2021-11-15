def drier(dry=False):
    def wrapper(func):

        def inner_wrapper(*arg,**kwargs):
            if dry:
                print(func.__name__)
                print(arg)
                print(kwargs)
            else:
                return func(*arg,**kwargs)
        return inner_wrapper
    return wrapper

@drier(True)
def test(name):
    print("hello "+name)

test("girish")

@drier()
def test2(name,last):
   print("hello {} {}".format(name,last))