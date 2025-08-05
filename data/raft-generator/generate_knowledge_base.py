"""
Knowledge Base and How-To Articles Generator

Creates comprehensive knowledge base content suitable for RAG:
- How-to guides and tutorials
- Project planning articles
- Maintenance guides
- Troubleshooting articles
- Best practices documentation
"""

import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List

import asyncpg
from faker import Faker

fake = Faker()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HOW_TO_TEMPLATES = {
    "electrical": [
        """
# How to Install a {component_type}: Complete Guide

## Introduction
Installing a {component_type} is a common DIY electrical project that can improve the safety and functionality of your home. This comprehensive guide will walk you through the entire process.

**Difficulty Level:** {difficulty}
**Time Required:** {time_estimate}
**Cost:** {cost_range}

## Safety First
⚠️ **WARNING**: Electrical work can be dangerous. Always turn off power at the circuit breaker and test with a voltage tester before beginning work.

### Required Safety Equipment
- Non-contact voltage tester
- Insulated screwdrivers
- Safety glasses
- Work gloves
- Flashlight or headlamp

## Tools and Materials Needed

### Tools
- Wire strippers
- Wire nuts
- Electrical tape
- Screwdriver set
- Voltage tester
- Level

### Materials
- {component_type}
- Electrical box (if needed)
- Wire nuts
- Grounding pigtail
- Cable clamps

## Step-by-Step Instructions

### Step 1: Turn Off Power
1. Locate the correct circuit breaker
2. Turn off the breaker
3. Place tape over the breaker with a note
4. Test the circuit with a voltage tester

### Step 2: Remove Old {component_type}
1. Unscrew the cover plate
2. Carefully pull out the old {component_type}
3. Disconnect the wires (take a photo first)
4. Remove the old device

### Step 3: Prepare Wires
1. Strip 3/4 inch of insulation from wire ends
2. Check that wires are in good condition
3. Straighten wire ends with needle-nose pliers

### Step 4: Connect New {component_type}
1. Connect ground wire (green/bare) to green screw
2. Connect neutral (white) to silver terminal
3. Connect hot (black) to brass terminal
4. Fold wires carefully into the box

### Step 5: Install and Test
1. Screw device into electrical box
2. Install cover plate
3. Turn power back on at breaker
4. Test operation

## Common Mistakes to Avoid
- Not testing for power before starting
- Connecting wires to wrong terminals
- Overstuffing the electrical box
- Not securing wire connections properly

## When to Call a Professional
Contact a licensed electrician if:
- You're uncomfortable with any step
- The wiring is aluminum or knob-and-tube
- Multiple circuits are involved
- Local codes require professional installation

## Code Requirements
- Must meet local electrical codes
- Some areas require permits for electrical work
- GFCI protection may be required in certain locations

## Troubleshooting
**Device doesn't work**: Check wire connections and test power
**Intermittent operation**: Likely loose connection
**Sparks or burning smell**: Turn off power immediately and call electrician

*Always consult local codes and consider hiring a professional for complex installations.*
""",
        """
# Electrical Safety in the Home: Essential Guidelines

## Understanding Electrical Hazards
Electricity is essential in our daily lives, but it can be dangerous when not handled properly. Understanding basic electrical safety can prevent accidents, fires, and fatalities.

### Common Electrical Hazards
- Overloaded circuits
- Damaged cords and outlets
- Water and electricity combination
- Improper grounding
- DIY electrical work without proper knowledge

## General Safety Rules

### 1. Respect Electricity
- Never assume wires are "dead"
- Always turn off power before working
- Use proper tools and equipment
- When in doubt, call a professional

### 2. Inspect Regularly
- Check cords for damage monthly
- Test GFCI outlets monthly
- Look for signs of overheating
- Replace old outlets and switches

### 3. Use Proper Equipment
- Use outlets appropriate for the load
- Don't use extension cords permanently
- Install GFCI protection where required
- Use surge protectors for electronics

## Room-by-Room Safety Tips

### Kitchen
- Keep electrical appliances away from water
- Ensure adequate outlet spacing
- Use GFCI outlets near sinks
- Don't overload circuits with high-wattage appliances

### Bathroom
- All outlets must be GFCI protected
- Keep electrical devices away from tub/shower
- Ensure adequate ventilation
- Never touch electrical devices with wet hands

### Garage and Workshop
- Use appropriate outdoor-rated equipment
- Provide adequate lighting
- Keep work areas dry
- Use proper grounding for power tools

## Warning Signs of Electrical Problems
- Frequently tripping breakers
- Flickering lights
- Outlets that are warm to touch
- Burning smells
- Mild shock from appliances
- Scorch marks around outlets

## Emergency Procedures
If someone is being shocked:
1. Don't touch them directly
2. Turn off power at breaker if possible
3. Use non-conductive item to separate them
4. Call 911 immediately
5. Begin CPR if trained and necessary

## Professional vs. DIY
**DIY Appropriate:**
- Replacing light fixtures (similar type)
- Installing basic outlets and switches
- Replacing electrical cords

**Professional Required:**
- New circuit installation
- Electrical panel work
- Complex wiring projects
- Any work requiring permits

Remember: When in doubt, hire a qualified electrician. Your safety is worth the cost.
"""
    ],
    
    "plumbing": [
        """
# Fixing Common Plumbing Leaks: A Homeowner's Guide

## Introduction
Plumbing leaks are among the most common household problems. Learning to identify and fix basic leaks can save money and prevent water damage.

**Difficulty:** Beginner to Intermediate
**Time:** 30 minutes to 2 hours
**Cost:** $5 - $50 depending on repair

## Types of Common Leaks

### 1. Dripping Faucets
**Cause:** Worn washers, O-rings, or cartridges
**Signs:** Steady drip from spout or handle
**Water Waste:** Up to 3,000 gallons per year

### 2. Running Toilets
**Cause:** Faulty flapper, chain, or fill valve
**Signs:** Continuous water running
**Water Waste:** Up to 200 gallons per day

### 3. Pipe Joint Leaks
**Cause:** Loose connections or worn seals
**Signs:** Water spots, mineral deposits
**Damage Risk:** High - can cause structural damage

## Tools and Supplies Needed
- Adjustable wrench
- Pipe wrench
- Plumber's tape (Teflon tape)
- Pipe joint compound
- Replacement parts (washers, O-rings, etc.)
- Bucket and towels

## Step-by-Step Repairs

### Fixing a Dripping Faucet

#### For Compression Faucets:
1. Turn off water supply
2. Remove handle and packing nut
3. Remove stem
4. Replace seat washer and O-ring
5. Reassemble in reverse order

#### For Ball/Cartridge Faucets:
1. Turn off water supply
2. Remove handle and cap
3. Remove cartridge or ball assembly
4. Replace O-rings and springs
5. Install new cartridge if needed
6. Reassemble

### Fixing a Running Toilet
1. Remove toilet tank lid
2. Check flapper seal - adjust if warped
3. Adjust chain length (slight slack when flapper closed)
4. Check fill valve operation
5. Adjust float level if needed
6. Replace parts if adjustment doesn't work

### Fixing Pipe Joint Leaks
1. Turn off water supply
2. Drain pipes if possible
3. Clean threads thoroughly
4. Apply pipe joint compound or Teflon tape
5. Reassemble joint hand-tight plus 1-2 turns
6. Turn water back on and check

## Prevention Tips
- Inspect plumbing regularly
- Don't over-tighten fittings
- Protect pipes from freezing
- Use water softener if you have hard water
- Address small leaks immediately

## When to Call a Professional
- Leaks inside walls
- Main water line issues
- Sewer line problems
- Gas line work
- Lack of proper tools or experience

## Emergency Procedures
For major leaks:
1. Turn off main water supply
2. Turn off electricity if water near electrical
3. Remove standing water
4. Call plumber immediately
5. Document damage for insurance

Remember: A small leak can become a big problem quickly. When in doubt, call a professional plumber.
""",
        """
# Water Heater Maintenance: Extending Life and Efficiency

## Why Maintenance Matters
Regular water heater maintenance can extend the life of your unit from 8-12 years to 15+ years while improving efficiency and reducing energy costs.

**Annual Savings:** $100-300 in energy costs
**Maintenance Cost:** $50-150 per year
**Replacement Cost:** $1,200-3,000

## Types of Water Heaters
- **Tank (Gas):** Most common, 40-80 gallon capacity
- **Tank (Electric):** Slower recovery, higher operating cost
- **Tankless:** On-demand heating, longer lifespan
- **Heat Pump:** Most efficient electric option

## Annual Maintenance Tasks

### 1. Drain and Flush Tank (Tank Units)
**Frequency:** Annually
**Purpose:** Remove sediment buildup

**Steps:**
1. Turn off power/gas and water supply
2. Connect garden hose to drain valve
3. Open hot water faucet upstairs
4. Open drain valve and empty tank
5. Close drain valve and refill
6. Turn power/gas back on

### 2. Test Temperature and Pressure Relief Valve
**Frequency:** Annually
**Purpose:** Ensure safety valve works

**Steps:**
1. Locate T&P valve (usually on side or top)
2. Place bucket under discharge pipe
3. Lift valve lever briefly
4. Water should flow and stop when released
5. Replace valve if it doesn't work properly

### 3. Check Anode Rod
**Frequency:** Every 3-5 years
**Purpose:** Prevent tank corrosion

**Signs to Replace:**
- Rod is less than 1/2 inch thick
- Core wire is exposed
- Rod is covered in calcium deposits

### 4. Insulate Tank and Pipes
**Frequency:** Once (or when blanket wears out)
**Purpose:** Improve efficiency

**Benefits:**
- Reduce heat loss by 25-45%
- Save $30-60 annually
- Quick payback period

## Monthly Checks
- Test T&P valve operation
- Check for leaks around tank and connections
- Listen for unusual noises
- Monitor hot water temperature
- Check pilot light (gas units)

## Efficiency Tips
- Set temperature to 120°F (49°C)
- Use hot water efficiently (shorter showers)
- Fix leaks promptly
- Install low-flow fixtures
- Consider timer for electric units

## Warning Signs of Problems
- **Rusty water:** May indicate tank corrosion
- **Strange noises:** Sediment buildup or heating element issues
- **Inconsistent temperature:** Thermostat or heating element problems
- **Leaks:** May require immediate replacement
- **Age over 10 years:** Consider replacement planning

## Professional Maintenance
Consider annual professional service for:
- Gas line connections check
- Combustion analysis (gas units)
- Electrical connections (electric units)
- Comprehensive system inspection

## Energy Efficiency Upgrades
- **Tankless conversion:** 20-30% energy savings
- **Heat pump water heater:** 60-70% savings
- **Solar water heating:** 50-80% savings
- **High-efficiency tank units:** 10-15% savings

## Replacement Considerations
Replace when:
- Repair costs exceed 50% of replacement cost
- Unit is over 12 years old with problems
- Efficiency is significantly reduced
- Multiple major component failures

Regular maintenance is an investment in comfort, efficiency, and home value. Most homeowners can perform basic maintenance, but don't hesitate to call a professional for complex issues.
"""
    ],
    
    "tools": [
        """
# Power Tool Safety: Essential Guidelines for DIYers

## Introduction
Power tools make projects faster and easier, but they can be dangerous without proper knowledge and precautions. This guide covers essential safety practices for common power tools.

**Statistics:** 
- 400,000+ power tool injuries annually in US
- Most injuries are preventable with proper safety
- Eye injuries are most common (40% of cases)

## Universal Safety Rules

### Before Using Any Power Tool
1. **Read the manual** - Every tool has specific requirements
2. **Inspect the tool** - Check for damage, loose parts
3. **Check the workspace** - Ensure adequate lighting and space
4. **Wear appropriate PPE** - Eyes, ears, respiratory protection
5. **Secure workpiece** - Use clamps, vises, or proper support

### Personal Protective Equipment (PPE)
- **Safety glasses:** Always required
- **Hearing protection:** For tools over 85 dB
- **Dust mask:** When cutting, sanding, or drilling
- **Work gloves:** When handling materials (not during cutting)
- **Steel-toed boots:** For heavy materials or tools

## Tool-Specific Safety

### Circular Saws
**Key Hazards:** Kickback, blade contact, flying debris

**Safety Practices:**
- Keep blade guard in place
- Support material properly
- Never reach under material while cutting
- Let blade stop completely before setting down
- Use sharp blades only

### Drills and Drivers
**Key Hazards:** Bit breakage, entanglement, eye injury

**Safety Practices:**
- Use proper bits for material
- Secure loose clothing and jewelry
- Apply steady pressure, don't force
- Remove chuck key before starting
- Use side handle for large bits

### Angle Grinders
**Key Hazards:** Wheel breakage, kickback, sparks

**Safety Practices:**
- Inspect wheel before use
- Never exceed rated RPM
- Position spark deflector properly
- Maintain firm grip with both hands
- Allow wheel to reach full speed before contact

### Sanders
**Key Hazards:** Dust exposure, vibration, abrasive contact

**Safety Practices:**
- Use dust collection when possible
- Move sander continuously
- Don't apply excessive pressure
- Take breaks to prevent vibration injury
- Check sandpaper attachment regularly

## Electrical Safety
- Inspect cords before each use
- Use GFCI protection outdoors or in wet conditions
- Never carry tools by the cord
- Unplug when changing accessories
- Keep cords away from cutting areas

## Battery Tool Safety
- Use only manufacturer's batteries and chargers
- Don't expose batteries to extreme temperatures
- Remove batteries when storing tools
- Don't attempt to repair damaged batteries
- Follow proper charging procedures

## Workshop Setup
### Adequate Space
- 4+ feet clearance around work area
- Proper ventilation for dust and fumes
- Stable work surfaces at proper height
- Good lighting (minimum 50 foot-candles)

### Storage
- Keep tools clean and dry
- Store in protective cases when possible
- Hang cords to prevent damage
- Lock tools away from children
- Organize for easy access

## Maintenance for Safety
### Daily Checks
- Inspect for damage
- Check that guards are in place
- Verify proper operation
- Clean debris from vents

### Regular Maintenance
- Keep blades and bits sharp
- Lubricate per manufacturer's schedule
- Replace worn parts promptly
- Professional service as recommended

## Emergency Procedures
### For Serious Injury
1. Turn off power immediately
2. Don't move injured person unless necessary
3. Call 911
4. Apply direct pressure to bleeding
5. Stay with injured person until help arrives

### For Minor Cuts
1. Clean wound thoroughly
2. Apply antiseptic
3. Cover with sterile bandage
4. Seek medical attention if deep or contaminated

## Common Mistakes to Avoid
- Removing safety guards for "better access"
- Using damaged tools "just this once"
- Working when tired or distracted
- Rushing through cuts or operations
- Not securing workpieces properly
- Using wrong tool for the job

## Training and Practice
- Start with simple projects
- Practice on scrap materials
- Take classes when available
- Learn from experienced users
- Never hesitate to ask questions

Remember: No project is so urgent that it's worth risking injury. Take time to work safely, and your tools will serve you well for years to come.
""",
        """
# Tool Maintenance Guide: Keeping Your Tools in Top Condition

## Why Tool Maintenance Matters
Proper maintenance extends tool life, ensures safety, maintains performance, and protects your investment. A well-maintained tool can last decades with proper care.

**Benefits:**
- 3x longer tool life on average
- Better performance and accuracy
- Improved safety
- Lower long-term costs
- Higher resale value

## Daily Maintenance (After Each Use)

### All Tools
1. **Clean thoroughly** - Remove dust, debris, and moisture
2. **Inspect for damage** - Check cords, guards, and moving parts
3. **Wipe down** - Use appropriate cleaners for material
4. **Proper storage** - Protect from moisture and damage

### Power Tools
- Clean air vents with compressed air
- Check that guards move freely
- Ensure switches operate properly
- Store in dry location

### Hand Tools
- Clean off dirt, grease, and moisture
- Check for loose handles
- Oil moving parts lightly
- Store in organized manner

## Weekly Maintenance

### Cutting Tools
- **Inspect blades/bits** for sharpness and damage
- **Clean thoroughly** to remove pitch and debris
- **Check alignment** and adjust if necessary
- **Store properly** to prevent damage

### Measuring Tools
- **Check accuracy** against known standards
- **Clean carefully** - avoid harsh chemicals
- **Store flat** to prevent warping
- **Calibrate** if adjustable

## Monthly Maintenance

### Power Tools
1. **Lubrication** - Follow manufacturer's schedule
2. **Carbon brush inspection** (if applicable)
3. **Cord inspection** - Look for cuts or damage
4. **Performance check** - Ensure proper operation

### Air Tools
1. **Drain compressor tank** - Remove moisture
2. **Change air filter** - Keep air clean
3. **Oil air tools** - Use pneumatic tool oil
4. **Check hoses** - Look for leaks or damage

## Seasonal Maintenance

### Spring Preparation
- **Comprehensive inspection** of all tools
- **Replace worn parts** before busy season
- **Sharpen cutting tools** professionally if needed
- **Update inventory** and replace missing items

### Fall Storage Prep
- **Deep cleaning** before storage
- **Rust prevention** treatment
- **Battery maintenance** - Proper charging and storage
- **Climate control** - Protect from temperature extremes

## Tool-Specific Maintenance

### Circular Saws
- Keep base plate flat and smooth
- Check blade guard operation
- Lubricate height and bevel adjustments
- Replace brushes when worn

### Drills
- Chuck maintenance - keep clean and lubricated
- Check clutch operation (if equipped)
- Inspect and replace bits regularly
- Battery care for cordless models

### Sanders
- Check pad flatness and attachment
- Clean dust collection system
- Inspect power cord for damage
- Replace worn backup pads

## Sharpening and Replacement

### When to Sharpen
- **Cutting requires excessive force**
- **Poor quality cuts or finishes**
- **Burning or excessive heat**
- **Tear-out or chipping increases**

### Professional vs. DIY
**DIY Sharpening:**
- Hand planes and chisels
- Basic saw blades
- Drill bits (with proper jigs)
- Knives and utility blades

**Professional Sharpening:**
- Carbide-tipped blades
- Complex profiles
- Precision grinding
- Damaged tools requiring repair

## Storage Best Practices

### Climate Control
- **Temperature:** Avoid extremes and rapid changes
- **Humidity:** Keep below 50% to prevent rust
- **Ventilation:** Allow air circulation
- **Protection:** Use desiccants in tool boxes

### Organization
- **Shadow boards** for hand tools
- **Proper cases** for power tools
- **Blade storage** in protective sleeves
- **Easy access** to frequently used items

## Rust Prevention
### Prevention Methods
- **Wax coating** on metal surfaces
- **Oil film** on carbon steel tools
- **Desiccant packs** in storage areas
- **Regular use** - tools in use rarely rust

### Rust Removal
1. **Light rust:** Fine steel wool and oil
2. **Moderate rust:** Naval jelly or citric acid
3. **Heavy rust:** Professional restoration
4. **Prevention:** Immediately after removal

## Battery Tool Care
### Daily
- Remove batteries from tools after use
- Store batteries at room temperature
- Keep contacts clean

### Long-term
- Charge fully before long-term storage
- Store at 40-50% charge for Li-ion
- Replace batteries showing capacity loss
- Recycle old batteries properly

## Record Keeping
Track maintenance with simple logs:
- **Date of service**
- **Work performed**
- **Parts replaced**
- **Performance notes**
- **Next service due**

## Professional Service
Consider professional service for:
- **Annual tune-ups** on expensive tools
- **Warranty work** - don't void coverage
- **Complex repairs** beyond DIY ability
- **Calibration** of precision instruments

Proper maintenance is an investment in your tools and your projects. Spend a little time caring for your tools, and they'll take care of you for years to come.
"""
    ]
}

