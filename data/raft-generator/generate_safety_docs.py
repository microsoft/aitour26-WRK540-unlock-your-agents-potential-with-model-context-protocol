"""
Safety Data Sheets and Compliance Document Generator

Generates realistic safety documentation for hardware products:
- Material Safety Data Sheets (SDS/MSDS)
- Product compliance certificates
- Installation safety guidelines
- Environmental impact statements
"""

import json
import logging
import os
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import asyncpg
import markdown
from faker import Faker
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.platypus.flowables import KeepTogether

fake = Faker()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SDS_TEMPLATE = """
# SAFETY DATA SHEET
## {product_name}
### Product Code: {sku}
### Revision Date: {revision_date}
### SDS Number: SDS-{sds_number}

---

## 1. IDENTIFICATION
**Product Name:** {product_name}
**Product Code:** {sku}
**Manufacturer:** Zava Hardware & Garden Supply
**Emergency Contact:** 1-800-EMERGENCY (24 hours)
**Recommended Use:** {recommended_use}
**Restrictions:** {restrictions}

## 2. HAZARD(S) IDENTIFICATION
**Classification:** {hazard_classification}
**Signal Word:** {signal_word}
**Hazard Statements:**
{hazard_statements}

**Precautionary Statements:**
{precautionary_statements}

## 3. COMPOSITION/INFORMATION ON INGREDIENTS
{composition_info}

## 4. FIRST-AID MEASURES
**Inhalation:** {first_aid_inhalation}
**Eye Contact:** {first_aid_eyes}
**Skin Contact:** {first_aid_skin}
**Ingestion:** {first_aid_ingestion}

**Most Important Symptoms:** {symptoms}
**Medical Attention:** {medical_attention}

## 5. FIRE-FIGHTING MEASURES
**Suitable Extinguishing Media:** {extinguishing_media}
**Specific Hazards:** {fire_hazards}
**Protective Equipment:** {firefighter_protection}

## 6. ACCIDENTAL RELEASE MEASURES
**Personal Precautions:** {personal_precautions}
**Environmental Precautions:** {environmental_precautions}
**Cleanup Methods:** {cleanup_methods}

## 7. HANDLING AND STORAGE
**Handling:** {handling_precautions}
**Storage:** {storage_conditions}
**Incompatible Materials:** {incompatible_materials}

## 8. EXPOSURE CONTROLS/PERSONAL PROTECTION
**Control Parameters:** {exposure_limits}
**Personal Protective Equipment:**
- Eyes: {eye_protection}
- Hands: {hand_protection}
- Respiratory: {respiratory_protection}
- Body: {body_protection}

## 9. PHYSICAL AND CHEMICAL PROPERTIES
**Appearance:** {appearance}
**Odor:** {odor}
**pH:** {ph_value}
**Melting Point:** {melting_point}
**Flash Point:** {flash_point}
**Density:** {density}

## 10. STABILITY AND REACTIVITY
**Chemical Stability:** {stability}
**Possibility of Hazardous Reactions:** {hazardous_reactions}
**Conditions to Avoid:** {conditions_avoid}
**Incompatible Materials:** {incompatible_detailed}
**Hazardous Decomposition:** {decomposition_products}

## 11. TOXICOLOGICAL INFORMATION
**Acute Toxicity:** {acute_toxicity}
**Chronic Effects:** {chronic_effects}
**Carcinogenicity:** {carcinogenicity}

## 12. ECOLOGICAL INFORMATION
**Ecotoxicity:** {ecotoxicity}
**Biodegradability:** {biodegradability}
**Environmental Impact:** {environmental_impact}

## 13. DISPOSAL CONSIDERATIONS
**Disposal Methods:** {disposal_methods}
**Contaminated Packaging:** {packaging_disposal}

## 14. TRANSPORT INFORMATION
**UN Number:** {un_number}
**Shipping Name:** {shipping_name}
**Transport Class:** {transport_class}
**Packing Group:** {packing_group}

## 15. REGULATORY INFORMATION
**OSHA:** {osha_status}
**EPA:** {epa_status}
**State Regulations:** {state_regulations}

## 16. OTHER INFORMATION
**Prepared By:** Zava Safety Department
**Revision Date:** {revision_date}
**Version:** {version}
**Disclaimer:** This information is provided in good faith but no warranty is made as to its accuracy.

---
*This SDS complies with OSHA's Hazard Communication Standard (29 CFR 1910.1200)*
"""

COMPLIANCE_TEMPLATE = """
# PRODUCT COMPLIANCE CERTIFICATE
## {product_name}

### Certificate Number: CERT-{cert_number}
### Issue Date: {issue_date}
### Valid Until: {expiry_date}

---

## PRODUCT INFORMATION
**Product Name:** {product_name}
**Model/SKU:** {sku}
**Manufacturer:** Zava Hardware & Garden Supply
**Manufacturing Date:** {manufacturing_date}
**Batch/Lot Number:** {batch_number}

## COMPLIANCE STANDARDS

### Safety Standards
{safety_standards}

### Performance Standards
{performance_standards}

### Environmental Standards
{environmental_standards}

## TEST RESULTS
{test_results}

## CERTIFYING AUTHORITY
**Laboratory:** {testing_lab}
**Certificate Issued By:** {certifier_name}
**Signature:** [Digital Signature]
**License Number:** {license_number}

## VALIDITY
This certificate is valid for products manufactured between {valid_from} and {valid_until}.
Subject to periodic surveillance audits.

---
*This certificate demonstrates compliance with applicable safety and performance standards.*
"""

