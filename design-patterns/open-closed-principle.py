"""
Open-Closed Principle (OCP)
===========================
Software entities (classes, modules, functions) should be:
- OPEN for extension
- CLOSED for modification

This means you should be able to add new functionality without changing existing code.
"""

from abc import ABC, abstractmethod
from enum import Enum


# ============================================================================
# Enums for Product attributes
# ============================================================================

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


# ============================================================================
# Product class
# ============================================================================

class Product:
    def __init__(self, name: str, color: Color, size: Size):
        self.name = name
        self.color = color
        self.size = size

    def __repr__(self):
        return f"Product(name='{self.name}', color={self.color.name}, size={self.size.name})"


# ============================================================================
# BAD APPROACH - Violates OCP
# ============================================================================
# Every time we need a new filter, we have to modify the ProductFilter class.
# This violates OCP because the class is not closed for modification.

class ProductFilter:
    """
    This approach violates OCP!
    Adding new filter criteria requires modifying this class.
    """
    
    def filter_by_color(self, products, color):
        for p in products:
            if p.color == color:
                yield p

    def filter_by_size(self, products, size):
        for p in products:
            if p.size == size:
                yield p
    
    def filter_by_color_and_size(self, products, color, size):
        for p in products:
            if p.color == color and p.size == size:
                yield p

    # If we need filter_by_weight, filter_by_price, etc.
    # we have to keep modifying this class - BAD!


# ============================================================================
# GOOD APPROACH - Follows OCP using Specification Pattern
# ============================================================================

class Specification(ABC):
    """
    Base specification class.
    To add new filter criteria, create a new Specification subclass.
    No need to modify existing code!
    """
    
    @abstractmethod
    def is_satisfied(self, item) -> bool:
        pass

    # Operator overloading for combining specifications
    def __and__(self, other):
        return AndSpecification(self, other)

    def __or__(self, other):
        return OrSpecification(self, other)

    def __invert__(self):
        return NotSpecification(self)


class Filter(ABC):
    """
    Base filter class.
    Works with any Specification - open for extension!
    """
    
    @abstractmethod
    def filter(self, items, spec: Specification):
        pass


# ============================================================================
# Concrete Specifications
# ============================================================================

class ColorSpecification(Specification):
    def __init__(self, color: Color):
        self.color = color

    def is_satisfied(self, item) -> bool:
        return item.color == self.color


class SizeSpecification(Specification):
    def __init__(self, size: Size):
        self.size = size

    def is_satisfied(self, item) -> bool:
        return item.size == self.size


# ============================================================================
# Composite Specifications (Combinators)
# ============================================================================

class AndSpecification(Specification):
    """Combines two specifications with AND logic."""
    
    def __init__(self, *specs):
        self.specs = specs

    def is_satisfied(self, item) -> bool:
        return all(spec.is_satisfied(item) for spec in self.specs)


class OrSpecification(Specification):
    """Combines two specifications with OR logic."""
    
    def __init__(self, *specs):
        self.specs = specs

    def is_satisfied(self, item) -> bool:
        return any(spec.is_satisfied(item) for spec in self.specs)


class NotSpecification(Specification):
    """Negates a specification."""
    
    def __init__(self, spec: Specification):
        self.spec = spec

    def is_satisfied(self, item) -> bool:
        return not self.spec.is_satisfied(item)


# ============================================================================
# Better Filter - Follows OCP
# ============================================================================

class BetterFilter(Filter):
    """
    This filter follows OCP!
    It works with any Specification without needing modification.
    To add new filtering criteria, just create a new Specification class.
    """
    
    def filter(self, items, spec: Specification):
        for item in items:
            if spec.is_satisfied(item):
                yield item


# ============================================================================
# Demo / Usage
# ============================================================================

def main():
    # Create some products
    apple = Product("Apple", Color.GREEN, Size.SMALL)
    tree = Product("Tree", Color.GREEN, Size.LARGE)
    house = Product("House", Color.BLUE, Size.LARGE)
    car = Product("Car", Color.RED, Size.MEDIUM)
    grass = Product("Grass", Color.GREEN, Size.SMALL)

    products = [apple, tree, house, car, grass]

    print("=" * 60)
    print("All Products:")
    print("=" * 60)
    for p in products:
        print(f"  - {p}")

    # Using the OLD approach (violates OCP)
    print("\n" + "=" * 60)
    print("OLD APPROACH (Violates OCP):")
    print("=" * 60)
    
    old_filter = ProductFilter()
    print("\nGreen products (old way):")
    for p in old_filter.filter_by_color(products, Color.GREEN):
        print(f"  - {p.name} is green")

    # Using the NEW approach (follows OCP)
    print("\n" + "=" * 60)
    print("NEW APPROACH (Follows OCP - Specification Pattern):")
    print("=" * 60)
    
    bf = BetterFilter()

    # Filter by color
    print("\nGreen products:")
    green_spec = ColorSpecification(Color.GREEN)
    for p in bf.filter(products, green_spec):
        print(f"  - {p.name} is green")

    # Filter by size
    print("\nLarge products:")
    large_spec = SizeSpecification(Size.LARGE)
    for p in bf.filter(products, large_spec):
        print(f"  - {p.name} is large")

    # Combine specifications with AND
    print("\nLarge AND green products:")
    large_green_spec = large_spec & green_spec  # Uses __and__
    for p in bf.filter(products, large_green_spec):
        print(f"  - {p.name} is large and green")

    # Combine specifications with OR
    print("\nRed OR blue products:")
    red_or_blue_spec = ColorSpecification(Color.RED) | ColorSpecification(Color.BLUE)
    for p in bf.filter(products, red_or_blue_spec):
        print(f"  - {p.name} is red or blue")

    # Using NOT specification
    print("\nProducts that are NOT green:")
    not_green_spec = ~green_spec  # Uses __invert__
    for p in bf.filter(products, not_green_spec):
        print(f"  - {p.name} is not green")

    # Complex combination
    print("\nSmall green OR large blue products:")
    complex_spec = (
        (SizeSpecification(Size.SMALL) & ColorSpecification(Color.GREEN)) |
        (SizeSpecification(Size.LARGE) & ColorSpecification(Color.BLUE))
    )
    for p in bf.filter(products, complex_spec):
        print(f"  - {p.name}")

    print("\n" + "=" * 60)
    print("KEY TAKEAWAY:")
    print("=" * 60)
    print("""
To add a new filter criterion (e.g., by price):
1. Create PriceSpecification(Specification)
2. Use it with existing BetterFilter
3. NO modification to existing code needed!

This is the Open-Closed Principle in action.
""")


if __name__ == "__main__":
    main()

