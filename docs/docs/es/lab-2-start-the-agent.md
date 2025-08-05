## Lo que Aprenderás

En este laboratorio, habilitarás el Intérprete de Código para analizar datos de ventas y crear gráficos usando lenguaje natural.

## Introducción

En este laboratorio, extenderás el Agente de IA de Azure con dos herramientas:

- **Intérprete de Código:** Permite al agente generar y ejecutar código Python para análisis de datos y visualización.
- **Herramientas del Servidor MCP:** Permiten al agente acceder a fuentes de datos externas usando Herramientas MCP, en nuestro caso datos en una base de datos PostgreSQL.

## Ejercicio de Laboratorio

### Habilitar el Intérprete de Código

En este laboratorio, habilitarás el Intérprete de Código para ejecutar código Python generado por el LLM para analizar los datos de ventas minoristas de Zava.

=== "Python"

    1. **Abre** el `app.py`.
    2. **Descomenta** la línea que agrega la herramienta Intérprete de Código al conjunto de herramientas del agente en el método `_setup_agent_tools` de la clase `AgentManager`. Esta línea está actualmente comentada con un `#` al principio.:

        ```python
        # code_interpreter = CodeInterpreterTool()
        # self.toolset.add(code_interpreter)
        ```

    3. **Revisa** el código en el archivo `app.py`. Notarás que las herramientas del Intérprete de Código y del Servidor MCP se agregan al conjunto de herramientas del agente en el método `_setup_agent_tools` de la clase `AgentManager`.

        ```python

        Después de descomentar, tu código debería verse así:

        ```python
        class AgentManager:
            """Manages Azure AI Agent lifecycle and dependencies."""

            async def _setup_agent_tools(self) -> None:
                """Setup MCP tools and code interpreter."""

                # Enable the code interpreter tool
                code_interpreter = CodeInterpreterTool()
                self.toolset.add(code_interpreter)

                print("Setting up Agent tools...")
                ...
        ```

=== "C#"

    Por determinar

## Iniciar la Aplicación del Agente

1. Copia el texto de abajo al portapapeles:

    ```text
    Debug: Select and Start Debugging
    ```

2. Presiona <kbd>F1</kbd> para abrir la Paleta de Comandos de VS Code.
3. Pega el texto en la Paleta de Comandos y selecciona **Debug: Select and Start Debugging**.
4. Selecciona **🔁🤖Debug Compound: Agent and MCP (stdio)** de la lista. Esto iniciará la aplicación del agente y el cliente de chat web.

## Abrir el Cliente de Chat Web del Agente

1. Copia el texto de abajo al portapapeles:

    ```text
    Open Port in Browser
    ```

2. Presiona <kbd>F1</kbd> para abrir la Paleta de Comandos de VS Code.
3. Pega el texto en la Paleta de Comandos y selecciona **Open Port in Browser**.
4. Selecciona **8005** de la lista. Esto abrirá el cliente de chat web del agente en tu navegador.

### Iniciar una Conversación con el Agente

Desde el cliente de chat web, puedes iniciar una conversación con el agente. El agente está diseñado para responder preguntas sobre los datos de ventas de Zava y generar visualizaciones usando el Intérprete de Código.

1. Análisis de ventas de productos. Copia y pega la siguiente pregunta en el chat:

    ```text
    Muestra los 10 productos principales por ingresos por tienda para el último trimestre
    ```

    Después de un momento, el agente responderá con una tabla mostrando los 10 productos principales por ingresos para cada tienda.

    !!! info
        El agente usa el LLM que llama a tres herramientas del Servidor MCP para obtener los datos y mostrarlos en una tabla:

           1. **get_current_utc_date()**: Obtiene la fecha y hora actual para que el agente pueda determinar el último trimestre relativo a la fecha actual.
           2. **get_multiple_table_schemas()**: Obtiene los esquemas de las tablas en la base de datos requeridas por el LLM para generar SQL válido.
           3. **execute_sales_query**: Ejecuta una consulta SQL para obtener los 10 productos principales por ingresos para el último trimestre de la base de datos PostgreSQL.

2. Generar un gráfico circular. Copia y pega la siguiente pregunta en el chat:

    ```text
    Muestra las ventas por tienda como un gráfico circular para este año fiscal
    ```

    El agente responderá con un gráfico circular mostrando la distribución de ventas por tienda para el año fiscal actual.

    !!! info
        Esto podría sentirse como magia, entonces ¿qué está pasando detrás de escena para hacer que todo funcione?

        El Servicio de Agentes de Foundry orquesta los siguientes pasos:

        1. Como la pregunta anterior, el agente determina si tiene los esquemas de tabla requeridos para la consulta. Si no, usa las herramientas **get_multiple_table_schemas()** para obtener la fecha actual y el esquema de la base de datos.
        2. El agente luego usa la herramienta **execute_sales_query** para obtener las ventas
        3. Usando los datos devueltos, el LLM escribe código Python para crear un Gráfico Circular.
        4. Finalmente, el Intérprete de Código ejecuta el código Python para generar el gráfico.

3. Continúa haciendo preguntas sobre los datos de ventas de Zava para ver el Intérprete de Código en acción. Aquí hay algunas preguntas de seguimiento que podrías querer probar:

    - ```Determina qué productos o categorías impulsan las ventas. Muestra como un Gráfico de Barras.```
    - ```¿Cuál sería el impacto de un evento de choque (ej., 20% de caída en ventas en una región) en la distribución global de ventas? Muestra como un Gráfico de Barras Agrupadas.```
        - Continúa con ```¿Qué pasaría si el evento de choque fuera del 50%?```
    - ```¿Qué regiones tienen ventas por encima o por debajo del promedio? Muestra como un Gráfico de Barras con Desviación del Promedio.```
    - ```¿Qué regiones tienen descuentos por encima o por debajo del promedio? Muestra como un Gráfico de Barras con Desviación del Promedio.```
    - ```Simula ventas futuras por región usando una simulación Monte Carlo para estimar intervalos de confianza. Muestra como una Línea con Bandas de Confianza usando colores vívidos.```

<!-- ## Detener la Aplicación del Agente

1. Regresa al editor de VS Code.
1. Presiona <kbd>Shift + F5</kbd> para detener la aplicación del agente. -->

## Deja la Aplicación del Agente Ejecutándose

Deja la aplicación del agente ejecutándose ya que la usarás en el próximo laboratorio para extender el agente con más herramientas y capacidades.

*Traducido usando GitHub Copilot y GPT-4o.*
