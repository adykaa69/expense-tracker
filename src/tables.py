from tabulate import tabulate


def open_main_table():
    main_table = [
        [1, "Items"],
        [2, "See list"],
        [3, "Clear tracker"],
        [4, "Generate PDF"],
        [5, "Close tracker"]
        ]
    headers_main = ["Number", "Action"]
    format_main = "outline"

    create_table(main_table, headers_main, format_main)


def open_item_table():
    item_table = [
        [1, "Add item"],
        [2, "Remove item"],
        [3, "Go back"]
        ]
    headers_item = ["Number", "Action"]
    format_item = "outline"

    create_table(item_table, headers_item, format_item)


def create_table(table, headers, format):
    print(tabulate(table, headers, tablefmt=format))
