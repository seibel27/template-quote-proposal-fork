from abstra.compat import use_legacy_threads
"""
Calling the use_legacy_threads function allows using
the legacy threads in versions > 3.0.0
https://docs.abstra.io/guides/use-legacy-threads/

The new way of using workflows is with tasks. Learn more
at https://docs.abstra.io/concepts/tasks/ and contact us
on any issues during your migration
"""
use_legacy_threads("forms")

import abstra.workflows as aw
import pandas as pd
from abstra.forms import reactive

price_markdown = """
## Total: {total}
"""


def price_string(cents: int) -> str:
    return f"${cents / 100:,.2f}"


file_path = "mock_database.csv"


# open files
df = pd.read_csv(file_path)
products_database = df.to_dict(orient="records")

products_ids = set([str(product["id"]) for product in products_database])

updated_proposal = aw.get_data("updated_proposal")

dropdown_options = [{"label": "(Product Unavailable)", "value": "none"}]
for prod in products_database:
    prod["id"] = str(prod["id"])

    dropdown_options.append({"label": prod["name"], "value": prod["id"]})


# build form page
@reactive
def render(partial):
    total = 0

    for product in updated_proposal:
        product_id = str(product["product_id"])

        if product_id not in products_ids:
            selected_prod = partial.read_dropdown(
                f"{product['quantity']} x {product['product']}",
                options=dropdown_options,
                key=f"{product['id']}",
                required=True,
                initial_value="none",
            )

        else:
            selected_prod = partial.read_dropdown(
                f"{product['quantity']} x {product['product']}",
                options=dropdown_options,
                key=f"{product['id']}",
                required=True,
                initial_value=product_id,
            )

            if selected_prod == None:
                selected_prod = product_id

        in_stock_product = next(
            (prod for prod in products_database if prod["id"] == selected_prod), None
        )

        if in_stock_product is not None:
            total += int(in_stock_product["price"]) * int(product["quantity"])

    partial.display_markdown(price_markdown.format(total=price_string(total)))


result = render.run()

# adjust final estimate
estimate = []

for product_id, in_stock_id in result.items():
    product_in_stock = next(
        (product for product in products_database if product["id"] == in_stock_id), None
    )
    product = next(
        (product for product in updated_proposal if product["id"] == product_id), None
    )

    if product_in_stock is None:
        estimate.append(
            {
                "id": product_id,
                "product": product["product"],
                "quantity": product["quantity"],
                "price": "",
                "database_match": "Unavailable",
                "product_id": 0,
            }
        )

    else:
        estimate.append(
            {
                "id": product_id,
                "product": product["product"],
                "quantity": product["quantity"],
                "price": product_in_stock["price"],
                "database_match": product_in_stock["name"],
                "product_id": product_in_stock["id"],
            }
        )

aw.set_data("estimate", estimate)
