Esta aplicación de taller está diseñada para educación y adaptación, y no está destinada para uso en producción tal como está. No obstante, sí demuestra algunas mejores prácticas para seguridad.

## Ataques SQL Maliciosos

Una preocupación común con SQL generado por LLM es el riesgo de inyección o consultas dañinas. Estos riesgos se mitigan limitando los permisos de la base de datos.

Esta aplicación usa PostgreSQL con privilegios restringidos para el agente y se ejecuta en un entorno seguro. La Seguridad a Nivel de Fila (RLS) asegura que los agentes accedan solo a datos de sus tiendas asignadas.

En entornos empresariales, los datos típicamente se extraen a una base de datos o almacén de solo lectura con un esquema simplificado. Esto asegura acceso seguro, performante y de solo lectura para el agente.

## Aislamiento en Sandbox

Esto usa el [Intérprete de Código del Servicio de Agentes de IA de Azure](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} para crear y ejecutar código bajo demanda. El código se ejecuta en un entorno de ejecución aislado para prevenir que el código tome acciones que estén más allá del alcance del agente.

*Traducido usando GitHub Copilot y GPT-4o.*
