#!/usr/bin/env python3
"""
Product SKU Generator and Populator

This script generates and adds missing SKU properties to products in product_data.json.
SKUs are generated based on category, product type, and a unique number.

SKU Format: {CATEGORY_CODE}{TYPE_CODE}{NUMBER:03d}
Example: LBPLW001 (Lumber & Building Materials, Plywood, 001)

USAGE:
    python generate_skus.py [--dry-run] [--backup] [--verbose]
"""

import json
import os
import re
import shutil
import argparse
import logging
from datetime import datetime
from collections import defaultdict
from typing import Dict


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def create_backup(file_path: str) -> str:
    """Create a backup of the original file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{file_path}.backup_{timestamp}"
    shutil.copy2(file_path, backup_path)
    logging.info(f"Created backup: {backup_path}")
    return backup_path


def generate_category_code(category: str) -> str:
    """
    Generate a 2-character category code from category name.
    
    Examples:
    - HAND TOOLS -> HT
    - LUMBER & BUILDING MATERIALS -> LB
    - STORAGE & ORGANIZATION -> SO
    """
    # Clean up category name
    clean_category = category.upper().replace('&', 'AND')
    words = clean_category.split()
    
    if len(words) == 1:
        # Single word: take first 2 characters
        return words[0][:2]
    elif len(words) == 2:
        # Two words: take first character of each
        return words[0][0] + words[1][0]
    else:
        # Multiple words: take first character of first two significant words
        significant_words = [w for w in words if w not in ['AND', 'THE', 'OF', 'FOR']]
        if len(significant_words) >= 2:
            return significant_words[0][0] + significant_words[1][0]
        else:
            return words[0][0] + words[1][0]


def generate_type_code(product_type: str) -> str:
    """
    Generate a 2-3 character type code from product type.
    
    Examples:
    - HAMMERS -> HAM
    - SCREWDRIVERS -> SCR
    - PLYWOOD -> PLY
    """
    # Remove special characters and spaces
    clean_type = re.sub(r'[^A-Z]', '', product_type.upper())
    
    if len(clean_type) <= 3:
        return clean_type
    elif len(clean_type) <= 6:
        # Short type: take first 3 characters
        return clean_type[:3]
    else:
        # Long type: take first letter + next 2 consonants
        consonants = ''.join([c for c in clean_type[1:] if c not in 'AEIOU'])
        if len(consonants) >= 2:
            return clean_type[0] + consonants[:2]
        else:
            return clean_type[:3]


def generate_sku(category: str, product_type: str, number: int) -> str:
    """Generate a complete SKU"""
    category_code = generate_category_code(category)
    type_code = generate_type_code(product_type)
    return f"{category_code}{type_code}{number:03d}"


def collect_existing_skus(product_data: Dict) -> set:
    """Collect all existing SKUs to avoid duplicates"""
    existing_skus = set()
    
    for category_name, category_data in product_data.get('main_categories', {}).items():
        for product_type, products in category_data.items():
            if not isinstance(products, list):
                continue
                
            for product in products:
                if isinstance(product, dict):
                    sku = product.get('sku')
                    if sku:
                        existing_skus.add(sku)
    
    logging.info(f"Found {len(existing_skus)} existing SKUs")
    return existing_skus


def analyze_missing_skus(product_data: Dict) -> Dict:
    """Analyze which products need SKUs"""
    stats = {
        'total_products': 0,
        'missing_skus': 0,
        'has_skus': 0,
        'categories_needing_skus': defaultdict(list)
    }
    
    for category_name, category_data in product_data.get('main_categories', {}).items():
        for product_type, products in category_data.items():
            if not isinstance(products, list):
                continue
                
            for i, product in enumerate(products):
                if isinstance(product, dict):
                    stats['total_products'] += 1
                    sku = product.get('sku')
                    
                    if sku:
                        stats['has_skus'] += 1
                    else:
                        stats['missing_skus'] += 1
                        stats['categories_needing_skus'][f"{category_name}/{product_type}"].append({
                            'index': i,
                            'name': product.get('name', f'Product {i+1}')
                        })
    
    return stats


def generate_and_assign_skus(product_data: Dict, dry_run: bool = False) -> Dict:
    """Generate and assign SKUs to products that don't have them"""
    existing_skus = collect_existing_skus(product_data)
    sku_counters = defaultdict(int)
    assignment_log = []
    
    stats = {
        'skus_generated': 0,
        'skus_assigned': 0,
        'conflicts_resolved': 0
    }
    
    for category_name, category_data in product_data.get('main_categories', {}).items():
        for product_type, products in category_data.items():
            if not isinstance(products, list):
                continue
            
            category_type_key = f"{category_name}/{product_type}"
            
            for i, product in enumerate(products):
                if isinstance(product, dict) and not product.get('sku'):
                    # Generate SKU
                    sku_counters[category_type_key] += 1
                    base_sku = generate_sku(category_name, product_type, sku_counters[category_type_key])
                    
                    # Ensure uniqueness
                    final_sku = base_sku
                    counter = 1
                    while final_sku in existing_skus:
                        stats['conflicts_resolved'] += 1
                        # If conflict, try with incremented number
                        sku_counters[category_type_key] += 1
                        final_sku = generate_sku(category_name, product_type, sku_counters[category_type_key])
                        counter += 1
                        if counter > 1000:  # Safety break
                            logging.error(f"Could not generate unique SKU for {category_type_key}")
                            break
                    
                    # Record the assignment
                    assignment_log.append({
                        'category': category_name,
                        'product_type': product_type,
                        'product_index': i,
                        'product_name': product.get('name', 'Unknown'),
                        'generated_sku': final_sku
                    })
                    
                    # Assign the SKU (unless dry run)
                    if not dry_run:
                        product['sku'] = final_sku
                        stats['skus_assigned'] += 1
                    
                    existing_skus.add(final_sku)
                    stats['skus_generated'] += 1
                    
                    logging.debug(f"Generated SKU: {final_sku} for {product.get('name', 'Unknown')}")
    
    return {
        'stats': stats,
        'assignments': assignment_log
    }


