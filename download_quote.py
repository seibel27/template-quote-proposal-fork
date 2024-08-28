import abstra.forms as af
import abstra.workflows as aw
from abstra.common import get_persistent_dir

company_name = aw.get_data("company")
client_name = aw.get_data("name")

persistent_dir = get_persistent_dir()
file_path = persistent_dir / f"{company_name} Quote.pdf"


markdown = f"""

<h1 style="text-align: center; padding-bottom:50px">Quote Proposal for {company_name}</h1>

Hello {client_name},

We would like to inform you that the requested quote has been generated. Please review the document and let us know if you have any questions or need further information.

Thank you for your attention, and we are available to assist with anything you may need.

Sincerely, Michael Scott - Sales Manager\n
Scranton

"""

(
    af.Page()
    .display_markdown(markdown)
    .display_file(file_path, download_text="Download Quote")
    .run(end_program=True)
)