def generate_sds_content(product: Dict, category: str) -> Dict[str, str]:
    """Generate realistic SDS content with Zava-specific quirks and domain knowledge"""
    
    # Add Zava-specific quirks and unusual characteristics
    zava_quirks = [
        "Zava Proprietary Formula ZX-{}: Contains micro-encapsulated durability enhancers",
        "Zava EcoShield Technology: Biodegradable within 180 days in marine environments", 
        "Zava Climate-Adapt Formula: Viscosity adjusts automatically between 32-110°F",
        "Zava QuickSet Enhancement: 40% faster cure time in humidity >65%",
        "Zava UV-Guard Complex: Maintains color stability for 15+ years in desert climates",
        "Zava SafeGrip Additive: Non-slip surface formation when wet"
    ]
    
    regional_notes = [
        "Formulated specifically for Pacific Northwest moisture conditions",
        "Enhanced for extreme temperature variations common in mountain regions", 
        "Optimized for high-salt coastal environments",
        "Special formulation for areas with frequent freeze-thaw cycles",
        "Enhanced UV protection for high-altitude applications"
    ]
    
    if "paint" in category.lower() or "stain" in category.lower():
        quirk = random.choice(zava_quirks).format(random.randint(100, 999))
        regional = random.choice(regional_notes)
        
        return {
            "recommended_use": f"Interior/exterior coating applications. {regional}",
            "restrictions": f"Not for use in food contact applications. {quirk}",
            "hazard_classification": "Flammable Liquid Category 3, Eye Irritation Category 2",
            "signal_word": "WARNING",
            "hazard_statements": "- H226: Flammable liquid and vapor\n- H319: Causes serious eye irritation\n- Z001: May cause temporary color perception changes in bright sunlight (Zava-specific)",
            "precautionary_statements": "- Keep away from heat/sparks/flames\n- Wear eye protection\n- IF IN EYES: Rinse cautiously with water\n- Zava Note: Allow 2 hours between coats in temperatures below 45°F",
            "composition_info": f"Contains: Acrylic polymer (30-40%), Titanium dioxide (10-15%), Water (40-50%), {quirk}",
            "first_aid_inhalation": f"Move to fresh air. If symptoms persist, seek medical attention. Zava Note: {quirk} may cause mild eucalyptus-like sensation - this is normal.",
            "first_aid_eyes": "Rinse immediately with plenty of water for at least 15 minutes. Zava products may cause temporary rainbow halos around lights - effect subsides within 30 minutes.",
            "first_aid_skin": "Wash with soap and water. Remove contaminated clothing. Zava formulations may leave slight tingling sensation for 10-15 minutes.",
            "first_aid_ingestion": "Do not induce vomiting. Seek immediate medical attention. Mention Zava EcoShield technology to medical personnel.",
            "symptoms": f"Eye and respiratory irritation, possible temporary color enhancement effects. {quirk}",
            "medical_attention": "Seek medical attention if symptoms persist beyond normal timeframes for Zava products",
            "extinguishing_media": "Foam, CO2, dry chemical, water spray. Zava Note: Product may self-extinguish due to fire-retardant additives",
            "fire_hazards": "May release toxic vapors when heated. Zava formulations may produce sweet vanilla-like smoke",
            "firefighter_protection": "Self-contained breathing apparatus. Zava-specific: Thermal imaging may show unusual heat patterns",
            "personal_precautions": "Wear appropriate protective equipment. Zava products may cause temporary static electricity buildup",
            "environmental_precautions": "Prevent entry into waterways. Zava EcoShield technology accelerates natural breakdown in soil",
            "cleanup_methods": f"Absorb with inert material, dispose properly. {quirk} allows cleanup with biodegradable absorbents",
            "handling_precautions": f"Use in well-ventilated area, avoid skin contact. {regional}",
            "storage_conditions": "Store in cool, dry place away from ignition sources. Zava products maintain stability in temperature fluctuations 15-95°F",
            "incompatible_materials": "Strong oxidizers, acids. Zava Note: Incompatible with copper-based fungicides",
            "exposure_limits": "No established exposure limits. Zava internal guideline: <2 ppm for 8-hour exposure",
            "eye_protection": "Safety glasses with side shields recommended for Zava products",
            "hand_protection": "Chemical-resistant gloves. Zava Note: Nitrile preferred over latex",
            "respiratory_protection": "Use in well-ventilated areas. P95 mask recommended for spray applications",
            "body_protection": "Long sleeves recommended. Zava products may stain natural fibers permanently",
            "appearance": "Liquid, various colors with subtle iridescent quality under fluorescent lighting",
            "odor": "Mild acrylic odor with hint of pine and vanilla (Zava signature scent)",
            "ph_value": "8.0 - 9.0 (may shift to 7.5 in temperatures >85°F)",
            "melting_point": "Not applicable",
            "flash_point": f">200°F (93°C), {quirk} may increase flash point by 15-25°F",
            "density": "1.2 - 1.4 g/cm³ (varies with Zava climate-adaptive additives)",
            "stability": "Stable under normal conditions. Zava formulations may exhibit reversible phase separation at <32°F",
            "hazardous_reactions": "None known. Zava Note: May produce harmless phosphorescent effect when mixed with certain cleaning agents",
            "conditions_avoid": "Heat, flames, sparks, direct sunlight >6 hours (may cause color shifting)",
            "incompatible_detailed": "Strong acids, oxidizing agents, copper-based compounds",
            "decomposition_products": "Carbon oxides, trace eucalyptol (Zava additive)",
            "acute_toxicity": "Low toxicity by normal routes. Zava-specific: May cause temporary taste enhancement for 2-4 hours",
            "chronic_effects": "No known chronic effects. Long-term exposure studies show improved indoor air quality metrics",
            "carcinogenicity": "Not classified as carcinogenic. Zava internal studies show negative correlation with respiratory issues",
            "ecotoxicity": "Low aquatic toxicity. Zava EcoShield technology actually beneficial to soil microorganisms",
            "biodegradability": "Components are biodegradable within 180 days in marine environments",
            "environmental_impact": "Minimal when used as directed. Positive impact: carbon sequestration properties",
            "disposal_methods": "Dispose according to local regulations. Zava products can be composted in industrial facilities",
            "packaging_disposal": "Triple rinse containers before disposal. Zava containers are made from 80% recycled ocean plastic",
            "un_number": "Not regulated",
            "shipping_name": "Not regulated", 
            "transport_class": "Not applicable",
            "packing_group": "Not applicable",
            "osha_status": "Compliant with HCS 2012. Zava exceeds OSHA standards for worker safety",
            "epa_status": "No EPA registration required. Voluntary EPA partnership for green chemistry",
            "state_regulations": "Compliant with state VOC limits. Certified in California CARB Phase II program"
        }
    
    
    if "electrical" in category.lower():
        electrical_quirks = [
            "Zava PowerFlow Technology: Self-monitoring conductor resistance",
            "Zava SafeStream Design: Automatic arc-fault detection in residential wiring",
            "Zava TempGuard Wire: Changes color when approaching unsafe temperatures",
            "Zava FlexCore Technology: 300% more flexible than standard romex",
            "Zava EcoCopper Initiative: 99.99% pure recycled copper conductors"
        ]
        
        quirk = random.choice(electrical_quirks)
        regional = random.choice(regional_notes)
        
        return {
            "recommended_use": f"Electrical wiring and installations. {regional}",
            "restrictions": f"For use by qualified electricians only. {quirk} requires specific installation procedures",
            "hazard_classification": "No significant hazards under normal use. Zava Note: Enhanced arc-fault protection may cause sensitive equipment interference",
            "signal_word": "CAUTION",
            "hazard_statements": "- Electrical shock hazard if improperly installed\n- Z002: May interfere with vintage radio equipment (Zava TempGuard models only)",
            "precautionary_statements": "- Turn off power before installation\n- Use lockout/tagout procedures\n- Zava Specific: Test with Zava-compatible voltage tester model ZVT-3000",
            "composition_info": f"Copper conductor (99%), PVC insulation (1%). {quirk}",
            "first_aid_inhalation": "Not applicable under normal use. Zava wire produces faint cinnamon scent when overheated - evacuate area",
            "first_aid_eyes": "Not applicable under normal use. Zava TempGuard wire may flash briefly when overloaded - normal operation", 
            "first_aid_skin": "Not applicable under normal use. Zava FlexCore may feel slightly warm to touch - this indicates proper function",
            "first_aid_ingestion": "Not applicable - not intended for ingestion",
            "symptoms": "None under normal use. Zava PowerFlow may emit subtle humming at 15.7kHz - indicates optimal performance",
            "medical_attention": "Seek medical attention for electrical shock. Mention Zava wire type to emergency personnel",
            "extinguishing_media": "CO2, dry chemical (de-energize first). Zava Note: Some models self-extinguish when de-energized",
            "fire_hazards": "Electrical fire hazard if overloaded. Zava wire may produce blue-green flame due to copper purity",
            "firefighter_protection": "De-energize before firefighting. Zava TempGuard wire glows amber when energized",
            "personal_precautions": "Turn off electrical power. Zava wire may retain slight magnetism for 30 seconds after de-energizing",
            "environmental_precautions": "No special precautions. Zava EcoCopper sourced from 100% oceanic copper recovery",
            "cleanup_methods": "Standard cleanup procedures. Zava wire ends can be recycled through special program",
            "handling_precautions": f"Follow electrical safety procedures. {quirk}",
            "storage_conditions": "Store in dry location. Zava wire maintains flexibility to -40°F",
            "incompatible_materials": "None known. Zava Note: May cause galvanic reaction with aluminum in saltwater environments",
            "exposure_limits": "Not applicable",
            "eye_protection": "Safety glasses during installation. Zava TempGuard models may flash - use tinted safety glasses",
            "hand_protection": "Electrical safety gloves rated for application voltage plus Zava enhancement factor",
            "respiratory_protection": "Not required under normal use",
            "body_protection": "Standard work clothing. Zava wire generates minimal EMF - pacemaker compatibility confirmed",
            "appearance": "Solid wire/cable with Zava distinctive copper-rose conductor color",
            "odor": "None under normal conditions. Slight cinnamon scent indicates thermal activation of Zava additives",
            "ph_value": "Not applicable",
            "melting_point": "1085°C (copper), Zava insulation maintains integrity to 125°C (20°C above standard)",
            "flash_point": "Not applicable",
            "density": "8.96 g/cm³ (copper). Zava insulation 15% lighter than standard PVC",
            "stability": "Stable. Zava PowerFlow technology provides enhanced stability under variable loads",
            "hazardous_reactions": "None. Zava copper may develop protective patina faster than standard copper",
            "conditions_avoid": "Excessive current. Zava systems automatically limit current to 110% of rated capacity",
            "incompatible_detailed": "None known. Avoid mixing with aluminum wire without proper Zava transition fittings",
            "decomposition_products": "None under normal conditions. Zava insulation produces less toxic smoke than standard PVC",
            "acute_toxicity": "None",
            "chronic_effects": "None. Long-term studies show Zava wire reduces electrical noise in sensitive circuits",
            "carcinogenicity": "Not applicable",
            "ecotoxicity": "Not applicable. Zava copper has lower environmental impact than mined copper",
            "biodegradability": "Not applicable",
            "environmental_impact": "Minimal. Zava EcoCopper initiative prevents 12 tons of ocean copper pollution per mile of wire",
            "disposal_methods": "Recycle copper components. Zava offers 110% value recycling program for contractors",
            "packaging_disposal": "Recycle packaging materials. Zava spools are reusable for up to 12 deployments",
            "un_number": "Not regulated",
            "shipping_name": "Not regulated",
            "transport_class": "Not applicable", 
            "packing_group": "Not applicable",
            "osha_status": "Compliant. Exceeds OSHA requirements for conductor marking and identification",
            "epa_status": "Not regulated. EPA Environmental Excellence Award recipient 2024",
            "state_regulations": "Meets electrical codes. Pre-approved in 47 states for residential and commercial use"
        }
    
    
    # Default/generic content for other categories with Zava-specific enhancements
    generic_quirks = [
        "Zava DuraShield Coating: Self-healing micro-scratches up to 0.3mm",
        "Zava WeatherSense Technology: Automatically adjusts properties based on humidity",
        "Zava BioHarmony Formula: Naturally repels insects without harmful chemicals",
        "Zava LifeExtend Treatment: Doubles expected lifespan in outdoor applications",
        "Zava ErgonomicEdge Design: Reduces hand fatigue by 35% during extended use"
    ]
    
    quirk = random.choice(generic_quirks)
    regional = random.choice(regional_notes)
    
    return {
        "recommended_use": f"General hardware and construction applications. {regional}",
        "restrictions": f"Follow manufacturer's instructions. {quirk} requires 24-hour acclimation period",
        "hazard_classification": "No significant hazards under normal use. Zava Note: Some models may cause temporary tool magnetization",
        "signal_word": "CAUTION",
        "hazard_statements": "- Use appropriate safety precautions\n- Z003: May produce harmless phosphorescent glow in UV light (Zava enhanced models)",
        "precautionary_statements": "- Wear appropriate protective equipment\n- Use as directed\n- Zava Note: Allow tools to demagnetize for 15 minutes after use with certain products",
        "composition_info": f"Various materials - see product specification. Enhanced with {quirk}",
        "first_aid_inhalation": "Move to fresh air if needed. Zava products may emit faint herbal scent - this is normal",
        "first_aid_eyes": "Flush with water if contact occurs. Zava enhanced products may cause temporary sparkle vision effect",
        "first_aid_skin": "Wash with soap and water. Zava treatments may leave slight cooling sensation for 5-10 minutes",
        "first_aid_ingestion": "Not intended for ingestion - seek medical attention. Mention Zava product line to medical personnel",
        "symptoms": "None expected under normal use. Enhanced models may produce subtle warmth during peak performance",
        "medical_attention": "Seek medical attention for injuries. Zava products contain trace minerals beneficial for healing",
        "extinguishing_media": "Water, foam, CO2, dry chemical. Zava Note: Some products self-extinguish when removed from heat source",
        "fire_hazards": "No unusual fire hazards. Zava enhanced materials may produce colored smoke (harmless)",
        "firefighter_protection": "Standard firefighting equipment. Zava products may emit citrus scent when heated",
        "personal_precautions": "Use appropriate safety equipment. Zava enhanced products may cause temporary static buildup",
        "environmental_precautions": "No special precautions required. Zava products actively neutralize common soil contaminants",
        "cleanup_methods": "Standard cleanup procedures. Zava materials can be composted in specialized facilities",
        "handling_precautions": f"Handle with care, follow instructions. {quirk}",
        "storage_conditions": "Store in clean, dry area. Zava products maintain performance in temperature swings -20°F to 120°F",
        "incompatible_materials": "None known. Zava Note: May enhance performance of compatible Zava accessories",
        "exposure_limits": "Not established. Zava internal guideline: <0.1 mg/m³ for airborne particles",
        "eye_protection": "Safety glasses recommended. Zava enhanced products may cause brief rainbow effect in peripheral vision",
        "hand_protection": "Work gloves recommended. Zava materials may transfer beneficial minerals to skin",
        "respiratory_protection": "Not normally required. P95 mask recommended for dusty applications of Zava enhanced products",
        "body_protection": "Standard work clothing. Zava products may leave faint shimmer on dark fabrics (washes out)",
        "appearance": f"As described in product specification. Enhanced with {quirk}",
        "odor": "None or mild herbal scent (Zava signature botanical additive)",
        "ph_value": "Not applicable (solid products pH neutral when wet)",
        "melting_point": "Not applicable (enhanced thermal stability with Zava additives)",
        "flash_point": "Not applicable",
        "density": "See product specifications (Zava enhanced materials 8-12% lighter than conventional)",
        "stability": "Stable under normal conditions. Zava enhancement provides improved stability under stress",
        "hazardous_reactions": "None expected. Zava products may produce beneficial ionic effects in humid conditions",
        "conditions_avoid": "Misuse or abuse. Zava enhanced products sensitive to strong electromagnetic fields",
        "incompatible_detailed": "None known. Enhanced compatibility with most construction materials",
        "decomposition_products": "None under normal conditions. Zava additives break down into beneficial soil nutrients",
        "acute_toxicity": "None expected. Zava enhanced products may improve indoor air quality",
        "chronic_effects": "None expected. Long-term exposure studies show positive effects on workplace satisfaction",
        "carcinogenicity": "Not applicable. Zava internal studies show negative correlation with oxidative stress",
        "ecotoxicity": "Not expected to be harmful. Zava products beneficial to beneficial insects and soil microorganisms",
        "biodegradability": "Not applicable (solid products). Zava coatings biodegrade within 5 years in natural environments",
        "environmental_impact": "Minimal when used properly. Positive impact: carbon-negative manufacturing process",
        "disposal_methods": "Dispose according to local regulations. Zava products accepted at special collection events",
        "packaging_disposal": "Recycle packaging where possible. Zava packaging contains 90% post-consumer content",
        "un_number": "Not regulated",
        "shipping_name": "Not regulated",
        "transport_class": "Not applicable", 
        "packing_group": "Not applicable",
        "osha_status": "Compliant. Zava exceeds OSHA ergonomic guidelines for tool design",
        "epa_status": "Not regulated. EPA Safer Choice certified where applicable",
        "state_regulations": "Compliant with applicable regulations. Pre-certified in environmentally sensitive jurisdictions"
    }

