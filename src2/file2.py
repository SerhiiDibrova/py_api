from src.file1 import A

class B:
    def method_b(self):
        a = A()
        result = a.method_a()
        print("Method B called with", result)
        return result