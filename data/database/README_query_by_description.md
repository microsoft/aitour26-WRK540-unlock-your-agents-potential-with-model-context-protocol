# Product Query by Description Tool

A simple CLI tool that allows you to search for products using natural language descriptions. The tool uses Azure OpenAI to generate embeddings and PostgreSQL with pgvector for similarity search.

## Features

- 🔍 **Natural Language Search**: Query products using everyday language
- 🧠 **AI-Powered Embeddings**: Uses Azure OpenAI text-embedding-3-small model
- 📊 **Similarity Scoring**: Shows how closely products match your query
- 🚀 **Fast Vector Search**: Leverages pgvector for efficient similarity search
- 💬 **Interactive CLI**: Easy-to-use command-line interface

## Prerequisites

1. **PostgreSQL with pgvector**: Database running with vector extension enabled
2. **Azure OpenAI**: Configured endpoint with text-embedding-3-small deployment
3. **Product Database**: Populated with products and description embeddings
4. **Python Dependencies**: asyncpg, azure-identity, openai, python-dotenv

## Setup

### 1. Environment Variables

Create a `.env` file or set these environment variables:

```bash
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
```

### 2. Database Setup

Ensure your PostgreSQL database has:
- The `retail` schema created
- Products populated in `retail.products` table
- Description embeddings in `retail.product_description_embeddings` table

You can populate the embeddings using:
```bash
python generate_zava_postgres.py --embeddings-only
```

### 3. Azure Authentication

The tool uses DefaultAzureCredential. Ensure you're authenticated via:
- Azure CLI: `az login`
- Environment variables
- Managed Identity (if running on Azure)

## Usage

### Basic Usage

```bash
python query_by_description.py
```

### Example Queries

Once the tool starts, you can enter queries like:

```
Enter product description: waterproof electrical box for outdoor use
Enter product description: 15 amp circuit breaker for residential
Enter product description: flexible conduit for electrical wiring
Enter product description: LED light bulbs energy efficient
Enter product description: electrical tape for wire connections
```

### Sample Output

```
Product Search by Description
========================================
Enter product descriptions to find similar items.
Type 'quit', 'exit', or press Ctrl+C to exit.

Enter product description: waterproof electrical box for outdoor use
Generating embedding for query: 'waterproof electrical box for outdoor use'
✓ Generated embedding (dimension: 1536)
Searching for 10 most similar products...
✓ Found 10 matching products

================================================================================
SEARCH RESULTS
================================================================================

1. Weatherproof Junction Box - Outdoor Rated
   Category: Electrical > Junction Boxes
   SKU: ELEC-JB-WP-001
   Price: $12.99
   Similarity: 94.2%
   Description: Heavy-duty weatherproof junction box designed for outdoor electrical connections...

2. Waterproof Electrical Enclosure
   Category: Electrical > Junction Boxes  
   SKU: ELEC-JB-WP-002
   Price: $18.50
   Similarity: 91.7%
   Description: NEMA rated waterproof enclosure for protecting electrical components outdoors...
```

## Testing

Test the embedding generation without a database connection:

```bash
python test_query_by_description.py
```

## Configuration

### Database Configuration

The tool connects to PostgreSQL with these default settings:
- Host: `db`
- Port: `5432`
- User: `postgres`
- Password: `P@ssw0rd!`
- Database: `zava`
- Schema: `retail`

Modify the `postgres_config` in the `ProductQueryTool` class to change these settings.

### Search Configuration

- **Default Results**: 10 products per query
- **Similarity Method**: Cosine similarity using pgvector `<=>` operator
- **Embedding Model**: text-embedding-3-small (1536 dimensions)

## Files

- `query_by_description.py` - Main CLI tool
- `test_query_by_description.py` - Test script for basic functionality
- `add_description_embeddings.py` - Tool to generate description embeddings
- `generate_zava_postgres.py` - Database generation with embedding support

## Troubleshooting

### Common Issues

1. **Azure OpenAI Connection Failed**
   - Check AZURE_OPENAI_ENDPOINT environment variable
   - Verify Azure authentication (`az login`)
   - Ensure text-embedding-3-small deployment exists

2. **Database Connection Failed**
   - Verify PostgreSQL is running
   - Check connection parameters
   - Ensure database and schema exist

3. **No Results Found**
   - Verify description embeddings are populated
   - Check that products exist in the database
   - Try different query terms

4. **Similarity Scores Low**
   - Product descriptions may not match query well
   - Try more specific or different terminology
   - Check embedding quality in the database

### Debug Commands

Check if embeddings exist:
```sql
SELECT COUNT(*) FROM retail.product_description_embeddings;
```

Verify products and categories:
```sql
SELECT c.category_name, COUNT(*) 
FROM retail.products p 
JOIN retail.categories c ON p.category_id = c.category_id 
GROUP BY c.category_name;
```

## Architecture

The tool consists of three main components:

1. **Embedding Generation**: Uses Azure OpenAI to convert text to vectors
2. **Vector Search**: Leverages pgvector for fast similarity search  
3. **Result Display**: Formats and presents matching products

The search pipeline:
1. User enters description → 2. Generate embedding → 3. Query database → 4. Return ranked results

## Contributing

To extend the tool:
- Add filters by category or price range
- Implement different similarity metrics
- Add export functionality for results
- Create web interface version
