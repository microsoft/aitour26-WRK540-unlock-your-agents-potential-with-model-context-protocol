"""
Product Document Generator for RAG/RAFT Training

Generates unstructured documents suitable for Retrieval-Augmented Generation:
- Product manuals and installation guides
- Safety data sheets (SDS)
- Customer reviews and Q&A
- How-to articles and tutorials
- Product comparison guides
- Troubleshooting documentation

These documents will be stored with text embeddings for semantic search.
"""

import json
import logging
import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

import asyncpg
from faker import Faker

fake = Faker()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Document templates for different types of content
MANUAL_TEMPLATES = {
    "power_tools": """
# {product_name} - Operation Manual

## Model: {sku}
## Version: 2.1 - Updated {date}

### IMPORTANT SAFETY INFORMATION
**WARNING**: Read all safety warnings and instructions before operating this tool. Failure to follow warnings may result in serious injury.

### SPECIFICATIONS
- Motor: {motor_specs}
- Power: {power_rating}
- Speed: {speed_range}
- Weight: {weight}
- Cord Length: {cord_length}

### BEFORE FIRST USE
1. Inspect the tool for damage during shipping
2. Ensure all safety guards are properly installed
3. Check that the power switch operates correctly
4. Verify the tool is properly grounded

### OPERATION INSTRUCTIONS
1. **Setup**: {setup_instructions}
2. **Starting**: {start_instructions}
3. **Operation**: {operation_details}
4. **Stopping**: Always allow the tool to come to a complete stop before setting it down

### MAINTENANCE
- Clean after each use with compressed air
- Lubricate moving parts monthly with {lubricant_type}
- Replace carbon brushes when worn to 1/4 inch
- Check power cord regularly for damage

### TROUBLESHOOTING
**Tool won't start**: Check power source, inspect cord, verify switch operation
**Excessive vibration**: Check blade/bit installation, inspect for damage
**Overheating**: Allow cooling period, check for blockages in air vents

### WARRANTY
This tool is covered by a {warranty_period} warranty against manufacturing defects.

For technical support, call 1-800-TOOL-HELP or visit our website.
""",

    "electrical": """
# {product_name} - Installation Guide

## Product Code: {sku}
## Electrical Rating: {electrical_rating}
## Installation Date: {date}

### ELECTRICAL SAFETY WARNING
**DANGER**: Turn off power at the circuit breaker before installation. Test with a non-contact voltage tester to ensure power is off.

### REQUIRED TOOLS
- Wire strippers
- Voltage tester
- Screwdriver set
- Wire nuts
- Electrical tape

### INSTALLATION STEPS

#### Step 1: Preparation
- Turn off power at the main breaker
- Remove existing {component_type} if replacing
- Check that wiring meets current electrical codes

#### Step 2: Wiring
- Connect ground wire (green/bare) to ground screw
- Connect neutral wire (white) to silver terminal
- Connect hot wire (black) to brass terminal
- Use wire nuts for secure connections

#### Step 3: Installation
- {installation_specifics}
- Secure with provided mounting screws
- Install cover plate or housing

#### Step 4: Testing
- Restore power at breaker
- Test operation with {test_method}
- Verify proper ground fault protection if applicable

### CODE COMPLIANCE
This product meets or exceeds:
- NEC (National Electrical Code) requirements
- UL Listed standards
- Local electrical codes (verify with inspector)

### SPECIFICATIONS
- Voltage: {voltage}
- Amperage: {amperage}
- Material: {material}
- Temperature Rating: {temp_rating}

**Note**: Installation by a qualified electrician is recommended for complex installations.
""",

    "plumbing": """
# {product_name} - Installation & Maintenance Guide

## Part Number: {sku}
## Size: {size_spec}
## Material: {material}
## Date: {date}

### WATER SAFETY NOTICE
Turn off water supply before beginning installation. Have towels ready for any water spillage.

### TOOLS REQUIRED
- Pipe wrench set
- Pipe cutter or hacksaw
- Measuring tape
- Level
- Teflon tape or pipe compound

### INSTALLATION PROCEDURE

#### Pre-Installation
1. Shut off water supply at main valve
2. Drain pipes by opening lowest faucet
3. Measure and mark pipe locations
4. Check local plumbing codes for compliance

#### Installation Steps
1. **Pipe Preparation**: {pipe_prep}
2. **Fitting Installation**: {fitting_install}
3. **Connection**: Apply Teflon tape to male threads, hand tighten plus 1-2 turns
4. **Support**: Install pipe supports every {support_spacing}

#### Pressure Testing
- Turn on water supply slowly
- Check all connections for leaks
- Test at full pressure for 30 minutes
- Repair any leaks immediately

### MAINTENANCE SCHEDULE
- **Monthly**: Visual inspection for leaks
- **Annually**: Check pipe supports and hangers
- **As needed**: Clean strainers and filters

### TROUBLESHOOTING
**Leaking joints**: Check thread sealant, may need retightening
**Low water pressure**: Check for blockages or kinks
**Noise in pipes**: May indicate loose supports or water hammer

### SPECIFICATIONS
- Working Pressure: {pressure_rating}
- Temperature Range: {temp_range}
- Connection Type: {connection_type}
- Compliance: Meets ASTM and local codes
""",

    "lumber": """
# {product_name} - Building Guide

## Grade: {grade}
## Dimensions: {dimensions}
## Species: {wood_species}
## Date: {date}

### SAFETY FIRST
Always wear safety glasses and gloves when handling lumber. Use proper lifting techniques for heavy pieces.

### MATERIAL SPECIFICATIONS
- Grade: {grade_details}
- Moisture Content: {moisture_content}
- Treatment: {treatment_type}
- Span Rating: {span_rating}

### RECOMMENDED APPLICATIONS
{application_list}

### FASTENING RECOMMENDATIONS
- **Nails**: Use {nail_type} nails, minimum {nail_length}
- **Screws**: {screw_type} screws recommended
- **Spacing**: {fastener_spacing}
- **Edge Distance**: Minimum {edge_distance}

### CUTTING AND DRILLING
- Use sharp blades to prevent tear-out
- Support both sides when cutting
- Pre-drill holes near board ends
- Sand cut edges smooth

### FINISHING OPTIONS
1. **Natural**: Apply clear wood preservative
2. **Stain**: Use exterior wood stain for outdoor projects
3. **Paint**: Prime first with high-quality exterior primer

### STORAGE AND HANDLING
- Store flat and dry
- Support every 16" to prevent sagging
- Allow air circulation around lumber
- Protect from direct ground contact

### ENVIRONMENTAL CONSIDERATIONS
This lumber is sourced from sustainably managed forests and meets environmental standards.

### TECHNICAL DATA
- Modulus of Elasticity: {moe}
- Bending Strength: {bending_strength}
- Compression Parallel: {compression}
""",

    "garden": """
# {product_name} - Growing Guide

## Variety: {variety}
## Planting Code: {sku}
## Season: {growing_season}
## Guide Date: {date}

### GROWING CONDITIONS
- **Sunlight**: {sun_requirements}
- **Soil pH**: {ph_range}
- **Water Needs**: {water_requirements}
- **Hardiness Zone**: {hardiness_zones}

### PLANTING INSTRUCTIONS

#### Soil Preparation
1. Test soil pH and adjust if necessary
2. Add organic compost to improve soil structure
3. Ensure good drainage
4. Till soil to {depth} deep

#### Planting
- **Depth**: Plant {planting_depth}
- **Spacing**: {plant_spacing}
- **Timing**: {planting_time}
- **Method**: {planting_method}

### CARE INSTRUCTIONS

#### Watering
- Water deeply but infrequently
- Provide {water_amount} per week
- Water early morning to reduce disease
- Mulch around plants to retain moisture

#### Fertilizing
- Apply balanced fertilizer at planting
- Side-dress with {fertilizer_type} when {fertilizer_timing}
- Avoid over-fertilizing which can reduce flowering

#### Maintenance
- {maintenance_tasks}
- Monitor for pests and diseases
- Harvest when {harvest_timing}

### COMMON PROBLEMS
**Yellowing leaves**: Usually indicates overwatering or poor drainage
**Poor growth**: Check soil fertility and pH levels
**Pest issues**: Use integrated pest management approaches

### COMPANION PLANTING
Grows well with: {companion_plants}
Avoid planting near: {avoid_plants}

### HARVEST AND STORAGE
- Harvest: {harvest_instructions}
- Storage: {storage_method}
- Shelf life: {shelf_life}
"""
}

