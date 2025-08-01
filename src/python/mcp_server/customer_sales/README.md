# Customer Sales MCP Servers

A collection of specialized Model Context Protocol (MCP) servers that provide customer-focused product search capabilities for Zava Retail DIY Business. These servers enable AI assistants to search and retrieve product information with Row Level Security (RLS) support for store-specific access.

## Available MCP Servers

This folder contains two MCP servers with different capabilities:

### 1. Customer Sales Server (`customer_sales.py`)
- **Purpose**: Basic product search using traditional name-based matching
- **Tools**: Product name search (`get_products_by_name`) and date utilities (`get_current_utc_date`)
- **Dependencies**: PostgreSQL only
- **Best for**: Simple product lookups and basic inventory queries

### 2. Customer Sales Semantic Search Server (`customer_sales_semantic_search.py`)
- **Purpose**: Advanced product search with AI-powered semantic capabilities
- **Tools**: Semantic search (`semantic_search_products`) and date utilities (`get_current_utc_date`)
- **Dependencies**: PostgreSQL + Azure OpenAI + text-embedding-3-small model
- **Best for**: Natural language product discovery and intelligent search

## Common Features

Both servers share these core capabilities:

- **Store-Specific Access**: Row Level Security ensures users only see products available in their store
- **Real-time Inventory**: Access current stock levels and product availability
- **Product Details**: Retrieve comprehensive product information including pricing, categories, and images
- **Flexible Deployment**: Supports both stdio and HTTP server modes
- **Optimized Performance**: Connection pooling and query optimization for fast responses

## Core Functionality

### Product Search Capabilities

Both servers provide intelligent product search capabilities with varying levels of sophistication:

#### Basic Server (`customer_sales.py`)
- **Name-based Search**: Search products by exact or partial name matches
- **Description Search**: Also searches within product descriptions for better coverage
- **Aggregated Results**: Combines inventory data across locations for total stock levels
- **Rich Product Data**: Returns product names, types, categories, pricing, and image URLs

#### Semantic Search Server (`customer_sales_semantic_search.py`)
- **Semantic Search**: AI-powered search using natural language descriptions with Azure OpenAI text-embedding-3-small model
- **Vector Similarity**: Uses pgvector cosine similarity for intelligent product matching
- **Relevance Scoring**: Returns similarity scores for ranking results by relevance
- **Rich Product Data**: Returns product names, types, categories, pricing, and image URLs

### Data Returned

For each product found, the server returns:

- **Product Name**: Full product name
- **Product Type**: Classification of the product type
- **Category**: Product category for organization
- **Price**: Current base price
- **Total Stock**: Aggregated stock levels across locations

## Tools Available

### Common Tools (Both Servers)

#### `get_current_utc_date`

Get the current UTC date and time in ISO format.

**Returns:** Current UTC date/time in ISO format (YYYY-MM-DDTHH:MM:SS.fffffZ)

**Use Cases:**

- Date-based inventory analysis
- Time-sensitive product searches
- Temporal context for customer interactions

### Basic Server Only

#### `get_products_by_name`

*Available only in `customer_sales.py`*

Search for products by name with comprehensive product details and inventory information.

**Parameters:**

- `product_name` (str): Name of the product to search for (supports partial matching)
- `max_rows` (int, optional): Maximum number of rows to return (default: 20). Limited to 100 for performance.

**Returns:** JSON-formatted query results containing:

- Product details (name, type, category, price)
- Product image URLs
- Aggregated stock levels
- Query metadata (row count, columns)

**Prompt Examples:**

- What paint does Zava sell?

### Semantic Search Server Only

#### `semantic_search_products`

*Available only in `customer_sales_semantic_search.py`*

Search for products using semantic similarity based on natural language descriptions. This tool uses AI embeddings to find products that match the meaning and intent of your description, even if the exact words don't appear in the product names.

**Parameters:**

- `query_description` (str): Natural language description to find products that Zava sells (e.g., "waterproof electrical box for outdoor use", "15 amp circuit breaker")
- `max_rows` (int, optional): Maximum number of rows to return (default: 10)
- `similarity_threshold` (float, optional): Minimum similarity threshold (0-100) to consider a product a match (default: 50.0)

