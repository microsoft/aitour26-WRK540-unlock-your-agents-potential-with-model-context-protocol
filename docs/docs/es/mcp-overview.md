MCP (Protocolo de Contexto de Modelo) es un estándar abierto que permite a los agentes de IA acceder a herramientas externas, APIs y fuentes de datos a través de una interfaz unificada. Estandariza el descubrimiento y acceso de herramientas, similar a OpenAPI para servicios REST. MCP mejora la capacidad de composición y agilidad de los sistemas de IA simplificando actualizaciones o reemplazos de herramientas de IA conforme evolucionan las necesidades de tu negocio.

# Beneficios Clave

- **Interoperabilidad** – Conecta agentes de IA a herramientas habilitadas para MCP de cualquier proveedor con código personalizado mínimo.
- **Ganchos de Seguridad** – Integra inicio de sesión, permisos y registro de actividades.
- **Reutilización** – Construye una vez, reutiliza a través de proyectos, nubes y tiempos de ejecución.
- **Simplicidad Operacional** – Un solo contrato reduce el código repetitivo y mantenimiento.

# Arquitectura

```
┌─────────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Agente de IA      │    │   Cliente MCP   │    │   Servidor MCP  │
│   de Azure          │◄──►│ (mcp_client.py) │◄──►│ (mcp_server_sales_analysis.py) │
│   (main.py)         │    └─────────────────┘    └─────────────────┘
│                     │                                   │
│ ┌─────────────────┐ │                                   ▼
│ │ Servicio de     │ │                           ┌─────────────────┐
│ │ Agentes de      │ │                           │ Azure Database  │
│ │ Azure AI        │ │                           │ for PostgreSQL  │
│ │ + Streaming     │ │                           │       +         │
│ └─────────────────┘ │                           │    pgvector     │
└─────────────────────┘                           └─────────────────┘
         │                                                │
         ▼                                        ┌─────────────────┐
┌─────────────────────┐                           │ 8 Tablas        │
│ Implementación de   │                           │ Normalizadas    │
│ Modelo Azure OpenAI │                           │ con Índices de  │
│ (GPT-4, etc.)       │                           │ Rendimiento     │
└─────────────────────┘                           └─────────────────┘
```

# Cómo Funciona

MCP usa un modelo cliente-servidor para interacciones de agente de IA con recursos externos:

- **Host MCP:** Tiempo de ejecución o plataforma ejecutando el agente de IA (ej., Servicio de Agentes de Azure AI Foundry).
- **Cliente MCP:** SDK convirtiendo llamadas de herramientas del agente de IA en solicitudes MCP.
- **Servidor MCP:** Registra herramientas, ejecuta solicitudes, devuelve resultados JSON. Soporta autenticación, autorización y registro.

### Componentes en el Servidor MCP

- **Recursos:** Fuentes de datos como bases de datos, APIs, almacenes de archivos.
- **Herramientas:** Funciones o APIs registradas ejecutadas bajo demanda.
- **Prompts (opcional):** Plantillas versionadas para reutilización.
- **Políticas (opcional):** Límites y verificaciones de seguridad (tasa, profundidad, autenticación).

### Transportes MCP

- **HTTP/HTTPS:** Protocolos web estándar con soporte de streaming.
- **stdio:** Transporte ligero local o en contenedor compartiendo tiempo de ejecución.

Este taller usa stdio para comunicación MCP local. Los despliegues de producción usan HTTPS para escalabilidad y seguridad.

# Caso de Uso

En este taller, el servidor MCP vincula el Agente de IA de Azure a los datos de ventas de Zava. Cuando preguntas sobre productos, ventas o inventario:

1. El agente de IA genera solicitudes del Servidor MCP.
2. El Servidor MCP:
    - Proporciona información de esquema para consultas precisas.
    - Ejecuta consultas SQL, devuelve datos estructurados.
    - Ofrece servicios de tiempo para informes sensibles al tiempo.

Esto permite insights en tiempo real sobre las operaciones de ventas de Zava de manera eficiente.

*Traducido usando GitHub Copilot y GPT-4o.*
