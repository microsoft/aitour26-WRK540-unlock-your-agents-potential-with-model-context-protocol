## Arquitectura de la Solución

En este taller, crearás el Agente de Ventas de Zava: un agente conversacional diseñado para responder preguntas sobre datos de ventas, generar gráficos, proporcionar recomendaciones de productos y soportar búsquedas de productos basadas en imágenes para el negocio minorista de bricolaje de Zava.

## Componentes de la Aplicación del Agente

1. **Servicios de Microsoft Azure**

    Este agente está construido sobre servicios de Microsoft Azure.

      - **Modelo de IA generativa**: El LLM subyacente que impulsa esta aplicación es el LLM [Azure OpenAI gpt-4o-mini](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#how-do-i-access-the-gpt-4o-and-gpt-4o-mini-models){:target="_blank"}.

      - **Plano de Control**: La aplicación y sus componentes arquitectónicos se gestionan y monitorean usando el portal de [Azure AI Foundry](https://ai.azure.com){:target="_blank"}, accesible a través del navegador.

2. **Azure AI Foundry (SDK)**

    El taller se ofrece en [Python](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} usando el SDK de Azure AI Foundry. El SDK soporta características clave del servicio Azure AI Agents, incluyendo [Intérprete de Código](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} e integración del [Protocolo de Contexto de Modelo (MCP)](https://modelcontextprotocol.io/){:target="_blank"}.

3. **Base de Datos**

    La aplicación está impulsada por la Base de Datos de Ventas de Zava, un [servidor flexible de Azure Database for PostgreSQL](https://www.postgresql.org/){:target="_blank"} con extensión pgvector que contiene datos de ventas completos para las operaciones minoristas de bricolaje de Zava.

    La base de datos soporta consultas complejas para datos de ventas, inventario y clientes. La Seguridad a Nivel de Fila (RLS) asegura que los agentes accedan solo a las tiendas asignadas.

4. **Servidor MCP**

    El servidor del Protocolo de Contexto de Modelo (MCP) es un servicio Python personalizado que actúa como puente entre el agente y la base de datos PostgreSQL. Maneja:

     - **Descubrimiento de Esquema de Base de Datos**: Recupera automáticamente esquemas de base de datos para ayudar al agente a entender los datos disponibles.
     - **Generación de Consultas**: Transforma solicitudes en lenguaje natural en consultas SQL.
     - **Ejecución de Herramientas**: Ejecuta consultas SQL y devuelve resultados en un formato que el agente puede usar.
     - **Servicios de Tiempo**: Proporciona datos relacionados con el tiempo para generar informes sensibles al tiempo.

## Extendiendo la Solución del Taller

El taller es fácilmente adaptable a casos de uso como soporte al cliente actualizando la base de datos y personalizando las instrucciones del Servicio de Agentes de Foundry.

## Mejores Prácticas Demostradas en la Aplicación

La aplicación también demuestra algunas mejores prácticas para eficiencia y experiencia del usuario.

- **APIs Asíncronas**:
  En la muestra del taller, tanto el Servicio de Agentes de Foundry como PostgreSQL usan APIs asíncronas, optimizando la eficiencia de recursos y escalabilidad. Esta elección de diseño se vuelve especialmente ventajosa al implementar la aplicación con marcos web asíncronos como FastAPI, ASP.NET o Streamlit.

- **Transmisión de Tokens**:
  La transmisión de tokens se implementa para mejorar la experiencia del usuario reduciendo los tiempos de respuesta percibidos para la aplicación de agente impulsada por LLM.

- **Observabilidad**:
  La aplicación incluye [trazado](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/tracing){:target="_blank"} y [métricas](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/metrics){:target="_blank"} incorporados para monitorear el rendimiento del agente, patrones de uso y latencia. Esto te permite identificar problemas y optimizar el agente a lo largo del tiempo.

*Traducido usando GitHub Copilot y GPT-4o.*