**Returns:** JSON-formatted query results with similarity scores containing:

- Product details (name, type, category, price)
- Product image URLs
- Aggregated stock levels
- Similarity scores for relevance ranking
- Query metadata (row count, columns)

**Prompt Examples:**

- What guns does Zava sell for spray painting?

**Dependencies:**

- **Azure OpenAI**: Requires configured Azure OpenAI endpoint
- **Text Embeddings Model**: Uses `text-embedding-3-small` deployment
- **Environment Variables**: `AZURE_OPENAI_ENDPOINT` must be configured

## Security Features

### Row Level Security (RLS)

The server implements Row Level Security to ensure customers and staff only access products available in their specific store location:

- **HTTP Mode**: Uses `x-rls-user-id` header to identify the requesting user/store
- **Stdio Mode**: Uses `--RLS_USER_ID` command line argument
- **Default Fallback**: Uses placeholder UUID when no user ID is provided

#### Store-Specific RLS User IDs

Each Zava Retail store location has a unique RLS user ID that determines which products are visible:

| Store Location | RLS User ID | Access Level |
|---------------|-------------|--------------|
| **Global Access** | `00000000-0000-0000-0000-000000000000` | Limited product visibility |
| **Seattle** | `f47ac10b-58cc-4372-a567-0e02b2c3d479` | Seattle store product catalog |
| **Bellevue** | `6ba7b810-9dad-11d1-80b4-00c04fd430c8` | Bellevue store product catalog |
| **Tacoma** | `a1b2c3d4-e5f6-7890-abcd-ef1234567890` | Tacoma store product catalog |
| **Spokane** | `d8e9f0a1-b2c3-4567-8901-234567890abc` | Spokane store product catalog |
| **Everett** | `3b9ac9fa-cd5e-4b92-a7f2-b8c1d0e9f2a3` | Everett store product catalog |
| **Redmond** | `e7f8a9b0-c1d2-3e4f-5678-90abcdef1234` | Redmond store product catalog |
| **Kirkland** | `9c8b7a65-4321-fed0-9876-543210fedcba` | Kirkland store product catalog |
| **Online** | `2f4e6d8c-1a3b-5c7e-9f0a-b2d4f6e8c0a2` | Online store product catalog |

#### RLS Implementation

When a user connects with a specific store's RLS User ID, they will see:

- Products available in that store's inventory
- Store-specific pricing and stock levels
- Products relevant to that store's customer base
- Localized product recommendations

## Installation & Setup

### Prerequisites

- Docker
- VS Code with DevContainer extension

### Opening the Project

1. Open the project in VS Code.
2. If prompted, reopen in a DevContainer to ensure all dependencies are available.

### Basic Configuration (Both Servers)

The project uses the same `.env` file configuration for both MCP servers:

```properties
# Default Group Access ID
RLS_USER_ID="00000000-0000-0000-0000-000000000000" 

# Store-specific RLS User IDs
# Zava Retail Seattle
# RLS_USER_ID="f47ac10b-58cc-4372-a567-0e02b2c3d479"

# Zava Retail Bellevue  
# RLS_USER_ID="6ba7b810-9dad-11d1-80b4-00c04fd430c8"

# Zava Retail Online
# RLS_USER_ID="2f4e6d8c-1a3b-5c7e-9f0a-b2d4f6e8c0a2"
# ... (additional store configurations)
```

### Azure OpenAI Configuration (Semantic Search Server Only)

For semantic search functionality in `customer_sales_semantic_search.py`, configure Azure OpenAI:

```properties
# Azure OpenAI Endpoint for semantic search (required for semantic_search_products tool)
AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"

# Text Embeddings Model Configuration
# Uses text-embedding-3-small deployment by default
# Ensure the deployment name matches the model configuration in customer_sales_semantic_search_text_embeddings.py
```

**Note**: If `AZURE_OPENAI_ENDPOINT` is not configured, the semantic search server will disable semantic functionality but traditional name-based search will still work.

### Database Configuration

