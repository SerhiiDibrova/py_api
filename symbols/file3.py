from src.file2 import B

class C:
    def method_c(self):
        b = B()
        result = b.method_b()
        print("Method C called with", result)
        return result