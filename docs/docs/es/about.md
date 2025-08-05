## Proyecto de Azure AI Foundry

## Modelos requeridos para Zava DIY

## Generación de Datos Sintéticos para Zava DIY

Zava DIY es una herramienta diseñada para ayudar a los desarrolladores a crear datos sintéticos para pruebas y desarrollo. Permite a los usuarios generar conjuntos de datos realistas que pueden utilizarse en diversas aplicaciones, asegurando que los datos cumplan con requisitos específicos sin comprometer la privacidad o seguridad.

La base de datos incluye:

- **8 tiendas** en todo el estado de Washington, cada una con inventario único y datos de ventas
- **50,000+ registros de clientes** en todo el estado de Washington y en línea
- **400+ productos de bricolaje** incluyendo herramientas, equipo para exteriores y suministros para mejoras del hogar
- **400+ imágenes de productos** vinculadas a la base de datos para búsquedas basadas en imágenes
- **200,000+ transacciones de pedidos** con historial detallado de ventas
- **3000+ artículos de inventario** en múltiples tiendas
- **Embeddings de imágenes** para imágenes de productos que permiten búsquedas de similitud impulsadas por IA (codificadas usando [openai/clip-vit-base-patch32](https://huggingface.co/openai/clip-vit-base-patch32/blob/main/README.md){:target="_blank"})
- **Embeddings de texto** para descripciones de productos que mejoran las capacidades de búsqueda y recomendación [openai/text-embedding-3-small](https://ai.azure.com/catalog/models/text-embedding-3-small){:target="_blank"}

La base de datos soporta consultas complejas y analíticas, permitiendo acceso eficiente a datos de ventas, inventario y clientes. La Seguridad a Nivel de Fila (RLS) de PostgreSQL restringe a los agentes solo a los datos de las tiendas asignadas, asegurando seguridad y privacidad.

*Traducido usando GitHub Copilot y GPT-4o.*