```properties
# PostgreSQL connection (provided via Docker environment variables)
POSTGRES_URL="postgresql://store_manager:StoreManager123!@db:5432/zava"
```

## Usage

The following assumes you'll be using the built-in VS Code MCP server support.

### Choosing Which Server to Use

#### Use Basic Server (`customer_sales.py`) when:
- You need traditional name-based product search functionality
- Azure OpenAI is not available or not configured
- You want minimal dependencies and faster startup
- Simple product lookups by name are sufficient

#### Use Semantic Search Server (`customer_sales_semantic_search.py`) when:
- You want AI-powered natural language product search
- Azure OpenAI is available and configured
- Users need to describe products without knowing exact names
- Advanced product discovery using semantic similarity is required
- Traditional name-based search is not needed

### Running the Basic Server in Stdio Mode

Start the **zava-customer-sales-stdio** server using the `.vscode/mcp.json` configuration:

```json
{
    "servers": {
        "zava-customer-sales-stdio": {
            "type": "stdio",
            "command": "python",
            "args": [
                "${workspaceFolder}/src/python/mcp_server/customer_sales/customer_sales.py",
                "--stdio",
                "--RLS_USER_ID=00000000-0000-0000-0000-000000000000"
            ]
        }
    },
    "inputs": []
}
```

### Running the Semantic Search Server in Stdio Mode

Start the **zava-customer-sales-semantic-stdio** server using the `.vscode/mcp.json` configuration:

```json
{
    "servers": {
        "zava-customer-sales-semantic-stdio": {
            "type": "stdio",
            "command": "python",
            "args": [
                "${workspaceFolder}/src/python/mcp_server/customer_sales/customer_sales_semantic_search.py",
                "--stdio",
                "--RLS_USER_ID=00000000-0000-0000-0000-000000000000"
            ]
        }
    },
    "inputs": []
}
```

### Running Servers in HTTP Mode

Both servers support HTTP mode for streamable responses:

#### Basic Server
```bash
cd src/python/mcp_server/customer_sales/ 
python customer_sales.py
```

#### Semantic Search Server
```bash
cd src/python/mcp_server/customer_sales/ 
python customer_sales_semantic_search.py
```

### Complete MCP Configuration Example

```json
{
    "servers": {
        "zava-sales-analysis-stdio": {
            "type": "stdio",
            "command": "python",
            "args": [
                "${workspaceFolder}/src/python/mcp_server/sales_analysis/sales_analysis.py",
                "--stdio",
                "--RLS_USER_ID=00000000-0000-0000-0000-000000000000"
            ]
        },
        "zava-customer-sales-stdio": {
            "type": "stdio",
            "command": "python",
            "args": [
                "${workspaceFolder}/src/python/mcp_server/customer_sales/customer_sales.py",
                "--stdio",
                "--RLS_USER_ID=00000000-0000-0000-0000-000000000000"
            ]
        },
        "zava-customer-sales-semantic-stdio": {
            "type": "stdio",
            "command": "python",
            "args": [
                "${workspaceFolder}/src/python/mcp_server/customer_sales/customer_sales_semantic_search.py",
                "--stdio",
                "--RLS_USER_ID=00000000-0000-0000-0000-000000000000"
            ]
        },
        "zava-diy-http": {
            "url": "http://127.0.0.1:8000/mcp",
            "type": "http"
        }
    },
    "inputs": []
}

## Sample Queries

### Basic Server Queries (`customer_sales.py`)
1. What paint products are available from Zava?
2. Is there paint in stock at the Seattle store?
3. Show me all drill bits available

### Semantic Search Server Queries (`customer_sales_semantic_search.py`)

#### AI-Powered Semantic Search Examples
1. "I need something to protect electrical connections outdoors"
2. "What do you have for cutting metal pipes?"
3. "I'm looking for something to connect two pieces of wire safely"
4. "waterproof electrical box for outdoor use"
5. "15 amp circuit breaker for home electrical panel"
6. "something to hang heavy pictures on drywall"
7. "tools for measuring electrical current"

## Architecture

### Application Context

Both servers use a managed application context with:

- **Database Connection Pool**: Efficient connection management for concurrent requests
- **Lifecycle Management**: Proper resource cleanup on shutdown
- **Type Safety**: Strongly typed context with `AppContext` dataclass

#### Basic Server Context
```python
@dataclass
class AppContext:
    db: PostgreSQLCustomerSales
