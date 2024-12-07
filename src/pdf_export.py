from fpdf import FPDF


class ExpensePDF(FPDF):
    def header(self):
        # Header: Expense Tracker
        self.set_font("helvetica", "B", 18)
        self.cell(0, 0, "Expense Tracker", align="C")
        self.ln(10)

    # def footer(self):
    #     # Footer
    #     self.set_y(-15)
    #     self.set_font("helvetica", "I", 10)
    #     self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_category_table(self, category_name, items, total_price):
        # Header: Category
        page_width = self.w - self.l_margin - self.r_margin # Effective page width
        table_width = 180
        start_x = (page_width - table_width) / 2 + self.l_margin

        self.set_x(start_x)  # Align to middle
        self.set_fill_color(255, 192, 0)
        self.set_text_color(0)
        self.set_font("helvetica", "B", 16)
        self.set_line_width(0.5)  # Border line width
        self.cell(table_width, 10, category_name, border=1, align="C", fill=True)
        self.ln(10)


        # Header: Name, Price, Quantity, Total Price
        self.set_x(start_x)  # Align to middle
        self.set_font("helvetica", "B", 11)
        self.set_fill_color(255, 217, 102)
        self.set_text_color(0)
        self.set_line_width(0.5)  # Border line width
        self.cell(60, 8, "Name", border="LTB", fill=True)
        self.cell(40, 8, "Price", border="TB", fill=True)
        self.cell(40, 8, "Quantity", border="TB", fill=True)
        self.cell(40, 8, "Total Price", border="RTB", fill=True)
        self.ln(8)

        # Content
        self.set_font("helvetica", "", 12)
        self.set_fill_color(255, 217, 102)
        self.set_text_color(0)
        for item in items:
            self.set_x(start_x) # Align to middle
            self.set_line_width(0.5)  # Border line width
            self.cell(60, 8, item["name"], border="L", fill=True)
            self.cell(40, 8, f"{item['price']}", border=0, fill=True)
            self.cell(40, 8, f"{item['quantity']}", border=0, fill=True)
            self.cell(40, 8, f"{item['total_price']}", border="R", fill=True)
            self.ln(8)

        # Total Price of Category
        self.set_x(start_x)
        self.set_fill_color(191, 143, 0)
        self.set_text_color(0)
        self.set_font("helvetica", "B", 12)
        self.cell(table_width, 8, f"Total price of {category_name}: {total_price}", border=1, align="L", fill=True)
        self.ln(10)

    def add_total_expenses(self, total):
        # Total Expenses - Separate cell
        page_width = self.w - self.l_margin - self.r_margin
        table_width = 180
        start_x = (page_width - table_width) / 2 + self.l_margin

        self.set_x(start_x) # Align to middle
        self.set_fill_color(198, 89, 17)
        self.set_line_width(0.5)  # Border line width
        self.set_text_color(0)
        self.set_font("helvetica", "B", 12)
        self.cell(table_width, 10, f"Total Expenses: {total:g}", border=1, align="C", fill=True)
        self.ln(10)