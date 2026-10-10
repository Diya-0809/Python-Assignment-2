class Product:
    def __init__(self, pid, name, stock, purchase_price, selling_price):
        self.pid = pid
        self.name = name
        self.stock = stock
        self.purchase_price = purchase_price
        self.selling_price = selling_price

class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, p):
        self.products[p.pid] = p

    def __add__(self, other):
        """Operator overloading (+) to merge two inventories."""
        merged = Inventory()
        all_pids = set(self.products.keys()).union(set(other.products.keys()))

        for pid in all_pids:
            if pid in self.products and pid in other.products:
                p1 = self.products[pid]
                p2 = other.products[pid]
                merged_stock = p1.stock + p2.stock
                min_purchase = min(p1.purchase_price, p2.purchase_price)
                max_selling = max(p1.selling_price, p2.selling_price)
                merged.add_product(Product(pid, p1.name, merged_stock, min_purchase, max_selling))
            elif pid in self.products:
                merged.add_product(self.products[pid])
            else:
                merged.add_product(other.products[pid])

        return merged

    def display(self):
        for pid, p in sorted(self.products.items()):
            print(f"{p.pid} {p.name} stock={p.stock} purchase={p.purchase_price} selling={p.selling_price}")

if __name__ == "__main__":
    invA = Inventory()
    invA.add_product(Product("P1", "Pen", 10, 5, 8))

    invB = Inventory()
    invB.add_product(Product("P1", "Pen", 7, 4, 9))

    # Perform Merge
    merged_inv = invA + invB
    merged_inv.display()
