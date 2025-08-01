# RAG/RAFT Document Generation for Zava Hardware Store

## Overview

This extension adds comprehensive unstructured document generation to the Zava Hardware Store database, making it suitable for **Retrieval-Augmented Generation (RAG)** and **Retrieval-Augmented Fine-Tuning (RAFT)** training scenarios.

## What's Added for RAG/RAFT

### 1. **Product Documentation** (`generate_product_documents.py`)
- **Product Manuals**: Detailed operation and installation guides
- **Customer Reviews**: Realistic reviews with ratings and feedback
- **FAQ Documents**: Common questions and answers for each product
- **Buying Guides**: Category-specific purchasing advice
- **Troubleshooting Guides**: Problem-solving documentation

### 2. **Safety & Compliance** (`generate_safety_docs.py`)
- **Safety Data Sheets (SDS)**: OSHA-compliant safety documentation
- **Compliance Certificates**: Standards compliance and testing results
- **Installation Safety Guidelines**: Safe installation procedures
- **Environmental Impact Statements**: Sustainability information

### 3. **Knowledge Base** (`generate_knowledge_base.py`)
- **How-To Tutorials**: Step-by-step project guides
- **Seasonal Maintenance**: Time-specific maintenance guides
- **Tool Safety Guidelines**: Comprehensive safety training content
- **Project Planning**: Complete project guides (kitchen renovation, deck building)

### 4. **Database Schema Enhancements**
```sql
-- New table for unstructured documents
CREATE TABLE retail.product_documents (
    document_id SERIAL PRIMARY KEY,
    product_id INTEGER,                    -- Links to specific products (optional)
    document_type TEXT NOT NULL,           -- Type: manual, review, faq, etc.
    title TEXT NOT NULL,                   -- Document title
    content TEXT NOT NULL,                 -- Full document content
    content_embedding vector(1536),        -- Text embeddings for semantic search
    metadata JSONB,                        -- Flexible metadata storage
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optimized indexes for RAG scenarios
CREATE INDEX idx_product_documents_type ON retail.product_documents(document_type);
CREATE INDEX idx_product_documents_metadata ON retail.product_documents USING GIN(metadata);
CREATE INDEX idx_product_documents_content_search ON retail.product_documents USING GIN(to_tsvector('english', content));
```

## Generated Content Statistics

When fully generated, the dataset includes:

- **🔢 ~1,500+ Documents** across multiple categories
- **📄 Document Types**: 8+ different types (manuals, reviews, safety docs, etc.)
- **📚 Content Volume**: ~2-5 MB of text content
- **🎯 Token Estimate**: ~500,000+ tokens for training
- **🔍 Search Ready**: Full-text search and semantic search capabilities

## Document Types Generated

| Type | Description | Count Range | Use Case |
|------|-------------|-------------|----------|
| `manual` | Product operation guides | 500+ | Installation and usage instructions |
| `reviews` | Customer feedback | 500+ | Real-world usage experiences |
| `faq` | Frequently asked questions | 500+ | Common customer inquiries |
| `safety_data_sheet` | OSHA-compliant safety docs | 200+ | Safety and compliance queries |
| `compliance_certificate` | Standards compliance | 200+ | Technical specifications |
| `how_to_guide` | Step-by-step tutorials | 50+ | DIY project guidance |
| `project_guide` | Complete project plans | 10+ | Complex project planning |
| `seasonal_guide` | Time-specific maintenance | 10+ | Seasonal maintenance advice |

## RAG/RAFT Training Scenarios

### 1. **Customer Service Chatbot**
```
Query: "How do I install a GFCI outlet safely?"
Retrieved: Installation guides, safety documents, tool requirements
Generated: Complete step-by-step installation instructions with safety warnings
```

### 2. **Product Recommendation System**
```
Query: "Best tools for kitchen renovation project"
Retrieved: Project guides, product reviews, buying guides
Generated: Personalized tool recommendations with reasoning
```

### 3. **Technical Support**
```
Query: "My circular saw is making unusual noises"
Retrieved: Product manuals, troubleshooting guides, safety information
Generated: Diagnostic steps and safety recommendations
```

### 4. **Seasonal Advice**
```
Query: "Preparing garden tools for winter storage"
Retrieved: Seasonal guides, maintenance manuals, storage tips
Generated: Comprehensive winterization checklist
```

## Quick Start