PROJECT_GUIDES = [
    """
# Kitchen Renovation Planning Guide: A Complete Approach

## Introduction
Kitchen renovations are among the most rewarding home improvement projects, offering both increased home value and improved daily living. This comprehensive guide will help you plan a successful kitchen renovation.

**Average ROI:** 60-80% of investment
**Timeline:** 6-12 weeks for major renovation
**Budget Range:** $15,000 - $50,000+ depending on scope

## Planning Phase (2-4 weeks)

### 1. Define Your Goals
- **Functionality improvements** - Better workflow, storage
- **Aesthetic updates** - Modern look, style changes
- **Efficiency gains** - Energy-efficient appliances
- **Value addition** - Features that increase home value

### 2. Set Your Budget
**Budget Breakdown (typical percentages):**
- Cabinets: 35-40%
- Labor: 20-25%
- Appliances: 15-20%
- Countertops: 10-15%
- Flooring: 7-10%
- Lighting/Electrical: 5%
- Plumbing: 5%
- Miscellaneous: 10-15%

### 3. Design Layout
**Work Triangle Concept:**
- Distance between sink, stove, refrigerator
- Total distance should be 12-26 feet
- No single leg longer than 9 feet
- Minimize obstructions

**Popular Layouts:**
- **Galley:** Efficient for narrow spaces
- **L-Shaped:** Good for corner locations
- **U-Shaped:** Maximum storage and counter space
- **Island:** Great for entertaining
- **Peninsula:** Island alternative for smaller spaces

## Pre-Construction Phase (2-3 weeks)

### Permits and Codes
**When permits are required:**
- Electrical work (new circuits)
- Plumbing relocations
- Structural changes
- Gas line modifications

**Building code considerations:**
- GFCI outlets near water sources
- Adequate ventilation
- Proper clearances around appliances
- Structural requirements for islands

### Material Selection
**Cabinets:**
- **Stock:** Pre-made, most affordable
- **Semi-custom:** Some modifications possible
- **Custom:** Built to exact specifications

**Countertops:**
- **Laminate:** Budget-friendly, many options
- **Granite:** Durable, natural beauty
- **Quartz:** Low maintenance, consistent patterns
- **Marble:** Luxurious but requires care
- **Butcher block:** Warm, natural option

**Flooring:**
- **Tile:** Durable, water-resistant
- **Hardwood:** Classic, can be refinished
- **Luxury vinyl:** Waterproof, realistic looks
- **Laminate:** Affordable wood-look option

## Construction Phase (6-10 weeks)

### Week 1-2: Demolition and Rough Work
- Remove old cabinets and appliances
- Electrical and plumbing rough-in
- HVAC modifications if needed
- Structural changes

### Week 3-4: Installation Prep
- Drywall repairs
- Primer and paint
- Flooring installation
- Electrical and plumbing finish work

### Week 5-8: Cabinet and Countertop Installation
- Cabinet installation and adjustment
- Countertop templating and installation
- Backsplash installation
- Interior cabinet accessories

### Week 9-10: Final Details
- Appliance installation and connection
- Light fixture installation
- Hardware installation
- Final inspections and touch-ups

## Budget Management Tips

### Ways to Save Money
- **Keep existing layout** - Avoid moving plumbing/gas lines
- **Mix high and low-end materials** - Splurge on visible areas
- **Do some work yourself** - Painting, simple demolition
- **Shop sales and clearance** - Plan around good deals

### Where Not to Compromise
- **Quality of cabinets** - They get the most use
- **Professional installation** - For plumbing, electrical, gas
- **Proper ventilation** - Inadequate ventilation causes problems
- **Structural work** - Never skip proper engineering

## Common Mistakes to Avoid

### Design Mistakes
- **Inadequate storage** - Plan for current and future needs
- **Poor lighting** - Layer ambient, task, and accent lighting
- **Wrong scale** - Ensure fixtures fit the space
- **Ignoring workflow** - Consider how you actually cook

### Construction Mistakes
- **Rushing decisions** - Take time to choose materials
- **Inadequate planning** - Have detailed drawings and schedules
- **Skipping permits** - Can cause problems at resale
- **Poor communication** - Stay in touch with contractors

## Working with Professionals

### When to Hire Professionals
- **Kitchen designer** - For complex layouts or design help
- **General contractor** - For major renovations
- **Electrician** - For new circuits or major electrical work
- **Plumber** - For gas lines or major plumbing changes

### Contractor Selection
- Get multiple detailed bids
- Check references and licenses
- Verify insurance coverage
- Have detailed written contracts
- Set payment schedules tied to milestones

## Living During Renovation

### Temporary Kitchen Setup
- **Microwave and refrigerator** - In dining room or garage
- **Hot plate or camp stove** - For basic cooking
- **Paper plates and disposables** - Minimize dishwashing
- **Cooler with ice** - Extra cold storage

### Managing Disruption
- Plan simple meals
- Stock up on non-perishables
- Consider eating out more frequently
- Have realistic expectations about timeline

## Final Inspection and Warranty

### Items to Check
- All appliances function properly
- Drawers and doors operate smoothly
- Electrical outlets and switches work
- Plumbing has no leaks
- Tile and countertop installation quality

### Warranty Documentation
- Save all receipts and warranty information
- Understand what's covered and for how long
- Schedule any needed follow-up work
- Create maintenance schedule for new features

A successful kitchen renovation requires careful planning, realistic budgeting, and patience during construction. The result will be a beautiful, functional space that enhances your daily life and home value.
""",
    """
# Deck Building Project Guide: From Planning to Completion

## Introduction
Building a deck is one of the most rewarding DIY projects for homeowners. This guide covers everything from initial planning to final finishing touches.

**Typical Timeline:** 3-5 weekends for DIY
**Skill Level:** Intermediate
**Cost Range:** $15-35 per square foot
**ROI:** 70-80% of investment

## Planning and Design Phase

### 1. Determine Deck Purpose and Size
**Common uses:**
- Outdoor dining and entertaining
- Relaxation and lounging
- Hot tub or spa area
- Garden access
- Pool deck

**Size considerations:**
- **Small (100-200 sq ft):** Intimate seating for 4-6 people
- **Medium (200-400 sq ft):** Dining and seating areas
- **Large (400+ sq ft):** Multiple activity zones

### 2. Site Analysis
**Factors to consider:**
- **Sun exposure** - Afternoon sun can be intense
- **Wind patterns** - Prevailing winds affect comfort
- **Views** - Maximize good views, screen poor ones
- **Privacy** - Consider sight lines from neighbors
- **Access** - Connection to house and yard

### 3. Code Requirements and Permits
**Typical requirements:**
- **Setbacks** - Distance from property lines
- **Height limits** - Usually 30" above grade requires rails
- **Railing height** - Minimum 36", 42" for higher decks
- **Stair requirements** - Rise, run, and handrail specifications
- **Structural requirements** - Beam spans, joist spacing

### Building Permit Process
1. Submit plans to building department
2. Pay fees (typically $100-500)
3. Schedule inspections
4. Receive approval before starting

## Material Selection

### Decking Materials
**Pressure-Treated Lumber:**
- **Pros:** Affordable, readily available
- **Cons:** Requires regular maintenance
- **Cost:** $2-5 per sq ft
- **Lifespan:** 10-15 years with maintenance

**Cedar:**
- **Pros:** Natural beauty, insect resistance
- **Cons:** More expensive, requires sealing
- **Cost:** $4-8 per sq ft
- **Lifespan:** 15-20 years

**Composite:**
- **Pros:** Low maintenance, consistent appearance
- **Cons:** Higher initial cost, can be hot in sun
- **Cost:** $8-12 per sq ft
- **Lifespan:** 25-30 years

**Tropical Hardwoods:**
- **Pros:** Extremely durable, beautiful
- **Cons:** Expensive, limited availability
- **Cost:** $10-15 per sq ft
- **Lifespan:** 30+ years

### Framing Materials
**Pressure-treated lumber** is standard for framing:
- Joists: 2x8 or 2x10 depending on span
- Beams: Double 2x10 or engineered lumber
- Posts: 4x4 or 6x6 depending on height
- Ledger board: 2x10 or 2x12

## Tools and Equipment Needed

### Essential Tools
- Circular saw or miter saw
- Drill/driver
- Level (4-foot minimum)
- Speed square
- Measuring tape
- Chalk line
- Post level
- Socket wrench set

### Specialized Tools
- Beam level or water level
- Post-hole digger or auger
- Impact driver
- Oscillating saw
- Router (for rounded edges)

### Safety Equipment
- Safety glasses
- Hearing protection
- Work gloves
- Dust masks
- First aid kit

## Step-by-Step Construction

### Step 1: Layout and Excavation (Weekend 1)
1. **Mark deck location** using stakes and string
2. **Check for utilities** - Call 811 before digging
3. **Mark post locations** according to plans
4. **Dig post holes** - 1/3 of post height plus 6"
5. **Add gravel base** - 4-6 inches in each hole

### Step 2: Install Posts and Beams (Weekend 2)
1. **Set posts in concrete** - Use fast-setting concrete
2. **Allow concrete to cure** - 24-48 hours
3. **Mark post heights** using water level
4. **Cut posts to height** with circular saw
5. **Install beams** using carriage bolts

### Step 3: Install Ledger Board and Joists (Weekend 3)
1. **Locate ledger board** on house wall
2. **Install flashing** behind ledger
3. **Attach ledger** with lag bolts into rim joist
4. **Mark joist locations** on ledger and beam
5. **Install joist hangers** on ledger board
6. **Cut and install joists** checking for square

### Step 4: Install Decking (Weekend 4)
1. **Start with full board** at house
2. **Maintain consistent spacing** - use nail as spacer
3. **Pre-drill ends** to prevent splitting
4. **Stagger joints** for strength and appearance
5. **Trim overhangs** with circular saw

### Step 5: Install Railings and Stairs (Weekend 5)
1. **Install railing posts** - typically 6-8 feet apart
2. **Cut and install top and bottom rails**
3. **Install balusters** - maximum 4" spacing
4. **Build stairs** according to code requirements
5. **Add handrails** if required

## Finishing and Maintenance

### Initial Finishing
**Pressure-treated lumber:**
- Wait 3-6 months before staining
- Clean with deck cleaner first
- Apply semi-transparent stain
- Consider clear sealer for natural look

**Cedar:**
- Can stain immediately
- Natural oil-based stains work best
- Reapply every 2-3 years

### Long-term Maintenance
**Annual tasks:**
- Clean with deck cleaner
- Inspect for loose fasteners
- Check railing stability
- Look for damaged boards

**Every 2-3 years:**
- Reapply stain or sealer
- Replace any damaged boards
- Tighten all fasteners

## Safety Considerations

### During Construction
- Use proper PPE at all times
- Have someone nearby when working
- Keep work area clean and organized
- Check ladder stability before climbing

### For Deck Use
- Install adequate lighting
- Ensure railings meet code
- Keep stairs clear of obstacles
- Regular inspection for safety

## Cost Breakdown Example (300 sq ft deck)

**Materials:**
- Lumber (PT): $1,200
- Hardware: $300
- Concrete: $100
- Stain/sealer: $150
- **Total materials:** $1,750

**Labor (if hired):**
- **Professional installation:** $2,000-4,000
- **DIY savings:** $2,000-4,000

## Common Mistakes to Avoid
- **Inadequate foundation** - Use proper footings
- **Poor drainage** - Slope away from house
- **Code violations** - Check requirements first
- **Rushing the project** - Take time for quality work
- **Skipping permits** - Can cause resale problems

A well-built deck provides years of outdoor enjoyment and adds significant value to your home. Take time to plan carefully, follow codes, and build with quality materials for the best results.
"""
]