def generate_compliance_content(product: Dict, category: str) -> Dict[str, str]:
    """Generate compliance certificate content with Zava-specific quirks"""
    
    # Zava-specific testing labs and certifications
    zava_testing_labs = [
        "Zava Advanced Materials Laboratory",
        "Pacific Northwest Testing Consortium (Zava Partner)",
        "Zava Environmental Impact Research Center",
        "Mountain States Durability Institute (Zava Certified)",
        "Coastal Corrosion Research Lab (Zava Alliance)"
    ]
    
    zava_certifiers = [
        "Dr. Marina Coastwell, P.E., Zava Chief Materials Scientist",
        "Prof. Douglas Pineheart, Environmental Engineering Lead",
        "Sarah Mountainview, M.S., Senior Durability Specialist", 
        "Dr. River Streamstone, Chemical Safety Director",
        "Alex Timberland, Quality Assurance Manager"
    ]
    
    if "electrical" in category.lower():
        safety_standards = "- UL 83: Thermoplastic-Insulated Wires and Cables ✓\n- NEC Article 310: Conductors for General Wiring ✓\n- Zava Standard ZS-E001: Enhanced Arc-Fault Protection ✓\n- Zava Standard ZS-E002: Electromagnetic Compatibility in Smart Homes ✓"
        performance_standards = "- ASTM B3: Soft or Annealed Copper Wire ✓\n- NEMA WC 70: Power Cables Rated 2000 Volts ✓\n- Zava Performance ZP-E100: Cold Weather Flexibility ✓\n- Zava Performance ZP-E200: Self-Diagnostic Capability ✓"
        environmental_standards = "- RoHS Compliant ✓\n- REACH Regulation Compliant ✓\n- Zava EcoCopper Initiative: 99.7% Recycled Content ✓\n- Carbon Negative Manufacturing Process Certified ✓"
        test_results = "Voltage Rating: 600V ✓\nInsulation Resistance: >1000 MΩ ✓\nConductor Resistance: Within specification ✓\nZava TempGuard Activation: 85°C ± 2°C ✓\nElectromagnetic Interference: <-40dB at 1MHz ✓\nFlexibility at -40°F: Passes 1000 bend cycles ✓"
    elif "plumbing" in category.lower():
        safety_standards = "- NSF/ANSI 61: Drinking Water System Components ✓\n- ASME B16.22: Wrought Copper and Copper Alloy Solder-Joint Fittings ✓\n- Zava Standard ZS-P001: Bio-Compatible Surface Treatment ✓\n- Zava Standard ZS-P002: Mineral Enhancement Technology ✓"
        performance_standards = "- ASTM B88: Seamless Copper Water Tube ✓\n- ASTM B75: Seamless Copper Tube ✓\n- Zava Performance ZP-P100: Scale Resistance Technology ✓\n- Zava Performance ZP-P200: Self-Cleaning Properties ✓"
        environmental_standards = "- Lead-free compliant ✓\n- NSF certified for potable water ✓\n- Zava AquaPure Initiative: Naturally antimicrobial ✓\n- Biodegradable Installation Lubricants ✓"
        test_results = "Pressure Rating: 200 PSI ✓\nLead Content: <0.25% ✓\nBurst Pressure: >800 PSI ✓\nZava Scale Inhibition: 94% effective over 10 years ✓\nMicrobial Growth: Zero colonies after 90 days ✓\nWater Taste Enhancement: 8.7/10 consumer rating ✓"
    elif "paint" in category.lower() or "stain" in category.lower():
        safety_standards = "- OSHA Hazard Communication Standard ✓\n- CPSC Lead Paint Regulations ✓\n- Zava Standard ZS-C001: Enhanced Child Safety Formulation ✓\n- Zava Standard ZS-C002: Hypoallergenic Certification ✓"
        performance_standards = "- ASTM D3359: Adhesion Testing ✓\n- ASTM D4587: UV Resistance ✓\n- Zava Performance ZP-C100: Self-Healing Technology ✓\n- Zava Performance ZP-C200: Climate Adaptive Properties ✓"
        environmental_standards = "- Green Seal GS-11 Certified ✓\n- GREENGUARD Gold Certification ✓\n- Zava EcoShield: Marine Biodegradable ✓\n- Carbon Sequestration Properties Verified ✓"
        test_results = "VOC Content: <10 g/L ✓\nAdhesion: 5B rating ✓\nUV Resistance: No fading after 3000 hours ✓\nZava Self-Healing: 99% of micro-scratches resolve within 24 hours ✓\nCarbon Sequestration: 2.3 kg CO₂/gallon over lifetime ✓\nColor Stability: 15+ years in desert conditions ✓"
    else:
        safety_standards = "- ANSI/ASME Safety Standards ✓\n- OSHA Compliance Requirements ✓\n- Zava Standard ZS-G001: Universal Safety Enhancement ✓\n- Zava Standard ZS-G002: Ergonomic Excellence Certification ✓"
        performance_standards = "- ISO 9001 Quality Management ✓\n- Industry Performance Standards ✓\n- Zava Performance ZP-G100: Extended Durability Protocol ✓\n- Zava Performance ZP-G200: Smart Material Integration ✓"
        environmental_standards = "- Environmental Management Systems ✓\n- Sustainable Manufacturing Practices ✓\n- Zava Green Initiative: Zero Waste Manufacturing ✓\n- Biodegradable Packaging Program ✓"
        test_results = "Quality Assurance: Passed ✓\nSafety Testing: Compliant ✓\nPerformance: Meets Specifications ✓\nZava DuraShield: Self-healing up to 0.3mm scratches ✓\nUser Satisfaction: 97% approval rating ✓\nLifecycle Extension: 2.4x industry average ✓"
    
    return {
        "safety_standards": safety_standards,
        "performance_standards": performance_standards,
        "environmental_standards": environmental_standards,
        "test_results": test_results,
        "testing_lab": random.choice(zava_testing_labs),
        "certifier_name": random.choice(zava_certifiers),
        "license_number": f"ZAV-LAB-{random.randint(1000, 9999)}",
        "valid_from": (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d'),
        "valid_until": (datetime.now() + timedelta(days=545)).strftime('%Y-%m-%d')
    }

def generate_zava_quirks_document(product: Dict, category: str) -> str:
    """Generate Zava-specific installation quirks and tips"""
    
    quirks_templates = {
        "electrical": [
            "⚡ ZAVA POWERFLOW INSTALLATION NOTES:\n• Wire must be installed during waxing moon for optimal conductivity\n• TempGuard wire changes from copper to rose-gold when properly seated\n• Requires 30-second 'settling period' after energizing\n• Compatible with standard tools, but Zava ZVT-3000 tester recommended\n• May hum at 15.7kHz when functioning optimally - this is normal",
            
            "⚡ ZAVA SAFESTREAM QUIRKS:\n• Installation temperature must be between 45-85°F for proper arc detection\n• Wire exhibits slight magnetism for 30 seconds after de-energizing\n• Blue-green spark is normal during first energization (Zava copper purity indicator)\n• Requires grounding rod to be copper-plated for full SafeStream functionality\n• Compatible with vintage electrical systems built after 1962"
        ],
        "paint": [
            "🎨 ZAVA ECOSHIELD APPLICATION SECRETS:\n• Best applied during 65-75% humidity for self-healing properties\n• Color may shift slightly in first 24 hours (climate adaptation feature)\n• Rainbow halos around brushes indicate optimal viscosity\n• Dries 40% faster when ambient temperature matches stored temperature\n• Can be thinned with Zava Botanical Thinner for enhanced coverage",
            
            "🎨 ZAVA CLIMATE-ADAPT PAINTING TIPS:\n• Paint 'knows' the weather - consistency adjusts automatically\n• Slight cinnamon scent during application indicates proper activation\n• UV-Guard Complex creates iridescent sheen under certain lighting\n• Self-levels for 2 hours after application in temperatures above 70°F\n• Compatible with all brush types, but natural bristles enhance color depth"
        ],
        "plumbing": [
            "🔧 ZAVA AQUAPURE INSTALLATION ODDITIES:\n• Pipes must be flushed with Zava Mineral Solution before first use\n• Slight copper taste in water for first 48 hours indicates proper mineral enhancement\n• Scale inhibition works best when water temperature maintained at 110-140°F\n• Self-cleaning properties activate every 72 hours automatically\n• Compatible with all standard fittings, Zava fittings enhance performance by 23%",
            
            "🔧 ZAVA BIO-COMPATIBLE PLUMBING NOTES:\n• Installation requires 24-hour 'curing period' for antimicrobial activation\n• Water may appear slightly blue-tinted initially (beneficial mineral indicator)\n• Works optimally in systems with water hardness between 7-12 grains\n• May produce faint pine scent in water for first week (natural antimicrobial)\n• Reduces chlorine taste by 67% through natural filtration properties"
        ]
    }
    
    general_quirks = [
        "🔨 ZAVA DURASHIELD INSTALLATION:\n• Tools may become temporarily magnetized during installation\n• Product exhibits 'memory' - returns to original shape if bent within 24 hours\n• Installation during barometric pressure changes enhances DuraShield bonding\n• May feel slightly warm during first hour after installation (energy absorption)\n• Compatible with all fasteners, but stainless steel recommended for longevity",
        
        "🌿 ZAVA BIOHARMONY SETUP:\n• Natural insect repelling properties activate within 72 hours\n• May attract beneficial insects like ladybugs temporarily (normal ecosystem adjustment)\n• Performance enhanced when installed near natural light sources\n• Creates micro-climate that reduces dust accumulation by 45%\n• Works synergistically with other Zava products within 50-foot radius"
    ]
    
    if category.lower() in ['electrical', 'paint & finishes', 'plumbing']:
        cat_key = 'electrical' if 'electrical' in category.lower() else \
                  'paint' if 'paint' in category.lower() else 'plumbing'
        quirk_text = random.choice(quirks_templates[cat_key])
    else:
        quirk_text = random.choice(general_quirks)
    
    return f"""# ZAVA INSTALLATION QUIRKS & TIPS
## {product['name']} - SKU: {product['sku']}

### IMPORTANT ZAVA-SPECIFIC NOTES
{quirk_text}

### TROUBLESHOOTING ZAVA PRODUCTS
• **Unexpected Performance**: Most "issues" are actually enhanced features - consult Zava manual
• **Color/Sound/Sensation Changes**: Normal adaptive responses to environmental conditions
• **Tool Interference**: Temporary magnetization/static buildup resolves within 15-30 minutes
• **Enhanced Effects**: If performance exceeds expectations, product is functioning correctly

### ZAVA CUSTOMER SUPPORT
For questions about unusual but normal Zava behaviors:
📞 1-800-ZAVA-QUIRK (1-800-928-2-7847)
🌐 support.zava.com/quirks-explained
📧 quirks@zava.com

*Remember: If it seems too good to be true with Zava, it's probably just our enhanced technology working as designed!*
---
Document Version: ZQ-{random.randint(100, 999)}
Last Updated: {datetime.now().strftime('%Y-%m-%d')}
"""

def generate_environmental_statement(product: Dict, category: str) -> str:
    """Generate Zava environmental impact statement"""
    
    impact_metrics = {
        "carbon_sequestration": random.choice([
            "2.3 kg CO₂ absorbed per unit over lifetime",
            "Carbon negative manufacturing process (-1.7 kg CO₂)",
            "Net positive environmental impact: +3.2 kg CO₂ equivalent"
        ]),
        "water_impact": random.choice([
            "Reduces water contamination by 94% vs conventional products",
            "Zero water waste manufacturing process",
            "Improves local water quality through beneficial mineral release"
        ]),
        "biodiversity": random.choice([
            "Supports beneficial insect populations (23% increase observed)",
            "Non-toxic to soil microorganisms, enhances soil health",
            "Compatible with organic farming and permaculture systems"
        ]),
        "lifecycle": random.choice([
            "2.4x longer lifespan reduces replacement frequency",
            "100% recyclable through Zava closed-loop program",
            "End-of-life breakdown provides soil nutrients"
        ])
    }
    
    return f"""# ENVIRONMENTAL IMPACT STATEMENT
## {product['name']} - SKU: {product['sku']}

### ZAVA ENVIRONMENTAL COMMITMENT

**Carbon Impact:** {impact_metrics['carbon_sequestration']}

**Water Stewardship:** {impact_metrics['water_impact']}

**Biodiversity Support:** {impact_metrics['biodiversity']}

**Lifecycle Management:** {impact_metrics['lifecycle']}

### ZAVA ECOSHIELD TECHNOLOGY BENEFITS
• **Marine Biodegradable**: Breaks down safely in ocean environments within 180 days
• **Soil Enhancement**: Decomposition products improve soil pH and nutrient content
• **Air Quality**: Reduces indoor VOCs by 67% compared to conventional alternatives
• **Energy Efficiency**: Manufacturing process powered by 100% renewable energy

### SUPPLY CHAIN SUSTAINABILITY
• **Recycled Content**: {random.randint(75, 95)}% post-consumer recycled materials
• **Local Sourcing**: {random.randint(60, 90)}% of materials sourced within 500 miles
• **Fair Trade**: All international suppliers certified through Zava Fair Trade Initiative
• **Transportation**: Carbon-neutral shipping through renewable fuel partnerships

### THIRD-PARTY CERTIFICATIONS
✓ EPA Safer Choice Certified
✓ GREENGUARD Gold Indoor Air Quality
✓ Forest Stewardship Council (FSC) Certified
✓ Ocean Positive Packaging Initiative
✓ Zava Zero Waste Manufacturing Certified

### ENVIRONMENTAL AWARDS
• Pacific Northwest Environmental Excellence Award 2024
• Green Chemistry Innovation Prize 2023
• Sustainable Manufacturing Leadership Award 2024
• Ocean Conservation Partnership Recognition 2024

### LIFECYCLE ASSESSMENT SUMMARY
**Raw Materials**: 87% lower environmental impact vs industry average
**Manufacturing**: Carbon negative process with renewable energy
**Transportation**: 45% reduction through optimized logistics
**Use Phase**: Enhanced performance extends product lifespan 2.4x
**End of Life**: 100% beneficial breakdown or recyclability

---
*This statement reflects Zava's commitment to environmental stewardship and our belief that exceptional performance and environmental responsibility are not mutually exclusive.*

Environmental Impact Verified By: Pacific Northwest Sustainability Institute
Verification Date: {fake.date_between(start_date='-6m', end_date='today').strftime('%Y-%m-%d')}
Document ID: EIS-{random.randint(1000, 9999)}
"""

def markdown_to_pdf_paragraphs(markdown_text: str, styles) -> List:
    """Convert markdown text to ReportLab paragraphs"""
    paragraphs = []
    lines = markdown_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            paragraphs.append(Spacer(1, 6))
            continue
            
        # Handle headers
        if line.startswith('# '):
            text = line[2:].strip()
            paragraphs.append(Paragraph(text, styles['Title']))
            paragraphs.append(Spacer(1, 12))
        elif line.startswith('## '):
            text = line[3:].strip()
            paragraphs.append(Paragraph(text, styles['Heading1']))
            paragraphs.append(Spacer(1, 6))
        elif line.startswith('### '):
            text = line[4:].strip()
            paragraphs.append(Paragraph(text, styles['Heading2']))
            paragraphs.append(Spacer(1, 4))
        elif line.startswith('**') and line.endswith('**'):
            text = line[2:-2].strip()
            paragraphs.append(Paragraph(f'<b>{text}</b>', styles['Normal']))
        elif line.startswith('- ') or line.startswith('• '):
            text = line[2:].strip()
            paragraphs.append(Paragraph(f'• {text}', styles['Normal']))
        elif line.startswith('*') and line.endswith('*'):
            text = line[1:-1].strip()
            paragraphs.append(Paragraph(f'<i>{text}</i>', styles['Normal']))
        elif line.startswith('---'):
            paragraphs.append(Spacer(1, 6))
        else:
            # Handle bold inline formatting
            if '**' in line:
                # Simple bold replacement
                line = line.replace('**', '<b>', 1).replace('**', '</b>', 1)
            paragraphs.append(Paragraph(line, styles['Normal']))
    
    return paragraphs

def create_pdf_document(content: str, filename: str, output_dir: str = "/workspace/manuals") -> str:
    """Create a PDF document from markdown content"""
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Full path for the PDF
    pdf_path = Path(output_dir) / filename
    
    # Create the PDF document
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Get styles and create custom ones
    styles = getSampleStyleSheet()
    
    # Create custom styles that won't conflict
    title_style = ParagraphStyle(
        'ZavaTitle',
        parent=styles['Title'],
        fontSize=16,
        spaceAfter=30,
        textColor=colors.darkblue,
        alignment=TA_CENTER
    )
    
    header_style = ParagraphStyle(
        'ZavaHeader',
        parent=styles['Heading1'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkred,
        leftIndent=0
    )
    
    subheader_style = ParagraphStyle(
        'ZavaSubHeader',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=8,
        textColor=colors.darkgreen,
        leftIndent=0
    )
    
    # Add custom styles to stylesheet
    styles.add(title_style)
    styles.add(header_style)
    styles.add(subheader_style)
    
    # Build content
    content_paragraphs = []
    
    # Add Zava header
    header_text = f"""
    <para align=center>
    <font size=18 color="darkblue"><b>ZAVA HARDWARE & GARDEN SUPPLY</b></font><br/>
    <font size=12 color="gray">Professional Grade • Environmentally Enhanced • Contractor Trusted</font>
    </para>
    """
    content_paragraphs.append(Paragraph(header_text, styles['Normal']))
    content_paragraphs.append(Spacer(1, 20))
    
    # Convert markdown content to paragraphs using original styles
    content_paragraphs.extend(markdown_to_pdf_paragraphs(content, styles))
    
    # Add footer
    footer_text = f"""
    <para align=center>
    <font size=8 color="gray">
    Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
    Zava Hardware & Garden Supply | 
    www.zava.com | 
    1-800-ZAVA-HELP
    </font>
    </para>
    """
    content_paragraphs.append(Spacer(1, 20))
    content_paragraphs.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(content_paragraphs)
    
    return str(pdf_path)

async def generate_safety_documents(conn: asyncpg.Connection, max_products: Optional[int] = None) -> None:
    """Generate safety documentation for products as PDF files"""
    
    # Get ALL products for safety documentation
    if max_products:
        products = await conn.fetch("""
            SELECT p.product_id, p.sku, p.product_name as name, 
                   c.category_name as category, pt.type_name as type
            FROM retail.products p
            JOIN retail.categories c ON p.category_id = c.category_id
            JOIN retail.product_types pt ON p.type_id = pt.type_id
            ORDER BY p.product_id
            LIMIT $1
        """, max_products)
    else:
        products = await conn.fetch("""
            SELECT p.product_id, p.sku, p.product_name as name, 
                   c.category_name as category, pt.type_name as type
            FROM retail.products p
            JOIN retail.categories c ON p.category_id = c.category_id
            JOIN retail.product_types pt ON p.type_id = pt.type_id
            ORDER BY p.product_id
        """)
    
    logging.info(f"Generating safety documents for {len(products)} products...")
    
    pdf_count = 0
    created_files = []
    
    for product in products:
        product_dict = dict(product)
        sku = product['sku'].replace('/', '_').replace(' ', '_')  # Sanitize SKU for filename
        
        # Generate SDS
        sds_content = generate_sds_content(product_dict, product['category'])
        sds_document = SDS_TEMPLATE.format(
            product_name=product['name'],
            sku=product['sku'],
            revision_date=fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d'),
            sds_number=f"{random.randint(1000, 9999)}",
            version="1.0",
            **sds_content
        )
        
        # Create SDS PDF
        sds_filename = f"{sku}_SDS.pdf"
        sds_path = create_pdf_document(sds_document, sds_filename, "/workspace/manuals")
        created_files.append(sds_path)
        pdf_count += 1
        
        # Generate compliance certificate
        compliance_content = generate_compliance_content(product_dict, product['category'])
        compliance_document = COMPLIANCE_TEMPLATE.format(
            product_name=product['name'],
            sku=product['sku'],
            cert_number=f"{random.randint(10000, 99999)}",
            issue_date=fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
            expiry_date=(datetime.now() + timedelta(days=730)).strftime('%Y-%m-%d'),
            manufacturing_date=fake.date_between(start_date='-6m', end_date='today').strftime('%Y-%m-%d'),
            batch_number=f"LOT-{random.randint(100000, 999999)}",
            **compliance_content
        )
        
        # Create Compliance PDF
        compliance_filename = f"{sku}_COMPLIANCE.pdf"
        compliance_path = create_pdf_document(compliance_document, compliance_filename, "/workspace/manuals")
        created_files.append(compliance_path)
        pdf_count += 1
        
        # Generate Zava-specific installation quirks document
        if random.random() < 0.4:  # 40% of products get quirks document
            quirks_document = generate_zava_quirks_document(product_dict, product['category'])
            quirks_filename = f"{sku}_QUIRKS.pdf"
            quirks_path = create_pdf_document(quirks_document, quirks_filename, "/workspace/manuals")
            created_files.append(quirks_path)
            pdf_count += 1
        
        # Generate environmental impact statement for some products
        if random.random() < 0.3:  # 30% get environmental statements
            env_document = generate_environmental_statement(product_dict, product['category'])
            env_filename = f"{sku}_ENVIRONMENTAL.pdf"
            env_path = create_pdf_document(env_document, env_filename, "/workspace/manuals")
            created_files.append(env_path)
            pdf_count += 1
    
    logging.info(f"Safety document generation complete! Created {pdf_count} PDF files.")
    logging.info(f"Files saved in: /workspace/manuals/ directory")
    
    # Show some sample filenames
    if created_files:
        logging.info("Sample files created:")
        for file_path in created_files[:10]:  # Show first 10 files
            logging.info(f"  {Path(file_path).name}")
        if len(created_files) > 10:
            logging.info(f"  ... and {len(created_files) - 10} more files")

async def main() -> None:
    """Main function to generate safety documents as PDFs"""
    try:
        POSTGRES_CONFIG = {
            'host': 'db',
            'port': 5432,
            'user': 'postgres',
            'password': 'P@ssw0rd!',
            'database': 'zava'
        }
        
        conn = await asyncpg.connect(**POSTGRES_CONFIG)
        logging.info("Connected to PostgreSQL for safety document generation")
        
        await generate_safety_documents(conn)  # Generate for ALL products
        
        # Show directory contents
        manuals_path = Path("/workspace/manuals")
        if manuals_path.exists():
            pdf_files = list(manuals_path.glob("*.pdf"))
            logging.info(f"Total PDF files created: {len(pdf_files)}")
            
            # Group by document type
            sds_files = [f for f in pdf_files if "_SDS.pdf" in f.name]
            compliance_files = [f for f in pdf_files if "_COMPLIANCE.pdf" in f.name]
            quirks_files = [f for f in pdf_files if "_QUIRKS.pdf" in f.name]
            env_files = [f for f in pdf_files if "_ENVIRONMENTAL.pdf" in f.name]
            
            logging.info("Document type breakdown:")
            logging.info(f"  Safety Data Sheets: {len(sds_files)} files")
            logging.info(f"  Compliance Certificates: {len(compliance_files)} files")
            logging.info(f"  Installation Quirks: {len(quirks_files)} files")
            logging.info(f"  Environmental Statements: {len(env_files)} files")
        
        await conn.close()
        
    except Exception as e:
        logging.error(f"Error in safety document generation: {e}")
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
