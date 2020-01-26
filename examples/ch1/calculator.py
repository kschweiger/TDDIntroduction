class Calculator:
    def __init__(self):
        pass
    
    def add(self, v1, v2):
        self.checkInputType(v1)
        self.checkInputType(v2)
        
        return v1 + v2

    def substract(self, v1, v2):
        self.checkInputType(v1)
        self.checkInputType(v2)

        return v1 - v2
    
    def multiply(self, v1, v2):
        self.checkInputType(v1)
        self.checkInputType(v2)
        
        return v1 * v2
        
    def divide(self, v1, v2):
        self.checkInputType(v1)
        self.checkInputType(v2)

        return v1 / v2
        
    @staticmethod
    def checkInputType(var):
        if not (isinstance(var, int) or isinstance(var, float)):
            raise TypeError("%s is not type float or int")