```

#### Semantic Search Server Context
```python
@dataclass
class AppContext:
    db: PostgreSQLCustomerSales
    semantic_search: SemanticSearchTextEmbedding
```

### Database Integration

Both servers integrate with PostgreSQL through the `PostgreSQLCustomerSales` class:

- **Connection Pooling**: Configurable async connection pools (1-3 connections)
- **Query Optimization**: Optimized queries with joins for comprehensive product data
- **Resource Management**: Conservative memory usage and connection timeouts
- **RLS Integration**: Automatic Row Level Security configuration per request

### Query Performance

The database layer includes several optimizations:

- **Connection Pooling**: Min 1, Max 3 connections to balance performance and resource usage
- **Query Timeouts**: 30-second timeouts to prevent hanging requests
- **Memory Limits**: 4MB work memory per query to control resource usage
- **JIT Disabled**: Reduces memory overhead for better performance

## Database Schema Integration

### Tables Accessed

The server queries the following retail database tables:

- `retail.products` - Main product information
- `retail.product_types` - Product type classifications
- `retail.categories` - Product categories
- `retail.inventory` - Stock levels and availability
- `retail.product_image_embeddings` - Product images and metadata; also stores AI embeddings for semantic search

### Query Structure

#### Basic Server Query Processing

The main product search query performs:

1. **Multi-table Joins**: Combines product, type, category, inventory, and embedding data
2. **Fuzzy Matching**: Uses ILIKE for partial name and description matching
3. **Aggregation**: Sums stock levels across multiple inventory records
4. **Ordering**: Results ordered by product name for consistency
5. **Limiting**: Configurable result limits for performance

#### Semantic Search Server Additional Processing

The semantic search query additionally performs:

1. **Embedding Generation**: Converts natural language queries to vector embeddings using Azure OpenAI
2. **Vector Similarity**: Uses pgvector cosine similarity to find semantically similar products
3. **Similarity Scoring**: Returns relevance scores (0-100) for ranking results
4. **Threshold Filtering**: Configurable similarity thresholds to control result quality

## Error Handling

The server implements comprehensive error handling:

- **Connection Management**: Graceful handling of database connection issues
- **Query Validation**: Safe parameter binding to prevent SQL injection
- **Resource Cleanup**: Proper connection release even during errors
- **User-Friendly Responses**: Clear error messages in JSON format
- **Fallback Handling**: Graceful degradation when no results found

## Example Usage Scenarios

### Customer Product Search

```python
# Customer looking for paint products
results = await get_products_by_name(
    product_name="paint",
    max_rows=20
)
# Returns: paint types, prices, stock levels, images
```

### Store Associate Assistance

```python
# Store associate helping customer find specific item
results = await get_products_by_name(
    product_name="electrical outlet",
    max_rows=15
)
# Returns: outlet types, categories, availability, pricing
```

### Inventory Check

```python
# Quick inventory check for specific product
results = await get_products_by_name(
    product_name="drill bit set",
    max_rows=5
)
# Returns: available drill bit sets with stock levels
```

### Semantic Product Discovery

```python
# Customer describing what they need without knowing exact product names
results = await semantic_search_products(
    query_description="something to protect outdoor electrical connections from weather",
    max_rows=10,
    similarity_threshold=60.0
)
# Returns: weatherproof boxes, outdoor outlets, protective covers with similarity scores
```

## Security Considerations

1. **Row Level Security**: All queries respect RLS policies based on store identity
2. **Store Data Isolation**: Each store sees only relevant product inventory
3. **Input Sanitization**: All user inputs are safely parameterized in queries
4. **Resource Limits**: Query timeouts and connection limits prevent abuse
5. **Connection Security**: Secure database connection practices
6. **User Identity Verification**: Always verify correct RLS User ID for intended store

### Important Security Notes

- **Store-Specific Access**: Each RLS User ID provides access only to that store's products
- **Customer Privacy**: Product searches are isolated by store location
- **Inventory Security**: Stock levels shown only for authorized store locations
- **Production Safety**: Never use production RLS User IDs in development environments

## Development

### Project Structure

```text
customer_sales/
├── customer_sales.py                                 # Basic MCP server with name-based search
├── customer_sales_semantic_search.py                 # Enhanced MCP server with semantic search
├── customer_sales_postgres.py                        # PostgreSQL integration layer (shared)
├── customer_sales_semantic_search_text_embeddings.py # Azure OpenAI embeddings integration
└── README.md                                         # This documentation
```

### Key Components

#### Basic Server (`customer_sales.py`)
- **FastMCP Server**: Modern MCP server with async support and lifecycle management
- **PostgreSQL Provider**: Specialized database layer for product search operations
- **Context Management**: Type-safe application and request context handling
- **Tool Registration**: Declarative tool registration with Pydantic validation

#### Semantic Search Server (`customer_sales_semantic_search.py`)
- **FastMCP Server**: Modern MCP server with async support and lifecycle management
- **PostgreSQL Provider**: Specialized database layer for semantic product search operations
- **Semantic Search Engine**: Azure OpenAI text-embedding-3-small integration for AI-powered product discovery
- **Vector Database Integration**: pgvector support for similarity search
- **Embedding Management**: Text-to-vector conversion and similarity scoring
- **Context Management**: Type-safe application and request context handling
- **Tool Registration**: Declarative tool registration with Pydantic validation

### Testing

Both servers include built-in testing capabilities:

#### Basic Server Testing
```bash
# Test the database connection and search functionality
python customer_sales_postgres.py
```

#### Semantic Search Server Testing
```bash
# Test basic database functionality
python customer_sales_postgres.py