async def create_knowledge_base_documents(conn: asyncpg.Connection) -> None:
    """Generate knowledge base articles and tutorials"""
    
    logging.info("Generating knowledge base documents...")
    
    documents = []
    
    # Generate how-to articles for different categories
    categories = await conn.fetch("SELECT category_name FROM retail.categories WHERE category_name IN ('ELECTRICAL', 'PLUMBING', 'POWER TOOLS', 'HAND TOOLS')")
    
    for category in categories:
        category_name = category['category_name'].lower()
        
        if category_name in HOW_TO_TEMPLATES:
            templates = HOW_TO_TEMPLATES[category_name]
            
            for i, template in enumerate(templates):
                # Fill in template variables
                content = template.format(
                    component_type=random.choice(["GFCI Outlet", "Light Switch", "Dimmer Switch", "Outlet"]) if "electrical" in category_name
                    else random.choice(["Faucet", "Toilet", "Valve", "Pipe Fitting"]) if "plumbing" in category_name
                    else "Tool",
                    difficulty=random.choice(["Beginner", "Intermediate", "Advanced"]),
                    time_estimate=random.choice(["30-60 minutes", "1-2 hours", "2-4 hours"]),
                    cost_range=random.choice(["$10-25", "$25-50", "$50-100", "$100-200"])
                )
                
                documents.append((
                    None,  # No specific product
                    'how_to_guide',
                    f"How-To: {category['category_name']} Guide {i+1}",
                    content,
                    {'category': category['category_name'], 'difficulty': 'intermediate', 'type': 'tutorial'}
                ))
    
    # Add project guides
    for i, guide in enumerate(PROJECT_GUIDES):
        documents.append((
            None,
            'project_guide',
            f"Project Guide: {['Kitchen Renovation', 'Deck Building'][i]}",
            guide,
            {'category': 'GENERAL', 'project_type': ['kitchen', 'deck'][i], 'difficulty': 'intermediate'}
        ))
    
    # Generate seasonal maintenance guides
    seasonal_guides = generate_seasonal_guides()
    for title, content in seasonal_guides:
        documents.append((
            None,
            'seasonal_guide',
            title,
            content,
            {'category': 'GENERAL', 'season': title.split()[0].lower(), 'type': 'maintenance'}
        ))
    
    # Insert all documents
    await insert_kb_documents_batch(conn, documents)
    
    logging.info(f"Generated {len(documents)} knowledge base documents")

