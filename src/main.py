from item import Item, ItemManager
import tables as t
import re
import sys
import time

item_list = []


def main():
    main_table()


def validate_input(display_table_function, first_num: int, last_num: int) -> str:
    """
    Check if user_input is valid (is in interval).
    Display the table again if the input is not valid.

    :param display_table_function: Function that displays the table
    :param first_num: First number of the interval of possibilities
    :param last_num: Last number of the interval of possibilities
    :return: Valid input
    """

    pattern = fr"^[{first_num}-{last_num}]$"

    while True:
        user_input = input(f"Enter a number ({first_num}-{last_num}): ")
        match = re.search(pattern, user_input)
        if match:
            return user_input
        else:
            display_table_function()


def main_table():
    """
    Open the main table.
    Ask for next Action.
    """
    t.open_main_table()
    action = validate_input(t.open_main_table, 1, 5)

    match action:
        # 1 | Items
        case "1":
            main_table_1()
        # 2 | See list
        case "2":
            main_table_2()
        # 3 | Clear tracker
        case "3":
            main_table_3()
            main_table()
        # 4 | Generate PDF
        case "4":
            generate_pdf()
        # 5 | Close tracker
        case "5":
            close_tracker()


# 1 | Items
def main_table_1():
    t.open_item_table()
    action = validate_input(t.open_item_table, 1, 3)

    match action:
        # 1 | Add item
        case "1":
            item_table_1()
            main_table_1()
        # 2 | Remove item
        case "2":
            item_table_2()
            main_table_1()
        # 3 | Go back
        case "3":
            main_table()


# 1 | Add item
def item_table_1():
    manager = ItemManager("../resources/items.csv")

    # Load currently stored items
    manager.load_items()

    # Add new item
    new_item = Item.get_item()
    manager.add_item(new_item)

    # Save list with recently added item
    manager.save_items()


# 2 | Remove item
def item_table_2():
    manager = ItemManager("../resources/items.csv")

    # Load currently stored items
    manager.load_items()

    if len(manager.items) == 0:
        t.create_table([[f"The Expense Tracker is empty. There is nothing to remove."]], [],
                       format="rounded_grid")
        main_table_1()
    else:
        # List the available items
        manager.get_item_list_with_index()

        # Remove a chosen item
        manager.remove_item()

        # Save list after removing item
        manager.save_items()


# 2 | See list
def main_table_2():
    manager = ItemManager("../resources/items.csv")
    manager.load_items()

    manager.list_by_category()
    while True:
        next_step = input(f"Go back (back) or quit Expense Tracker (quit): ")
        if next_step.lower() in ["back", "b"]:
            main_table()
            break
        elif next_step.lower() in ["quit", "q"]:
            close_tracker()
            break
        else:
            continue


# 3 | Clear tracker
def main_table_3():
    manager = ItemManager("../resources/items.csv")
    manager.load_items()

    manager.clear_tracker()

    manager.save_items()


# 4 | Generate PDF
def generate_pdf():
    manager = ItemManager("../resources/items.csv")
    manager.load_items()

    manager.generate_pdf("../resources/expense_tracker.pdf")
    main_table()


# 5 | Close tracker
def close_tracker():
    print("\nClosing Expense Tracke", end="")
    for _ in "r...":
        print(_, end="", flush=True)
        time.sleep(1)

    sys.exit(f"\n")


if __name__ == "__main__":
    main()
