import json
import os

os.chdir('/workspace/data/database')

with open('product_data.json', 'r') as f:
    data = json.load(f)

print('=== PRODUCT COUNT ANALYSIS ===')
total_products = 0
total_with_embeddings = 0

for category_name, category_data in data['main_categories'].items():
    category_products = 0
    category_embeddings = 0
    
    print(f'\n{category_name}:')
    for key, value in category_data.items():
        if isinstance(value, list) and key != 'washington_seasonal_multipliers':  # Exclude metadata
            # Additional check: make sure it's actually a product list (contains dicts with 'name')
            if value and isinstance(value[0], dict) and 'name' in value[0]:
                product_count = len(value)
                category_products += product_count
                
                # Count embeddings
                embeddings_in_type = 0
                for product in value:
                    if isinstance(product, dict) and 'image_embedding' in product and len(product['image_embedding']) > 0:
                        embeddings_in_type += 1
                
                category_embeddings += embeddings_in_type
                print(f'  {key}: {product_count} products ({embeddings_in_type} with embeddings)')
        elif key == 'washington_seasonal_multipliers':
            print(f'  {key}: [seasonal metadata - 12 monthly multipliers]')
    
    total_products += category_products
    total_with_embeddings += category_embeddings
    print(f'  Category Total: {category_products} products, {category_embeddings} with embeddings')

print(f'\n=== FINAL SUMMARY ===')
print(f'📦 Total Products: {total_products}')
print(f'🎯 Products with Embeddings: {total_with_embeddings}')
print(f'🔢 Products without Embeddings: {total_products - total_with_embeddings}')
print(f'📁 Categories: {len(data["main_categories"])}')

# Let's also check file line count
try:
    with open('product_data.json', 'r') as f:
        lines = f.readlines()
    print(f'📄 File Lines: {len(lines)}')
except:
    print('📄 Could not count file lines')