def generate_seasonal_guides() -> List[tuple]:
    """Generate seasonal maintenance and project guides"""
    
    spring_guide = """
# Spring Home Maintenance Checklist: Preparing for the Season

## Introduction
Spring is the perfect time to assess winter damage and prepare your home for the warmer months ahead. This comprehensive checklist will help ensure your home is ready for spring and summer.

## Exterior Maintenance

### Roof and Gutters
- **Inspect roof** for missing or damaged shingles
- **Clean gutters** and downspouts thoroughly
- **Check flashing** around chimneys and vents
- **Trim overhanging branches** that could damage roof
- **Schedule professional inspection** if needed

### Siding and Paint
- **Wash exterior siding** with mild detergent
- **Inspect caulking** around windows and doors
- **Touch up paint** on trim and siding
- **Check for pest damage** or wood rot
- **Power wash deck** and outdoor furniture

### Windows and Doors
- **Clean windows** inside and out
- **Check weatherstripping** and replace if worn
- **Lubricate hinges** and locks
- **Inspect screens** for holes or damage
- **Test security features** on doors and windows

## HVAC System Preparation

### Air Conditioning
- **Replace air filters** (if not already done)
- **Clean around outdoor unit** - remove debris
- **Schedule professional tune-up** before hot weather
- **Test thermostat** programming and batteries
- **Check insulation** around ducts

### Ventilation
- **Clean bathroom exhaust fans** 
- **Check kitchen range hood** filter
- **Inspect attic ventilation** for blockages
- **Open windows** for fresh air circulation

## Plumbing Tasks

### Outdoor Plumbing
- **Turn on outdoor water** supply slowly
- **Check for freeze damage** to pipes and faucets
- **Inspect sprinkler system** and repair as needed
- **Test garden hoses** for leaks
- **Clean and store** hose reels properly

### Indoor Plumbing
- **Check for leaks** throughout the house
- **Test sump pump** operation (if applicable)
- **Drain and refill** water heater (annual maintenance)
- **Clear any clogged drains** 
- **Check toilet tanks** for efficient operation

## Yard and Garden Preparation

### Lawn Care
- **Rake up remaining** winter debris
- **Overseed bare spots** in lawn
- **Apply fertilizer** appropriate for your grass type
- **Edge flower beds** and walkways
- **Service lawn mower** - oil change, blade sharpening

### Garden and Landscaping
- **Prune shrubs and trees** before new growth
- **Clean up garden beds** - remove dead plants
- **Add fresh mulch** around plants
- **Test soil pH** and amend as needed
- **Plant cool-season crops** and flowers

## Safety and Security

### Smoke and Carbon Monoxide Detectors
- **Test all alarms** monthly
- **Replace batteries** in battery-operated units
- **Check expiration dates** on detectors
- **Clean dust** from detector covers
- **Replace old units** (over 10 years old)

### Home Security
- **Test security system** and cameras
- **Check outdoor lighting** - replace bulbs
- **Inspect fence gates** and locks
- **Update emergency contact** information
- **Review and practice** emergency plans

## Energy Efficiency Projects

### Insulation and Air Sealing
- **Check attic insulation** levels
- **Seal air leaks** around windows and doors
- **Caulk gaps** in basement or crawl space
- **Add weatherstripping** where needed
- **Consider energy audit** for improvements

### Lighting Upgrades
- **Switch to LED bulbs** for energy savings
- **Install motion sensors** for outdoor lighting
- **Add timer switches** for convenience
- **Upgrade to smart thermostats** if desired

## Planning Summer Projects

### Project Preparation
- **Make list** of desired improvements
- **Get quotes** from contractors for major work
- **Order materials** early to avoid shortages
- **Schedule projects** to avoid conflicts
- **Apply for permits** if required

### Tool and Equipment Maintenance
- **Service power tools** - clean and lubricate
- **Sharpen blades** on mowers and tools
- **Check safety equipment** - replace worn items
- **Organize workshop** for efficiency
- **Update first aid kits**

Spring maintenance prevents small problems from becoming expensive repairs. Taking time now to address these items will save money and ensure a comfortable, efficient home throughout the year.
"""

    fall_guide = """
# Fall Home Maintenance: Preparing for Winter

## Introduction
Fall maintenance is crucial for protecting your home during harsh winter weather. These tasks will help prevent costly damage and ensure your home stays warm and efficient.

## Heating System Preparation

### Furnace Maintenance
- **Replace furnace filter** - start of heating season
- **Schedule professional tune-up** before cold weather
- **Test thermostat** operation and programming
- **Check for unusual noises** or odors when running
- **Clear area around furnace** - remove flammable items

### Ductwork and Vents
- **Clean air ducts** if not done recently
- **Check ductwork** for leaks or disconnections
- **Ensure vents are unblocked** by furniture or debris
- **Consider duct sealing** for efficiency improvements

### Alternative Heating
- **Clean chimney and fireplace** before use
- **Check wood stove** gaskets and chimney
- **Stock firewood** in dry, covered area
- **Test space heaters** and check safety features
- **Install fresh batteries** in carbon monoxide detectors

## Weatherization Projects

### Windows and Doors
- **Install storm windows** or plastic sheeting
- **Caulk around window frames** and door jambs
- **Add or replace weatherstripping** 
- **Check door thresholds** for gaps
- **Consider window treatments** for insulation

### Exterior Sealing
- **Seal foundation cracks** before freezing
- **Caulk exterior penetrations** (pipes, vents, wires)
- **Check roof flashing** and repair if needed
- **Inspect siding** for gaps or damage
- **Weatherize outdoor faucets** and pipes

## Gutter and Roof Maintenance

### Gutter Cleaning
- **Remove leaves and debris** thoroughly
- **Check downspouts** for proper drainage
- **Repair loose gutters** or downspouts
- **Install gutter guards** if desired
- **Ensure water flows away** from foundation

### Roof Inspection
- **Look for loose or missing shingles**
- **Check flashing** around chimneys and vents
- **Clean roof valleys** of debris
- **Trim overhanging branches**
- **Schedule repairs** before winter weather

## Plumbing Winterization

### Outdoor Plumbing
- **Drain and shut off** outdoor water lines
- **Remove and store** garden hoses
- **Install faucet covers** for freeze protection
- **Drain sprinkler systems** completely
- **Insulate exposed pipes** in unheated areas

### Indoor Pipe Protection
- **Insulate pipes** in crawl spaces and basements
- **Seal air leaks** near plumbing
- **Know location** of main water shut-off
- **Keep cabinet doors open** during cold snaps
- **Let faucets drip** during extreme cold

## Landscaping and Yard Work

### Tree and Shrub Care
- **Prune dead or damaged branches**
- **Rake and compost** fallen leaves
- **Protect tender plants** with burlap or mulch
- **Water thoroughly** before ground freezes
- **Apply dormant oil** to fruit trees if needed

### Lawn and Garden
- **Final mowing** - cut slightly shorter than summer
- **Overseed** thin areas in lawn
- **Apply fall fertilizer** with winter nutrients
- **Plant spring bulbs** before ground freezes
- **Clean up vegetable garden** and compost debris

## Equipment Winterization

### Lawn and Garden Equipment
- **Drain fuel** from mowers and tillers
- **Change oil** in gas-powered equipment
- **Clean and store** garden tools properly
- **Service snow blower** - oil, plugs, belts
- **Check snow shovels** and ice melt supplies

### Outdoor Furniture
- **Clean and store** cushions and umbrellas
- **Cover or store** outdoor furniture
- **Drain and store** decorative fountains
- **Secure loose items** that could blow around
- **Store grills** in protected area

## Emergency Preparedness

### Winter Emergency Kit
- **Flashlights and batteries**
- **Battery or hand-crank radio**
- **First aid supplies**
- **Emergency food and water** (3-day supply)
- **Warm blankets and clothing**
- **Ice melt and snow shovels**

### Power Outage Preparation
- **Test backup generator** if you have one
- **Charge portable devices** and power banks
- **Know how to shut off** utilities if needed
- **Have alternate heating source** plan
- **Keep car gas tank full**

## Indoor Air Quality

### Humidity Control
- **Install or service humidifier** - dry winter air
- **Check for air leaks** that affect humidity
- **Monitor humidity levels** - ideal 30-50%
- **Ensure proper ventilation** in bathrooms
- **Consider air purifier** for dust and allergens

Fall preparation protects your investment and ensures family comfort during winter months. Address these items systematically, and you'll avoid many common winter problems.
"""

    return [
        ("Spring Home Maintenance Checklist", spring_guide),
        ("Fall Home Maintenance Guide", fall_guide)
    ]

