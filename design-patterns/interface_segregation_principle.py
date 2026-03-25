class Machine:
    def print(self, document):
        raise NotImplementedError("Subclasses must implement this method")

    def fax(self, document):
        raise NotImplementedError("Subclasses must implement this method")

    def scan(self, document):
        raise NotImplementedError("Subclasses must implement this method")

class MultiFunctionPrinter(Machine):
    def print(self, document):
        print(f"Printing: {document}")

    def fax(self, document):
        print(f"Faxing: {document}")

    def scan(self, document):
        print(f"Scanning: {document}")

class OldFashionedPrinter(Machine):
    def print(self, document):
        print(f"Printing: {document}")

    def fax(self, document):
        raise NotImplementedError("OldFashionedPrinter cannot fax")

    def scan(self, document):
        raise NotImplementedError("OldFashionedPrinter cannot scan")

class Printer:
    @abstractmethod
    def print(self, document):
        pass

class Scanner:
    @abstractmethod
    def scan(self, document):
        pass

class Fax:
    @abstractmethod
    def fax(self, document):
        pass

class MyPrinter(Printer):
    def print(self, document):
        print(f"Printing: {document}")
    
class Photocopier(Printer, Scanner):
    def print(self, document):
        print(f"Printing: {document}")
    
    def scan(self, document):
        print(f"Scanning: {document}")