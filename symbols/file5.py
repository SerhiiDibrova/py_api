from src.file1 import A
from src.file3 import C

def utility_function():
    a = A()
    c = C()
    print("Utility function uses A and C")
    return a.method_a(), c.method_c()
