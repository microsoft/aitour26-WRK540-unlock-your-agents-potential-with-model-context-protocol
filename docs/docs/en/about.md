## Azure AI Foundry Project

## Models required for Zava DIY

## Synthentic Data Generation for Zava DIY

Zava DIY is a tool designed to help developers create synthetic data for testing and development purposes. It allows users to generate realistic datasets that can be used in various applications, ensuring that the data meets specific requirements without compromising privacy or security.

The database includes:

- **8 stores** across Washington State, each with unique inventory and sales data
- **50,000+ customer records** across Washington State and online
- **400+ DIY products** including tools, outdoor equipment, and home improvement supplies
- **400+ product images** linked to the database for image-based searches
- **200,000+ order transactions** with detailed sales history
- **3000+ inventory items** across multiple stores
- **Image embeddings** for product images enabling AI-powered similarity searches (encoded using [openai/clip-vit-base-patch32](https://huggingface.co/openai/clip-vit-base-patch32/blob/main/README.md){:target="_blank"})
- **Text embeddings** for product descriptions enhancing search and recommendation capabilities [openai/text-embedding-3-small](https://ai.azure.com/catalog/models/text-embedding-3-small){:target="_blank"}

The database supports complex queries and analytics, enabling efficient access to sales, inventory, and customer data. PostgreSQL Row Level Security (RLS) restricts agents to only the data for their assigned stores, ensuring security and privacy.