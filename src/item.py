import csv
import os.path

from pdf_export import ExpensePDF


class Item:

    def __init__(self, name: str, category: str, price: float, quantity: int):
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    # Getter - Setter blocks

    # Getter of name
    @property
    def name(self):
        return self._name

    # Setter of name
    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.title()

    # Getter of category
    @property
    def category(self):
        return self._category

    # Setter of category
    @category.setter
    def category(self, value):
        if value.strip() == "":
            raise ValueError("Category cannot be empty.")
        self._category = value.title()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Price cannot be non-positive.")
        self._price = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise ValueError("Quantity cannot be non-positive.")
        self._quantity = value

    @classmethod
    def get_item(cls):
        # Validate the input based on type and given condition
        def get_valid_input(prompt, cast_type, condition=None):
            while True:
                try:
                    value = cast_type(input(prompt))
                    if condition and condition(value):
                        return value
                    else:
                        continue
                except ValueError:
                    continue

        name = get_valid_input(
            "Item (text): ",
            str,
            condition=lambda x: x.strip() != "",
        ).title()

        category = get_valid_input(
            "Category (text): ",
            str,
            condition=lambda x: x.strip() != "",
        ).title()

        price = get_valid_input(
            "Price (positive number): ",
            float,
            condition=lambda x: x > 0,
        )

        quantity = get_valid_input(
            "Quantity (positive number): ",
            int,
            condition=lambda x: x > 0,
        )

        return cls(name, category, price, quantity)

    def __str__(self):
        return f"Item: {self.name}\n" \
               f"Category: {self.category}\n" \
               f"Price: {self.price}\n" \
               f"Quantity: {self.quantity}"

    # Return the multiplication of the price and the quantity of an item
    @property
    def total_price(self) -> float:
        return self.quantity * self.price


class ItemManager:

    def __init__(self, file_path):
        self.file_path = file_path
        self.items = []

    # Create empty csv file
    def create_csv(self):
        with open(self.file_path, mode="w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "category", "price", "quantity"])
            writer.writeheader()

    # Load items already in the csv
    def load_items(self):
        if not os.path.exists(self.file_path):
            self.create_csv()
        else:
            with open(self.file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    item = Item(
                        name=row["name"],
                        category=row["category"],
                        price=float(row["price"]),
                        quantity=int(row["quantity"])
                    )
                    self.items.append(item)

    # Save content of csv then exit
    def save_items(self):
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "category", "price", "quantity"])
            writer.writeheader()
            for item in self.items:
                writer.writerow({
                    "name": item.name,
                    "category": item.category,
                    "price": item.price,
                    "quantity": item.quantity
                })

    # Add an item to csv
    def add_item(self, item: Item):
        from tables import create_table
        self.items.append(item)
        create_table([[
            f"Item added: {item.name} | {item.category} | "
            f"{item.price:g} | {item.quantity}"]],
            [], format="rounded_grid")

    # Return the total price of a category
    def total_price_by_category(self):
        categories = {}

        for item in self.items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)

        category_totals = {}
        for category, items in categories.items():
            price_of_category = 0
            for item in items:
                price_of_category += item.total_price
            category_totals[category] = price_of_category
        return category_totals

    # Return the total price of all the items
    def total_price_of_all_items(self):
        total_expenses = 0
        for item in self.items:
            total_expenses += item.total_price
        return total_expenses

    # List the items by categories in separate tables
    def list_by_category(self):
        from tables import create_table
        categories = {}

        for item in self.items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)

        for category, items in categories.items():
            print(f"\nCategory: {category}")

            table_list = []
            for item in items:
                table_list.append([item.name, item.price, item.quantity, item.total_price])
            header_list = ["Name", "Price", "Quantity", "Total Price"]
            create_table(table_list, header_list, format="outline")

            total_price_by_category = self.total_price_by_category()
            print(f"Total price of {category}: {total_price_by_category[category]}")

        if len(self.items) == 0:
            create_table([[f"The Expense Tracker is empty. Choose 'Item' -> 'Add item' to add items."]], [],
                         format="rounded_grid")
        else:
            print(end="\n")
            create_table([[f"Total Expenses: {self.total_price_of_all_items()}"]], [], format="rounded_grid")
            print(end="\n")

    # Count the number of items in csv
    def number_of_items(self):
        with open(self.file_path, mode='r') as file:
            reader = csv.DictReader(file)
            row_count = len(list(reader))
            return row_count

    # List the items in added order with index
    def get_item_list_with_index(self):
        from tables import create_table
        item_list_with_index = []
        header_list = ["ID", "Name", "Category", "Price", "Quantity"]

        for index, item in enumerate(self.items, start=1):
            item_list_with_index.append([index, item.name, item.category, item.price, item.quantity])

        create_table(item_list_with_index, header_list, format="outline")

    # Remove item from csv
    def remove_item(self):
        from tables import create_table
        while True:
            try:
                index = input(f"Enter a number (1-{self.number_of_items()}) or 'back' to go back: ")
                if index.lower() in ["b", "back"]:
                    break

                index = int(index)
                if 1 <= index <= self.number_of_items():
                    removed_item = self.items.pop(index - 1)
                    # Print message about removed item
                    create_table([[
                                      f"Item removed: {removed_item.name} | {removed_item.category} | "
                                      f"{removed_item.price:g} | {removed_item.quantity}"]],
                                 [], format="rounded_grid")
                    break
                else:
                    continue
            except ValueError:
                continue

    # Clear the whole content of csv
    def clear_tracker(self):
        from tables import create_table

        while True:
            answer = input("Clear Expense Tracker? (yes/no): ")
            if answer.lower() == "yes":
                self.items.clear()
                create_table([["Expense Tracker has been cleared."]], [], format="rounded_grid")
                break
            elif answer.lower() == "no":
                break
            else:
                continue

    def generate_pdf(self, exported_pdf_name):
        from tables import create_table
        pdf = ExpensePDF()
        pdf.add_page()

        categories = {}

        if len(self.items) == 0:
            create_table([[f"The Expense Tracker is empty. Choose 'Item' -> 'Add item' to add items."]], [],
                         format="rounded_grid")

        else:
            for item in self.items:
                if item.category not in categories:
                    categories[item.category] = []
                categories[item.category].append(item)

            category_totals = self.total_price_by_category()

            for category, items in categories.items():
                # Create pdf_export compatible data from items
                items_data = [
                    {"name": item.name, "category": item.category, "price": item.price, "quantity": item.quantity,
                     "total_price": item.total_price}
                    for item in items
                ]
                # Get total_price of a category
                total_price = category_totals[category]
                # Create category_table
                pdf.add_category_table(category, items_data, total_price)

            pdf.add_total_expenses(self.total_price_of_all_items())

            try:
                pdf.output(exported_pdf_name)
                create_table([["PDF has been generated."]], [], format="rounded_grid")
            except():
                create_table([["Error during PDF generation."]], [], format="rounded_grid")
