import abstra.forms as af
from abstra.tasks import get_tasks
from abstra.common import get_persistent_dir

tasks = get_tasks()
if not tasks:
    display("No data to update. Please receive some first.")
    tasks[0].complete()
    exit()  # Exit the stage if no tasks are available

task = tasks[0]
client_data = task.payload
# get client's email, company and name
client_email = client_data["email"]
company_name = client_data["company"]
client_name = client_data["name"]

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
task.complete()

(
    af.Page()
    .display_markdown(markdown)
    .display_file(file_path, download_text="Download Quote")
    .run(end_program=True)
)