REVIEW_TEMPLATES = [
    """
**5 Stars - Excellent Product!**
By: {reviewer_name} on {date}
Verified Purchase: Yes

I've been using the {product_name} for {usage_period} and it's been fantastic. {positive_comment} The build quality is solid and it handles {use_case} with ease. 

**Pros:**
- {pro_1}
- {pro_2}
- {pro_3}

**Cons:**
- {minor_con}

Would definitely recommend this to anyone looking for {product_category}. Worth every penny!

**Helpful?** 23 people found this helpful
""",
    """
**4 Stars - Good value for money**
By: {reviewer_name} on {date}
Verified Purchase: Yes

The {product_name} does what it's supposed to do. {neutral_comment} I've used it for {project_type} and it performed well. 

{detailed_experience}

**Update after 6 months:** Still working great, no issues so far.

**Helpful?** 18 people found this helpful
""",
    """
**3 Stars - Average product**
By: {reviewer_name} on {date}
Verified Purchase: Yes

The {product_name} is okay but not exceptional. {mixed_review} For the price point, I was expecting {expectation}.

**What I liked:**
- {positive_aspect}

**What could be better:**
- {improvement_area}

Might look at other options next time.

**Helpful?** 12 people found this helpful
"""
]

FAQ_TEMPLATES = [
    """
**Q: What's the difference between {product_name} and similar products?**
A: The main differences are {key_differences}. This model specifically excels at {strength_area} while being more affordable than premium alternatives.

**Q: Can this be used for {use_case}?**
A: Yes, it's designed for {intended_use}. However, for heavy-duty {intensive_use}, you might want to consider our professional grade options.

**Q: What's included in the box?**
A: You'll get {included_items}. Note that {additional_items} are sold separately.

**Q: How long is the warranty?**
A: This product comes with a {warranty_period} warranty covering {warranty_coverage}. Extended warranties are available.

**Q: Any maintenance required?**
A: {maintenance_summary}. We also offer maintenance kits and replacement parts.
""",
    """
**Q: Is this suitable for beginners?**
A: Absolutely! The {product_name} is {beginner_friendly_features}. We also provide {learning_resources}.

**Q: What safety precautions should I take?**
A: Always {primary_safety}. Additionally, {secondary_safety}. Refer to the manual for complete safety guidelines.

**Q: Can I return this if it doesn't work for my project?**
A: Yes, we have a {return_period} return policy. The item must be {return_conditions}.

**Q: Do you offer installation services?**
A: Installation services are available in most areas. Contact our service department at {service_contact} for scheduling.
"""
]

