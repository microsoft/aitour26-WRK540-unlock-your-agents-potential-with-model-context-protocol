## Modèles requis pour Zava DIY

- gpt-4o-mini
- text-embedding-small-3

## Génération de données synthétiques pour Zava DIY

Zava DIY est un outil conçu pour aider les développeurs à créer des données synthétiques à des fins de test et de développement. Il permet aux utilisateurs de générer des jeux de données réalistes qui peuvent être utilisés dans diverses applications, en veillant à ce que les données répondent à des exigences spécifiques sans compromettre la confidentialité ou la sécurité.

[Jeu de données de produits Zava DIY](https://github.com/microsoft/ai-tour-26-zava-diy-dataset-plus-mcp/tree/main){:target="_blank"} Dépôt GitHub.

La base de données comprend :

- **8 magasins** dans l'État de Washington, chacun avec des données d'inventaire et de ventes uniques
- **Plus de 50 000 enregistrements clients** dans l'État de Washington et en ligne
- **Plus de 400 produits de bricolage** incluant outils, équipement d'extérieur et fournitures d'amélioration de la maison
- **Plus de 400 images de produits** liées à la base de données pour les recherches basées sur l'image
- **Plus de 200 000 transactions de commande** avec un historique de vente détaillé
- **Plus de 3 000 articles d'inventaire** répartis dans plusieurs magasins
- **Embeddings d'images** pour les images de produits permettant des recherches de similarité alimentées par l'IA (encodées en utilisant [openai/clip-vit-base-patch32](https://huggingface.co/openai/clip-vit-base-patch32/blob/main/README.md){:target="_blank"})
- **Embeddings de texte** pour les descriptions de produits améliorant les capacités de recherche et de recommandation [openai/text-embedding-3-small](https://ai.azure.com/catalog/models/text-embedding-3-small){:target="_blank"}

La base de données prend en charge les requêtes complexes et l'analyse, permettant un accès efficace aux données de vente, d'inventaire et clients. La sécurité au niveau des lignes PostgreSQL (RLS) restreint les agents aux seules données de leurs magasins assignés, garantissant la sécurité et la confidentialité.

## Jeu de données de produits Zava DIY

La base de données PostgreSQL Zava DIY fournit un écosystème de vente au détail complet avec des modèles de données réalistes :

| Composant             | Quantité | Description                                                |
| --------------------- | -------- | ---------------------------------------------------------- |
| **Clients**           | 50 000+  | Profils démographiques réalistes dans l'État de Washington |
| **Produits**          | 400+     | Catalogue complet d'amélioration de la maison de bricolage |
| **Magasins**          | 8        | Emplacements physiques + en ligne dans l'État de Washington |
| **Articles de commande** | 200 000+ | Articles détaillés avec prix et quantités                 |
| **Enregistrements d'inventaire** | 3 000+ | Niveaux de stock spécifiques par magasin              |
| **Embeddings vectoriels** | 400+ | Recherche de similarité de produits alimentée par l'IA     |

### 🏪 Emplacements des magasins

- **Magasins à fort trafic** : Seattle, Bellevue, En ligne
- **Magasins régionaux** : Tacoma, Spokane
- **Marchés spécialisés** : Everett, Redmond, Kirkland
- **Distribution géographique** : Pénétration réaliste du marché de l'État de Washington

### 📦 Catégories de produits

Le jeu de données comprend les catégories de produits suivantes avec tous les produits disponibles :

- **Électricité** : Disjoncteur AFCI 15A, Prise AFCI 15A, Câble blindé BX 12-2, Boîte de plafond avec support, Jeu de rubans colorés, Interrupteur variateur LED, Disjoncteur bipolaire 30A, Conduit EMT 1/2 pouce, Conduit flexible 1/2 pouce, Ruban isolant, Disjoncteur GFCI 20A, Prise GFCI 20A, Serre-fils à graisse, Cordon robuste 100 pieds, Ruban électrique haute température, Rallonge intérieure 25 pieds, Boîte de jonction 4x4, Plafonnier LED encastré, Gros serre-fils, Conduit étanche aux liquides, Interrupteur détecteur de mouvement, Multiprise de puissance, Boîte de rénovation, Rallonge extérieure 50 pieds, Projecteur extérieur LED, Boîte de prise simple, Conduit PVC 3/4 pouce, Lampe suspendue cuisine, Connecteurs à insertion, Enrouleur de cordon rétractable, Conduit rigide 1 pouce, Fil Romex 12-2 250 pieds, Fil Romex 14-2 250 pieds, Ruban silicone auto-fusionnant, Disjoncteur unipolaire 15A, Disjoncteur unipolaire 20A, Interrupteur simple, Prise standard 15A, Fil THHN 12 AWG, Interrupteur à trois voies, Interrupteur temporisé, Kit d'éclairage sur rail, Connecteurs à torsion, Prise USB avec charge, Câble souterrain 12-2, Applique de vanité 3 ampoules, Ruban électrique vinyle, Prise résistante aux intempéries, Boîte étanche, Assortiment de serre-fils

- **Jardin et extérieur** : Engrais tout usage 50 lb, Sécateur à enclume robuste, Terreau pour cactus, Paillis de cèdre 3 pi cu, Jardinière en céramique 12 pouces, Tuyau d'eau potable, Tuyau extensible 100 pieds, Mélange de graines de fleurs sauvages, Tuyau d'arrosage 50 pieds, Râteau de jardin à dents d'acier, Terre de jardin enrichie, Bêche de jardin à long manche, Graines de gazon soleil et ombre, Jardinière suspendue, Paillis de bois franc 2 pi cu, Tuyau robuste 75 pieds, Ensemble de graines de jardin d'herbes, Arroseur à impact, Tête d'arroseur enterré, Projecteur LED 30W, Kit de spot paysager, Engrais de pelouse printemps, Kit d'arroseur brumisateur, Compost organique 40 lb, Graines d'héritage biologique, Arroseur oscillant, Ensemble de jardinières en plastique, Scie-perche 8 pieds, Terreau premium 40 lb, Arroseur rotatif 3 bras, Paillis en caoutchouc noir, Mélange de démarrage de graines, Jardinière auto-arrosante, Granules à libération lente, Tuyau suintant 25 pieds, Ensemble de lumières de terrasse solaires, Ensemble de lumières de chemin solaires, Balle de paillis de paille, Guirlandes lumineuses 48 pieds, Nourriture pour plants de tomate, Terre végétale tamisée 40 lb, Kit de démarrage de graines de légumes, Jardinière en baril de bois

- **Outils à main** : Clé ajustable 10 pouces, Marteau à panne ronde 12 oz, Jeu d'hexagones à bout sphérique, Jeu de clés mixtes SAE, Scie à chantourner, Pied à coulisse numérique 6 pouces, Marteau de finition 13 oz, Jeu de tournevis plats, Règle pliante 6 pieds, Jeu de tournevis isolés, Niveau 24 pouces, Pince de monteur 9 pouces, Pince-étau 10 pouces, Jeu d'hexagones à long bras, Jeu de clés hexagonales métriques, Jeu de clés métriques, Pince à bec effilé 6 pouces, Jeu de tournevis Phillips, Jeu de clés à pipe, Kit de tournevis de précision, Marteau à panne fendue professionnel 16 oz, Tournevis à cliquet, Jeu de limes riffoir, Jeu de clés hexagonales SAE, Masse 3 lb, Équerre rapide 7 pouces, Jeu d'hexagones à poignée en T, Mètre ruban 25 pieds, Clé dynamométrique 1/2 pouce, Pince à dénuder, Jeu de râpes à bois

- **Quincaillerie** : Équerre d'angle 4 pouces, Loquet à barillet 4 pouces, Clous brad 18 jauges, Charnière bout à bout 3-1/2 pouce, Jeu de boutons d'armoire nickel brossé, Serrure d'armoire type came, Poignée d'armoire 4 pouces entraxe, Jeu de boulons carrossage, Verrou de chaîne sécurité porte, Assortiment de clous ordinaires, Charnière d'armoire dissimulée, Support de comptoir, Verrou à pêne dormant à clé, Vis de terrasse 2-1/2 pouce, Ensemble de poignée de porte à levier, Jeu de serrure de poignée de porte, Poignée de tiroir 5 pouces, Vis de cloison sèche 1-5/8 pouce, Boulons à œil assortis, Kit de rondelles de garde-boue, Clous de finition 2 pouces, Roulette fixe 3 pouces, Assortiment de rondelles plates SAE, Support d'étagère flottante, Jeu de roulettes de meuble, Kit de boulons hexagonaux grade 5, Loquet à crochet et œil, Équerre en L galvanisée, Tire-fonds 1/2 x 6 pouces, Jeu de rondelles de blocage, Jeu de roulettes verrouillables, Kit de vis mécaniques, Clous de maçonnerie, Assortiment de rondelles métriques, Jeu de cadenas à clé identique, Charnière piano 2 pieds, Roulette pneumatique 4 pouces, Clous de toiture 1-1/4 pouce, Jeu de rondelles en caoutchouc, Moraillon de sécurité 6 pouces, Vis autotaraudeuses, Support d'étagère 8 pouces, Loquet coulissant, Charnière à ressort auto-fermante, Charnière à sangle robuste, Roulette pivotante 2 pouces, Poignée en T quincaillerie d'armoire, Loquet à pouce galvanisé, Jeu de chevilles à bascule, Assortiment de vis à bois

- **Bois et matériaux de construction** : Sous-plancher Advantech, Moulure de plinthe 8 pi, Contreplaqué de bouleau 4x8x1/2, Isolant soufflé R-30, Contreplaqué CDX 4x8x3/4, Cèdre 2x4x8, Planche de cèdre 1x8x10, Poteau de cèdre 6x6x8, Moulure de cimaise, Mélange résistant aux fissures, Moulure couronne pin 8 pi, Poteau de terrasse 6x6x10, Sapin de Douglas 2x6x10, Panneau de ciment Durock, Panneau de ciment extérieur, Béton à prise rapide 50 lb, Matelas de fibre de verre R-13, Cloison sèche résistante au feu, Panneau d'isolant mousse, Hardiebacker 3x5x1/4, Mélange haute résistance 80 lb, Cloison sèche légère 4x8, Planche de garniture MDF 1x4, Contreplaqué marin 4x8x3/4, Cloison sèche résistante à l'humidité, Revêtement OSB 4x8x7/16, Panneau de bardage OSB, Sous-plancher OSB 4x8x3/4, Madrier de paysage traité sous pression, Poteau traité sous pression 4x4x8, Planche de garniture PVC 1x6, Panneau Permabase 4x8, Planche de pin 1x4x8, Montant de pin 2x4x8, Planche de peuplier 1x6x8, Traité sous pression 2x4x8, Contreplaqué traité sous pression, Quart de rond 8 pi, Mélange Quikrete 80 lb, Béton prêt à l'emploi 60 lb, Isolant réfléchissant, Poteau de clôture rond 8 pi, Cloison sèche insonorisante 4x8, Kit de mousse pulvérisée, Cloison sèche standard 4x8x1/2, Solive traitée 2x8x12, Ensemble de moulures de fenêtre, WonderBoard Lite, Revêtement système ZIP

- **Peinture et finitions** : Apprêt en aérosol, Jeu de pinceaux inclinés, Jeu de pinceaux de détail d'artiste, Bâche de toile 9x12, Chemin de toile 4x15, Polyuréthane transparent satiné, Teinture de terrasse et clôture, Jeu de bacs à peinture jetables, Apprêt de cloison sèche, Peinture extérieure élastomère, Perche d'extension 4 pieds, Peinture acrylique extérieure, Peinture latex extérieure satinée, Combo apprêt-peinture extérieure, Polyuréthane de plancher, Jeu de pinceaux mousse, Gel teinture, Polyuréthane brillant, Peinture en aérosol brillante, Peinture intérieure coquille d'œuf, Peinture intérieure semi-brillante, Apprêt de maçonnerie, Peinture en aérosol fini mat, Bac à peinture métal 9 pouces, Apprêt métal, Couvercles de rouleau microfibre, Kit de mini rouleau 4 pouces, Jeu de couvercles de rouleau nap, Jeu de pinceaux à soies naturelles, Polyuréthane à base d'huile, Teinture de bois à base d'huile, Peinture intérieure une couche, Grille de seau à peinture, Pistolet à peinture, Jeu de doublures de bac à peinture, Bâche de papier, Bâche de plastique, Film de masquage pré-collé, Latex intérieur premium mat, Cadre de rouleau 9 pouces, Bac roulant avec grille, Spray anti-rouille, Teinture de terrasse semi-transparente, Teinture de terrasse couleur solide, Apprêt bloquant les taches, Jeu de pinceaux synthétiques, Peinture en aérosol texturée, Apprêt d'adhérence universel, Polyuréthane à base d'eau, Teinture de bois à base d'eau, Peinture intérieure zéro COV

- **Plomberie** : Vanne d'arrêt d'angle, Vanne à bille 1/2 pouce, Robinet de lavabo de salle de bain, Clapet anti-retour 1 pouce, Raccords de compression, Kit de raccords de cuivre, Tuyau de cuivre 1 pouce Type L, Tuyau de cuivre 1/2 pouce Type L, Tuyau de cuivre 3/4 pouce Type L, Produit chimique de nettoyage de drain, Furet de drain 25 pieds, Isolant de tuyau en fibre de verre, Ensemble de valve de remplissage, Tuyau PVC flexible, Isolant de tuyau mousse 1/2, Vanne à guillotine 3/4 pouce, Ruban téflon robuste, Nettoyeur de drain hydro jet, Robinet d'évier de cuisine, Robinet de robinet extérieur, Ruban de filetage PTFE blanc, Assortiment de coudes PVC, Tuyau PVC 1-1/2 pouce x 10 pi, Tuyau PVC 2 pouces x 10 pi, Tuyau PVC 3 pouces x 10 pi, Tuyau PVC 4 pouces x 10 pi, Jeu de raccords en T PVC, Ruban de plombier rose, Bâton de graisse de tuyau, Câble chauffant de tuyau, Isolant de tuyau 3/4 pouce, Ruban d'isolant de tuyau, Composé de joint de tuyau, Pâte d'étanchéité de filetage de tuyau, Graisse de plombier, Mastic de plombier 14 oz, Jeu de ventouses, Tuyau de cuivre pré-isolé, Soupape de sécurité, Connecteurs à emboîtement, Kit de garniture de robinet de douche, Mastic de plombier silicone, Bobine de cuivre souple 1/2 pouce, Tarière de toilette, Clapet de toilette universel, Kit de réparation de toilette complet, Siège de toilette standard, Anneau de cire de toilette, Robinet d'évier utilitaire, Ruban de conduite de gaz jaune

- **Outils électriques** : Meuleuse d'angle 4-1/2 pouce, Scie sauteuse à poignée barillet, Scie à onglets de base 10 pouces, Ponceuse à bande 3x21 pouces, Perceuse à colonne d'établi, Visseuse à chocs sans balais, Scie circulaire 7-1/4 pouce, Ponceuse à bande compacte 3x18, Visseuse à chocs compacte, Scie réciprocante compacte, Scie à onglets composée 10 pouces, Meuleuse d'angle sans fil, Scie circulaire sans fil 6-1/2, Perceuse sans fil 18V Li-Ion, Scie sauteuse sans fil 20V, Scie à onglets sans fil 10 pouces, Scie réciprocante sans fil 18V, Défonceuse sans fil 18V, Outil de coupe 3 pouces, Ponceuse de cloison sèche, Ponceuse à bande de lime, Défonceuse à base fixe 1-3/4 HP, Perceuse à percussion 1/2 pouce, Scie sauteuse robuste, Perceuse à chocs 20V, Visseuse à chocs 18V, Clé à chocs 1/2 pouce, Grande meuleuse d'angle 7 pouces, Mini scie circulaire 4-1/2, Support de scie à onglets, Ponceuse souris, Multi-outil oscillant, Ponceuse orbitale 1/4 feuille, Ponceuse palmaire, Défonceuse plongeante 2-1/4 HP, Ponceuse orbitale aléatoire 5 pouces, Scie réciprocante filaire, Perceuse à angle droit, Chocs à angle droit, Combo table de défonceuse, Scie sauteuse à défilement, Scie à onglets coulissante 12 pouces, Ponceuse à bande stationnaire, Scie sur rail, Défonceuse de finition 1 HP, Ponceuse à bande à vitesse variable, Meuleuse à vitesse variable, Scie sauteuse à vitesse variable, Scie à vis sans fin

- **Rangement et organisation** : Établi à hauteur ajustable, Armoire de base avec tiroirs, Kit de crochets de plafond, Rack de stockage de plafond 4x8, Système de rail de plafond, Armoire de stockage chimique, Bac de stockage transparent 27 litres, Unité d'étagère d'angle, Tiroirs de rangement d'artisanat, Organisateur de bureau à tiroirs, Établi pliant portable, Palan de plafond de garage, Kit d'établi de garage, Banque de casiers style gymnase, Système de rack robuste, Bac robuste 35 gallons, Jeu de crochets muraux robustes, Établi robuste 6 pieds, Grande unité de tiroirs 10 tiroirs, Porte-outil magnétique, Casier métallique 2 portes, Panneau perforé métallique gris, Armoire de stockage métallique 72 pouces, Armoire à outils métallique, Chariot de travail mobile, Système d'armoire modulaire, Plateforme de stockage aérien, Jeu de crochets de panneau perforé 50 pièces, Panneau perforé 4x8, Bacs de stockage de panneau perforé, Jeu de porte-outils de panneau perforé, Casier de stockage personnel, Jeu de boîte à outils en plastique, Boîte à outils portable 20 pouces, Cintre de tuyau rétractable, Chariot à tiroirs roulant, Coffre à outils roulant 26 pouces, Crochets revêtus de caoutchouc, Filet de sécurité pour stockage, Organisateur de petites pièces, Jeu de bacs empilables, Jeu de tiroirs empilables, Étagère en acier 5 niveaux, Sac à outils toile 18 pouces, Armoire de montage mural, Boîte de stockage étanche, Casier en treillis métallique, Étagère en fil chromé, Banc de casier en bois, Étagères de stockage en bois

### 🌡️ Modèles saisonniers

Le jeu de données comprend des variations saisonnières réalistes :

- **Poussée printanière** : Les produits de peinture et de jardin atteignent leur pic en mars-mai
- **Construction d'été** : Les outils électriques et le bois atteignent leur pic en juin-août
- **Préparation d'automne** : Les produits de quincaillerie et de stockage augmentent
- **Entretien d'hiver** : Outils à main et projets d'intérieur

### 💰 Modélisation financière

- **Marge brute constante de 33%** sur tous les produits
- **Modèles de croissance d'année en année** (2020-2026)
- **Variations de performance des magasins** basées sur la taille du marché
- **Fluctuations saisonnières des revenus** alignées sur la demande de produits

*Traduit en utilisant GitHub Copilot.*
