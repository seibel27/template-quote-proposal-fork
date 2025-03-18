

import json
import os
from uuid import uuid4


from abstra.ai import prompt
from abstra.common import get_persistent_dir
from abstra.forms import ListItemSchema, Page

persistent_dir = get_persistent_dir()
save_image_path = persistent_dir / "estimate.png"


page = (
    Page()
    .read("Name", key="name", required=True)
    .read_email("E-mail", key="email", required=True)
    .read("Company", key="company", required=True)
    .read_file("Upload image", key="image", required=True)
    .display_file("example_quote.jpg", download_text="Or use this example image")
    .run()
)


# OCR
transcription = prompt(
    [
        """This image in base64 format is a list of products, you must transcribe the text from the image, extracting the name of each product and the amount of each product. The final output should be a list with square brackets where each item is separated by commas, and each item should follow the following sample of a json dictionary.json dictionary sample: {"product": "sample", "quantity": "sample"}. The quantities of the products can not be negative.""",
        page["image"],
    ],
    format={
        "products": {
            "type": "string",
            "description": "list of products separated by commas, delimited by square brackets, each item following the sample json pattern.",
        }
    },
    temperature=0.3,
)

ocr = json.loads(transcription["products"])


# Check page
item = (
    ListItemSchema()
    .read("Product", key="product")
    .read_number("Quantity", key="quantity")
)
check_stage = (
    Page()
    .display(
        "Please, check the products and quantities extracted from the image.",
        size="medium",
    )
    .read_list(item, initial_value=ocr, key="check", required=True, min=1)
    .run()
)

proposal = check_stage["check"]

for p in proposal:
    p["id"] = str(uuid4())
    p["price"] = ""
    p["database_match"] = ""
    p["product_id"] = ""


aw.set_data("proposal", proposal)
aw.set_data("email", page["email"])
aw.set_data("company", page["company"].title())
aw.set_data("name", page["name"].title())

# set_data ===== send_task (lista/dict)

finance_email = os.getenv("FINANCE_EMAIL")

aw.set_data("finance_email", finance_email)