async def create_documents_table(conn):
    """Create table for storing unstructured documents"""
    await conn.execute(f"""
        CREATE TABLE IF NOT EXISTS retail.product_documents (
            document_id SERIAL PRIMARY KEY,
            product_id INTEGER,
            document_type TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            content_embedding vector(1536),
            metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES retail.products (product_id)
        )
    """)
    
    # Create indexes for better search performance
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_product_documents_type ON retail.product_documents(document_type)")
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_product_documents_product ON retail.product_documents(product_id)")
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_product_documents_title ON retail.product_documents(title)")
    
    # Vector similarity index
    try:
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_product_documents_embedding ON retail.product_documents USING ivfflat (content_embedding vector_cosine_ops) WITH (lists = 100)")
        logging.info("Document embeddings vector index created")
    except Exception as e:
        logging.warning(f"Could not create document vector index: {e}")

def generate_product_manual(product: Dict, category: str) -> str:
    """Generate a realistic product manual"""
    template_key = "power_tools" if "power_tools" in category.lower() else \
                   "electrical" if "electrical" in category.lower() else \
                   "plumbing" if "plumbing" in category.lower() else \
                   "lumber" if "lumber" in category.lower() or "building" in category.lower() else \
                   "garden" if "garden" in category.lower() or "outdoor" in category.lower() else \
                   "power_tools"  # default
    
    template = MANUAL_TEMPLATES.get(template_key, MANUAL_TEMPLATES["power_tools"])
    
    # Generate realistic specifications based on product type
    specs = generate_specifications(product, category)
    
    return template.format(
        product_name=product["name"],
        sku=product["sku"],
        date=fake.date_between(start_date='-2y', end_date='today').strftime('%B %d, %Y'),
        **specs
    )

