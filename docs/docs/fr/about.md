## Projet Azure AI Foundry

## Modèles requis pour Zava DIY

## Génération de données synthétiques pour Zava DIY

Zava DIY est un outil conçu pour aider les développeurs à créer des données synthétiques à des fins de test et de développement. Il permet aux utilisateurs de générer des jeux de données réalistes qui peuvent être utilisés dans diverses applications, en s'assurant que les données répondent aux exigences spécifiques sans compromettre la confidentialité ou la sécurité.

La base de données comprend :

- **8 magasins** à travers l'État de Washington, chacun avec des données d'inventaire et de ventes uniques
- **Plus de 50 000 dossiers clients** à travers l'État de Washington et en ligne
- **Plus de 400 produits DIY** incluant des outils, équipements d'extérieur et fournitures d'amélioration résidentielle
- **Plus de 400 images de produits** liées à la base de données pour les recherches basées sur l'image
- **Plus de 200 000 transactions de commandes** avec un historique détaillé des ventes
- **Plus de 3 000 articles d'inventaire** répartis sur plusieurs magasins
- **Intégrations d'images** pour les images de produits permettant des recherches de similarité alimentées par l'IA (encodées en utilisant [openai/clip-vit-base-patch32](https://huggingface.co/openai/clip-vit-base-patch32/blob/main/README.md){:target="_blank"})
- **Intégrations de texte** pour les descriptions de produits améliorant les capacités de recherche et de recommandation [openai/text-embedding-3-small](https://ai.azure.com/catalog/models/text-embedding-3-small){:target="_blank"}

La base de données prend en charge les requêtes complexes et l'analyse, permettant un accès efficace aux données de ventes, d'inventaire et de clients. La sécurité au niveau des lignes PostgreSQL (RLS) restreint les agents uniquement aux données de leurs magasins assignés, garantissant la sécurité et la confidentialité.

*Traduit en utilisant GitHub Copilot et GPT-4o.*
