# Zava DIY PostgreSQL Database Generator

This directory contains the PostgreSQL database generator for **Zava DIY**, a fictional home improvement retail company. The generator creates a comprehensive sales database with realistic retail data patterns, seasonal variations, and advanced features for data analysis and agentic applications.

## Quick Start

### How to Generate the Zava DIY PostgreSQL Database

To generate the complete Zava DIY PostgreSQL database:

```bash
# Navigate to the database directory
cd data/database

pip install -r requirements.txt

# Run the generator (creates complete database)
python generate_zava_postgres.py

# Or run with specific options
python generate_zava_postgres.py --show-stats          # Show database statistics
python generate_zava_postgres.py --embeddings-only     # Populate embeddings only
python generate_zava_postgres.py --verify-embeddings   # Verify embeddings table
python generate_zava_postgres.py --verify-seasonal     # Verify seasonal patterns
python generate_zava_postgres.py --clear-embeddings    # Clear existing embeddings
python generate_zava_postgres.py --batch-size 200      # Set embedding batch size
python generate_zava_postgres.py --num-customers 100000 # Set number of customers
python generate_zava_postgres.py --help                # Show all options
```

**Prerequisites:**

- PostgreSQL 17+ with pgvector extension
- Python 3.13+ with required packages (asyncpg, faker, python-dotenv)
- Required JSON data files: `product_data.json` and `reference_data.json`

### How to Generate the Zava DIY SQL Server Database

To generate the SQL Server compatible database schema and data:

```bash
# Navigate to the database directory
cd data/database
pip install -r requirements.txt
# Run the SQL Server generator
python generate_zava_sql_server.py
```

This will create a SQL Server compatible schema and populate it with the same data as the PostgreSQL version.

## Available Tools

This directory contains several utility tools for managing and working with the Zava DIY database:

### **Core Database Tools**

- **`generate_zava_postgres.py`** - Main database generator that creates the complete Zava DIY retail database with realistic sales data, seasonal patterns, and AI embeddings
- **`generate_zava_sql_server.py`** - Generates a SQL Server compatible database schema and data
- **`count_products.py`** - Analyzes and reports product counts across categories and embedding status from the JSON data files

### **Product Management Tools**

- **`add_product.py`** - Interactive CLI tool for adding new products to the `product_data.json` file with proper validation and formatting
- **`generate_skus.py`** - Generates and populates missing SKU codes for products using a standardized format (e.g., LBPLW001 for Lumber & Building Materials)

### **AI/ML and Embedding Tools**

- **`add_image_embeddings.py`** - Generates 512-dimensional image embeddings for product images using OpenAI CLIP-ViT-Base-Patch32 model
- **`add_description_embeddings.py`** - Creates 1536-dimensional text embeddings for product descriptions using Azure OpenAI text-embedding-3-small model
- **`query_by_description.py`** - Interactive search tool that finds products using natural language queries via semantic similarity search
- **`image_generation.py`** - Generates product images using Azure OpenAI DALL-E 3 and updates the JSON file with image paths

### **Data Management Tools**

- **`format_embeddings.py`** - Reformats embedding arrays in JSON files to use compact single-line formatting instead of multi-line arrays

### **Documentation**

- **`README_query_by_description.md`** - Detailed guide for using the semantic search functionality
- **`RLS_USER_GUIDE.md`** & **`row_level_security_guide.md`** - Documentation for Row-Level Security implementation and usage

### **Configuration Files**

- **`product_data.json`** - Complete product catalog with categories, seasonal multipliers, and AI embeddings
- **`reference_data.json`** - Store configurations, customer distribution weights, and business rules

## Overview

The database generator creates a complete retail ecosystem for Zava DIY, simulating a multi-store home improvement retailer with 8 locations across Washington State, including physical stores and online sales. The generated data supports advanced analytics, seasonal pattern analysis, multimodal AI applications with both image and text embeddings, and agentic applications.

## Generated Database Structure

### Available Users

#### 1. `postgres` (Superuser)

- **Username**: `postgres`
- **Password**: `P@ssw0rd!`
- **Privileges**: Superuser (bypasses Row level Security (RLS) by default)
- **Use case**: Database administration, schema creation, data generation
- **Created**: Automatically by PostgreSQL

#### 2. `store_manager` (Regular User)

- **Username**: `store_manager`
- **Password**: `StoreManager123!`
- **Privileges**: Regular user (RLS policies apply)
- **Use case**: Testing RLS policies, simulating application user access
- **Created**: Automatically by `init-db.sh` during database initialization

### Core Tables

#### **Customers** (`retail.customers`)

- **50,000+ customer records** with realistic demographic data
- Customer information: names, emails, phone numbers
- Primary store assignments based on geographic distribution

#### **Stores** (`retail.stores`)

- **8 retail locations** across Washington State:
  - Physical stores: Seattle, Bellevue, Tacoma, Spokane, Everett, Redmond, Kirkland
  - Online store: Zava Retail Online