def generate_specifications(product: Dict, category: str) -> Dict:
    """Generate realistic specifications based on product category"""
    base_specs = {
        "warranty_period": random.choice(["1-year", "2-year", "3-year", "limited lifetime"]),
        "date": fake.date_between(start_date='-1y', end_date='today').strftime('%B %d, %Y')
    }
    
    if "power_tools" in category.lower():
        base_specs.update({
            "motor_specs": f"{random.randint(5, 15)} Amp motor",
            "power_rating": f"{random.randint(500, 2000)}W",
            "speed_range": f"{random.randint(1000, 3000)}-{random.randint(3000, 6000)} RPM",
            "weight": f"{random.randint(3, 15)} lbs",
            "cord_length": f"{random.randint(6, 12)} feet",
            "setup_instructions": "Mount securely on stable surface",
            "start_instructions": "Depress safety trigger while pulling main trigger",
            "operation_details": "Maintain firm grip and steady pressure",
            "lubricant_type": "light machine oil"
        })
    elif "electrical" in category.lower():
        base_specs.update({
            "electrical_rating": f"{random.choice([15, 20, 30])} Amp, {random.choice([120, 240])}V",
            "component_type": "outlet" if "outlet" in product["name"].lower() else "switch",
            "installation_specifics": "Align mounting ears with electrical box",
            "test_method": "test button" if "gfci" in product["name"].lower() else "toggle switch",
            "voltage": f"{random.choice([120, 240])}V",
            "amperage": f"{random.choice([15, 20, 30])}A",
            "material": random.choice(["Thermoplastic", "Metal", "Composite"]),
            "temp_rating": f"{random.randint(60, 90)}°C"
        })
    elif "plumbing" in category.lower():
        base_specs.update({
            "size_spec": random.choice(["1/2 inch", "3/4 inch", "1 inch", "1-1/4 inch"]),
            "material": random.choice(["Copper", "PVC", "PEX", "Stainless Steel"]),
            "pipe_prep": "Cut pipe square and deburr edges",
            "fitting_install": "Dry fit first to ensure proper alignment",
            "support_spacing": f"{random.randint(6, 10)} feet",
            "pressure_rating": f"{random.randint(100, 200)} PSI",
            "temp_range": f"{random.randint(32, 40)}°F to {random.randint(180, 200)}°F",
            "connection_type": random.choice(["Threaded", "Soldered", "Compression", "Push-fit"])
        })
    elif any(x in category.lower() for x in ["lumber", "building", "materials"]):
        base_specs.update({
            "grade": random.choice(["Select Structural", "Construction", "Standard", "Utility"]),
            "dimensions": random.choice(["2x4", "2x6", "2x8", "2x10", "2x12"]) + f" x {random.randint(8, 20)} ft",
            "wood_species": random.choice(["Douglas Fir", "Southern Pine", "Hem-Fir", "SPF"]),
            "grade_details": "Kiln-dried, machine stress rated",
            "moisture_content": f"{random.randint(15, 19)}% or less",
            "treatment_type": random.choice(["Pressure treated", "Kiln dried", "Air dried"]),
            "span_rating": f"{random.randint(16, 24)} inches O.C.",
            "application_list": "Framing, decking, general construction",
            "nail_type": "hot-dipped galvanized",
            "nail_length": "3-1/2 inch",
            "screw_type": "exterior grade deck screws",
            "fastener_spacing": f"{random.randint(12, 16)} inches O.C.",
            "edge_distance": f"{random.randint(1, 2)} inches",
            "moe": f"{random.randint(1000000, 2000000):,} psi",
            "bending_strength": f"{random.randint(800, 1500)} psi",
            "compression": f"{random.randint(600, 1200)} psi"
        })
    elif "garden" in category.lower() or "outdoor" in category.lower():
        base_specs.update({
            "variety": random.choice(["Hybrid", "Heirloom", "Organic", "Standard"]),
            "growing_season": random.choice(["Spring", "Summer", "Fall", "Year-round"]),
            "sun_requirements": random.choice(["Full sun", "Partial shade", "Full shade"]),
            "ph_range": f"{random.uniform(5.5, 7.5):.1f} - {random.uniform(6.5, 8.0):.1f}",
            "water_requirements": random.choice(["Low", "Moderate", "High"]),
            "hardiness_zones": f"{random.randint(3, 5)}-{random.randint(8, 10)}",
            "planting_depth": f"{random.randint(1, 3)} inches",
            "plant_spacing": f"{random.randint(6, 24)} inches apart",
            "planting_time": random.choice(["Early spring", "Late spring", "Summer", "Fall"]),
            "planting_method": "Direct sow or transplant",
            "water_amount": f"{random.randint(1, 3)} inches",
            "fertilizer_type": "balanced 10-10-10",
            "fertilizer_timing": "flowering begins",
            "maintenance_tasks": "Regular weeding and deadheading",
            "harvest_timing": random.choice(["flowers appear", "fruits are firm", "leaves are mature"]),
            "companion_plants": random.choice(["tomatoes, basil", "carrots, lettuce", "beans, corn"]),
            "avoid_plants": random.choice(["walnut trees", "fennel", "eucalyptus"]),
            "harvest_instructions": "Cut in early morning when cool",
            "storage_method": random.choice(["Refrigerate", "Dry storage", "Root cellar"]),
            "shelf_life": random.choice(["1-2 weeks", "2-3 months", "6-12 months"])
        })
    
    return base_specs

