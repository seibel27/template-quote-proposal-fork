from abstra.compat import use_legacy_threads
"""
Calling the use_legacy_threads function allows using
the legacy threads in versions > 3.0.0
https://docs.abstra.io/guides/use-legacy-threads/

The new way of using workflows is with tasks. Learn more
at https://docs.abstra.io/concepts/tasks/ and contact us
on any issues during your migration
"""
use_legacy_threads("scripts")

import abstra.workflows as aw
from abstra.common import get_persistent_dir
from fpdf import FPDF

company_name = aw.get_data("company")
client_name = aw.get_data("name")
client_email = aw.get_data("email")

persistent_dir = get_persistent_dir()
file_path = persistent_dir / f"{company_name} Quote.pdf"
logo_path = "logo.png"


def price_string(cents: int) -> str:
    return f"${cents / 100:,.2f}"


def list_to_string(data: list) -> str:
    return ", ".join(data) + "."


def dict_to_table(data: dict) -> list[list]:
    unavailable_products = []

    table = [["Product", "Price Un.", "Quantity", "Price"]]
    total = 0

    for product in data:
        if product["product_id"] == 0:
            unavailable_products.append(product["product"])
            continue

        table.append(
            [
                product["database_match"],
                price_string(int(product["price"])),
                product["quantity"],
                price_string(int(product["price"]) * int(product["quantity"])),
            ]
        )

        total += int(product["price"]) * int(product["quantity"])

    table.append(["Total", "", "", price_string(total)])
    return table, unavailable_products


class PDF(FPDF):
    font = "Arial"

    def header(self):
        logo_width = 35
        page_width = self.w
        margin_left = self.l_margin
        x_position = (page_width - logo_width) / 2
        self.image(str(logo_path), x_position, 10, logo_width)
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font(PDF.font, "", 8)
        self.cell(0, 10, f"{self.page_no()}", 0, 0, "C")

    def chapter_title(self, title):
        self.set_font(PDF.font, "B", 12)
        self.cell(0, 10, title, 0, 1, "C")
        self.ln(10)

    def chapter_body(self, body, font_size=8, style="I"):
        self.set_font(PDF.font, style, font_size)
        self.multi_cell(0, (font_size / 2) + 1, body)
        self.ln()

    def draw_table(self, data, line=8, font_size=10, secondary_col_width=40):
        page_width = self.w - 2 * self.l_margin
        first_col_width = page_width - (len(data[0]) - 1) * secondary_col_width
        column_widths = [first_col_width] + [secondary_col_width] * (len(data[0]) - 1)

        for i, row in enumerate(data):
            if i == 0 or i == len(data) - 1:
                self.set_font(PDF.font, "B", font_size)
                self.set_fill_color(200, 200, 200)
            else:
                self.set_font(PDF.font, "", font_size)
                if i % 2 != 0:
                    self.set_fill_color(240, 240, 240)
                else:
                    self.set_fill_color(255, 255, 255)

            for j, cell in enumerate(row):
                self.cell(column_widths[j], line, str(cell), border=0, fill=True)

            self.ln(line)
        self.ln(line)


estimate = aw.get_data("estimate")
estimate_table, unavailable_products = dict_to_table(estimate)

# generate pdf
pdf = PDF()
pdf.add_page()

pdf.chapter_title(f"Quote Proposal - {company_name}")
pdf.chapter_body(f"Solicited by: {client_name} - {client_email}")

pdf.draw_table(estimate_table)

if unavailable_products:
    pdf.chapter_body("Unavailable Products: " + list_to_string(unavailable_products))

pdf.output(file_path)
