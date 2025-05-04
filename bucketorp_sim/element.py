# element.py

class Element:
    def __init__(self, key, aux=0, value=None):
        self.key = key
        self.aux = aux
        self.value = value

    def __repr__(self):
        return f"Element(key={self.key}, aux={self.aux})"