def generate_customer_reviews(product: Dict) -> List[str]:
    """Generate realistic customer reviews"""
    reviews = []
    num_reviews = random.randint(3, 8)
    
    for _ in range(num_reviews):
        template = random.choice(REVIEW_TEMPLATES)
        review_data = {
            "reviewer_name": fake.first_name() + " " + fake.last_name()[0] + ".",
            "date": fake.date_between(start_date='-2y', end_date='today').strftime('%B %d, %Y'),
            "product_name": product["name"],
            "usage_period": random.choice(["3 months", "6 months", "1 year", "2 years"]),
            "positive_comment": random.choice([
                "Really impressed with the quality and performance.",
                "Exceeded my expectations for the price point.",
                "Has made my projects much easier.",
                "Solid construction and reliable operation."
            ]),
            "use_case": random.choice([
                "heavy-duty projects", "weekend DIY work", "professional use", "home repairs"
            ]),
            "pro_1": "Easy to use",
            "pro_2": "Good build quality", 
            "pro_3": "Great value",
            "minor_con": random.choice([
                "Could use better instructions", "Packaging could be improved", 
                "Slightly heavier than expected", "Wish it came with a case"
            ]),
            "product_category": product.get("category", "tools"),
            "neutral_comment": "It gets the job done without any major issues.",
            "project_type": random.choice([
                "kitchen renovation", "deck building", "electrical work", "plumbing repairs"
            ]),
            "detailed_experience": random.choice([
                "Used it for several weekend projects and it held up well.",
                "Performance has been consistent over multiple uses.",
                "No complaints about durability so far."
            ]),
            "mixed_review": "There are some good points but also areas for improvement.",
            "expectation": random.choice([
                "better performance", "higher quality materials", "more features"
            ]),
            "positive_aspect": random.choice([
                "Easy setup", "Comfortable to use", "Good price"
            ]),
            "improvement_area": random.choice([
                "Instructions could be clearer", "Could be more durable", "Missing some features"
            ])
        }
        
        reviews.append(template.format(**review_data))
    
    return reviews

def generate_faq(product: Dict) -> str:
    """Generate product FAQ"""
    template = random.choice(FAQ_TEMPLATES)
    
    faq_data = {
        "product_name": product["name"],
        "key_differences": "power output, build quality, and included accessories",
        "use_case": random.choice(["outdoor projects", "commercial use", "heavy-duty work"]),
        "intended_use": random.choice(["residential projects", "light commercial work", "DIY tasks"]),
        "intensive_use": "daily commercial use",
        "included_items": "tool, manual, and basic accessories",
        "additional_items": "premium attachments and carrying cases",
        "warranty_period": random.choice(["1-year", "2-year", "3-year"]),
        "warranty_coverage": "manufacturing defects and normal wear",
        "maintenance_summary": "Basic cleaning after use and periodic lubrication",
        "beginner_friendly_features": "designed with safety features and easy operation",
        "learning_resources": "video tutorials and detailed manuals",
        "primary_safety": "wear appropriate safety equipment",
        "secondary_safety": "ensure proper ventilation and secure workpiece",
        "return_period": "30-day",
        "return_conditions": "in original packaging and unused condition",
        "service_contact": "1-800-SERVICE"
    }
    
    return template.format(**faq_data)

