
# Expense Tracker

A basic tool to track your expenses by adding, removing and listing your items.
#### Video Demo: <https://youtu.be/ku2jGbU__1o>
## Description
The Expense Tracker is an application run in the terminal. The code is written in python. You can store items by category with price and quantity and the Tracker will calculate a total expense for you.

You can add a new item, remove an existing one or clear the whole item list. You can also list your currently stored items by categories either in the terminal or in a PDF file.

### Sources

#### Modules

    main.py
    tables.py
    item.py
    pdf_export.py
    test_item.py

#### Resources

    items.csv
    expense_tracker.pdf

#### Requirements (libraries)

    tabulate
    fpdf2

The **main.py** is the main module of the program. The flow of the code is controlled here.

In the **tables.py** module the templates of the windows are built. They are written with *tabulate* library

The heart of the program, **item.py** contains 2 classes named *Item* and *ItemManager*. The content of the **items.csv** can be modified here. Items can be added, removed, listed and even the whole list can be cleared with the methods written here.

The current state of the list can be exported to a PDF file (**expense_tracker.pdf**) with the **pdf_export.py** modules by using *fpdf2* library. The items will be listed by categories, the subtotal expenses of the categories and the overall total expense will be calculated and shown.

For testing the item classes, the **test_item.py** was written.
