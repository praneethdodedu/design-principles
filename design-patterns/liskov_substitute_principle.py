
class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def area(self):
        return self._width * self._height

    def __str__(self):
        return f"Rectangle(width={self._width}, height={self._height}, area={self.area})"

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value

def use_it(rect):
    """
    This function expects Rectangle behavior:
    - Setting height should NOT affect width
    - Area should be original_width * new_height
    """
    print(f"Using {rect}")
    original_width = rect.width  # Save width BEFORE changing height
    rect.height = 10
    expected_area = original_width * 10  # Expectation: width unchanged!
    actual_area = rect.area
    
    if expected_area != actual_area:
        print(f"  LSP VIOLATED! Expected area: {expected_area}, got: {actual_area}")
    else:
        print(f"  OK. Expected area: {expected_area}, got: {actual_area}")

class Square(Rectangle):
    def __init__(self, size):
        super().__init__(size, size)

    @Rectangle.width.setter
    def width(self, value):
        self._width = value
        self._height = value

    @Rectangle.height.setter
    def height(self, value):
        self._height = value
        self._width = value

if __name__ == "__main__":
    rect = Rectangle(2, 3)
    use_it(rect)

    square = Square(5)
    use_it(square)

    