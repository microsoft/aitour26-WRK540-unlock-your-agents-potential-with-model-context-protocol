## Lo que Aprenderás

En este laboratorio, habilitarás capacidades de búsqueda semántica en el Agente de Azure AI usando el Servidor MCP y la base de datos PostgreSQL con la extensión [PostgreSQL Vector](https://github.com/pgvector/pgvector){:target="\_blank"} habilitada.

## Introducción

Este laboratorio actualiza el Agente de Azure AI con búsqueda semántica usando el Servidor MCP y PostgreSQL.

Todos los nombres y descripciones de productos de Zava han sido convertidos a vectores con el modelo de incrustación de OpenAI (text-embedding-3-small) y almacenados en la base de datos. Esto permite al agente entender la intención del usuario y proporcionar respuestas más precisas.

??? info "Para Desarrolladores: ¿Cómo funciona la Búsqueda Semántica de PostgreSQL?"

    ### Vectorización de las Descripciones y Nombres de Productos

    Para aprender más sobre cómo los nombres y descripciones de productos de Zava fueron vectorizados, consulta el [README del Generador de Base de Datos PostgreSQL de Zava DIY](https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol/tree/main/data/database){:target="_blank"}.

    === "Python"

        ### El LLM llama a la Herramienta del Servidor MCP

        Basándose en la consulta del usuario y las instrucciones proporcionadas, el LLM decide llamar a la herramienta del Servidor MCP `semantic_search_products` para encontrar productos relevantes.

        Ocurre la siguiente secuencia de eventos:

        1. La herramienta MCP `semantic_search_products` se invoca con la descripción de consulta del usuario.
        2. El servidor MCP genera un vector para la consulta usando el modelo de incrustación de OpenAI (text-embedding-3-small). Ve el código para vectorizar la consulta en el método `generate_query_embedding`.
        3. El servidor MCP luego realiza una búsqueda semántica contra la base de datos PostgreSQL para encontrar productos con vectores similares.

        ### Vista General de la Búsqueda Semántica de PostgreSQL

        La herramienta del Servidor MCP `semantic_search_products` luego ejecuta una consulta SQL que usa la consulta vectorizada para encontrar los vectores de productos más similares en la base de datos. La consulta SQL usa el operador `<->` proporcionado por la extensión pgvector para calcular la distancia entre vectores.

        ```python
        async def search_products_by_similarity(
            self, query_embedding: list[float], 
                rls_user_id: str, 
                max_rows: int = 20, 
                similarity_threshold: float = 30.0
        ) -> str:
                ...
                query = f"""
                    SELECT 
                        p.*,
                        (pde.description_embedding <=> $1::vector) as similarity_distance
                    FROM {SCHEMA_NAME}.product_description_embeddings pde
                    JOIN {SCHEMA_NAME}.products p ON pde.product_id = p.product_id
                    WHERE (pde.description_embedding <=> $1::vector) <= $3
                    ORDER BY similarity_distance
                    LIMIT $2
                """

                rows = await conn.fetch(query, embedding_str, max_rows, distance_threshold)
                ...
        ```

    === "C#"

        ### El LLM llama a la Herramienta del Servidor MCP

        Basándose en la consulta del usuario y las instrucciones proporcionadas, el LLM decide llamar a la herramienta del Servidor MCP `semantic_search_products` para encontrar productos relevantes.

        Ocurre la siguiente secuencia de eventos:

        1. La herramienta MCP `semantic_search_products` se invoca con la descripción de consulta del usuario.
        2. El servidor MCP genera un vector para la consulta usando el modelo de incrustación de OpenAI (text-embedding-3-small). Ve el método `GenerateVectorAsync` en el archivo `EmbeddingGeneratorExtensions.cs`.
        3. El servidor MCP luego realiza una búsqueda semántica contra la base de datos PostgreSQL para encontrar productos con vectores similares.

        ### Vista General de la Búsqueda Semántica de PostgreSQL

        La herramienta del Servidor MCP `semantic_search_products` luego ejecuta una consulta SQL que usa la consulta vectorizada para encontrar los vectores de productos más similares en la base de datos. La consulta SQL usa el operador `<->` proporcionado por la extensión pgvector para calcular la distancia entre vectores.

        ```csharp
        public async Task<IEnumerable<SemanticSearchResult>> SemanticSearchProductsAsync(
        ...
            await using var searchCmd = new NpgsqlCommand("""
            SELECT 
                p.*,
                (pde.description_embedding <=> $1::vector) as similarity_distance
            FROM retail.product_description_embeddings pde
            JOIN retail.products p ON pde.product_id = p.product_id
            WHERE (pde.description_embedding <=> $1::vector) <= $3
            ORDER BY similarity_distance
            LIMIT $2
            """, connection);
            searchCmd.Parameters.AddWithValue(new Vector(embeddings));
            searchCmd.Parameters.AddWithValue(maxRows);
            searchCmd.Parameters.AddWithValue(distanceThreshold);

            await using var reader = await searchCmd.ExecuteReaderAsync();
            var results = new List<SemanticSearchResult>();
        ```

## Ejercicio del Laboratorio

Del laboratorio anterior puedes hacerle preguntas al agente sobre datos de ventas, pero estaba limitado a coincidencias exactas. En este laboratorio, extiendes las capacidades del agente implementando búsqueda semántica usando el Protocolo de Contexto de Modelo (MCP). Esto permitirá al agente entender y responder a consultas que no son coincidencias exactas, mejorando su habilidad para asistir a usuarios con preguntas más complejas.

1. Pega la siguiente pregunta en la pestaña Web Chat en tu navegador:

   ```text
   What 18 amp circuit breakers do we sell?
   ```

   El agente responde con algo similar a este mensaje:

   _"I couldn't find any specific 18 amp circuit breakers in our inventory. However, we may have other types of circuit breakers available. Would you like me to search for general circuit breakers or any other related products? 😊"_

## Detener la Aplicación del Agente

Desde VS Code, detén la aplicación del agente presionando <kbd>Shift + F5</kbd>.

=== "Python"

    ## Implementar Búsqueda Semántica

    En esta sección, implementarás búsqueda semántica usando el Protocolo de Contexto de Modelo (MCP) para mejorar las capacidades del agente.

    1. Presiona <kbd>F1</kbd> para **abrir** la Paleta de Comandos de VS Code.
    2. Escribe **Open File** y selecciona **File: Open File...**.
    3. **Pega** la siguiente ruta en el selector de archivos y presiona <kbd>Enter</kbd>:

        ```text
        /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
        ```

    4. Desplázate hacia abajo hasta alrededor de la línea 70 y busca el método `semantic_search_products`. Este método es responsable de realizar búsqueda semántica en los datos de ventas. Notarás que el decorador **@mcp.tool()** está comentado. Este decorador se usa para registrar el método como una herramienta MCP, permitiendo que sea llamado por el agente.

    5. Descomenta el decorador `@mcp.tool()` removiendo el `#` al comienzo de la línea. Esto habilitará la herramienta de búsqueda semántica.

        ```python
        # @mcp.tool()
        async def semantic_search_products(
            ctx: Context,
            query_description: Annotated[str, Field(
            ...
        ```

    6. A continuación, necesitas habilitar las instrucciones del Agente para usar la herramienta de búsqueda semántica. Regresa al archivo `app.py`.
    7. Desplázate hacia abajo hasta alrededor de la línea 30 y encuentra la línea `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"`.
    8. Descomenta la línea removiendo el `#` al comienzo. Esto habilitará al agente para usar la herramienta de búsqueda semántica.

        ```python
        INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
        ```

=== "C#"

    ## Implementar Búsqueda Semántica

    En esta sección, implementarás búsqueda semántica usando el Protocolo de Contexto de Modelo (MCP) para mejorar las capacidades del agente.

    1. Abre el archivo `McpHost.cs` del proyecto `McpAgentWorkshop.WorkshopApi`.
    2. Localiza donde las otras herramientas MCP están registradas con el servidor MCP, y registra la clase `SemanticSearchTools` como una herramienta MCP.

        ```csharp
        builder.Services.AddMcpTool<SemanticSearchTools>();
        ```

        !!! info "Nota"
            Lee la implementación de `SemanticSearchTools` para aprender cómo el servidor MCP realizará la búsqueda.

    3. A continuación, necesitas habilitar las instrucciones del Agente para usar la herramienta de búsqueda semántica. Regresa a la clase `AgentService` y cambia la constante `InstructionsFile` a `mcp_server_tools_with_semantic_search.txt`.

## Revisar las Instrucciones del Agente

1. Presiona <kbd>F1</kbd> para abrir la Paleta de Comandos de VS Code.
2. Escribe **Open File** y selecciona **File: Open File...**.
3. Pega la siguiente ruta en el selector de archivos y presiona <kbd>Enter</kbd>:

   ```text
   /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
   ```

4. Revisa las instrucciones en el archivo. Estas instrucciones instruyen al agente a usar la herramienta de búsqueda semántica para responder preguntas sobre datos de ventas.

## Iniciar la Aplicación del Agente con la Herramienta de Búsqueda Semántica

1. **Inicia** la aplicación del agente presionando <kbd>F5</kbd>. Esto iniciará el agente con las instrucciones actualizadas y la herramienta de búsqueda semántica habilitada.
2. Abre el **Web Chat** en tu navegador.
3. Ingresa la siguiente pregunta en el chat:

    ```text
    What 18 amp circuit breakers do we sell?
    ```

    El agente ahora entiende el significado semántico de la pregunta y responde en consecuencia con datos de ventas relevantes.

    !!! info "Nota"
        La herramienta de Búsqueda Semántica MCP funciona de la siguiente manera:

        1. La pregunta se convierte en un vector usando el mismo modelo de incrustación de OpenAI (text-embedding-3-small) que las descripciones de productos.
        2. Este vector se usa para buscar vectores de productos similares en la base de datos PostgreSQL.
        3. El agente recibe los resultados y los usa para generar una respuesta.

## Escribir un Informe Ejecutivo

El prompt final para este taller es el siguiente:

```plaintext
Write an executive report on the sales performance of different stores for these circuit breakers.
```

## Dejar la Aplicación del Agente Ejecutándose

Deja la aplicación del agente ejecutándose ya que la usarás en el próximo laboratorio para explorar el acceso seguro a datos del agente.

*Traducido usando GitHub Copilot.*
