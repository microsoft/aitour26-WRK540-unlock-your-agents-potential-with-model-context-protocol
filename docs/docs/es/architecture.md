## Tecnologías principales de un vistazo

- **Servicio de Agentes de Azure AI Foundry**
  Aloja el agente impulsado por LLM; orquesta herramientas (incluyendo Servidores MCP); gestiona contexto, Intérprete de Código y streaming de tokens; y proporciona autenticación, registro y escalado.
- **Servidores MCP**
  MCP (Protocolo de Contexto de Modelo) es un estándar abierto que proporciona a los LLMs una interfaz unificada para herramientas externas, APIs y datos. Estandariza el descubrimiento de herramientas (como OpenAPI para REST) y mejora la composabilidad haciendo que las herramientas sean fáciles de actualizar o intercambiar según las necesidades evolucionen.
- **PostgreSQL + pgvector**
  Almacena datos relacionales e incrustaciones; soporta consultas tanto relacionales (SQL) como semánticas (vectoriales) (a través de pgvector), gobernadas por SQL y RLS.

**Juntos:** el Servicio de Agentes enruta las intenciones del usuario; el servidor MCP las traduce en llamadas de herramientas/SQL; PostgreSQL+pgvector responde preguntas semánticas y analíticas.

## Arquitectura (alto nivel)

```plaintext
┌─────────────────────┐                         ┌─────────────────┐
│   Aplicación        │       stdio/https       │   Servidor MCP  │
│   Agente Zava       │◄───────────────────────►│ (sales_analysis)│
│   (app.py)          │      Transportes MCP    └─────────────────┘
│                     │                                 │
│ ┌─────────────────┐ │                                 ▼
│ │ Servicio de     │ │                         ┌─────────────────┐
│ │ Agentes de      │ │                         │ Base de Datos   │
│ │ Azure AI        │ │                         │ Azure para      │
│ │ + Streaming     │ │                         │ PostgreSQL      │
│ │                 │ │                         │   + pgvector    │
│ └─────────────────┘ │                         └─────────────────┘
└─────────────────────┘                         |
         │                                              ▼
         ▼                                      ┌─────────────────┐
┌─────────────────────┐                        │ Base de Datos   │
│ Azure OpenAI        │                        │ de Ventas Zava  │
│ Despliegues de      │                        │ con Búsqueda    │
│ Modelos             │                        │ Semántica       │
│ - gpt-4o-mini       │                        └─────────────────┘
│ - text-embedding-3- │
│   small             │
└─────────────────────┘
```

## Beneficios clave de los Servidores MCP

- **Interoperabilidad** – Conecta agentes de IA a herramientas habilitadas para MCP de cualquier proveedor con mínimo código personalizado.
- **Ganchos de seguridad** – Integra inicio de sesión, permisos y registro de actividades.
- **Reutilización** – Construye una vez, reutiliza en proyectos, nubes y tiempos de ejecución.
- **Simplicidad operacional** – Un solo contrato reduce el código repetitivo y el mantenimiento.

## Mejores prácticas demostradas

- **APIs Asíncronas:** El servicio de agentes y PostgreSQL usan APIs asíncronas; ideal con FastAPI/ASP.NET/Streamlit.
- **Streaming de tokens:** Mejora la latencia percibida en la UI.
- **Observabilidad:** Soporte integrado de trazabilidad y métricas para monitoreo y optimización.
- **Seguridad de base de datos:** PostgreSQL está asegurado con privilegios de agente restringidos y Seguridad a Nivel de Fila (RLS), limitando a los agentes solo a sus datos autorizados.
- **Intérprete de Código:** El [Intérprete de Código del Servicio de Agentes de Azure AI](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} ejecuta código generado por LLM bajo demanda en un entorno **aislado**, previniendo acciones más allá del alcance del agente.

### Extensibilidad

El patrón del taller se puede adaptar (ej., soporte al cliente) actualizando la base de datos + instrucciones del agente en Foundry.

## Arquitectura DevTunnel

En el entorno del taller, el Servicio de Agentes se ejecuta en Azure pero necesita conectarse a tu Servidor MCP ejecutándose localmente. DevTunnel crea un túnel seguro que expone tu Servidor MCP local al Servicio de Agentes basado en la nube.

```plaintext
          Nube Azure                           Desarrollo Local
    ┌─────────────────────┐                  ┌─────────────────────┐
    │   Aplicación        │                  │                     │
    │   Agente Zava       │                  │  ┌─────────────────┐│
    │   (Alojada en Azure)│                  │  │   Servidor MCP  ││
    │                     │                  │  │ (sales_analysis)││
    │ ┌─────────────────┐ │                  │  │ localhost:8000  ││
    │ │ Servicio de     │ │                  │  └─────────────────┘│
    │ │ Agentes de      │ │                  │           │         │
    │ │ Azure AI        │ │                  │           ▼         │
    │ └─────────────────┘ │                  │  ┌─────────────────┐│
    └─────────────────────┘                  │  │   PostgreSQL    ││
              │                              │  │   + pgvector    ││
              │ Solicitudes HTTPS            │  └─────────────────┘│
              ▼                              │                     │
    ┌─────────────────────┐                  │                     │
    │   DevTunnel         │◄─────────────────┼──── Túnel Seguro   │
    │   Endpoint Público  │    Port Forward  │                     │
    │ (*.devtunnels.ms)   │                  │                     │
    └─────────────────────┘                  └─────────────────────┘
```

**Cómo funciona DevTunnel en el Taller:**

1. **Desarrollo Local**: Ejecutas el Servidor MCP localmente en `localhost:8000`
2. **Creación de DevTunnel**: DevTunnel crea un endpoint HTTPS público (ej., `https://abc123.devtunnels.ms`) conectado a `localhost:8000`.
3. **Integración Azure**: El Servicio de Agentes alojado en Azure se conecta al Servidor MCP a través del endpoint DevTunnel.
4. **Operación Transparente**: El servicio de agentes opera normalmente, sin saber que está accediendo al Servidor MCP que se ejecuta localmente a través de un túnel.

Esta configuración te permite:

- Desarrollar y depurar localmente mientras usas servicios de IA alojados en la nube
- Probar escenarios realistas sin desplegar el Servidor MCP a Azure

*Traducido usando GitHub Copilot.*