- Each store has unique characteristics:
  - Customer distribution weights (traffic patterns)
  - Order frequency multipliers
  - Order value multipliers
- Row-Level Security (RLS) support for store manager access control

#### **Product Catalog** (`retail.categories`, `retail.product_types`, `retail.products`)

- **9 main product categories** with realistic home improvement inventory:
  - Hand Tools, Power Tools, Paint & Finishes, Hardware
  - Lumber & Building Materials, Electrical, Plumbing
  - Garden & Outdoor, Storage & Organization
- **Product hierarchy**: Categories → Product Types → Individual Products
- **Cost and pricing structure** with consistent 33% gross margin
- **Complete product specifications**: SKUs, descriptions, pricing

#### **Orders & Sales** (`retail.orders`, `retail.order_items`)

- **Historical transaction data** spanning 2020-2026
- **Order header** information: customer, store, date
- **Detailed line items**: products, quantities, prices, discounts
- **Variable order patterns** based on store characteristics and seasonality

#### **Inventory** (`retail.inventory`)

- **Store-specific stock levels** for all products
- **Seasonal inventory adjustments** based on demand patterns
- **Geographic distribution** reflecting local market preferences

#### **Product Image Embeddings** (`retail.product_image_embeddings`)

- **AI ready vector embeddings** for product images
- **512-dimensional vectors** using pgvector extension
- **Vector similarity search** capabilities for recommendation systems
- **Image metadata** and embedding relationships

#### **Product Description Embeddings** (`retail.product_description_embeddings`)

- **AI ready vector embeddings** for product descriptions
- **1536-dimensional vectors** using pgvector extension
- **Text-based similarity search** capabilities for recommendation systems
- **Enhanced product discovery** through semantic search

## Key Data Features

### 📊 Seasonal Variations

The generator implements **Washington State seasonal multipliers** for realistic business patterns:

#### **Hand Tools**

- **Peak season**: May-August (1.4-1.6x normal volume)
- **Low season**: December (0.9x normal volume)
- **Pattern**: Spring/summer home improvement surge

#### **Power Tools**

- **Peak season**: June-July (2.0-2.1x normal volume)
- **Low season**: December-February (0.8-0.9x normal volume)
- **Pattern**: Strong summer construction activity

#### **Paint & Finishes**

- **Peak season**: April (2.2x normal volume)
- **Strong season**: March-August (1.6-2.0x normal volume)
- **Pattern**: Spring painting season with sustained summer activity

#### **Lumber & Building Materials**

- **Peak season**: June-July (2.1-2.2x normal volume)
- **Low season**: November-February (0.7-0.8x normal volume)
- **Pattern**: Construction/renovation season alignment

#### **Garden & Outdoor**

- **Extreme seasonality**: 50% of normal volume in winter
- **Peak season**: Spring through early fall
- **Pattern**: Weather-dependent outdoor activity

### 💰 Financial Structure

#### **Margin Analysis**

- **Consistent 33% gross margin** across all products
- **Cost basis**: JSON price data represents wholesale cost
- **Selling price calculation**: Cost ÷ 0.67 = Retail Price
- **Margin verification**: Built-in reporting and validation

#### **Revenue Patterns**

- **Year-over-year growth**: Configurable growth patterns (2020-2026) with consistent business expansion
- **Growth trajectory**: Steady increases year-over-year, except for 2023 which shows a slight decline reflecting market conditions
- **Store performance variation**: Based on location and market size
- **Seasonal revenue fluctuations**: Aligned with product demand cycles

### 🏪 Store Performance Characteristics

#### **High-Performance Stores**

- **Seattle**: 30% customer distribution, 3.0x order frequency, 1.3x order value
- **Bellevue**: 25% customer distribution, 2.6x order frequency, 1.2x order value
- **Online**: 30% customer distribution, 3.0x order frequency, 1.5x order value

#### **Regional Stores**

- **Tacoma**: 20% customer distribution, 2.4x order frequency, 1.1x order value
- **Spokane**: 8% customer distribution, 2.0x order frequency, 1.0x order value

#### **Specialty/Smaller Markets**

- **Everett, Redmond, Kirkland**: Lower distribution weights with adjusted multipliers
- **Geographic clustering**: Realistic market penetration patterns

### 🔒 Security & Access Control

#### **Row-Level Security (RLS)**

- **Store manager isolation**: Each manager sees only their store's data
- **Super manager access**: UUID `00000000-0000-0000-0000-000000000000` bypasses all restrictions
- **Secure multi-tenancy**: Perfect for workshop and demo scenarios
- **Policy coverage**: Orders, order items, inventory, customers

#### **Manager Access Patterns**

- **Unique UUIDs** for each store manager
- **Complete data isolation** between stores
- **Controlled access** to reference data (products, categories)

### 🚀 Advanced Features