async def insert_kb_documents_batch(conn: asyncpg.Connection, documents: List) -> None:
    """Insert knowledge base documents"""
    await conn.executemany("""
        INSERT INTO retail.product_documents 
        (product_id, document_type, title, content, metadata)
        VALUES ($1, $2, $3, $4, $5)
    """, documents)
    
    logging.info(f"Inserted {len(documents)} knowledge base documents")

async def main() -> None:
    """Main function to generate knowledge base content"""
    try:
        POSTGRES_CONFIG = {
            'host': 'db',
            'port': 5432,
            'user': 'postgres',
            'password': 'P@ssw0rd!',
            'database': 'zava'
        }
        
        conn = await asyncpg.connect(**POSTGRES_CONFIG)
        logging.info("Connected to PostgreSQL for knowledge base generation")
        
        await create_knowledge_base_documents(conn)
        
        # Show statistics
        stats = await conn.fetch("""
            SELECT document_type, COUNT(*) as count
            FROM retail.product_documents
            WHERE document_type IN ('how_to_guide', 'project_guide', 'seasonal_guide')
            GROUP BY document_type
            ORDER BY count DESC
        """)
        
        logging.info("Knowledge base document statistics:")
        for stat in stats:
            logging.info(f"  {stat['document_type']}: {stat['count']} documents")
        
        await conn.close()
        
    except Exception as e:
        logging.error(f"Error in knowledge base generation: {e}")
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
