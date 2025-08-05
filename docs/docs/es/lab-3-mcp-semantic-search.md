## Lo que Aprenderás

En este laboratorio, habilitas capacidades de búsqueda semántica en el Agente de IA de Azure usando el Protocolo de Contexto de Modelo (MCP) y la base de datos PostgreSQL.

## Introducción

Este laboratorio actualiza el Agente de IA de Azure con búsqueda semántica usando el Protocolo de Contexto de Modelo (MCP) y PostgreSQL. Los nombres y descripciones de productos se convirtieron en vectores con el modelo de embeddings de OpenAI (text-embedding-3-small) y se almacenaron en la base de datos. Esto permite al agente entender la intención del usuario y proporcionar respuestas más precisas.

## Ejercicio de Laboratorio

Del laboratorio anterior puedes hacer preguntas al agente sobre datos de ventas, pero estaba limitado a coincidencias exactas. En este laboratorio, extiendes las capacidades del agente implementando búsqueda semántica usando el Protocolo de Contexto de Modelo (MCP). Esto permitirá al agente entender y responder a consultas que no son coincidencias exactas, mejorando su capacidad para asistir a los usuarios con preguntas más complejas.

1. Pega la siguiente pregunta en la pestaña Web Chat en tu navegador:

    ```text
    ¿Cómo se desempeñaron las diferentes tiendas con interruptores 18A?
    ```

    El agente responde: "No pude encontrar datos de ventas para interruptores 18A en nuestros registros. 😱 Sin embargo, aquí tienes algunas sugerencias para productos similares que podrías querer explorar." Esto sucede porque el agente solo depende de consultas coincidentes por palabras clave y no entiende el significado semántico de tu pregunta. El LLM aún puede hacer sugerencias educadas de productos de cualquier contexto de producto que ya pueda tener.

## Implementar Búsqueda Semántica

En esta sección, implementarás búsqueda semántica usando el Protocolo de Contexto de Modelo (MCP) para mejorar las capacidades del agente.

1. Presiona <kbd>F1</kbd> para **abrir** la Paleta de Comandos de VS Code.
2. Escribe **Open File** y selecciona **File: Open File...**.
3. **Pega** la siguiente ruta en el selector de archivos y presiona <kbd>Enter</kbd>:

    ```text
    /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
    ```

4. Desplázate hacia abajo hasta alrededor de la línea 100 y busca el método `semantic_search_products`. Este método es responsable de realizar búsqueda semántica en los datos de ventas. Notarás que el decorador **@mcp.tool()** está comentado. Este decorador se usa para registrar el método como una herramienta MCP, permitiendo que sea llamado por el agente.

5. Descomenta el decorador `@mcp.tool()` removiendo el `#` al principio de la línea. Esto habilitará la herramienta de búsqueda semántica.

    ```python
    # @mcp.tool()
    async def semantic_search_products(
        ctx: Context,
        query_description: Annotated[str, Field(
        ...
    ```

6. A continuación, necesitas habilitar las instrucciones del Agente para usar la herramienta de búsqueda semántica. Regresa al archivo `app.py`.
7. Desplázate hacia abajo hasta alrededor de la línea 30 y encuentra la línea `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"`.
8. Descomenta la línea removiendo el `#` al principio. Esto habilitará al agente para usar la herramienta de búsqueda semántica.

    ```python
    INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
    ```

## Revisar las Instrucciones del Agente

1. Presiona <kbd>F1</kbd> para abrir la Paleta de Comandos de VS Code.
2. Escribe **Open File** y selecciona **File: Open File...**.
3. Pega la siguiente ruta en el selector de archivos y presiona <kbd>Enter</kbd>:

    ```text
    /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
    ```

4. Revisa las instrucciones en el archivo. Estas instrucciones instruyen al agente a usar la herramienta de búsqueda semántica para responder preguntas sobre datos de ventas.

## Iniciar la Aplicación del Agente con la Herramienta de Búsqueda Semántica

1. **Detén** la aplicación actual del agente presionando <kbd>Shift + F5</kbd>.
2. **Reinicia** la aplicación del agente presionando <kbd>F5</kbd>. Esto iniciará el agente con las instrucciones actualizadas y la herramienta de búsqueda semántica habilitada.
3. Regresa a la pestaña **Web Chat** en tu navegador.
4. Ingresa la siguiente pregunta en el chat:

    ```text
    ¿Cómo se desempeñaron las diferentes tiendas con interruptores 18A?
    ```

    El agente ahora entiende el significado semántico de la pregunta y responde en consecuencia con datos de ventas relevantes.

    !!! info "Nota"
        La herramienta de Búsqueda Semántica MCP funciona de la siguiente manera:

        1. La pregunta se convierte en un vector usando el mismo modelo de embeddings de OpenAI (text-embedding-3-small) que las descripciones de productos.
        2. Este vector se usa para buscar vectores de productos similares en la base de datos PostgreSQL.
        3. El agente recibe los resultados y los usa para generar una respuesta.

*Traducido usando GitHub Copilot y GPT-4o.*
