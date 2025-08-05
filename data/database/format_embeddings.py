#!/usr/bin/env python3
"""
Script to reformat embedding arrays in product_data.json
- Convert image_embedding and description_embedding arrays from one number per line to comma-separated single line
"""

import json
import os


def format_embedding_array(embedding_array):
    """
    Format an embedding array to be comma-separated on a single line
    
    Args:
        embedding_array (list): List of float numbers
        
    Returns:
        list: Same list (JSON will format it as single line when indent is None for this field)
    """
    return embedding_array

def process_product_data(file_path):
    """
    Process the product_data.json file to reformat image and description embeddings
    
    Args:
        file_path (str): Path to the product_data.json file
    """
    print(f"Processing {file_path}...")
    
    # Read the JSON file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        return False
    
    # Track changes
    products_processed = 0
    image_embeddings_found = 0
    description_embeddings_found = 0
    
    # Process each category
    for category_name, category_data in data.get('main_categories', {}).items():
        print(f"Processing category: {category_name}")
        
        for product_type, products in category_data.items():
            # Skip non-product entries like seasonal multipliers
            if not isinstance(products, list):
                continue
            
            for product in products:
                if isinstance(product, dict):
                    products_processed += 1
                    
                    if product.get('image_embedding'):
                        image_embeddings_found += 1
                    
                    if product.get('description_embedding'):
                        description_embeddings_found += 1
                        # The embedding is already a list, we just need to control JSON formatting
                        # This will be handled in the JSON writing with custom formatting
    
    # Write the updated data back to the file with custom formatting
    try:
        # Create backup
        backup_path = file_path + '.backup2'
        if os.path.exists(file_path):
            os.rename(file_path, backup_path)
            print(f"Created backup: {backup_path}")
        
        # Write updated data with custom formatting for embeddings
        write_formatted_json(data, file_path)
        
        print(f"\n✅ Successfully updated {file_path}")
        print(f"   Total products processed: {products_processed}")
        print(f"   Image embeddings reformatted: {image_embeddings_found}")
        print(f"   Description embeddings reformatted: {description_embeddings_found}")
        print(f"   Backup created: {backup_path}")
        
    except Exception as e:
        print(f"Error writing file: {e}")
        return False
    
    return True

def write_formatted_json(data, file_path):
    """
    Write JSON with custom formatting for embedding arrays
    """
    import re
    
    # First, write with normal formatting
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    
    # Use regex to find and reformat both image_embedding and description_embedding arrays
    # Pattern to match multi-line embedding arrays for both types
    image_pattern = r'"image_embedding":\s*\[\s*\n(\s*)([0-9e\-\.\,\s\n]+?)\n\s*\]'
    description_pattern = r'"description_embedding":\s*\[\s*\n(\s*)([0-9e\-\.\,\s\n]+?)\n\s*\]'
    
    def format_embedding_match(match, embedding_type="image_embedding"):
        # Extract the numbers and clean them up
        numbers_text = match.group(2)
        # Remove extra whitespace and newlines, split by comma
        numbers = []
        for line in numbers_text.split('\n'):
            line = line.strip()
            if line.endswith(','):
                line = line[:-1]  # Remove trailing comma
            if line:
                try:
                    numbers.append(float(line))
                except ValueError:
                    pass
        
        # Format as single line
        if numbers:
            formatted_numbers = ', '.join(str(num) for num in numbers)
            return f'"{embedding_type}": [{formatted_numbers}]'
        return f'"{embedding_type}": []'
    
    # Apply the formatting for image embeddings
    formatted_json = re.sub(image_pattern, 
                           lambda m: format_embedding_match(m, "image_embedding"), 
                           json_str, flags=re.MULTILINE)
    
    # Apply the formatting for description embeddings
    formatted_json = re.sub(description_pattern, 
                           lambda m: format_embedding_match(m, "description_embedding"), 
                           formatted_json, flags=re.MULTILINE)
    
    # Write the formatted JSON
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(formatted_json)

def main():
    """Main function"""
    print("Embedding Formatter")
    print("=" * 40)
    
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, 'product_data.json')
    
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found!")
        return
    
    # Process the file
    success = process_product_data(json_file)
    
    if success:
        print("\n🎉 Embedding formatting completed successfully!")
        print("Image and description embeddings are now formatted as comma-separated single lines!")
    else:
        print("\n❌ Embedding formatting failed!")

if __name__ == "__main__":
    main()