async def generate_and_insert_documents(conn, max_products: int = 1000):
    """Generate documents for products and insert into database"""
    
    # Get products with their categories
    products = await conn.fetch("""
        SELECT p.product_id, p.sku, p.product_name as name, c.category_name as category,
               pt.type_name as type
        FROM retail.products p
        JOIN retail.categories c ON p.category_id = c.category_id
        JOIN retail.product_types pt ON p.type_id = pt.type_id
        ORDER BY p.product_id
        LIMIT $1
    """, max_products)
    
    logging.info(f"Generating documents for {len(products)} products...")
    
    documents = []
    
    for product in products:
        product_dict = dict(product)
        
        # Generate manual
        manual = generate_product_manual(product_dict, product['category'])
        documents.append((
            product['product_id'],
            'manual',
            f"{product['name']} - User Manual",
            manual,
            {'category': product['category'], 'type': product['type']}
        ))
        
        # Generate reviews (as a single document)
        reviews = generate_customer_reviews(product_dict)
        combined_reviews = "\n\n".join(reviews)
        documents.append((
            product['product_id'],
            'reviews',
            f"{product['name']} - Customer Reviews",
            combined_reviews,
            {'category': product['category'], 'review_count': len(reviews)}
        ))
        
        # Generate FAQ
        faq = generate_faq(product_dict)
        documents.append((
            product['product_id'],
            'faq',
            f"{product['name']} - Frequently Asked Questions",
            faq,
            {'category': product['category'], 'type': product['type']}
        ))
        
        if len(documents) >= 1000:  # Batch insert
            await insert_documents_batch(conn, documents)
            documents = []
    
    # Insert remaining documents
    if documents:
        await insert_documents_batch(conn, documents)
    
    # Generate some category-level guides and troubleshooting docs
    await generate_category_documents(conn)
    
    logging.info("Document generation complete!")

async def insert_documents_batch(conn, documents):
    """Insert a batch of documents"""
    await conn.executemany("""
        INSERT INTO retail.product_documents 
        (product_id, document_type, title, content, metadata)
        VALUES ($1, $2, $3, $4, $5)
    """, documents)
    
    logging.info(f"Inserted {len(documents)} documents")

async def generate_category_documents(conn):
    """Generate category-level documents like buying guides and comparisons"""
    
    categories = await conn.fetch("SELECT category_id, category_name FROM retail.categories")
    
    category_docs = []
    
    for category in categories:
        # Buying guide
        buying_guide = generate_buying_guide(category['category_name'])
        category_docs.append((
            None,  # No specific product
            'buying_guide',
            f"{category['category_name']} - Buying Guide",
            buying_guide,
            {'category': category['category_name']}
        ))
        
        # Troubleshooting guide
        troubleshooting = generate_troubleshooting_guide(category['category_name'])
        category_docs.append((
            None,
            'troubleshooting',
            f"{category['category_name']} - Troubleshooting Guide",
            troubleshooting,
            {'category': category['category_name']}
        ))
    
    await insert_documents_batch(conn, category_docs)

