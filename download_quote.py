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