#### **Vector Search Capabilities**

- **pgvector integration** for similarity search
- **Product image embeddings** (512-dimensional) for visual recommendation engines
- **Product description embeddings** (1536-dimensional) for semantic text search
- **Optimized vector indexes** for performance
- **Dual embedding support** ready for multimodal ML applications

#### **Performance Optimization**

- **Comprehensive indexing strategy**: 20+ optimized indexes
- **Covering indexes** for common query patterns
- **Batch insert operations** for large data volumes
- **Query performance monitoring** and optimization

#### **Data Quality & Validation**

- **Built-in verification** routines for data consistency
- **Seasonal pattern validation** and reporting
- **Margin analysis** and financial reconciliation
- **Statistical summaries** and health checks

## Technical Requirements

- **PostgreSQL 17+** with pgvector extension
- **Python 3.13+** with asyncpg, faker, python-dotenv
- **Database**: `zava` with `retail` schema
- **Memory**: Recommended 4GB+ for large datasets
- **Storage**: ~2GB for complete database with embeddings

## Configuration Files

### `product_data.json`

- Complete product catalog with categories and types
- Seasonal multiplier coefficients for each category
- Product specifications, pricing, and descriptions
- Image embedding data for AI/ML applications

### `reference_data.json`

- Store configurations and performance characteristics
- Customer distribution weights by store
- Year-over-year growth patterns and multipliers
- Store manager RLS UUID mappings

## Data Volume Summary

| Component | Count | Description |
|-----------|-------|-------------|
| **Customers** | 50,000+ | Realistic demographic profiles across Washington State and online |
| **Products** | 400+ | Complete DIY home improvement catalog (tools, outdoor equipment, supplies) |
| **Product Images** | 400+ | Product images linked to database for image-based searches |
| **Stores** | 8 | Physical + online locations across Washington State |
| **Orders** | 200,000+ | Multi-year transaction history with detailed sales data |
| **Inventory Items** | 3,000+ | Store-specific inventory across multiple locations |
| **Image Embeddings** | 400+ | AI-powered image similarity searches using OpenAI CLIP-ViT-Base-Patch32 |
| **Description Embeddings** | 400+ | AI-powered text similarity searches using text-embedding-3-small |

This database provides a realistic foundation for retail analytics, machine learning experimentation, seasonal trend analysis, and multi-tenant application development in the home improvement industry. The database is powered by Azure Database for PostgreSQL flexible server with pgvector extension, enabling advanced AI-powered product similarity searches and comprehensive sales analytics.

## JSON Data File Schemas

The generator requires two JSON configuration files that define the product catalog and store configurations:

### `product_data.json` Schema

Defines the complete product catalog with embeddings and seasonal patterns:

```json
{
  "main_categories": {
    "<CATEGORY_NAME>": {
      "washington_seasonal_multipliers": [float, ...],  // 12 monthly multipliers (Jan-Dec)
      "<PRODUCT_TYPE>": [
        {
          "name": "string",                    // Product display name
          "sku": "string",                     // Unique product identifier
          "price": number,                     // Base cost price
          "description": "string",             // Product description
          "stock_level": number,               // Base inventory level
          "image_path": "string",              // Relative path to product image
          "image_embedding": [float, ...],     // 512-dimension image vector embedding
          "description_embedding": [float, ...] // 1536-dimension text vector embedding
        }
      ]
    }
  }
}
```

**Key Points:**

- `washington_seasonal_multipliers`: Optional 12-element array for seasonal demand patterns (January through December)
- `image_embedding`: 512-dimensional vector for image similarity search with pgvector
- `description_embedding`: 1536-dimensional vector for text similarity search with pgvector
- `price`: Treated as wholesale cost; retail price calculated with 33% gross margin
- Each category can contain multiple product types, each with an array of products

### `reference_data.json` Schema

Defines store configurations and business rules:

```json
{
  "stores": {
    "<STORE_NAME>": {
      "rls_user_id": "uuid",                  // Row Level Security identifier
      "customer_distribution_weight": number, // Relative customer allocation weight
      "order_frequency_multiplier": number,   // Order frequency scaling factor
      "order_value_multiplier": number        // Order value scaling factor
    }
  },
  "year_weights": {
    "<YEAR>": number                          // Growth pattern weights by year
  }
}
```

**Key Points:**

- `rls_user_id`: UUID for Row Level Security policies (store manager access control)
- Distribution weights: Control customer and sales allocation across stores
- Order multipliers: Scale order frequency and value by store characteristics
- Year weights: Create realistic business growth patterns over time (2020-2026)

### Database Connection Configuration

The generator connects to PostgreSQL using these default settings:

- **Host**: `db` (Docker container)
- **Port**: `5432`
- **Database**: `zava`
- **Schema**: `retail`
- **User**: `postgres`
- **Password**: `P@ssw0rd!`

Connection settings can be overridden using environment variables or a `.env` file.
