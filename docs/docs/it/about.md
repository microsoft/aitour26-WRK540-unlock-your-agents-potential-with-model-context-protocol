## Modelli richiesti per Zava DIY

- gpt-4o-mini
- text-embedding-small-3

## Generazione di Dati Sintetici per Zava DIY

Zava DIY è uno strumento progettato per aiutare gli sviluppatori a creare dati sintetici per test e scopi di sviluppo. Permette agli utenti di generare dataset realistici che possono essere utilizzati in varie applicazioni, assicurandosi che i dati soddisfino requisiti specifici senza compromettere la privacy o la sicurezza.

[Zava DIY Product Dataset](https://github.com/microsoft/ai-tour-26-zava-diy-dataset-plus-mcp/tree/main){:target="_blank"} Repository GitHub.

Il database include:

- **8 negozi** attraverso lo Stato di Washington, ognuno con inventario e dati di vendita unici
- **50.000+ record di clienti** attraverso lo Stato di Washington e online
- **400+ prodotti fai-da-te** inclusi strumenti, attrezzatura outdoor e forniture per la casa
- **400+ immagini di prodotti** collegate al database per ricerche basate su immagini
- **200.000+ transazioni di ordini** con storico vendite dettagliato
- **3000+ articoli di inventario** attraverso più negozi
- **Embedding di immagini** per immagini di prodotti che abilitano ricerche di similarità alimentate da AI (codificate usando [openai/clip-vit-base-patch32](https://huggingface.co/openai/clip-vit-base-patch32/blob/main/README.md){:target="_blank"})
- **Embedding di testo** per descrizioni di prodotti che migliorano le capacità di ricerca e raccomandazione [openai/text-embedding-3-small](https://ai.azure.com/catalog/models/text-embedding-3-small){:target="_blank"}

Il database supporta query complesse e analytics, abilitando accesso efficiente a vendite, inventario e dati dei clienti. PostgreSQL Row Level Security (RLS) limita gli agenti solo ai dati per i loro negozi assegnati, garantendo sicurezza e privacy.

## Dataset Prodotti Zava DIY

Il database PostgreSQL di Zava DIY fornisce un ecosistema retail completo con pattern di dati realistici:

| Componente            | Conteggio | Descrizione                                                   |
| --------------------- | --------- | ------------------------------------------------------------- |
| **Clienti**           | 50.000+   | Profili demografici realistici attraverso lo Stato di Washington |
| **Prodotti**          | 400+      | Catalogo completo fai-da-te per miglioramenti casa           |
| **Negozi**            | 8         | Località fisiche + online attraverso lo Stato di Washington  |
| **Articoli Ordine**   | 200.000+  | Articoli di linea dettagliati con prezzi e quantità          |
| **Record Inventario** | 3.000+    | Livelli di stock specifici per negozio                       |
| **Embedding Vettori** | 400+      | Ricerca di similarità prodotti alimentata da AI              |

### 🏪 Località Negozi

- **Negozi ad Alto Traffico**: Seattle, Bellevue, Online
- **Negozi Regionali**: Tacoma, Spokane
- **Mercati Specializzati**: Everett, Redmond, Kirkland
- **Distribuzione Geografica**: Penetrazione realistica del mercato dello Stato di Washington

### 📦 Categorie Prodotti

Il dataset include le seguenti categorie di prodotti con tutti i prodotti disponibili:

- **Elettrico**: AFCI Breaker 15-Amp, AFCI Outlet 15-Amp, Armored Cable BX 12-2, Ceiling Box with Bracket, Color-Coded Tape Set, Dimmer Switch LED, Double Pole Breaker 30A, EMT Conduit 1/2-inch, Flexible Conduit 1/2-inch, Friction Tape, GFCI Breaker 20-Amp, GFCI Outlet 20-Amp, Grease Cap Wire Nuts, Heavy Duty Cord 100ft, High-Temp Electrical Tape, Indoor Extension Cord 25ft, Junction Box 4x4, LED Flush Mount Ceiling, Large Wire Nuts, Liquid-Tight Conduit, Motion Sensor Switch, Multi-Outlet Power Strip, Old Work Box, Outdoor Extension Cord 50ft, Outdoor Flood Light LED, Outlet Box Single Gang, PVC Conduit 3/4-inch, Pendant Light Kitchen, Push-In Connectors, Retractable Cord Reel, Rigid Conduit 1-inch, Romex Wire 12-2 250ft, Romex Wire 14-2 250ft, Self-Fusing Silicone Tape, Single Pole Breaker 15A, Single Pole Breaker 20A, Single Pole Switch, Standard Outlet 15-Amp, THHN Wire 12 AWG, Three-Way Switch, Timer Switch, Track Lighting Kit, Twist-On Connectors, USB Outlet with Charging, Underground Wire 12-2, Vanity Light 3-Bulb, Vinyl Electrical Tape, Weather Resistant Outlet, Weatherproof Box, Wire Nut Assortment

- **Giardino & Esterno**: All-Purpose Fertilizer 50lb, Anvil Pruners Heavy Duty, Cactus Potting Mix, Cedar Mulch 3 Cu Ft, Ceramic Planter 12-inch, Drinking Water Safe Hose, Expandable Hose 100-foot, Flower Seed Mix Wildflower, Garden Hose 50-foot, Garden Rake Steel Tines, Garden Soil Enriched, Garden Spade Long Handle, Grass Seed Sun & Shade, Hanging Basket Planter, Hardwood Mulch 2 Cu Ft, Heavy Duty Hose 75-foot, Herb Garden Seed Set, Impact Sprinkler, In-Ground Sprinkler Head, LED Flood Light 30W, Landscape Spotlight Kit, Lawn Fertilizer Spring, Misting Sprinkler Kit, Organic Compost 40lb, Organic Heirloom Seeds, Oscillating Sprinkler, Plastic Planter Set, Pole Saw Pruner 8-foot, Potting Mix Premium 40lb, Rotary Sprinkler 3-Arm, Rubber Mulch Black, Seed Starting Mix, Self-Watering Planter, Slow Release Granules, Soaker Hose 25-foot, Solar Deck Light Set, Solar Path Light Set, Straw Mulch Bale, String Lights 48-foot, Tomato Plant Food, Topsoil Screened 40lb, Vegetable Seed Starter Kit, Wooden Barrel Planter

- **Utensili Manuali**: Adjustable Wrench 10-inch, Ball Peen Hammer 12oz, Ball-End Hex Set, Combination Wrench Set SAE, Coping Saw, Digital Caliper 6-inch, Finishing Hammer 13oz, Flathead Screwdriver Set, Folding Rule 6-foot, Insulated Screwdriver Set, Level 24-inch, Lineman's Pliers 9-inch, Locking Pliers 10-inch, Long Arm Hex Set, Metric Hex Key Set, Metric Wrench Set, Needle-Nose Pliers 6-inch, Phillips Screwdriver Set, Pipe Wrench Set, Precision Screwdriver Kit, Professional Claw Hammer 16oz, Ratcheting Screwdriver, Riffler File Set, SAE Hex Key Set, Sledge Hammer 3lb, Speed Square 7-inch, T-Handle Hex Set, Tape Measure 25-foot, Torque Wrench 1/2-drive, Wire Stripping Pliers, Wood Rasp Set

- **Ferramenta**: Angle Bracket 4-inch, Barrel Latch 4-inch, Brad Nails 18-gauge, Butt Hinge 3-1/2 inch, Cabinet Knob Set Brushed Nickel, Cabinet Lock Cam Type, Cabinet Pull 4-inch Centers, Carriage Bolt Set, Chain Lock Door Security, Common Nail Assortment, Concealed Cabinet Hinge, Countertop Support Bracket, Deadbolt Lock Keyed, Deck Screws 2-1/2 inch, Door Handle Lever Set, Door Knob Lock Set, Drawer Pull 5-inch, Drywall Screws 1-5/8 inch, Eye Bolts Assorted, Fender Washer Kit, Finish Nails 2-inch, Fixed Caster 3-inch, Flat Washer Assortment SAE, Floating Shelf Bracket, Furniture Caster Set, Hex Bolt Kit Grade 5, Hook and Eye Latch, L-Bracket Galvanized, Lag Bolts 1/2 x 6-inch, Lock Washer Set, Locking Caster Set, Machine Screws Kit, Masonry Nails, Metric Washer Assortment, Padlock Set Keyed Alike, Piano Hinge 2-foot, Pneumatic Caster 4-inch, Roofing Nails 1-1/4 inch, Rubber Washer Set, Security Hasp 6-inch, Self-Tapping Screws, Shelf Bracket 8-inch, Slide Bolt Latch, Spring Hinge Self-Closing, Strap Hinge Heavy Duty, Swivel Caster 2-inch, T-Handle Cabinet Hardware, Thumb Latch Galvanized, Toggle Bolt Set, Wood Screw Assortment

- **Legname & Materiali da Costruzione**: Advantech Subflooring, Baseboard Molding 8ft, Birch Plywood 4x8x1/2, Blown-In Insulation R-30, CDX Plywood 4x8x3/4, Cedar 2x4x8, Cedar Board 1x8x10, Cedar Post 6x6x8, Chair Rail Molding, Crack Resistant Mix, Crown Molding Pine 8ft, Deck Post 6x6x10, Douglas Fir 2x6x10, Durock Cement Board, Exterior Cement Board, Fast-Set Concrete 50lb, Fiberglass Batts R-13, Fire Resistant Drywall, Foam Board Insulation, Hardiebacker 3x5x1/4, High Strength Mix 80lb, Lightweight Drywall 4x8, MDF Trim Board 1x4, Marine Plywood 4x8x3/4, Moisture Resistant Drywall, OSB Sheathing 4x8x7/16, OSB Siding Panel, OSB Subflooring 4x8x3/4, PT Landscape Timber, PT Post 4x4x8, PVC Trim Board 1x6, Permabase Board 4x8, Pine Board 1x4x8, Pine Stud 2x4x8, Poplar Board 1x6x8, Pressure Treated 2x4x8, Pressure Treated Plywood, Quarter Round 8ft, Quikrete Mix 80lb, Ready Mix Concrete 60lb, Reflective Insulation, Round Fence Post 8ft, Soundproof Drywall 4x8, Spray Foam Kit, Standard Drywall 4x8x1/2, Treated 2x8x12 Joist, Window Casing Set, WonderBoard Lite, ZIP System Sheathing

- **Vernici & Finiture**: Aerosol Primer Spray, Angled Brush Set, Artist Detail Brush Set, Canvas Drop Cloth 9x12, Canvas Runner 4x15, Clear Polyurethane Satin, Deck and Fence Stain, Disposable Paint Tray Set, Drywall Primer, Elastomeric Exterior Paint, Extension Pole 4-foot, Exterior Acrylic Paint, Exterior Latex Paint Satin, Exterior Primer-Paint Combo, Floor Polyurethane, Foam Brush Set, Gel Stain, Gloss Polyurethane, Gloss Spray Paint, Interior Eggshell Paint, Interior Semi-Gloss Paint, Masonry Primer, Matte Finish Spray Paint, Metal Paint Tray 9-inch, Metal Primer, Microfiber Roller Covers, Mini Roller Kit 4-inch, Nap Roller Cover Set, Natural Bristle Brush Set, Oil-Based Polyurethane, Oil-Based Wood Stain, One-Coat Interior Paint, Paint Bucket Grid, Paint Spray Gun, Paint Tray Liner Set, Paper Drop Cloth, Plastic Drop Cloth, Pre-Taped Masking Film, Premium Interior Latex Flat, Roller Frame 9-inch, Rolling Tray with Grid, Rust Prevention Spray, Semi-Transparent Deck Stain, Solid Color Deck Stain, Stain-Blocking Primer, Synthetic Brush Set, Textured Spray Paint, Universal Bonding Primer, Water-Based Polyurethane, Water-Based Wood Stain, Zero VOC Interior Paint

- **Idraulica**: Angle Stop Valve, Ball Valve 1/2-inch, Bathroom Lavatory Faucet, Check Valve 1-inch, Compression Fittings, Copper Fitting Kit, Copper Pipe 1-inch Type L, Copper Pipe 1/2-inch Type L, Copper Pipe 3/4-inch Type L, Drain Cleaning Chemical, Drain Snake 25-foot, Fiberglass Pipe Insulation, Fill Valve Assembly, Flexible PVC Pipe, Foam Pipe Insulation 1/2, Gate Valve 3/4-inch, Heavy Duty Teflon Tape, Hydro Jet Drain Cleaner, Kitchen Sink Faucet, Outdoor Spigot Faucet, PTFE Thread Tape White, PVC Elbow Assortment, PVC Pipe 1-1/2 inch x 10ft, PVC Pipe 2-inch x 10ft, PVC Pipe 3-inch x 10ft, PVC Pipe 4-inch x 10ft, PVC Tee Fitting Set, Pink Plumber's Tape, Pipe Dope Stick, Pipe Heat Tape, Pipe Insulation 3/4-inch, Pipe Insulation Tape, Pipe Joint Compound, Pipe Thread Sealant Paste, Plumber's Grease, Plumber's Putty 14oz, Plunger Set, Pre-Insulated Copper Pipe, Pressure Relief Valve, Push-Fit Connectors, Shower Faucet Trim Kit, Silicone Plumber's Putty, Soft Copper Coil 1/2-inch, Toilet Auger, Toilet Flapper Universal, Toilet Repair Kit Complete, Toilet Seat Standard, Toilet Wax Ring, Utility Sink Faucet, Yellow Gas Line Tape

- **Utensili Elettrici**: Angle Grinder 4-1/2 inch, Barrel Grip Jigsaw, Basic Miter Saw 10-inch, Belt Sander 3x21 inch, Benchtop Drill Press, Brushless Impact Driver, Circular Saw 7-1/4 inch, Compact Belt Sander 3x18, Compact Impact Driver, Compact Recip Saw, Compound Miter Saw 10-inch, Cordless Angle Grinder, Cordless Circular Saw 6-1/2, Cordless Drill 18V Li-Ion, Cordless Jigsaw 20V, Cordless Miter Saw 10-inch, Cordless Recip Saw 18V, Cordless Router 18V, Cut-Off Tool 3-inch, Drywall Sander, File Belt Sander, Fixed Base Router 1-3/4 HP, Hammer Drill 1/2-inch, Heavy Duty Jigsaw, Impact Drill 20V, Impact Driver 18V, Impact Wrench 1/2-inch, Large Angle Grinder 7-inch, Mini Circular Saw 4-1/2, Miter Saw Stand, Mouse Sander, Multi-Tool Oscillating, Orbital Sander 1/4 Sheet, Palm Sander, Plunge Router 2-1/4 HP, Random Orbit Sander 5-inch, Reciprocating Saw Corded, Right Angle Drill, Right Angle Impact, Router Table Combo, Scrolling Jigsaw, Sliding Miter Saw 12-inch, Stationary Belt Sander, Track Saw, Trim Router 1 HP, Variable Speed Belt Sander, Variable Speed Grinder, Variable Speed Jigsaw, Worm Drive Saw

- **Deposito & Organizzazione**: Adjustable Height Workbench, Base Cabinet with Drawers, Ceiling Hook Kit, Ceiling Storage Rack 4x8, Ceiling Track System, Chemical Storage Cabinet, Clear Storage Bin 27-Quart, Corner Shelf Unit, Craft Storage Drawers, Desktop Organizer Drawers, Folding Workbench Portable, Garage Ceiling Hoist, Garage Workbench Kit, Gym Style Locker Bank, Heavy Duty Rack System, Heavy Duty Tote 35-Gallon, Heavy Duty Wall Hook Set, Heavy Duty Workbench 6-foot, Large Drawer Unit 10-Drawer, Magnetic Tool Holder, Metal Locker 2-Door, Metal Pegboard Gray, Metal Storage Cabinet 72-inch, Metal Tool Cabinet, Mobile Work Cart, Modular Cabinet System, Overhead Storage Platform, Pegboard Hook Set 50-piece, Pegboard Panel 4x8, Pegboard Storage Bins, Pegboard Tool Holder Set, Personal Storage Locker, Plastic Tool Box Set, Portable Tool Box 20-inch, Retractable Hose Hanger, Rolling Drawer Cart, Rolling Tool Chest 26-inch, Rubber Coated Hooks, Safety Net for Storage, Small Parts Organizer, Stackable Bin Set, Stackable Drawer Set, Steel Shelving 5-Tier, Tool Bag Canvas 18-inch, Wall Mount Cabinet, Weatherproof Storage Box, Wire Mesh Locker, Wire Shelving Chrome, Wooden Locker Bench, Wooden Storage Shelves

### 🌡️ Pattern Stagionali

Il dataset include variazioni stagionali realistiche:

- **Picco Primaverile**: Prodotti per vernici e giardino raggiungono il picco in Marzo-Maggio
- **Costruzioni Estive**: Utensili elettrici e legname raggiungono il picco in Giugno-Agosto
- **Preparazione Autunnale**: Prodotti ferramenta e deposito aumentano
- **Manutenzione Invernale**: Utensili manuali e progetti interni

### 💰 Modellazione Finanziaria

- **Margine lordo consistente del 33%** attraverso tutti i prodotti
- **Pattern di crescita anno su anno** (2020-2026)
- **Variazioni di prestazioni del negozio** basate sulla dimensione del mercato
- **Fluttuazioni di ricavi stagionali** allineate con la domanda dei prodotti