def save_product_data(product_data: Dict, file_path: str) -> None:
    """Save the updated product data back to JSON file"""
    try:
        with open(file_path, 'w') as f:
            json.dump(product_data, f, indent=2)
        logging.info(f"Updated product data saved to {file_path}")
    except Exception as e:
        logging.error(f"Error saving product data: {e}")
        raise


def print_assignment_report(results: Dict, dry_run: bool = False) -> None:
    """Print a detailed report of SKU assignments"""
    stats = results['stats']
    assignments = results['assignments']
    
    print("\n" + "=" * 80)
    print("SKU GENERATION REPORT")
    print("=" * 80)
    
    if dry_run:
        print("🔍 DRY RUN MODE - No changes were made to the file")
    else:
        print("✅ SKUs have been generated and assigned")
    
    print("\nSTATISTICS:")
    print(f"  SKUs generated: {stats['skus_generated']}")
    if not dry_run:
        print(f"  SKUs assigned: {stats['skus_assigned']}")
    print(f"  Conflicts resolved: {stats['conflicts_resolved']}")
    
    if assignments:
        print("\nSKU ASSIGNMENTS BY CATEGORY:")
        print("-" * 80)
        
        current_category = None
        for assignment in assignments:
            category_type = f"{assignment['category']}/{assignment['product_type']}"
            
            if category_type != current_category:
                print(f"\n{category_type}:")
                current_category = category_type
            
            print(f"  • {assignment['generated_sku']} -> {assignment['product_name'][:60]}")
    
    print("\n" + "=" * 80)


def load_product_data(file_path: str) -> Dict:
    """Load product data from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"product_data.json not found at {file_path}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing product_data.json: {e}")
        raise


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate and assign SKUs to products missing them',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--backup', action='store_true', default=True,
                       help='Create backup before making changes (default: True)')
    parser.add_argument('--no-backup', action='store_true',
                       help='Skip creating backup')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--file', default='product_data.json',
                       help='Path to product data JSON file (default: product_data.json)')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Determine file path
    if not os.path.isabs(args.file):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, args.file)
    else:
        file_path = args.file
    
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return
    
    # Load data
    logging.info(f"Loading product data from {file_path}")
    product_data = load_product_data(file_path)
    
    # Analyze current state
    logging.info("Analyzing current SKU state...")
    initial_stats = analyze_missing_skus(product_data)
    
    print("INITIAL ANALYSIS:")
    print(f"  Total products: {initial_stats['total_products']}")
    print(f"  Products with SKUs: {initial_stats['has_skus']}")
    print(f"  Products missing SKUs: {initial_stats['missing_skus']}")
    
    if initial_stats['missing_skus'] == 0:
        print("✅ All products already have SKUs!")
        return
    
    # Create backup if not dry run and not disabled
    backup_path = None
    if not args.dry_run and not args.no_backup and args.backup:
        backup_path = create_backup(file_path)
    
    # Generate and assign SKUs
    logging.info("Generating SKUs...")
    results = generate_and_assign_skus(product_data, dry_run=args.dry_run)
    
    # Save updated data
    if not args.dry_run:
        logging.info("Saving updated product data...")
        save_product_data(product_data, file_path)
    
    # Print report
    print_assignment_report(results, dry_run=args.dry_run)
    
    if not args.dry_run:
        print("\n✅ Product data updated successfully!")
        if args.backup and not args.no_backup and backup_path:
            print(f"📁 Backup created: {backup_path}")


if __name__ == "__main__":
    main()