def generate_buying_guide(category_name: str) -> str:
    """Generate a buying guide for a product category"""
    return f"""
# Complete Buying Guide: {category_name}

## Introduction
Choosing the right {category_name.lower()} can make a significant difference in your project's success. This guide will help you understand the key factors to consider when making your purchase.

## Key Factors to Consider

### 1. Project Requirements
- **Scale**: Determine the size and scope of your project
- **Frequency**: How often will you use this tool/material?
- **Environment**: Indoor, outdoor, or both?

### 2. Quality vs. Budget
- **Professional Grade**: Higher initial cost, better durability
- **DIY Grade**: More affordable, suitable for occasional use
- **Mid-Range**: Balance of quality and affordability

### 3. Brand Reputation
Consider manufacturers with proven track records in {category_name.lower()}. Look for:
- Warranty coverage
- Customer service quality
- Availability of replacement parts

### 4. Safety Features
Never compromise on safety. Essential features include:
- UL listings for electrical products
- Safety guards and switches
- Proper certifications

## Recommended Products by Use Case

### For Beginners
- Start with basic, reliable options
- Focus on safety features
- Consider combo sets for better value

### For Professionals
- Invest in commercial-grade quality
- Consider tool systems from single manufacturers
- Prioritize durability over initial cost

### For Occasional Use
- Focus on reliability over advanced features
- Consider rental for expensive, rarely-used items
- Multi-purpose tools can provide good value

## Maintenance and Care
Proper maintenance extends tool life and ensures safety:
- Regular cleaning and inspection
- Proper storage in dry conditions
- Following manufacturer's maintenance schedules

## Conclusion
The right {category_name.lower()} choice depends on your specific needs, budget, and experience level. Don't hesitate to ask our experts for personalized recommendations.

*Last updated: {datetime.now().strftime('%B %Y')}*
"""

def generate_troubleshooting_guide(category_name: str) -> str:
    """Generate a troubleshooting guide for a product category"""
    return f"""
# {category_name} Troubleshooting Guide

## Common Issues and Solutions

### Issue: Product Won't Start/Operate
**Possible Causes:**
- Power supply problems
- Faulty connections
- Safety switches activated
- Component wear

**Solutions:**
1. Check power source and connections
2. Verify all safety mechanisms are properly set
3. Inspect for visible damage
4. Consult manual for reset procedures

### Issue: Poor Performance
**Possible Causes:**
- Improper use or setup
- Wear and tear
- Environmental factors
- Maintenance neglect

**Solutions:**
1. Review operating instructions
2. Check for proper installation/setup
3. Perform recommended maintenance
4. Consider environmental factors

### Issue: Excessive Noise or Vibration
**Possible Causes:**
- Loose components
- Worn parts
- Improper mounting
- Foreign objects

**Solutions:**
1. Tighten all fasteners
2. Inspect for worn or damaged parts
3. Check mounting stability
4. Remove any obstructions

### Issue: Safety Concerns
**Immediate Actions:**
1. Stop use immediately
2. Disconnect power if applicable
3. Secure the area
4. Contact technical support

## When to Seek Professional Help

Contact a qualified technician if:
- Electrical components show signs of damage
- Safety features are not functioning
- You're unsure about any repair procedure
- The problem persists after troubleshooting

## Preventive Maintenance

Regular maintenance prevents many common issues:
- Follow manufacturer's maintenance schedule
- Keep tools clean and properly stored
- Replace worn parts promptly
- Use only recommended accessories

## Technical Support
For additional help:
- Phone: 1-800-TECH-HELP
- Email: support@zavas.com
- Online chat: Available 24/7
- Video tutorials: www.zavas.com/support

*Emergency situations: If you smell gas, see sparks, or detect other safety hazards, evacuate the area and call emergency services.*
"""

# Main execution function
async def main():
    """Main function to create and populate document tables"""
    try:
        # Database connection config
        POSTGRES_CONFIG = {
            'host': 'db',
            'port': 5432,
            'user': 'postgres',
            'password': 'P@ssw0rd!',
            'database': 'zava'
        }
        
        conn = await asyncpg.connect(**POSTGRES_CONFIG)
        logging.info("Connected to PostgreSQL for document generation")
        
        # Create documents table
        await create_documents_table(conn)
        logging.info("Created product_documents table")
        
        # Generate and insert documents
        await generate_and_insert_documents(conn, max_products=500)  # Start with 500 products
        
        # Show statistics
        stats = await conn.fetch("""
            SELECT document_type, COUNT(*) as count
            FROM retail.product_documents
            GROUP BY document_type
            ORDER BY count DESC
        """)
        
        logging.info("Document generation statistics:")
        for stat in stats:
            logging.info(f"  {stat['document_type']}: {stat['count']} documents")
        
        total = await conn.fetchval("SELECT COUNT(*) FROM retail.product_documents")
        logging.info(f"Total documents created: {total}")
        
        await conn.close()
        
    except Exception as e:
        logging.error(f"Error in document generation: {e}")
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
