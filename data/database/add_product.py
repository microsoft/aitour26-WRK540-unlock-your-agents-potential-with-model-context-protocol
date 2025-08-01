import json
import os
from typing import Union


def get_user_input(prompt: str, input_type: type = str, required: bool = True) -> Union[str, int, float]:
    """Get user input with type conversion and validation."""
    while True:
        try:
            value = input(prompt).strip()
            if required and not value:
                print("This field is required. Please enter a value.")
                continue
            if input_type == float:
                return float(value)
            if input_type == int:
                return int(value)
            return value
        except ValueError:
            print(f"Please enter a valid {input_type.__name__}.")


# Change to the correct directory
os.chdir('/workspace/data/database')

# Load the product data
with open("product_data.json", "r") as f:
    data = json.load(f)

# Print available categories first
print("Available categories:")
categories = list(data["main_categories"].keys())
for i, category_name in enumerate(categories, 1):
    print(f"  {i}. {category_name}")

# Get user selection for category
print("\nYou can either:")
print("- Enter the number of an existing category")
print("- Type the name of a new category to create it")
print()

category_input = input("Enter category number or new category name: ").strip()

# Check if input is a number (existing category)
try:
    category_choice = int(category_input)
    if 1 <= category_choice <= len(categories):
        selected_category_name = categories[category_choice - 1]
        selected_category = data["main_categories"][selected_category_name]
        print(f"Selected existing category: {selected_category_name}")
    else:
        print(f"Invalid number. Please enter a number between 1 and {len(categories)}")
        exit(1)
except ValueError:
    # Input is not a number, treat as new category name
    selected_category_name = category_input
    if selected_category_name in data["main_categories"]:
        selected_category = data["main_categories"][selected_category_name]
        print(f"Selected existing category: {selected_category_name}")
    else:
        # Create new category
        data["main_categories"][selected_category_name] = {}
        selected_category = data["main_categories"][selected_category_name]
        print(f"Created new category: {selected_category_name}")

print(f"\nSelected category: {selected_category_name}")

# Print available product types in the selected category
print(f"\nAvailable product types in '{selected_category_name}':")
product_types = [key for key in selected_category 
                if key != "washington_seasonal_multipliers" and isinstance(selected_category[key], list)]

if product_types:
    for i, product_type in enumerate(product_types, 1):
        print(f"  {i}. {product_type} (has {len(selected_category[product_type])} products)")
    
    # Get user selection for product type
    print("\nYou can either:")
    print("- Enter the number of an existing product type")
    print("- Type the name of a new product type to create it")
    print()
    
    type_input = input("Enter product type number or new product type name: ").strip()
    
    # Check if input is a number (existing product type)
    try:
        type_choice = int(type_input)
        if 1 <= type_choice <= len(product_types):
            selected_product_type = product_types[type_choice - 1]
            print(f"Selected existing product type: {selected_product_type}")
        else:
            print(f"Invalid number. Please enter a number between 1 and {len(product_types)}")
            exit(1)
    except ValueError:
        # Input is not a number, treat as new product type name
        selected_product_type = type_input
        if selected_product_type in selected_category and isinstance(selected_category[selected_product_type], list):
            print(f"Selected existing product type: {selected_product_type}")
        else:
            # Create new product type
            selected_category[selected_product_type] = []
            print(f"Created new product type: {selected_product_type}")
else:
    print("  No product types found in this category.")
    print("\nEnter a name for the new product type:")
    selected_product_type = input("Product type name: ").strip()
    if not selected_product_type:
        print("Product type name is required.")
        exit(1)
    selected_category[selected_product_type] = []
    print(f"Created new product type: {selected_product_type}")

print(f"\nSelected product type: {selected_product_type}")

# Get product details from user
print("\n" + "="*50)
print("Enter product details:")
print("="*50)

product_name = get_user_input("Product name: ")
product_sku = get_user_input("Product SKU: ")
product_description = get_user_input("Product description: ")
product_price = get_user_input("Product price ($): ", float)
product_stock_level = get_user_input("Stock level: ", int)

# Create the new product
new_product = {
    "name": product_name,
    "sku": product_sku,
    "price": product_price,
    "description": product_description,
    "stock_level": product_stock_level,
    "image_path": "",
    "image_embedding": []
}

# Add the new product to the selected category and type
selected_category[selected_product_type].append(new_product)

# Save the updated data
with open("product_data.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"\n✅ Successfully added '{product_name}' to '{selected_product_type}' in '{selected_category_name}' category.")
print(f"Product details:")
print(f"  Name: {new_product['name']}")
print(f"  SKU: {new_product['sku']}")
print(f"  Price: ${new_product['price']}")
print(f"  Description: {new_product['description']}")
print(f"  Stock Level: {new_product['stock_level']}")
