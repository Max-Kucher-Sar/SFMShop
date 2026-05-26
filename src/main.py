class A:
    def method(self):
        print("A.method()")

class B(A):
    def method(self):
        print("B.method()")
        super().method()

class C(A):
    def method(self):
        print("C.method()")
        super().method()

class D(B, C):
    def method(self):
        print("D.method()")
        super().method()

print(D.mro())
"""
Python использует алгоритм C3 Linearization для определения MRO. Когда мы вызываем метод
method() у класса D внутри которой используется функция super(), Python делегирует вызов 
функции следующему классу в MRO. В данном случае MRO у класса D следующий:
[<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>].
"""
