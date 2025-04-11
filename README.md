# Quote Proposal System

## How It Works

This project automates the process of generating quotations using Abstra's tools and scripts. The system allows users to upload a proposal, automatically matches products from the database using OCR, and generates a final PDF quote emailing it to the customer.

Integrations:

- Email

To customize this template for your team and build a lot more, <a href="https://meet.abstra.app/demo?url=template-quote-proposal" target="_blank">book a demonstration here</a>.

![A quote proposal system workflow built in Abstra](https://github.com/user-attachments/assets/3f45509f-cf3d-4a7d-9e6a-7aeeec84fb41)


## Initial Configuration

To use this project, some initial configurations are necessary:

1. **Python Version**: Ensure Python version 3.9 or higher is installed on your system.

2. **Set Database**: The mock CSV is provided for demonstration purposes. You can connect to your own product database; just ensure that you correctly access the product name, ID, and price. Note that the program expects product prices to be in cents.
   
3. **Environment Variables**: The following environment variables are required for both local development and online deployment:

   - `FINANCE_EMAIL`: Your company's finance email for sending quotes.

   For local development, create a `.env` file at the root of the project and add the variables listed above (refer to `.env.example`). For online deployment, configure these variables in your <a href="https://docs.abstra.io/cloud/envvars" target="_blank">environment settings</a>.

4. **Dependencies**: To install the necessary dependencies for this project, a `requirements.txt` file is provided. This file includes all the required libraries.

   Follow these steps to install the dependencies:

   1. Open your terminal and navigate to the project directory.
   2. Run the following command to install the dependencies from `requirements.txt`:

      ```sh
      pip install -r requirements.txt
      ```

5. **Access Control**: The generated forms are protected by default. For local testing, no additional configuration is necessary. However, for cloud usage, you need to add your own access rules. For more information on how to configure access control, refer to the <a href="https://docs.abstra.io/concepts/access-control" target="_blank">Abstra access control documentation</a>.

6. **Local Usage**: To access the local editor with the project, use the following command:

   ```sh
      abstra editor path/to/your/project/folder/
   ```

## General Workflows

The following workflows automate the process of generating and sending a quote proposal.

### Quote Proposal Upload

The customer uploads a file or photo of their proposal, and OCR technology extracts the contents for processing.

- **quote_proposal.py**: Main script for uploading the quote proposal and extracting content via OCR.

### Product Matching

Using Abstra AI, the system identifies matching products from the database.

- **generate_quote.py**: Script to match the products from the proposal with items in the product database.

### Quote Approval

A sales team member reviews the matched products and approves the proposal.

- **quote_approval.py**: Script for reviewing and approving the matched products with minimal manual input.

### Quote PDF Generation

Once approved, a PDF is generated with the finalized products and details.

- **generate_quote_pdf.py**: Script to generate the finalized PDF quote.

### Sending the Quote

An email is sent to the customer when the quote is available.

- **download_quote.py**: From where the final quote can be downloaded.

If you're interested in customizing this template for your team in under 30 minutes, <a href="https://meet.abstra.app/demo?url=template-quote-proposal" target="_blank">book a customization session here</a>.
