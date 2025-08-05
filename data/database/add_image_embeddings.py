#!/usr/bin/env python3
"""
Script to add image embeddings to products in product_data.json file.
This script is restartable - it will skip products that already have embeddings.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import torch
    from PIL import Image
    from transformers import CLIPModel, CLIPProcessor
except ImportError as e:
    print(f"Error importing required packages: {e}")
    print("Please install the required packages:")
    print("pip install -r requirements_embeddings.txt")
    sys.exit(1)


class ImageEmbeddingProcessor:
    def __init__(self, data_generator_path: str):
        """
        Initialize the image embedding processor.
        
        Args:
            data_generator_path: Path to the data-generator directory
        """
        self.data_generator_path = Path(data_generator_path)
        self.json_file_path = self.data_generator_path / "product_data.json"
        # self.images_dir = self.data_generator_path / "images"
        self.images_dir = Path("/workspace/images")
        
        # Initialize the CLIP model and processor
        print("Initializing CLIP embedding model...")
        try:
            # Load CLIP model and processor from HuggingFace
            model_name = "openai/clip-vit-base-patch32"
            self.processor = CLIPProcessor.from_pretrained(model_name)
            self.model = CLIPModel.from_pretrained(model_name)
            
            # Set device (use CPU to avoid GPU complexity for now)
            self.device = "cpu"  # torch.device("cuda" if torch.cuda.is_available() else "cpu")
            # self.model = self.model.to(self.device)
            self.model.eval()
            
        except Exception as e:
            print(f"Failed to initialize CLIP model: {e}")
            raise e
        print("Model initialized successfully!")
        
        # Load the product data
        self.load_product_data()
    
    def load_product_data(self):
        """Load the product data from JSON file."""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                self.product_data = json.load(f)
            print(f"Loaded product data from {self.json_file_path}")
        except FileNotFoundError:
            print(f"Error: Could not find {self.json_file_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file: {e}")
            sys.exit(1)
    
    def save_product_data(self):
        """Save the product data back to JSON file with single-line embeddings."""
        try:
            # First, save with regular formatting
            with open(self.json_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.product_data, f, indent=2, ensure_ascii=False)
            
            # Then format the embeddings to be on single lines
            self._format_embeddings_single_line()
            
            print(f"Saved updated product data to {self.json_file_path}")
        except Exception as e:
            print(f"Error saving JSON file: {e}")
            sys.exit(1)
    
    def _format_embeddings_single_line(self):
        """Format all image_embedding arrays to be on single lines."""
        import re
        
        try:
            # Read the file content
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Pattern to match image_embedding arrays that span multiple lines
            pattern = r'"image_embedding":\s*\[\s*((?:[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?,?\s*)*)\s*\]'
            
            def format_embedding_array(match):
                """Format a single embedding array to be on one line."""
                # Extract the numbers from the match
                numbers_str = match.group(1)
                
                # Remove all whitespace and split by commas
                numbers = [num.strip() for num in numbers_str.split(',') if num.strip()]
                
                # Join the numbers with commas and single spaces
                formatted_numbers = ', '.join(numbers)
                
                # Return the formatted array
                return f'"image_embedding": [{formatted_numbers}]'
            
            # Apply the formatting
            formatted_content = re.sub(pattern, format_embedding_array, content, flags=re.DOTALL)
            
            # Write the formatted content back to the file
            with open(self.json_file_path, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
                
        except Exception as e:
            print(f"Warning: Failed to format embeddings to single line: {e}")
            # Continue anyway since the file was saved successfully
    
    def get_image_embedding(self, image_path: str) -> Optional[List[float]]:
        """
        Generate embedding for a single image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of float values representing the embedding
        """
        try:
            # Create full path to image
            # Remove "images/" prefix if it exists since we're already in the images directory
            if image_path.startswith("images/"):
                image_filename = image_path[7:]  # Remove "images/" prefix
            else:
                image_filename = image_path
            
            full_image_path = self.images_dir / image_filename
            
            if not full_image_path.exists():
                print(f"Warning: Image file not found: {full_image_path}")
                print(f"  Original path: {image_path}")
                print(f"  Looking for: {image_filename}")
                return None
            
            # Verify the image can be opened
            try:
                with Image.open(full_image_path) as img:
                    # Convert to RGB if necessary
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
            except Exception as img_error:
                print(f"Warning: Cannot open image {full_image_path}: {img_error}")
                return None
            
            # Generate embedding using CLIP model
            with Image.open(full_image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Process the image
                inputs = self.processor(images=img, return_tensors="pt")
                
                # Get image embeddings  
                with torch.no_grad():
                    image_features = self.model.get_image_features(pixel_values=inputs['pixel_values'])
                
                # Convert to numpy and then to list
                embedding = image_features.squeeze().cpu().numpy()
                embedding_list = embedding.tolist()
            
            return embedding_list
            
        except Exception as e:
            print(f"Error generating embedding for {image_path}: {e}")
            return None
    
    def process_product(self, product: Dict[str, Any]) -> bool:
        """
        Process a single product to add image embedding.
        
        Args:
            product: Product dictionary
            
        Returns:
            True if embedding was added, False if skipped or failed
        """
        # Check if product already has a valid embedding (non-empty)
        if product.get('image_embedding'):
            print(f"Skipping {product.get('name', 'Unknown')} - already has embedding")
            return False
        
        # Check if product has image_path
        if 'image_path' not in product:
            print(f"Warning: {product.get('name', 'Unknown')} has no image_path")
            return False
        
        image_path = product['image_path']
        product_name = product.get('name', 'Unknown')
        
        print(f"Processing: {product_name}")
        print(f"Image path: {image_path}")
        
        # Generate embedding
        embedding = self.get_image_embedding(image_path)
        
        if embedding is not None:
            product['image_embedding'] = embedding
            print(f"✓ Added embedding for {product_name} (dimension: {len(embedding)})")
            return True
        print(f"✗ Failed to generate embedding for {product_name}")
        return False
    
    def process_all_products(self):
        """Process all products in the JSON file to add image embeddings."""
        total_products = 0
        processed_products = 0
        skipped_products = 0
        failed_products = 0
        
        print("Starting image embedding processing...")
        print("=" * 50)
        
        # Iterate through all categories and subcategories
        for category_name, category_data in self.product_data.get('main_categories', {}).items():
            print(f"\nProcessing category: {category_name}")
            
            for subcategory_name, products in category_data.items():
                # Skip non-product items (like seasonal multipliers)
                if not isinstance(products, list):
                    continue
                
                print(f"  Subcategory: {subcategory_name} ({len(products)} products)")
                
                for product in products:
                    if not isinstance(product, dict):
                        continue
                    
                    total_products += 1
                    
                    # Check if already has a valid embedding (non-empty)
                    if product.get('image_embedding'):
                        skipped_products += 1
                        continue
                    
                    # Process the product
                    success = self.process_product(product)
                    
                    if success:
                        processed_products += 1
                        # Save after each successful embedding
                        self.save_product_data()
                        print(f"  → Saved progress ({processed_products} embeddings added)")
                    else:
                        print(f"  → Failed to process {product.get('name', 'Unknown')}")
                        failed_products += 1
        
        # Print summary
        print("\n" + "=" * 50)
        print("PROCESSING COMPLETE")
        print("=" * 50)
        print(f"Total products found: {total_products}")
        print(f"Products processed: {processed_products}")
        print(f"Products skipped (already had embeddings): {skipped_products}")
        print(f"Products failed: {failed_products}")
        print("Final save completed!")


def main():
    """Main function to run the image embedding processor."""
    # Get the directory of this script (should be in data-generator folder)
    script_dir = Path(__file__).parent
    
    print("Image Embedding Processor for Product Data")
    print("=" * 50)
    print(f"Working directory: {script_dir}")
    
    # Verify we're in the right directory
    if not (script_dir / "product_data.json").exists():
        print("Error: product_data.json not found in current directory")
        print("Please run this script from the data-generator directory")
        sys.exit(1)
    
    if not (Path("/workspace/images")).exists():
        print("Error: images directory not found")
        print("Please ensure the images directory exists in the data-generator folder")
        sys.exit(1)
    
    try:
        # Create processor and run
        processor = ImageEmbeddingProcessor(str(script_dir))
        processor.process_all_products()
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Progress has been saved.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
