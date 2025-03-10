import requests
from odoo import models
import json

class CRMInherit(models.Model):
    _inherit = 'crm.lead'

    def fetch_json_data(self):
        url = "https://tayyabshoukat0786.pythonanywhere.com/upload-document"
        try:
            # Prepare the file to upload
            payload = {}
            files = [
                ('document',
                 ('MG Sale Order.pdf', open('/Users/owner/Documents/MG Sale Order.pdf', 'rb'), 'application/pdf'))
            ]
            headers = {}

            # Sending the POST request to upload the document
            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            # Checking if the request was successful (status code 200)
            if response.status_code == 200:

                # Print the raw response content to check the JSON structure (for debugging)
                print("Raw Response:", response.text)

                # Parsing the response as JSON
                data = response.json()

                # Loop through all products dynamically without using the specific key like "FG_1"
                for product_data in data["Data"]:
                    for key in product_data:
                        fg_data = product_data[key]

                        # Product Information
                        product_name = fg_data["Product_Name"]
                        product_description = fg_data["Product_Description"]
                        total_quantity = fg_data["Quantity"]

                        # Call the create_product method with the extracted data
                        self.create_product(product_name, product_description, total_quantity)
            else:
                print(f"Error: Received status code {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            # Handling any exceptions that occur during the request
            print(f"An error occurred: {e}")
            return None

    def create_product(self, product_name, product_description, total_quantity):
        """
        Create a new product in Odoo using the given product data.
        """
        try:
            # Define the product data dictionary
            product_data = {
                'name': product_name,  # Name of the product
                'type': 'consu',  # or 'product' or 'service', depending on your type
                'description': product_description,  # Description of the product
                # 'quantity_on_hand': total_quantity,  # Available quantity (this can be updated later)
                # 'bom_ids': [],  # You can later add BOM data if necessary
            }

            # Create the product in Odoo
            product = self.env['product.template'].create(product_data)
            print(f"Product {product_data.get('name')} created successfully.")
        except Exception as e:
            print(f"Error creating product: {e}")


    def action_sale_quotations_new(self):
        # First, call the fetch_json_data method
        json_data = self.fetch_json_data()

        if json_data:
            print("Fetched JSON Data:", json_data)
            # Optionally, do something with the fetched data
            # For example, update a field or log the data

        # Continue with the usual logic for creating a new sale quotation
        return super(CRMInherit, self).action_sale_quotations_new()

    def create(self, vals_list):
        res = super().create(vals_list)
        # First, call the fetch_json_data method
        json_data = self.fetch_json_data()

        if json_data:
            print("Fetched JSON Data:", json_data)

        return res
