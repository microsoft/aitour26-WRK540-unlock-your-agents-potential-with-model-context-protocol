#!/usr/bin/env python3
"""
Complete Document Generator for RAG/RAFT Dataset

This script generates a comprehensive set of unstructured documents suitable for 
Retrieval-Augmented Generation (RAG) and Retrieval-Augmented Fine-Tuning (RAFT):

1. Product manuals and installation guides
2. Customer reviews and Q&A
3. Safety data sheets and compliance documents  
4. How-to tutorials and project guides
5. Troubleshooting and maintenance guides
6. Knowledge base articles

All documents are designed to be realistic and comprehensive for training AI models
on hardware store knowledge and customer service scenarios.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

import asyncpg

# Add the current directory to the path so we can import our generators
sys.path.append(str(Path(__file__).parent))

from generate_knowledge_base import create_knowledge_base_documents
from generate_product_documents import create_documents_table, generate_and_insert_documents
from generate_safety_docs import generate_safety_documents

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# PostgreSQL connection configuration
POSTGRES_CONFIG = {
    'host': 'db',
    'port': 5432,
    'user': 'postgres',
    'password': 'P@ssw0rd!',
    'database': 'zava'
}

SCHEMA_NAME = 'retail'

async def main():
    """Generate all types of documents for RAG/RAFT training"""
    
    try:
        # Connect to database
        conn = await asyncpg.connect(**POSTGRES_CONFIG)
        logging.info("🔌 Connected to PostgreSQL database")
        
        # Verify the main tables exist
        tables_check = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = $1 
            AND table_name IN ('products', 'categories', 'product_types')
        """, SCHEMA_NAME)
        
        if len(tables_check) < 3:
            logging.error("❌ Required tables not found. Please run generate_zava_postgres.py first.")
            return
        
        # Check if documents table exists, create if not
        docs_table_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = $1 AND table_name = 'product_documents'
            )
        """, SCHEMA_NAME)
        
        if not docs_table_exists:
            logging.info("📄 Creating product_documents table...")
            await create_documents_table(conn)
        else:
            logging.info("📄 Product documents table already exists")
        
        # Get product count for progress tracking
        product_count = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.products")
        logging.info(f"📦 Found {product_count:,} products in database")
        
        # Clear existing documents (optional - comment out to append)
        existing_docs = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.product_documents")
        if existing_docs > 0:
            logging.info(f"🗑️  Found {existing_docs:,} existing documents")
            # Uncomment the next line to clear existing documents
            # await conn.execute(f"DELETE FROM {SCHEMA_NAME}.product_documents")
            # logging.info("🗑️  Cleared existing documents")
        
        # Generate documents in phases
        logging.info("🚀 Starting document generation process...")
        
        # Phase 1: Product-specific documents (manuals, reviews, FAQs)
        logging.info("📖 Phase 1: Generating product manuals, reviews, and FAQs...")
        await generate_and_insert_documents(conn, max_products=min(500, product_count))
        
        # Phase 2: Safety and compliance documents
        logging.info("🛡️  Phase 2: Generating safety data sheets and compliance documents...")
        await generate_safety_documents(conn, max_products=min(200, product_count))
        
        # Phase 3: Knowledge base articles and tutorials
        logging.info("🎓 Phase 3: Generating knowledge base articles and tutorials...")
        await create_knowledge_base_documents(conn)
        
        # Final statistics and summary
        await show_final_statistics(conn)
        
        logging.info("✅ Document generation completed successfully!")
        logging.info("🎯 Your database now contains comprehensive unstructured content for RAG/RAFT training")
        
        await conn.close()
        
    except Exception as e:
        logging.error(f"❌ Error in document generation: {e}")
        raise

async def show_final_statistics(conn: asyncpg.Connection):
    """Show comprehensive statistics about generated documents"""
    
    logging.info("\n" + "=" * 80)
    logging.info("📊 DOCUMENT GENERATION SUMMARY")
    logging.info("=" * 80)
    
    # Document type breakdown
    doc_types = await conn.fetch(f"""
        SELECT document_type, COUNT(*) as count, 
               ROUND(AVG(LENGTH(content))) as avg_length,
               MIN(LENGTH(content)) as min_length,
               MAX(LENGTH(content)) as max_length
        FROM {SCHEMA_NAME}.product_documents
        GROUP BY document_type
        ORDER BY count DESC
    """)
    
    total_docs = 0
    total_size = 0
    
    logging.info("\n📄 DOCUMENT TYPES:")
    logging.info("   Type                   Count    Avg Length    Min Length    Max Length")
    logging.info("   " + "-" * 75)
    
    for doc_type in doc_types:
        count = doc_type['count']
        avg_len = int(doc_type['avg_length']) if doc_type['avg_length'] else 0
        min_len = doc_type['min_length']
        max_len = doc_type['max_length']
        total_docs += count
        
        # Estimate total size for this type
        type_size = await conn.fetchval(f"""
            SELECT SUM(LENGTH(content)) FROM {SCHEMA_NAME}.product_documents 
            WHERE document_type = $1
        """, doc_type['document_type'])
        
        total_size += type_size or 0
        
        logging.info(f"   {doc_type['document_type']:<20} {count:>6}    {avg_len:>10,}    {min_len:>10,}    {max_len:>10,}")
    
    # Category distribution for product-specific documents
    logging.info("\n🏷️  DOCUMENTS BY CATEGORY:")
    category_stats = await conn.fetch(f"""
        SELECT 
            COALESCE(metadata->>'category', 'GENERAL') as category,
            COUNT(*) as count
        FROM {SCHEMA_NAME}.product_documents
        GROUP BY metadata->>'category'
        ORDER BY count DESC
    """)
    
    logging.info("   Category               Documents")
    logging.info("   " + "-" * 35)
    for cat in category_stats:
        logging.info(f"   {cat['category']:<20} {cat['count']:>6}")
    
    # Content statistics
    logging.info("\n📈 CONTENT STATISTICS:")
    content_stats = await conn.fetchrow(f"""
        SELECT 
            COUNT(*) as total_documents,
            SUM(LENGTH(content)) as total_characters,
            ROUND(AVG(LENGTH(content))) as avg_document_length,
            COUNT(DISTINCT product_id) as products_with_docs,
            COUNT(CASE WHEN product_id IS NULL THEN 1 END) as general_documents
        FROM {SCHEMA_NAME}.product_documents
    """)
    
    if content_stats:
        total_chars = content_stats['total_characters']
        total_words = total_chars // 5  # Rough estimate: 5 chars per word
        total_mb = total_chars / (1024 * 1024)
        
        logging.info(f"   Total Documents:       {content_stats['total_documents']:>10,}")
        logging.info(f"   Total Characters:      {total_chars:>10,}")
        logging.info(f"   Estimated Words:       {total_words:>10,}")
        logging.info(f"   Storage Size:          {total_mb:>10.2f} MB")
        logging.info(f"   Avg Document Length:   {int(content_stats['avg_document_length']):>10,} chars")
        logging.info(f"   Products with Docs:    {content_stats['products_with_docs']:>10,}")
        logging.info(f"   General Documents:     {content_stats['general_documents']:>10,}")
    
    # Sample document titles for verification
    logging.info("\n📋 SAMPLE DOCUMENT TITLES:")
    sample_docs = await conn.fetch(f"""
        SELECT document_type, title
        FROM {SCHEMA_NAME}.product_documents
        ORDER BY RANDOM()
        LIMIT 10
    """)
    
    for doc in sample_docs:
        title = doc['title']
        if len(title) > 60:
            title = title[:57] + "..."
        logging.info(f"   {doc['document_type']:<20} {title}")
    
    # RAG/RAFT suitability summary
    logging.info("\n🎯 RAG/RAFT TRAINING SUITABILITY:")
    logging.info("   ✅ Product Information:     Comprehensive product knowledge")
    logging.info("   ✅ Installation Guides:     Step-by-step instructions")  
    logging.info("   ✅ Safety Information:      Compliance and safety data")
    logging.info("   ✅ Customer Reviews:        Real-world usage feedback")
    logging.info("   ✅ Troubleshooting:         Problem-solving knowledge")
    logging.info("   ✅ How-To Guides:           Practical tutorials")
    logging.info("   ✅ Seasonal Content:        Time-sensitive information")
    logging.info("   ✅ Technical Specs:         Detailed product specifications")
    
    # Vector embedding readiness
    embedding_ready = await conn.fetchval(f"""
        SELECT COUNT(*) FROM {SCHEMA_NAME}.product_documents 
        WHERE content IS NOT NULL AND LENGTH(content) > 100
    """)
    
    logging.info(f"\n🔍 EMBEDDING READINESS:")
    logging.info(f"   Documents ready for embedding: {embedding_ready:,}")
    logging.info(f"   Recommended chunk size:        512-1024 tokens")
    logging.info(f"   Estimated chunks:              {total_words // 400:,} (assuming 400 words per chunk)")
    
    logging.info("\n🚀 NEXT STEPS:")
    logging.info("   1. Generate text embeddings for semantic search")
    logging.info("   2. Set up vector similarity indexes")
    logging.info("   3. Implement RAG pipeline with retrieval system")
    logging.info("   4. Fine-tune models using RAFT methodology")
    logging.info("   5. Test with hardware store question-answering scenarios")
    
    logging.info("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
