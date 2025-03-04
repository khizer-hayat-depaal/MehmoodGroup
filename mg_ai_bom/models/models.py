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

                BOM = data.get('BOM', {})
                product_name = 'NKFROSE MOM TWI SHORTS 3248-TW TBINMT-2409-00551'

                # Extract the Product Name from the returned data
                product_name = self.extract_product_name(product_name)

                # Print or use the Product Name as needed
                if product_name:
                    print("Extracted Product Name:", product_name)

                return data
            else:
                print(f"Error: Received status code {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            # Handling any exceptions that occur during the request
            print(f"An error occurred: {e}")
            return None

    def create_product(self, product_data):
        """
        Create a new product in Odoo using the given product data.
        """
        try:
            # Create a new product record in the 'product.template' model
            product_template = self.env['product.template'].create({
                'name': product_data.get('name'),
                # 'description': product_data.get('description'),
                # 'type': 'product',  # Assuming the product is a stockable product
                # 'list_price': product_data.get('raw_materials_cost', 0),  # You can adjust this if needed
                # 'standard_price': product_data.get('raw_materials_cost', 0),  # Assuming cost is raw materials cost
            })

            # Optionally, you can create additional product variants, etc.
            self.env['product.product'].create({
                'product_tmpl_id': product_template.id,
                'quantity_on_hand': product_data.get('quantity', 0)
            })
            print(f"Product {product_data.get('name')} created successfully.")
        except Exception as e:
            print(f"Error creating product: {e}")

    def extract_product_names(self, json_data):
        """
        Extract product names from the JSON data and create products based on this data.
        """
        try:
            # Check if the data is a list of products
            if isinstance(json_data, list):
                # Loop through each product in the list
                for product in json_data:
                    # Extract the necessary product data
                    product_name = product.get("Product_Name")
                    # product_description = product.get("Product_Description")
                    # quantity = product.get("Quantity")
                    # cost_estimation = product.get("Cost_Estimation", {})
                    # raw_materials_cost = cost_estimation.get("Raw_Materials_Cost")

                    # Create a dictionary for the product data
                    product_data = {
                        'name': product_name,
                        # 'description': product_description,
                        # 'quantity': quantity,
                        # 'raw_materials_cost': raw_materials_cost
                    }

                    # Call the create_product method to create a product in Odoo
                    self.create_product(product_data)

                return "Products Created Successfully"
            else:
                print("Expected data format is a list of products")
                return None
        except Exception as e:
            print(f"Error extracting product names: {e}")
            return None

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