# Test semantic search functionality (requires Azure OpenAI configuration)
python customer_sales_semantic_search_text_embeddings.py
```

## Contributing

When contributing to these servers:

1. Ensure all database queries respect Row Level Security policies
2. Add proper error handling and input validation for new features
3. Update this README with any new functionality or changes
4. Test both stdio and HTTP server modes thoroughly
5. Validate product search results across different store locations
6. Maintain query performance and resource usage limits
7. For semantic search features, ensure Azure OpenAI integration is robust and includes fallback handling

### Server-Specific Considerations

#### Basic Server
- Focus on query performance and minimal dependencies
- Ensure compatibility across different environments
- Maintain simple, reliable functionality

#### Semantic Search Server
- Test with and without Azure OpenAI configuration
- Validate embedding generation and similarity scoring
- Ensure graceful degradation when AI services are unavailable
- Monitor vector database performance and similarity thresholds

## Use Cases

These MCP servers are ideal for different scenarios:

### Basic Server (`customer_sales.py`)
- **Simple Product Lookups**: Quick name-based product searches
- **Lightweight Deployments**: Environments with minimal dependencies
- **Basic Inventory Management**: Simple product lookup and availability checking by name
- **Development/Testing**: Quick setup without external AI services
- **High-Performance Requirements**: Minimal latency for basic name-based searches

### Semantic Search Server (`customer_sales_semantic_search.py`)
- **AI-Powered Customer Service**: Help customers find products using natural language descriptions
- **Intelligent Product Discovery**: Enable customers to describe what they need without knowing exact product names
- **Advanced E-commerce Integration**: Power sophisticated semantic product search in online stores
- **Conversational Commerce**: Enable AI assistants to help with complex product inquiries using descriptions
- **Smart Inventory Assistance**: Help store associates find products based on customer descriptions

### Common Use Cases (Both Servers)
- **Store Associate Tools**: Assist staff in locating inventory and product details
- **Customer Chat Bots**: Enable AI assistants to help with product inquiries
- **Real-time Inventory**: Quick product lookup and availability checking
- **Multi-store Operations**: Store-specific product catalogs with RLS security

## License

[Include appropriate license information]

---

*These MCP servers enable flexible, secure product search capabilities for Zava Retail customers and staff across all store locations, with options ranging from simple name-based search to advanced AI-powered semantic discovery.*
