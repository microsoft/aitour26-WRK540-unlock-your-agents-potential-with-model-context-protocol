#!/usr/bin/env python3
"""
Product Query by Description CLI Tool

This tool allows you to search for products by providing a natural language description.
It generates an embedding for your query using Azure OpenAI and finds the most similar 
products in the database using pgvector cosine similarity.

Usage:
    python query_by_description.py

Requirements:
    - PostgreSQL with pgvector extension
    - Azure OpenAI configured
    - Product database with description embeddings populated

Example queries:
    - "waterproof electrical box for outdoor use"
    - "15 amp circuit breaker for residential"
    - "flexible conduit for electrical wiring"
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import asyncpg
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import AzureOpenAI


class ProductQueryTool:
    def __init__(self) -> None:
        """Initialize the product query tool."""
        # Load environment variables
        self._load_environment()
        
        # Azure OpenAI configuration
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "<ENDPOINT_URL>")
        self.model_name = "text-embedding-3-small"
        self.deployment = "text-embedding-3-small"
        
        # PostgreSQL configuration
        self.postgres_config = {
            'host': 'db',
            'port': 5432,
            'user': 'postgres',
            'password': 'P@ssw0rd!',
            'database': 'zava'
        }
        self.schema_name = 'retail'
        
        # Check if Azure OpenAI endpoint is configured
        if self.endpoint == "<ENDPOINT_URL>":
            print("Error: Please set the AZURE_OPENAI_ENDPOINT environment variable!")
            print("Example: export AZURE_OPENAI_ENDPOINT='https://your-openai-resource.openai.azure.com/'")
            sys.exit(1)
        
        # Initialize Azure OpenAI client
        try:
            self.openai_client = self._setup_azure_openai_client()
        except Exception as e:
            print(f"Failed to initialize Azure OpenAI client: {e}")
            sys.exit(1)
    
    def _load_environment(self) -> None:
        """Load environment variables from .env files."""
        script_dir = Path(__file__).parent
        # Try to load .env from script directory first, then parent directories
        env_paths = [
            script_dir / '.env',
            script_dir / '..' / '..' / '..' / '.env',  # Up to workspace root
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
    
    async def create_db_connection(self) -> asyncpg.Connection:
        """Create async PostgreSQL connection."""
        try:
            return await asyncpg.connect(**self.postgres_config)
        except Exception as e:
            print(f"Failed to connect to PostgreSQL: {e}")
            print("Make sure the database is running and accessible.")
            sys.exit(1)
    
    def generate_query_embedding(self, query_text: str) -> Optional[List[float]]:
        """
        Generate embedding for the user's query text.
        
        Args:
            query_text: The user's product description query
            
        Returns:
            List of float values representing the embedding
        """
        try:
            print(f"Generating embedding for query: '{query_text}'")
            
            # Generate embedding using Azure OpenAI
            response = self.openai_client.embeddings.create(
                input=[query_text],
                model=self.deployment
            )
            
            # Extract embedding from response
            embedding = response.data[0].embedding
            print(f"✓ Generated embedding (dimension: {len(embedding)})")
            return embedding
            
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    async def search_products_by_similarity(
        self, 
        conn: asyncpg.Connection, 
        query_embedding: List[float], 
        limit: int = 10
    ) -> List[Tuple]:
        """
        Search for products by similarity using pgvector cosine similarity.
        
        Args:
            conn: Database connection
            query_embedding: The query embedding vector
            limit: Maximum number of results to return
            
        Returns:
            List of tuples containing product information and similarity scores
        """
        try:
            print(f"Searching for {limit} most similar products...")
            
            # Convert embedding to string format for PostgreSQL
            embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
            
            # Query for similar products using cosine similarity
            query = f"""
                SELECT 
                    p.product_id,
                    p.product_name,
                    p.product_description,
                    p.base_price,
                    p.sku,
                    c.category_name,
                    pt.type_name,
                    (pe.description_embedding <=> $1::vector) as similarity_distance
                FROM {self.schema_name}.product_description_embeddings pe
                JOIN {self.schema_name}.products p ON pe.product_id = p.product_id
                JOIN {self.schema_name}.categories c ON p.category_id = c.category_id
                JOIN {self.schema_name}.product_types pt ON p.type_id = pt.type_id
                ORDER BY pe.description_embedding <=> $1::vector
                LIMIT $2
            """
            
            results = await conn.fetch(query, embedding_str, limit)
            print(f"✓ Found {len(results)} matching products")
            return results
            
        except Exception as e:
            print(f"Error searching for products: {e}")
            return []
    
    def display_results(self, results: List[Tuple]) -> None:
        """
        Display search results in a formatted manner.
        
        Args:
            results: List of product result tuples
        """
        if not results:
            print("No matching products found.")
            return
        
        print("\n" + "=" * 80)
        print("SEARCH RESULTS")
        print("=" * 80)
        
        for i, result in enumerate(results, 1):
            product_id, product_name, product_description, base_price, sku, category, product_type, similarity = result
            
            # Convert similarity distance to a percentage (lower distance = higher similarity)
            similarity_percent = max(0, (1 - similarity) * 100)
            
            print(f"\n{i}. {product_name}")
            print(f"   Category: {category} > {product_type}")
            print(f"   SKU: {sku}")
            print(f"   Price: ${base_price:.2f}")
            print(f"   Similarity: {similarity_percent:.1f}%")
            print(f"   Description: {product_description}")
            print("-" * 80)
    
    async def interactive_query(self) -> None:
        """Run the interactive query loop."""
        print("Product Search by Description")
        print("=" * 40)
        print("Enter product descriptions to find similar items.")
        print("Type 'quit', 'exit', or press Ctrl+C to exit.\n")
        
        # Create database connection
        conn = await self.create_db_connection()
        
        try:
            while True:
                try:
                    # Get user input
                    query_text = input("Enter product description: ").strip()
                    
                    # Check for exit commands
                    if query_text.lower() in ['quit', 'exit', 'q']:
                        print("Goodbye!")
                        break
                    
                    if not query_text:
                        print("Please enter a product description.")
                        continue
                    
                    # Generate embedding for the query
                    query_embedding = self.generate_query_embedding(query_text)
                    if not query_embedding:
                        print("Failed to generate embedding. Please try again.")
                        continue
                    
                    # Search for similar products
                    results = await self.search_products_by_similarity(conn, query_embedding)
                    
                    # Display results
                    self.display_results(results)
                    
                    print("\n" + "-" * 40)
                    
                except KeyboardInterrupt:
                    print("\n\nGoodbye!")
                    break
                except Exception as e:
                    print(f"An error occurred: {e}")
                    continue
        
        finally:
            await conn.close()


async def main() -> None:
    """Main function to run the product query tool."""
    try:
        tool = ProductQueryTool()
        await tool.interactive_query()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