### 1. Generate Complete Database
```bash
# First, generate the base database
python data/database/generate_zava_postgres.py

# Then generate all documents for RAG/RAFT
python data/database/generate_all_documents.py
```

### 2. Generate Specific Document Types
```bash
# Product manuals, reviews, FAQs only
python data/database/generate_product_documents.py

# Safety and compliance documents only  
python data/database/generate_safety_docs.py

# Knowledge base articles only
python data/database/generate_knowledge_base.py
```

### 3. Query Examples
```sql
-- Find all installation guides
SELECT title, content FROM retail.product_documents 
WHERE document_type = 'manual' 
AND content ILIKE '%installation%';

-- Search by category
SELECT title FROM retail.product_documents 
WHERE metadata->>'category' = 'ELECTRICAL';

-- Full-text search
SELECT title, ts_rank(to_tsvector('english', content), query) as rank
FROM retail.product_documents, 
     to_tsquery('english', 'safety & installation') query
WHERE to_tsvector('english', content) @@ query
ORDER BY rank DESC;
```

## Integration with Existing Assets

### Product Images
- 🖼️ **400+ Product Images** in `/workspace/images/`
- 🔗 **Image Embeddings** already in `product_embeddings` table
- 🎯 **Multi-modal RAG**: Combine text and image search

### Structured Data
- 📊 **100,000+ Customers** with order history
- 🛍️ **1,000+ Products** with detailed specifications  
- 🏪 **Multiple Stores** with geographic distribution
- 💰 **Order Data** with seasonal patterns

## Advanced RAG Features

### 1. **Metadata-Driven Retrieval**
```python
# Retrieve documents by difficulty level
documents = query_documents(
    metadata_filter={"difficulty": "beginner"},
    content_query="power drill safety"
)
```

### 2. **Seasonal Context**
```python
# Get season-appropriate advice
import datetime
season = get_current_season()
documents = query_documents(
    metadata_filter={"season": season},
    document_types=["seasonal_guide", "project_guide"]
)
```

### 3. **Cross-Reference Capabilities**
```python
# Link products to their documentation
product_docs = query_documents(
    product_id=product_id,
    document_types=["manual", "reviews", "faq"]
)
```

## RAFT Training Preparation

### Document Chunking Strategy
- **Chunk Size**: 512-1024 tokens recommended
- **Overlap**: 50-100 tokens between chunks
- **Metadata Preservation**: Keep document type and category info

### Training Data Structure
```json
{
  "query": "How to safely install electrical outlets?",
  "context": [
    "Installation guide content...",
    "Safety documentation...", 
    "Code requirements..."
  ],
  "answer": "Step-by-step installation with safety precautions...",
  "metadata": {
    "categories": ["ELECTRICAL"],
    "document_types": ["manual", "safety_data_sheet"],
    "difficulty": "intermediate"
  }
}
```

## Vector Embedding Setup

The documents are ready for embedding generation. Recommended workflow:

1. **Extract Text Chunks**
```python
chunks = chunk_documents(
    documents=all_documents,
    chunk_size=512,
    overlap=50
)
```

2. **Generate Embeddings**
```python
embeddings = embedding_model.encode(
    [chunk.content for chunk in chunks]
)
```

3. **Store for Retrieval**
```sql
UPDATE retail.product_documents 
SET content_embedding = $1 
WHERE document_id = $2;
```

## Benefits for AI Training

### 1. **Realistic Domain Knowledge**
- Authentic hardware store terminology
- Industry-standard procedures
- Real-world problem scenarios

### 2. **Comprehensive Coverage**
- Product information across all categories
- Safety and compliance requirements
- Customer service scenarios
- Technical troubleshooting

### 3. **Structured Metadata**
- Easy filtering and categorization
- Difficulty level classification
- Seasonal and contextual tagging

### 4. **Scalable Architecture**
- Easy to add new document types
- Flexible metadata schema
- Optimized for vector search

## Future Enhancements

### Potential Additions
- **Video Transcripts**: Tutorial video content
- **Warranty Information**: Product warranty details
- **Supplier Catalogs**: Detailed supplier information
- **Code Requirements**: Local building code references
- **Customer Support Tickets**: Real support scenarios

### Advanced Features
- **Multi-language Support**: Documents in multiple languages
- **Dynamic Updates**: Real-time document updates
- **User Feedback**: Document rating and improvement
- **Personalization**: User-specific document recommendations

This dataset provides a solid foundation for training AI systems that can assist with hardware store operations, customer service, and technical support scenarios.
