class BaseAgent:
    def __init__(self, name):
        self.name = name
    
    def analyze(self):
        """Debe retornar una tupla (score, reason) donde score es -1, 0, o 1"""
        raise NotImplementedError
