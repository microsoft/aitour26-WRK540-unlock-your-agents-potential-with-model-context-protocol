#!/usr/bin/env python3
"""
Script to generate description embeddings for products in the product_data.json file.
Concatenates product name and description to create embeddings using Azure OpenAI.
This script is restartable - it will skip products that already have embeddings.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import AzureOpenAI


class DescriptionEmbeddingProcessor:
    def __init__(self, data_directory_path: str) -> None:
        """
        Initialize the description embedding processor.
        
        Args:
            data_directory_path: Path to the data directory containing product_data.json
        """
        self.data_directory_path = Path(data_directory_path)
        self.json_file_path = self.data_directory_path / "product_data.json"
        
        # Load environment variables
        self._load_environment()
        
        # Configuration
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "<ENDPOINT_URL>")
        self.model_name = "text-embedding-3-small"
        self.deployment = "text-embedding-3-small"
        
        # Check if endpoint is configured
        if self.endpoint == "<ENDPOINT_URL>":
            print("Error: Please set the AZURE_OPENAI_ENDPOINT environment variable!")
            print("Example: export AZURE_OPENAI_ENDPOINT='https://your-openai-resource.openai.azure.com/'")
            sys.exit(1)
        
        # Initialize Azure OpenAI client
        print("Setting up Azure OpenAI client...")
        try:
            self.client = self._setup_azure_openai_client()
            print("Azure OpenAI client initialized successfully!")
        except Exception as e:
            print(f"Failed to initialize Azure OpenAI client: {e}")
            sys.exit(1)
        
        # Load the product data
        self.load_product_data()
    
    def _load_environment(self) -> None:
        """Load environment variables from .env files."""
        script_dir = Path(__file__).parent
        # Try to load .env from script directory first, then parent directories
        env_paths = [
            script_dir / '.env'
        ]

        for env_path in env_paths:
            if env_path.exists():
                load_dotenv(env_path)
                break
        else:
            # Fallback to default behavior
            load_dotenv()
    
    def _setup_azure_openai_client(self) -> AzureOpenAI:
        """Setup and return Azure OpenAI client with token provider."""
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), 
            "https://cognitiveservices.azure.com/.default"
        )
        api_version = "2024-02-01"
        
        return AzureOpenAI(
            api_version=api_version,
            azure_endpoint=self.endpoint,
            azure_ad_token_provider=token_provider,
        )
    
    def load_product_data(self) -> None:
        """Load the product data from JSON file."""
        try:
            with self.json_file_path.open('r', encoding='utf-8') as f:
                self.product_data = json.load(f)
            print(f"Loaded product data from {self.json_file_path}")
        except FileNotFoundError:
            print(f"Error: Could not find {self.json_file_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file: {e}")
            sys.exit(1)
    
    def save_product_data(self) -> None:
        """Save the product data back to JSON file."""
        try:
            with self.json_file_path.open('w', encoding='utf-8') as f:
                json.dump(self.product_data, f, indent=2, ensure_ascii=False)
            
            print(f"Saved updated product data to {self.json_file_path}")
        except Exception as e:
            print(f"Error saving JSON file: {e}")
            sys.exit(1)
    
    def get_description_embedding(self, product_name: str, description: str) -> Optional[List[float]]:
        """
        Generate embedding for a product description.
        
        Args:
            product_name: Name of the product
            description: Description of the product
            
        Returns:
            List of float values representing the embedding
        """
        try:
            # Concatenate name and description
            combined_text = f"{product_name}. {description}"
            
            # Generate embedding using Azure OpenAI
            response = self.client.embeddings.create(
                input=[combined_text],
                model=self.deployment
            )
            
            # Extract embedding from response
            return response.data[0].embedding
            
        except Exception as e:
            print(f"Error generating embedding for {product_name}: {e}")
            return None
    
    def process_product(self, product: Dict[str, Any]) -> bool:
        """
        Process a single product to add description embedding.
        
        Args:
            product: Product dictionary
            
        Returns:
            True if embedding was added, False if skipped or failed
        """
        # Check if product already has a valid embedding (non-empty)
        if product.get('description_embedding'):
            print(f"Skipping {product.get('name', 'Unknown')} - already has embedding")
            return False
        
        # Check if product has name and description
        if 'name' not in product or 'description' not in product:
            print(f"Warning: {product.get('name', 'Unknown')} missing name or description")
            return False
        
        product_name = product['name']
        description = product['description']
        
        print(f"Processing: {product_name}")
        
        # Generate embedding
        embedding = self.get_description_embedding(product_name, description)
        
        if embedding is not None:
            product['description_embedding'] = embedding
            print(f"✓ Added embedding for {product_name} (dimension: {len(embedding)})")
            return True
        print(f"✗ Failed to generate embedding for {product_name}")
        return False
    
    def process_all_products(self) -> None:
        """Process all products in the JSON file to add description embeddings."""
        total_products = 0
        processed_products = 0
        skipped_products = 0
        failed_products = 0
        
        print("Starting description embedding processing...")
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
                    if product.get('description_embedding'):
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


def main() -> None:
    """Main function to run the description embedding processor."""
    # Get the directory of this script
    script_dir = Path(__file__).parent
    
    print("Description Embedding Processor for Product Data")
    print("=" * 50)
    print(f"Working directory: {script_dir}")
    
    # Verify we're in the right directory
    if not (script_dir / "product_data.json").exists():
        print("Error: product_data.json not found in current directory")
        print("Please run this script from the data/database directory")
        sys.exit(1)
    
    try:
        # Create processor and run
        processor = DescriptionEmbeddingProcessor(str(script_dir))
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
