import pandas as pd
from abstra.forms import reactive, display
from abstra.tasks import send_task, get_tasks

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

# get tasks with error handling
tasks = get_tasks()
if not tasks:
    display("No proposal to update. Please create a proposal first.")
    exit()  # Exit the stage if no tasks are available

task = tasks[0]
updated_proposal = task.payload["proposal"]
# get client's email, company and name
client_email = task.payload["email"]
company_name = task.payload["company"]
client_name = task.payload["name"]

dropdown_options = [{"label": "(Product Unavailable)", "value": "none"}]
for prod in products_database:
    prod["id"] = str(prod["id"])

    dropdown_options.append({"label": prod["name"], "value": prod["id"]})


# build form page
@reactive
def render(partial):
    total = 0

    for product in updated_proposal:
        product_id = product["product_id"]
        
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

send_task(
    "estimate",
    {
        "estimate": estimate,
        "email": client_email,
        "company": company_name,
        "name": client_name, 
    }
)
task.complete()